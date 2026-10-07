from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass(slots=True)
class OptionContract:
    strike: float
    option_type: str
    gamma: float
    open_interest: float
    spot: float
    expiration: str = ""
    symbol: str = "EWZ"

@dataclass(slots=True)
class StrikeExposure:
    strike: float
    call_gex: float = 0.0
    put_gex: float = 0.0
    net_gex: float = 0.0
    call_oi: float = 0.0
    put_oi: float = 0.0

@dataclass(slots=True)
class LevelValue:
    key: str
    label: str
    value: Optional[float]
    origin: str
    confidence: str
    note: str = ""

@dataclass(slots=True)
class GexSnapshot:
    symbol: str
    spot: float
    levels: list[LevelValue]
    exposures: list[StrikeExposure] = field(default_factory=list)
    expirations: list[str] = field(default_factory=list)
    source_url: str = ""
    source_timestamp: str = ""
    warnings: list[str] = field(default_factory=list)
