import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import edge_profiles


def test_detects_profiles_and_cold_turkey(tmp_path, monkeypatch):
    local = tmp_path / "Local"
    user_data = local / "Microsoft" / "Edge" / "User Data"
    default = user_data / "Default"
    cold = default / "Extensions" / edge_profiles.COLD_TURKEY_EDGE_EXTENSION_ID / "1.0.0"
    cold.mkdir(parents=True)
    (user_data / "Local State").write_text(
        json.dumps({"profile": {"info_cache": {"Default": {"name": "Pessoal"}}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("LOCALAPPDATA", str(local))

    profiles = edge_profiles.list_edge_profiles()
    assert len(profiles) == 1
    assert profiles[0].directory == "Default"
    assert profiles[0].name == "Pessoal"
    assert profiles[0].has_cold_turkey is True
    assert profiles[0].extension_count == 1


def test_prepare_profile_copies_extension_state(tmp_path, monkeypatch):
    local = tmp_path / "Local"
    home = tmp_path / "Home"
    user_data = local / "Microsoft" / "Edge" / "User Data"
    default = user_data / "Default"
    ext = default / "Extensions" / edge_profiles.COLD_TURKEY_EDGE_EXTENSION_ID / "1.0.0"
    ext.mkdir(parents=True)
    (ext / "manifest.json").write_text('{"name":"Cold Turkey"}', encoding="utf-8")
    (default / "Preferences").write_text("{}", encoding="utf-8")
    (default / "Secure Preferences").write_text("{}", encoding="utf-8")
    (user_data / "Local State").write_text("{}", encoding="utf-8")
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))

    dest_root, report = edge_profiles.prepare_automation_profile("Default")
    assert report["cold_turkey"] is True
    assert report["extension_count"] == 1
    assert (dest_root / "Default" / "Extensions" / edge_profiles.COLD_TURKEY_EDGE_EXTENSION_ID / "1.0.0" / "manifest.json").exists()
