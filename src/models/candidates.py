from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

import flet as ft


class MetricName(StrEnum):
    """Fixed metric identifiers supported by the app."""

    M1 = "M1"
    M2 = "M2"
    M3 = "M3"


@dataclass(frozen=True)
class Metric:
    """Single metric displayed as a circular progress indicator."""

    label: str
    value: float
    icon: ft.IconData
    color: str = "#FF8A00"


@dataclass(frozen=True)
class UserDetails:
    """Contract returned by the backend for each candidate/user."""

    user_id: str
    name: str
    subtitle: str
    image_url: str | None
    main_metric: float
    metrics: dict[MetricName, float]
    final_score: float


class CandidatesBackend(Protocol):
    """Small backend contract used by the UI."""

    def get_candidates(self) -> list[UserDetails]:
        """Return all available candidates."""
        ...
