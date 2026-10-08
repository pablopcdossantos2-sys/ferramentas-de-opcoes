from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Optional

from models import GexSnapshot, LevelValue, OptionContract, StrikeExposure

CONTRACT_MULTIPLIER = 100.0
LEVEL_SPECS = [
    ("teto", "Call/Put teto"),
    ("cw2", "Call Wall 2"),
    ("cw1", "Call Wall 1"),
    ("gres", "Gamma resistência"),
    ("flip", "Gamma Flip"),
    ("gsup", "Gamma suporte"),
    ("pw2", "Put Wall 2"),
    ("floor", "Put Wall chão"),
]

def _num(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if text in {"-", "—", "N/A", "NA", "null", "None"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None

def _pick(raw: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if name in raw and raw[name] not in (None, ""):
            return raw[name]
    return None


def extract_market_prices(records: Iterable[Mapping[str, Any]]) -> tuple[Optional[float], Optional[float]]:
    """
    Returns (current/premarket spot, prior regular-session reference close).

    Barchart responses commonly expose baseLastPrice for the current quote and
    baseDailyLastPrice for the daily/regular-session reference. We keep them
    separate because the lecture uses the current EWZ price to contextualize
    strikes, but the prior regular close to measure percentage distances.
    """
    current: Optional[float] = None
    reference: Optional[float] = None
    for item in records:
        raw = item.get("raw") if isinstance(item.get("raw"), Mapping) else item
        if current is None:
            current = _num(_pick(raw, "baseLastPrice", "lastPrice"))
        if reference is None:
            reference = _num(_pick(raw, "baseDailyLastPrice", "previousClose", "priorClose"))
        if current is not None and reference is not None:
            break
    return current, reference

def level_distance_pct(level: Optional[float], reference_close: Optional[float]) -> Optional[float]:
    if level is None or reference_close is None or reference_close <= 0:
        return None
    return (level / reference_close) - 1.0

def project_level_1to1(level: Optional[float], ewz_reference: Optional[float], win_reference: Optional[float]) -> Optional[float]:
    pct = level_distance_pct(level, ewz_reference)
    if pct is None or win_reference is None or win_reference <= 0:
        return None
    return win_reference * (1.0 + pct)

def contracts_from_records(records: Iterable[Mapping[str, Any]], *, prefer_eod: bool = True) -> list[OptionContract]:
    out: list[OptionContract] = []
    seen: set[tuple] = set()
    for item in records:
        raw = item.get("raw") if isinstance(item.get("raw"), Mapping) else item
        strike = _num(_pick(raw, "strikePrice", "strike"))
        opt_type = str(_pick(raw, "optionType", "type") or "").strip().lower()
        if opt_type.startswith("c"):
            opt_type = "call"
        elif opt_type.startswith("p"):
            opt_type = "put"
        else:
            continue
        gamma_names = ("dailyGamma", "gamma") if prefer_eod else ("gamma", "dailyGamma")
        oi_names = ("dailyOpenInterest", "openInterest") if prefer_eod else ("openInterest", "dailyOpenInterest")
        spot_names = ("baseDailyLastPrice", "baseLastPrice") if prefer_eod else ("baseLastPrice", "baseDailyLastPrice")
        gamma = _num(_pick(raw, *gamma_names))
        oi = _num(_pick(raw, *oi_names))
        spot = _num(_pick(raw, *spot_names))
        expiration = str(_pick(raw, "expirationDate", "expiration") or "")
        symbol = str(_pick(raw, "baseSymbol", "underlyingSymbol") or "EWZ")
        if strike is None or gamma is None or oi is None or spot is None or spot <= 0 or oi < 0:
            continue
        sig = (strike, opt_type, gamma, oi, expiration)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(OptionContract(strike, opt_type, gamma, oi, spot, expiration, symbol))
    return out

def aggregate_exposure(contracts: Iterable[OptionContract]) -> list[StrikeExposure]:
    buckets: dict[float, StrikeExposure] = {}
    for c in contracts:
        row = buckets.setdefault(c.strike, StrikeExposure(c.strike))
        magnitude = c.gamma * c.open_interest * CONTRACT_MULTIPLIER * (c.spot ** 2) * 0.01
        if c.option_type == "call":
            row.call_gex += magnitude
            row.call_oi += c.open_interest
            row.net_gex += magnitude
        else:
            row.put_gex -= magnitude
            row.put_oi += c.open_interest
            row.net_gex -= magnitude
    return [buckets[k] for k in sorted(buckets)]

def _top(rows: list[StrikeExposure], metric, *, side: str, spot: float, n: int = 2) -> list[StrikeExposure]:
    if side == "above":
        candidates = [r for r in rows if r.strike >= spot]
    elif side == "below":
        candidates = [r for r in rows if r.strike <= spot]
    else:
        candidates = list(rows)
    return sorted(candidates, key=metric, reverse=True)[:n]

def derive_levels(
    contracts: list[OptionContract],
    official_levels: Optional[Mapping[str, float]] = None,
    *,
    source_url: str = "",
    warnings: Optional[list[str]] = None,
    selection_spot: Optional[float] = None,
    reference_close: Optional[float] = None,
) -> GexSnapshot:
    if not contracts:
        raise ValueError("Nenhum contrato de opções válido foi encontrado.")
    official_levels = {k: float(v) for k, v in (official_levels or {}).items() if v is not None}
    eod_spot = next((c.spot for c in contracts if c.spot > 0), 0.0)
    spot = selection_spot if selection_spot is not None and selection_spot > 0 else eod_spot
    reference_close = reference_close if reference_close is not None and reference_close > 0 else eod_spot
    rows = aggregate_exposure(contracts)
    calls = _top(rows, lambda r: r.call_gex, side="above", spot=spot, n=4)
    puts = _top(rows, lambda r: abs(r.put_gex), side="below", spot=spot, n=4)
    pos = _top(rows, lambda r: max(r.net_gex, 0), side="above", spot=spot, n=5)
    neg = _top(rows, lambda r: max(-r.net_gex, 0), side="below", spot=spot, n=5)

    cw1_local = calls[0].strike if calls else None
    cw2_local = calls[1].strike if len(calls) > 1 else None
    floor_local = puts[0].strike if puts else None
    pw2_local = puts[1].strike if len(puts) > 1 else None
    gres_local = next((r.strike for r in pos if r.strike not in {cw1_local, cw2_local}), None)
    gsup_local = next((r.strike for r in neg if r.strike not in {floor_local, pw2_local}), None)
    top3_calls = calls[:3]
    teto_local = max((r.strike for r in top3_calls), default=None)

    def mk(key: str, label: str, local_value: Optional[float], local_note: str) -> LevelValue:
        if key in official_levels:
            return LevelValue(
                key, label, official_levels[key],
                "Barchart (extraído da página)", "alta",
                "Valor identificado na página renderizada."
            )
        return LevelValue(key, label, local_value, "Estimativa local", "baixa", local_note)

    levels = [
        mk("teto", "Call/Put teto", teto_local, "Proxy: strike mais alto entre as três maiores concentrações de GEX de calls acima do spot."),
        mk("cw2", "Call Wall 2", cw2_local, "Proxy: segunda maior concentração de GEX de calls acima do spot."),
        mk("cw1", "Call Wall 1", cw1_local, "Proxy: maior concentração de GEX de calls acima do spot."),
        mk("gres", "Gamma resistência", gres_local, "Proxy: maior GEX líquido positivo acima do spot que não coincide com as duas Call Walls."),
        mk("flip", "Gamma Flip", None, "Não é estimado localmente: o flip exige recomputar o gamma agregado em diferentes preços. A aplicação tenta extrair o valor publicado pelo Barchart."),
        mk("gsup", "Gamma suporte", gsup_local, "Proxy: maior magnitude de GEX líquido negativo abaixo do spot que não coincide com as Put Walls."),
        mk("pw2", "Put Wall 2", pw2_local, "Proxy: segunda maior magnitude de GEX de puts abaixo do spot."),
        mk("floor", "Put Wall chão", floor_local, "Proxy: maior magnitude de GEX de puts abaixo do spot."),
    ]
    exps = sorted({c.expiration for c in contracts if c.expiration})
    ws = list(warnings or [])
    if "flip" not in official_levels:
        ws.append("Gamma Flip não foi encontrado na página; ele permanece em branco para evitar uma estimativa metodologicamente fraca.")
    return GexSnapshot(
        symbol="EWZ",
        spot=spot,
        reference_close=reference_close,
        levels=levels,
        exposures=rows,
        expirations=exps,
        source_url=source_url,
        source_timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        warnings=ws,
    )

def format_export_block(snapshot: GexSnapshot, overrides: Optional[Mapping[str, Optional[float]]] = None) -> str:
    vals = {lv.key: lv.value for lv in snapshot.levels}
    if overrides:
        vals.update(overrides)

    def f(v: Optional[float]) -> str:
        return "0" if v is None else (f"{v:.4f}".rstrip("0").rstrip("."))

    date = snapshot.source_timestamp[:10] if snapshot.source_timestamp else ""
    parts = [
        "EWZGEX1",
        "symbol=EWZ",
        f"date={date}",
        f"spot={f(snapshot.spot)}",
        f"ewzref={f(snapshot.reference_close)}",
    ]
    for key, _ in LEVEL_SPECS:
        parts.append(f"{key}={f(vals.get(key))}")
    parts.append("source=barchart")
    return "|".join(parts)

def parse_export_block(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in text.strip().split("|"):
        if "=" in token:
            k, v = token.split("=", 1)
            out[k.strip().lower()] = v.strip()
        elif token.strip():
            out.setdefault("version", token.strip())
    return out
