from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import flet as ft


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
    metrics: list[Metric]
    final_score: float


class CandidatesBackend(Protocol):
    """Small backend contract used by the UI."""

    def get_candidates(self) -> list[UserDetails]:
        """Return all available candidates."""
        ...
