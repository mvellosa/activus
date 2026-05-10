from __future__ import annotations

import flet as ft

from models import UserDetails
from theme import (
    APP_BG_COLOR,
    PROFILE_BANNER_GRADIENT,
    SURFACE_COLOR,
    TEXT_MUTED_COLOR,
    TEXT_PRIMARY_COLOR,
)

from .user_avatar import UserAvatar


class ProfileHeader(ft.Container):
    def __init__(self, user: UserDetails) -> None:
        super().__init__()
        self.user = user
        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        return ft.Column(
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self._build_banner(),
                ft.Container(height=38),
                ft.Text(
                    self.user.name,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY_COLOR,
                ),
                ft.Container(height=4),
                ft.Text(
                    self.user.subtitle,
                    size=11,
                    color=TEXT_MUTED_COLOR,
                ),
            ],
        )

    def _build_banner(self) -> ft.Stack:
        return ft.Stack(
            height=132,
            controls=[
                ft.Container(
                    height=104,
                    border_radius=18,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=list(PROFILE_BANNER_GRADIENT),
                    ),
                    content=ft.Stack(
                        controls=[
                            ft.Container(
                                left=0,
                                right=0,
                                bottom=-18,
                                height=82,
                                border_radius=ft.BorderRadius.only(
                                    top_left=52,
                                    top_right=52,
                                    bottom_left=18,
                                    bottom_right=18,
                                ),
                                bgcolor="#4B0E93",
                                opacity=0.65,
                            ),
                            ft.Container(
                                left=22,
                                top=30,
                                width=86,
                                height=44,
                                border_radius=ft.BorderRadius.only(
                                    top_left=48,
                                    top_right=48,
                                    bottom_left=28,
                                    bottom_right=28,
                                ),
                                bgcolor="#7B39E6",
                                opacity=0.35,
                            ),
                            ft.Container(
                                right=28,
                                top=10,
                                width=74,
                                height=74,
                                border_radius=37,
                                bgcolor="#7B39E6",
                                opacity=0.22,
                            ),
                        ]
                    ),
                ),
                ft.Container(
                    top=66,
                    left=0,
                    right=0,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Container(
                        width=76,
                        height=76,
                        border_radius=38,
                        padding=4,
                        bgcolor=SURFACE_COLOR,
                        content=ft.Container(
                            border_radius=34,
                            bgcolor=APP_BG_COLOR,
                            content=UserAvatar(self.user, size=68),
                        ),
                    ),
                ),
            ],
        )
