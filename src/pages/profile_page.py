from __future__ import annotations

import flet as ft

from app_state import AppState
from components import CircularMetric, MetricsGrid, ProfileHeader, SectionTitle
from components.metric_definitions import build_profile_metrics
from models import Metric
from theme import CARD_SHADOW, RING_GRADIENT, SURFACE_COLOR


class ProfilePage(ft.Container):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=12, top=16, right=12, bottom=0)
        self.content = self._build_content(state)

    def _build_content(self, state: AppState) -> ft.Column:
        user = state.logged_user
        metrics = build_profile_metrics(user.main_metric, user.metrics)

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
                    content=CircularMetric(
                        metric=Metric(
                            label="Geral",
                            value=user.final_score,
                            icon=ft.Icons.EMOJI_EVENTS_OUTLINED,
                            color="#FF8A00",
                        ),
                        size=104,
                        stroke_width=8,
                        show_number=True,
                        interactive=False,
                        gradient_colors=RING_GRADIENT,
                    ),
                ),
            ],
        )
