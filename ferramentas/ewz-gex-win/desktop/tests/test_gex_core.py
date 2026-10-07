import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gex_core import contracts_from_records, derive_levels, format_export_block, parse_export_block

def sample_records():
    rows = []
    spot = 40
    for strike, cg, pg, coi, poi in [
        (36, .02, .04, 100, 2000),
        (38, .04, .05, 500, 1500),
        (40, .06, .06, 1000, 1000),
        (42, .07, .04, 2000, 400),
        (44, .05, .02, 1500, 200),
        (46, .03, .01, 700, 100),
    ]:
        rows.append({"raw": {"strikePrice": strike, "optionType": "Call", "dailyGamma": cg, "dailyOpenInterest": coi, "baseDailyLastPrice": spot, "expirationDate": "2026-10-16"}})
        rows.append({"raw": {"strikePrice": strike, "optionType": "Put", "dailyGamma": pg, "dailyOpenInterest": poi, "baseDailyLastPrice": spot, "expirationDate": "2026-10-16"}})
    return rows

def test_contracts_and_levels():
    cs = contracts_from_records(sample_records())
    assert len(cs) == 12
    snap = derive_levels(cs, {"flip": 40.5, "cw1": 42, "floor": 38})
    vals = {x.key: x.value for x in snap.levels}
    assert vals["flip"] == 40.5
    assert vals["cw1"] == 42
    assert vals["floor"] == 38
    assert vals["cw2"] is not None
    assert len(snap.exposures) == 6

def test_export_roundtrip():
    cs = contracts_from_records(sample_records())
    snap = derive_levels(cs, {"flip": 40.5, "cw1": 42, "floor": 38})
    block = format_export_block(snap)
    parsed = parse_export_block(block)
    assert parsed["version"] == "EWZGEX1"
    assert parsed["symbol"] == "EWZ"
    assert parsed["flip"] == "40.5"
