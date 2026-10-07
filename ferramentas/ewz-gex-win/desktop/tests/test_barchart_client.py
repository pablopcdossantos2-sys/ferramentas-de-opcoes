import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from barchart_client import extract_official_levels_from_payload, parse_official_levels

def test_parse_levels_from_rendered_text():
    text = "Call Wall: 42.50  Gamma Flip 40.25  Put Wall: 37.00"
    out = parse_official_levels(text)
    assert out["cw1"] == 42.5
    assert out["flip"] == 40.25
    assert out["floor"] == 37.0

def test_extract_levels_from_payload_keys_and_labels():
    payload = {
        "summary": {
            "gammaFlipPoint": 40.25,
            "callWall": {"value": 42.5},
            "levels": [
                {"label": "Put Wall", "price": 37.0}
            ],
        }
    }
    out = extract_official_levels_from_payload(payload)
    assert out["flip"] == 40.25
    assert out["cw1"] == 42.5
    assert out["floor"] == 37.0
