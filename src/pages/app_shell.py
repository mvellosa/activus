from __future__ import annotations

import flet as ft

from app_state import AppState, AppTab
from components import BottomNav
from models import CandidatesBackend, DailyMetricInputs, UserDetails
from theme import APP_BG_COLOR

from .competition_page import CompetitionPage
from .metrics_form_page import MetricsFormPage
from .profile_page import ProfilePage
from .rewards_page import RewardsPage


class CompetitionApp:
    """Application shell with shared state and bottom navigation."""

    def __init__(self, backend: CandidatesBackend) -> None:
        self.backend = backend
        self.state: AppState | None = None
        self.page: ft.Page | None = None

    def build(self, page: ft.Page) -> None:
        users = self.backend.get_candidates()
        if not users:
            page.add(ft.Text("No candidates available."))
            return

        logged_user = users[0]
        self.state = AppState(
            logged_user=logged_user,
            selected_candidate=logged_user,
            users=self._rank_users(users),
        )
        self.page = page

        page.title = "Competicao"
        page.window.width = 420
        page.window.height = 760
        page.padding = 0
        page.bgcolor = APP_BG_COLOR
        page.theme_mode = ft.ThemeMode.LIGHT

        self._render()

    def _render(self) -> None:
        if self.page is None or self.state is None:
            return

        if self.state.is_editing_metrics:
            body: ft.Control = MetricsFormPage(
                user=self.state.logged_user,
                history=self.backend.get_history(self.state.logged_user.user_id),
                on_submit=self.update_logged_user_metrics,
                on_cancel=self.close_metrics_form,
            )
            controls = [body]
        elif self.state.is_viewing_rewards:
            body = RewardsPage(
                rewards=self.backend.get_rewards(self.state.selected_competition_id),
            )
            controls = [
                body,
                BottomNav(
                    selected_tab=self.state.selected_tab,
                    on_change=self.change_tab,
                ),
            ]
        elif self.state.selected_tab == AppTab.PROFILE:
            body = ProfilePage(
                self.state,
                on_edit_metrics=self.open_metrics_form,
            )
            controls = [
                body,
                BottomNav(
                    selected_tab=self.state.selected_tab,
                    on_change=self.change_tab,
                ),
            ]
        else:
            body = CompetitionPage(
                self.state,
                on_select_user=self.select_user,
                on_open_rewards=self.open_rewards,
            )
            controls = [
                body,
                BottomNav(
                    selected_tab=self.state.selected_tab,
                    on_change=self.change_tab,
                ),
            ]

        self.page.clean()
        self.page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                    spacing=12,
                    controls=controls,
                ),
            )
        )
        self.page.update()

    def select_user(self, user: UserDetails) -> None:
        if self.state is None:
            return

        self.state.selected_candidate = user
        self._render()

    def change_tab(self, tab: AppTab) -> None:
        if self.state is None:
            return

        if self.state.selected_tab == tab and not self.state.is_viewing_rewards:
            return

        self.state.selected_tab = tab
        self.state.is_editing_metrics = False
        self.state.is_viewing_rewards = False
        self._render()

    def open_metrics_form(self) -> None:
        if self.state is None:
            return

        self.state.is_editing_metrics = True
        self.state.is_viewing_rewards = False
        self._render()

    def open_rewards(self) -> None:
        if self.state is None:
            return

        self.state.selected_tab = AppTab.COMPETITION
        self.state.is_editing_metrics = False
        self.state.is_viewing_rewards = True
        self._render()

    def close_metrics_form(self) -> None:
        if self.state is None:
            return

        self.state.is_editing_metrics = False
        self._render()

    def update_logged_user_metrics(self, metric_inputs: DailyMetricInputs) -> None:
        if self.state is None:
            return

        updated_user = self.backend.update_user_info(
            user_id=self.state.logged_user.user_id,
            metric_inputs=metric_inputs,
        )
        self.state.logged_user = updated_user
        self.state.users = self._rank_users(
            [
                updated_user if user.user_id == updated_user.user_id else user
                for user in self.state.users
            ]
        )

        if self.state.selected_candidate.user_id == updated_user.user_id:
            self.state.selected_candidate = updated_user

        self.state.is_editing_metrics = False
        self._render()

    @staticmethod
    def _rank_users(users: list[UserDetails]) -> list[UserDetails]:
        return sorted(users, key=lambda user: user.final_score, reverse=True)
