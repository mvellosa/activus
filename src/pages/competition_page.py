from __future__ import annotations

import flet as ft
from typing import Callable

from app_state import AppState
from components import MainUserCard, SectionTitle, UsersList
from models import UserDetails


class CompetitionPage(ft.Container):
    def __init__(self, state: AppState, on_select_user: Callable[[UserDetails], None]) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=12, top=16, right=12, bottom=0)
        self.content = ft.Column(
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
