from __future__ import annotations

from typing import Callable

import flet as ft

from app_state import AppState
from components import CircularMetric, MetricsGrid, ProfileHeader, SectionTitle
from components.metric_definitions import build_metrics
from models import Metric
from theme import CARD_SHADOW, RING_GRADIENT, SURFACE_COLOR


class ProfilePage(ft.Container):
    def __init__(self, state: AppState, on_edit_metrics: Callable[[], None]) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=12, top=16, right=12, bottom=0)
        self.content = ft.Stack(
            expand=True,
            controls=[
                self._build_content(state),
                self._build_edit_button(on_edit_metrics),
            ],
        )

    def _build_content(self, state: AppState) -> ft.Column:
        user = state.logged_user
        metrics = build_metrics(user.metrics)

        return ft.Column(
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ProfileHeader(user),
                SectionTitle("Metricas"),
                MetricsGrid(metrics),
                SectionTitle("Geral"),
                ft.Container(
                    bgcolor=SURFACE_COLOR,
                    border_radius=16,
                    shadow=CARD_SHADOW,
                    padding=24,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            CircularMetric(
                                metric=Metric(
                                    label="Geral",
                                    value=user.main_metric,
                                    icon=ft.Icons.EMOJI_EVENTS_OUTLINED,
                                    color="#FF8A00",
                                ),
                                size=104,
                                stroke_width=8,
                                show_number=True,
                                interactive=False,
                                gradient_colors=RING_GRADIENT,
                            ),
                            ft.Text(
                                "readiness",
                                size=11,
                                weight=ft.FontWeight.W_500,
                                color="#FF8A00",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _build_edit_button(self, on_edit_metrics: Callable[[], None]) -> ft.Container:
        return ft.Container(
            right=10,
            bottom=16,
            width=58,
            height=58,
            border_radius=29,
            shadow=CARD_SHADOW,
            content=ft.FloatingActionButton(
                icon=ft.Icons.EDIT_NOTE,
                bgcolor="#FF8A00",
                foreground_color="#FFFFFF",
                on_click=lambda _: on_edit_metrics(),
            ),
        )
