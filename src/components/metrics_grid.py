from __future__ import annotations

import flet as ft

from models import Metric
from theme import BORDER_COLOR, CARD_SHADOW, SURFACE_COLOR

from .metric_tile import MetricTile


class MetricsGrid(ft.Container):
    def __init__(self, metrics: list[Metric]) -> None:
        super().__init__()
        self.bgcolor = SURFACE_COLOR
        self.border_radius = 16
        self.shadow = CARD_SHADOW
        self.padding = 12

        rows: list[ft.Control] = []
        chunk_size = 2
        for start in range(0, len(metrics), chunk_size):
            metric_pair = metrics[start:start + chunk_size]
            tile_controls: list[ft.Control] = []
            for index, metric in enumerate(metric_pair):
                tile_controls.append(MetricTile(metric))
                if index < len(metric_pair) - 1:
                    tile_controls.append(
                        ft.VerticalDivider(width=1, thickness=1, color=BORDER_COLOR)
                    )

            rows.append(
                ft.Row(
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=tile_controls,
                )
            )

            if start + chunk_size < len(metrics):
                rows.append(ft.Divider(height=1, thickness=1, color=BORDER_COLOR))

        self.content = ft.Column(spacing=0, controls=rows)
