from __future__ import annotations

import flet as ft
from typing import Callable

from app_state import AppState
from components import MainUserCard, SectionTitle, UsersList
from models import UserDetails
from theme import CARD_SHADOW


class CompetitionPage(ft.Container):
    def __init__(
        self,
        state: AppState,
        on_select_user: Callable[[UserDetails], None],
        on_open_rewards: Callable[[], None],
    ) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=12, top=16, right=12, bottom=0)
        self.content = ft.Stack(
            expand=True,
            controls=[
                self._build_content(state, on_select_user),
                self._build_rewards_button(on_open_rewards),
            ],
        )

    def _build_content(
        self,
        state: AppState,
        on_select_user: Callable[[UserDetails], None],
    ) -> ft.Column:
        return ft.Column(
            spacing=12,
            controls=[
                SectionTitle("Competicao"),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=MainUserCard(state.selected_candidate),
                ),
                SectionTitle("Social"),
                ft.Container(
                    expand=True,
                    padding=ft.Padding(left=6, top=0, right=6, bottom=0),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                        controls=[
                            UsersList(
                                users=state.users,
                                selected_user_id=state.selected_candidate.user_id,
                                on_select=on_select_user,
                            )
                        ],
                    ),
                ),
            ],
        )

    def _build_rewards_button(self, on_open_rewards: Callable[[], None]) -> ft.Container:
        return ft.Container(
            right=10,
            bottom=16,
            width=58,
            height=58,
            border_radius=29,
            shadow=CARD_SHADOW,
            content=ft.FloatingActionButton(
                icon=ft.Icons.CARD_GIFTCARD,
                bgcolor="#FF8A00",
                foreground_color="#FFFFFF",
                on_click=lambda _: on_open_rewards(),
            ),
        )
