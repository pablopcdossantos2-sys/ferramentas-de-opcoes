from __future__ import annotations
import re
import time
from pathlib import Path
from typing import Any, Mapping

from gex_core import contracts_from_records

BARCHART_URL = "https://www.barchart.com/etfs-funds/quotes/EWZ/gamma-exposure"

def _flatten_records(data: Any) -> list[Mapping[str, Any]]:
    found: list[Mapping[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, Mapping):
            raw = node.get("raw") if isinstance(node.get("raw"), Mapping) else node
            if any(k in raw for k in ("strikePrice", "strike")) and any(k in raw for k in ("gamma", "dailyGamma")):
                found.append(node)
            else:
                for value in node.values():
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    return found

def parse_official_levels(text: str) -> dict[str, float]:
    text = re.sub(r"[\u00a0\t]+", " ", text or "")
    patterns = {
        "flip": [
            r"gamma\s+flip(?:\s+point)?\s*[:\-]?\s*\$?\s*([0-9]+(?:\.[0-9]+)?)",
            r"flip\s+point\s*[:\-]?\s*\$?\s*([0-9]+(?:\.[0-9]+)?)",
        ],
        "cw1": [r"call\s+wall\s*[:\-]?\s*\$?\s*([0-9]+(?:\.[0-9]+)?)"],
        "floor": [r"put\s+wall\s*[:\-]?\s*\$?\s*([0-9]+(?:\.[0-9]+)?)"],
    }
    out: dict[str, float] = {}
    for key, pats in patterns.items():
        for pat in pats:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                out[key] = float(match.group(1))
                break
    return out

def _floatish(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"-?[0-9]+(?:\.[0-9]+)?", value.replace(",", ""))
        return float(match.group(0)) if match else None
    if isinstance(value, Mapping):
        for key in ("value", "price", "strike", "strikePrice", "rawValue"):
            if key in value:
                parsed = _floatish(value[key])
                if parsed is not None:
                    return parsed
    return None

def extract_official_levels_from_payload(data: Any) -> dict[str, float]:
    out: dict[str, float] = {}
    key_targets = {
        "gammaflip": "flip",
        "gammaflippoint": "flip",
        "flippoint": "flip",
        "callwall": "cw1",
        "putwall": "floor",
    }

    def normalized(text: Any) -> str:
        return re.sub(r"[^a-z]", "", str(text).lower())

    def walk(node: Any) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                target = key_targets.get(normalized(key))
                if target:
                    parsed = _floatish(value)
                    if parsed is not None:
                        out.setdefault(target, parsed)

            label = node.get("label") or node.get("name") or node.get("title") or node.get("levelName")
            value = node.get("value") or node.get("price") or node.get("level") or node.get("strike")
            if label is not None and value is not None:
                label_key = normalized(label)
                for source, target in key_targets.items():
                    if source in label_key:
                        parsed = _floatish(value)
                        if parsed is not None:
                            out.setdefault(target, parsed)

            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    return out

class BarchartBrowserClient:
    def __init__(self, *, visible: bool = True, timeout_seconds: int = 90):
        self.visible = visible
        self.timeout_seconds = timeout_seconds

    def fetch(self) -> tuple[list[Mapping[str, Any]], dict[str, float], dict[str, Any]]:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("Playwright não está instalado. Execute: pip install -r requirements.txt") from exc

        captured: list[tuple[str, Any]] = []
        with sync_playwright() as p:
            profile_dir = Path.home() / ".ewz-gex-win" / "edge-profile"
            profile_dir.mkdir(parents=True, exist_ok=True)
            try:
                context = p.chromium.launch_persistent_context(
                    str(profile_dir),
                    channel="msedge",
                    headless=not self.visible,
                    locale="en-US",
                )
            except Exception as exc:
                raise RuntimeError("Não foi possível abrir o Microsoft Edge. Verifique se o Edge está instalado e atualizado.") from exc

            page = context.pages[0] if context.pages else context.new_page()

            def on_response(response):
                url = response.url
                if "/proxies/core-api/v1/options/" not in url:
                    return
                try:
                    content_type = response.headers.get("content-type", "")
                    if "json" in content_type:
                        captured.append((url, response.json()))
                except Exception:
                    pass

            page.on("response", on_response)
            page.goto(BARCHART_URL, wait_until="domcontentloaded", timeout=self.timeout_seconds * 1000)

            deadline = time.time() + self.timeout_seconds
            body_text = ""
            while time.time() < deadline:
                try:
                    body_text = page.locator("body").inner_text(timeout=1500)
                except Exception:
                    body_text = ""
                lower = body_text.lower()
                if (
                    "gamma exposure" in lower
                    and "javascript is disabled" not in lower
                    and "verify that you're not a robot" not in lower
                ):
                    break
                page.wait_for_timeout(750)

            page.wait_for_timeout(2500)
            try:
                body_text = page.locator("body").inner_text(timeout=3000)
            except Exception:
                pass

            official = parse_official_levels(body_text)
            records: list[Mapping[str, Any]] = []
            best_url = ""
            largest_response = 0
            for url, payload in captured:
                official.update(extract_official_levels_from_payload(payload))
                recs = _flatten_records(payload.get("data", payload) if isinstance(payload, Mapping) else payload)
                if recs:
                    records.extend(recs)
                    if len(recs) > largest_response:
                        largest_response = len(recs)
                        best_url = url

            if not records:
                payload = page.evaluate("""
                async () => {
                  const fields = [
                    'symbol','baseSymbol','strikePrice','optionType','baseDailyLastPrice','baseLastPrice',
                    'dailyGamma','gamma','delta','dailyDelta','dailyOpenInterest','openInterest',
                    'dailyVolume','volume','daysToExpiration','expirationDate','averageVolatility'
                  ].join(',');
                  const csrf = document.querySelector('meta[name="csrf-token"]')?.content || '';
                  const headers = csrf ? {'X-CSRF-TOKEN': csrf, 'X-XSRF-TOKEN': csrf} : {};
                  const urls = [
                    '/proxies/core-api/v1/options/get?baseSymbol=EWZ&fields=' + encodeURIComponent(fields) + '&groupBy=strikePrice&raw=1&meta=expirations',
                    '/proxies/core-api/v1/options/chain?symbol=EWZ&fields=' + encodeURIComponent(fields) + '&raw=1'
                  ];
                  for (const url of urls) {
                    try {
                      const r = await fetch(url, {credentials:'include', headers});
                      if (r.ok) return {url, data: await r.json()};
                    } catch (_) {}
                  }
                  return null;
                }
                """)
                if payload and payload.get("data"):
                    data = payload["data"]
                    official.update(extract_official_levels_from_payload(data))
                    records.extend(_flatten_records(data.get("data", data) if isinstance(data, dict) else data))
                    best_url = payload.get("url", "")

            context.close()

        if not records:
            raise RuntimeError(
                "O Barchart foi aberto, mas a aplicação não conseguiu capturar a cadeia de opções. "
                "Tente novamente com o navegador visível e conclua qualquer verificação exibida pelo site."
            )

        contracts = contracts_from_records(records, prefer_eod=True)
        if not contracts:
            raise RuntimeError("A resposta do Barchart não continha gamma/OI utilizáveis para o EWZ.")

        meta = {
            "page_url": BARCHART_URL,
            "api_url": best_url,
            "captured_requests": len(captured),
            "body_text": body_text[:5000],
        }
        return records, official, meta
