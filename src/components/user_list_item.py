from __future__ import annotations

from typing import Callable

import flet as ft

from models import Metric, UserDetails

from .circular_metric import CircularMetric
from .user_avatar import UserAvatar


class UserListItem(ft.Container):
    """Row item for a candidate in the bottom list."""

    def __init__(
        self,
        user: UserDetails,
        selected: bool,
        on_select: Callable[[UserDetails], None],
    ) -> None:
        super().__init__()
        self.user = user
        self._on_select = on_select
        self.on_click = lambda e: self._handle_click(e)
        self.ink = True
        self.border_radius = 14
        self.padding = ft.Padding(left=12, top=10, right=12, bottom=10)
        self.bgcolor = "#F7F5FC" if selected else "#FFFFFF"
        self.border = ft.Border.all(1, "#E9E4F2") if selected else None
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color="#1600211A",
            offset=ft.Offset(0, 3),
        )
        self.content = self._build_content()

    def _build_content(self) -> ft.Row:
        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                UserAvatar(self.user, size=46),
                ft.Column(
                    spacing=1,
                    expand=True,
                    controls=[
                        ft.Text(
                            self.user.name,
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color="#2D253C",
                        ),
                        ft.Text(
                            self.user.subtitle,
                            size=10,
                            color="#9A95A5",
                        ),
                    ],
                ),
                CircularMetric(
                    metric=Metric(
                        label="Final",
                        value=self.user.final_score,
                        icon=ft.Icons.EMOJI_EVENTS_OUTLINED,
                        color="#FF9800",
                    ),
                    size=42,
                    stroke_width=6,
                    show_number=True,
                    interactive=False,
                ),
            ],
        )

    def _handle_click(self, _: ft.ControlEvent) -> None:
        self._on_select(self.user)
