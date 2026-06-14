from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from models import MetricHistoryEntry, UserDetails


class AppTab(StrEnum):
    PROFILE = "profile"
    COMPETITION = "competition"


@dataclass
class AppState:
    logged_user: UserDetails
    logged_user_history: list[MetricHistoryEntry]
    selected_candidate: UserDetails
    users: list[UserDetails]
    selected_tab: AppTab = AppTab.PROFILE
    is_editing_metrics: bool = False
    is_viewing_rewards: bool = False
    is_viewing_metrics_info: bool = False
    selected_competition_id: str = "competition_main"
