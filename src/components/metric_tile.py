from __future__ import annotations

import flet as ft

from models import Metric
from theme import SURFACE_COLOR

from .circular_metric import CircularMetric


class MetricTile(ft.Container):
    def __init__(self, metric: Metric) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=8, top=12, right=8, bottom=12)
        self.alignment = ft.Alignment(0, 0)
        self.bgcolor = SURFACE_COLOR
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                CircularMetric(
                    metric=metric,
                    size=48,
                    stroke_width=5,
                    show_number=True,
                    interactive=False,
                    gradient_colors=(metric.color, "#FFE7C6"),
                ),
                ft.Text(
                    metric.label,
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=metric.color,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )
