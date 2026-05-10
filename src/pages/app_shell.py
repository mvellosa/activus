from __future__ import annotations

import flet as ft

from app_state import AppState, AppTab
from components import BottomNav
from models import CandidatesBackend, UserDetails
from theme import APP_BG_COLOR

from .competition_page import CompetitionPage
from .profile_page import ProfilePage


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
            users=users,
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

        if self.state.selected_tab == AppTab.PROFILE:
            body: ft.Control = ProfilePage(self.state)
        else:
            body = CompetitionPage(self.state, on_select_user=self.select_user)

        self.page.clean()
        self.page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        body,
                        BottomNav(
                            selected_tab=self.state.selected_tab,
                            on_change=self.change_tab,
                        ),
                    ],
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
        if self.state is None or self.state.selected_tab == tab:
            return

        self.state.selected_tab = tab
        self._render()
