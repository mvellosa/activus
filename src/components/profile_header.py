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
            height=202,
            controls=[
                ft.Container(
                    height=154,
                    border_radius=ft.BorderRadius.only(
                        bottom_left=0,
                        bottom_right=0,
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=list(PROFILE_BANNER_GRADIENT),
                    ),
                    content=ft.Stack(
                        controls=[
                            ft.Container(
                                left=-28,
                                top=58,
                                width=138,
                                height=86,
                                border_radius=48,
                                bgcolor="#4B0E93",
                                opacity=0.82,
                            ),
                            ft.Container(
                                left=116,
                                top=36,
                                width=146,
                                height=128,
                                border_radius=60,
                                bgcolor="#3D087E",
                                opacity=0.9,
                            ),
                            ft.Container(
                                right=-18,
                                top=88,
                                width=118,
                                height=50,
                                border_radius=30,
                                bgcolor="#4B0E93",
                                opacity=0.88,
                            ),
                        ]
                    ),
                ),
                ft.Container(
                    top=102,
                    left=0,
                    right=0,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Stack(
                        width=112,
                        height=112,
                        controls=[
                            ft.Container(
                                width=104,
                                height=104,
                                border_radius=52,
                                padding=5,
                                bgcolor=SURFACE_COLOR,
                                content=ft.Container(
                                    border_radius=48,
                                    bgcolor=APP_BG_COLOR,
                                    content=UserAvatar(self.user, size=94),
                                ),
                            ),
                            ft.Container(
                                right=5,
                                bottom=10,
                                width=34,
                                height=34,
                                border_radius=17,
                                bgcolor=APP_BG_COLOR,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.EDIT_OUTLINED,
                                    size=27,
                                    color=TEXT_MUTED_COLOR,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )
