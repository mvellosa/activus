from __future__ import annotations

import flet as ft
from typing import Callable

from app_state import AppState
from components import MainUserCard, SectionTitle, UsersList
from models import UserDetails
from theme import CARD_SHADOW


class CompetitionPage(ft.Container):
    _CARD_COMPRESSION_SCROLL_DISTANCE = 140

    def __init__(
        self,
        state: AppState,
        on_select_user: Callable[[UserDetails], None],
        on_open_rewards: Callable[[], None],
    ) -> None:
        super().__init__()
        self._main_user_card = MainUserCard(state.selected_candidate)
        self._users_scroll_spacer = ft.Container(height=0)
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
                    content=self._main_user_card,
                ),
                SectionTitle("Social"),
                ft.Container(
                    expand=True,
                    padding=ft.Padding(left=6, top=0, right=6, bottom=0),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        on_scroll=self._handle_users_scroll,
                        spacing=0,
                        controls=[
                            self._users_scroll_spacer,
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

    def _handle_users_scroll(self, event: ft.OnScrollEvent) -> None:
        consumed_scroll = min(event.pixels, self._CARD_COMPRESSION_SCROLL_DISTANCE)
        compression = consumed_scroll / self._CARD_COMPRESSION_SCROLL_DISTANCE
        self._main_user_card.set_compression(compression)
        self._set_users_scroll_spacer(consumed_scroll)

    def _set_users_scroll_spacer(self, height: float) -> None:
        if self._users_scroll_spacer.height == height:
            return

        self._users_scroll_spacer.height = height
        try:
            self._users_scroll_spacer.update()
        except RuntimeError:
            pass

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
