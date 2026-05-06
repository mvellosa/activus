from __future__ import annotations

import flet as ft

from components import BottomNav, MainUserCard, UsersList
from models import CandidatesBackend, UserDetails


class CompetitionApp:
    """Composes the page using a small injected backend."""

    def __init__(self, backend: CandidatesBackend) -> None:
        self.backend = backend
        self.users: list[UserDetails] = []
        self.selected_user: UserDetails | None = None
        self.main_card: MainUserCard | None = None
        self.users_list: UsersList | None = None

    def build(self, page: ft.Page) -> None:
        self.users = self.backend.get_candidates()
        if not self.users:
            page.add(ft.Text("No candidates available."))
            return

        self.selected_user = self.users[0]
        self.main_card = MainUserCard(self.selected_user)
        self.users_list = UsersList(
            users=self.users,
            selected_user_id=self.selected_user.user_id,
            on_select=self.select_user,
        )

        page.title = "Competicao"
        page.window.width = 420
        page.window.height = 760
        page.padding = 0
        page.bgcolor = "#F5F2FA"
        page.theme_mode = ft.ThemeMode.LIGHT

        page.add(
            ft.Container(
                expand=True,
                padding=ft.Padding(left=12, top=16, right=12, bottom=0),
                content=ft.Column(
                    spacing=12,
                    controls=[
                        self._build_section_title("Competicao"),
                        ft.Container(
                            alignment=ft.Alignment(0, 0),
                            content=self.main_card,
                        ),
                        self._build_section_title("Social"),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding(left=6, top=0, right=6, bottom=0),
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=0,
                                controls=[self.users_list],
                            ),
                        ),
                        BottomNav(),
                    ],
                ),
            )
        )

    def select_user(self, user: UserDetails) -> None:
        self.selected_user = user
        if self.main_card is not None:
            self.main_card.update_user(user)
        if self.users_list is not None:
            self.users_list.update_selection(user.user_id)

    @staticmethod
    def _build_section_title(title: str) -> ft.Container:
        return ft.Container(
            padding=ft.Padding(left=8, top=0, right=8, bottom=0),
            content=ft.Text(
                title,
                size=16,
                weight=ft.FontWeight.BOLD,
                color="#2D253C",
            ),
        )
