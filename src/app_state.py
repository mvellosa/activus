from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from models import UserDetails


class AppTab(StrEnum):
    PROFILE = "profile"
    COMPETITION = "competition"


@dataclass
class AppState:
    logged_user: UserDetails
    selected_candidate: UserDetails
    users: list[UserDetails]
    selected_tab: AppTab = AppTab.PROFILE
