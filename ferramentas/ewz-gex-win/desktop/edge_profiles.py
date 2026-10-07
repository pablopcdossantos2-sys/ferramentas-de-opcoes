from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

COLD_TURKEY_EDGE_EXTENSION_ID = "jfphahkinplobmabmgjmjgflbhjjddeb"


@dataclass(slots=True)
class EdgeProfile:
    directory: str
    name: str
    extension_count: int
    has_cold_turkey: bool

    @property
    def display_name(self) -> str:
        suffix = " · Cold Turkey ✓" if self.has_cold_turkey else ""
        return f"{self.name} ({self.directory}) · {self.extension_count} extensões{suffix}"


def edge_user_data_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise RuntimeError("A variável LOCALAPPDATA não está disponível neste Windows.")
    return Path(local) / "Microsoft" / "Edge" / "User Data"


def _extension_count(profile_path: Path) -> int:
    ext_root = profile_path / "Extensions"
    if not ext_root.exists():
        return 0
    return sum(1 for p in ext_root.iterdir() if p.is_dir())


def profile_has_cold_turkey(profile_path: Path) -> bool:
    return (profile_path / "Extensions" / COLD_TURKEY_EDGE_EXTENSION_ID).exists()


def list_edge_profiles() -> list[EdgeProfile]:
    root = edge_user_data_dir()
    if not root.exists():
        return []

    names: dict[str, str] = {}
    local_state = root / "Local State"
    if local_state.exists():
        try:
            data = json.loads(local_state.read_text(encoding="utf-8"))
            info_cache = data.get("profile", {}).get("info_cache", {})
            for directory, meta in info_cache.items():
                if isinstance(meta, dict):
                    names[directory] = str(meta.get("name") or directory)
        except Exception:
            pass

    candidates = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if child.name == "Default" or child.name.startswith("Profile "):
            candidates.append(child.name)

    profiles: list[EdgeProfile] = []
    for directory in sorted(set(candidates), key=lambda x: (x != "Default", x)):
        p = root / directory
        profiles.append(
            EdgeProfile(
                directory=directory,
                name=names.get(directory, directory),
                extension_count=_extension_count(p),
                has_cold_turkey=profile_has_cold_turkey(p),
            )
        )
    return profiles


def _copy_file(src: Path, dst: Path, errors: list[str]) -> None:
    try:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    except Exception as exc:
        errors.append(f"{src.name}: {exc}")


def _copy_dir(src: Path, dst: Path, errors: list[str]) -> None:
    try:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True, copy_function=shutil.copy2)
    except Exception as exc:
        errors.append(f"{src.name}: {exc}")


def prepare_automation_profile(profile_directory: str) -> tuple[Path, dict]:
    """
    Creates/refreshes a dedicated Edge user-data directory containing the
    selected profile's installed extensions and extension settings.

    We intentionally do NOT automate the user's live Edge User Data directory.
    That avoids profile-lock conflicts and follows Playwright's recommendation
    to use a separate automation profile.
    """
    source_root = edge_user_data_dir()
    source_profile = source_root / profile_directory
    if not source_profile.exists():
        raise RuntimeError(f"Perfil do Edge não encontrado: {profile_directory}")

    dest_root = Path.home() / ".ewz-gex-win" / "edge-with-extensions"
    dest_profile = dest_root / profile_directory
    dest_profile.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []

    # Root metadata is useful for Edge to recognize the copied profile.
    _copy_file(source_root / "Local State", dest_root / "Local State", errors)

    # Extension installation registry and preferences.
    for name in ("Preferences", "Secure Preferences"):
        _copy_file(source_profile / name, dest_profile / name, errors)

    # Extension binaries and extension-specific state. Site cookies, history,
    # passwords and normal browsing data are deliberately not copied.
    for name in (
        "Extensions",
        "Local Extension Settings",
        "Sync Extension Settings",
        "Managed Extension Settings",
        "Extension State",
        "Extension Rules",
        "DNR Extension Rules",
    ):
        _copy_dir(source_profile / name, dest_profile / name, errors)

    # Newer Chromium builds can keep extension storage here.
    _copy_dir(
        source_profile / "Storage" / "ext",
        dest_profile / "Storage" / "ext",
        errors,
    )

    extension_count = _extension_count(dest_profile)
    cold_turkey = profile_has_cold_turkey(dest_profile)

    if extension_count == 0:
        raise RuntimeError(
            "Nenhuma extensão foi encontrada no perfil selecionado do Edge. "
            "Selecione o perfil que você usa normalmente."
        )

    report = {
        "source_profile": profile_directory,
        "extension_count": extension_count,
        "cold_turkey": cold_turkey,
        "copy_warnings": errors,
    }
    return dest_root, report
