from __future__ import annotations

from typing import Callable

import flet as ft

from models import Metric, MetricName
from theme import CARD_SHADOW, SURFACE_COLOR, TEXT_MUTED_COLOR

from .circular_metric import CircularMetric


class MetricSelector(ft.Row):
    def __init__(
        self,
        metrics: list[tuple[MetricName, Metric]],
        selected_metric: MetricName,
        on_select: Callable[[MetricName], None],
        compact: bool = False,
        highlight_selected: bool = True,
    ) -> None:
        super().__init__()
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 8
        self.height = 36 if compact else 84
        self.controls = [
            self._build_metric_button(
                metric_name,
                metric,
                selected_metric,
                on_select,
                compact,
                highlight_selected,
            )
            for metric_name, metric in metrics
        ]

    def _build_metric_button(
        self,
        metric_name: MetricName,
        metric: Metric,
        selected_metric: MetricName,
        on_select: Callable[[MetricName], None],
        compact: bool,
        highlight_selected: bool,
    ) -> ft.Control:
        selected = highlight_selected and metric_name == selected_metric
        size = 32 if compact else 54
        icon_size = 16 if compact else 24

        if compact:
            indicator: ft.Control = ft.Container(
                width=size,
                height=size,
                border_radius=size // 2,
                bgcolor=self._tint_color(metric.color, 0.84) if selected else SURFACE_COLOR,
                border=ft.Border.all(
                    1,
                    self._tint_color(metric.color, 0.62) if selected else "#EFEAF7",
                ),
                shadow=CARD_SHADOW,
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(metric.icon, size=icon_size, color=metric.color),
            )
        elif selected:
            indicator = ft.Container(
                width=size,
                height=size,
                border_radius=size // 2,
                bgcolor=self._tint_color(metric.color, 0.78),
                border=ft.Border.all(1, self._tint_color(metric.color, 0.62)),
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(metric.icon, size=icon_size, color=metric.color),
            )
        else:
            indicator = CircularMetric(
                metric=metric,
                size=size,
                stroke_width=3 if compact else 5,
                show_number=False,
                interactive=False,
                gradient_colors=(metric.color, "#EDE8F5"),
            )

        content: ft.Control
        if compact:
            content = indicator
        else:
            content = ft.Column(
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    indicator,
                    ft.Container(
                        width=86,
                        height=20,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(
                            metric.label,
                            size=10,
                            weight=ft.FontWeight.W_600,
                            color=metric.color if selected else TEXT_MUTED_COLOR,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=1,
                            no_wrap=True,
                            overflow=ft.TextOverflow.VISIBLE,
                        ),
                    ),
                ],
            )

        return ft.Container(
            width=86 if not compact else size,
            height=82 if not compact else size,
            alignment=ft.Alignment(0, 0),
            ink=True,
            border_radius=36 if not compact else size // 2,
            on_click=lambda _: on_select(metric_name),
            content=content,
        )

    def _tint_color(self, color: str, white_amount: float) -> str:
        amount = max(0, min(1, white_amount))
        red, green, blue = self._hex_to_rgb(color)
        tinted = (
            round(red + (255 - red) * amount),
            round(green + (255 - green) * amount),
            round(blue + (255 - blue) * amount),
        )
        return "#{:02X}{:02X}{:02X}".format(*tinted)

    def _hex_to_rgb(self, color: str) -> tuple[int, int, int]:
        normalized = color.removeprefix("#")
        if len(normalized) == 3:
            normalized = "".join(channel * 2 for channel in normalized)

        return (
            int(normalized[0:2], 16),
            int(normalized[2:4], 16),
            int(normalized[4:6], 16),
        )
