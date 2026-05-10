from __future__ import annotations

import math
from typing import Callable, Sequence

import flet as ft
import flet.canvas as cv

from models import Metric
from theme import RING_GRADIENT, TEXT_PRIMARY_COLOR, TRACK_COLOR


class CircularMetric(ft.Container):
    """Reusable clickable circular progress component."""

    _TRACK_COLOR = TRACK_COLOR
    _DEFAULT_GRADIENT_COLORS = RING_GRADIENT

    def __init__(
        self,
        metric: Metric,
        size: int = 54,
        stroke_width: int = 2,
        show_number: bool = False,
        center_content: ft.Control | None = None,
        toggle_center_content: bool = False,
        gradient_colors: Sequence[str] | None = None,
        clockwise: bool = False,
        interactive: bool = True,
        on_click: Callable[[Metric], None] | None = None,
    ) -> None:
        super().__init__()
        self.metric = metric
        self._size = size
        self._stroke_width = stroke_width
        self._show_number = show_number
        self._center_content = center_content
        self._toggle_center_content = toggle_center_content
        self._gradient_colors = tuple(gradient_colors or self._DEFAULT_GRADIENT_COLORS)
        self._clockwise = clockwise
        self._on_click = on_click
        self.width = size
        self.height = size
        self.border_radius = size // 2
        self.content = self._build_content()
        self.on_click = (lambda e: self._handle_click(e)) if interactive else None
        self.ink = interactive

    def _build_content(self) -> ft.Stack:
        return ft.Stack(
            width=self._size,
            height=self._size,
            alignment=ft.Alignment(0, 0),
            controls=[
                self._build_progress_ring(),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=self._build_center_content(),
                ),
            ],
        )

    def _build_center_content(self) -> ft.Control:
        if self._center_content is not None and not self._show_number:
            return self._center_content

        if self._show_number:
            return ft.Text(
                f"{round(self.metric.value * 100)}",
                size=max(10, self._size // 3),
                weight=ft.FontWeight.BOLD,
                font_family="Roboto",
                color=TEXT_PRIMARY_COLOR,
            )

        return ft.Icon(
            self.metric.icon,
            size=max(14, self._size // 2.5),
            color=self.metric.color,
        )

    def _build_progress_ring(self) -> ft.Stack:
        progress_value = self._clamp_progress(self.metric.value)

        return ft.Stack(
            width=self._size,
            height=self._size,
            controls=[
                cv.Canvas(
                    width=self._size,
                    height=self._size,
                    shapes=[
                        self._build_track_shape(),
                        *self._build_progress_shapes(progress_value),
                    ],
                ),
            ],
        )

    def _build_track_shape(self) -> cv.Oval:
        inset = self._stroke_width / 2
        diameter = self._size - self._stroke_width

        return cv.Oval(
            inset,
            inset,
            diameter,
            diameter,
            paint=ft.Paint(
                color=self._TRACK_COLOR,
                stroke_width=self._stroke_width,
                style=ft.PaintingStyle.STROKE,
                stroke_cap=ft.StrokeCap.BUTT,
            ),
        )

    def _build_progress_shapes(self, value: float) -> list[cv.Arc]:
        if value <= 0:
            return []

        inset = self._stroke_width / 2
        diameter = self._size - self._stroke_width
        direction = 1 if self._clockwise else -1
        total_sweep = direction * value * math.tau
        segment_count = self._segment_count(value)

        return [
            cv.Arc(
                inset,
                inset,
                diameter,
                diameter,
                start_angle=(-math.pi / 2) + (total_sweep * index / segment_count),
                sweep_angle=total_sweep / segment_count,
                use_center=False,
                paint=ft.Paint(
                    color=self._color_at(index / max(1, segment_count - 1)),
                    stroke_width=self._stroke_width,
                    style=ft.PaintingStyle.STROKE,
                    stroke_cap=ft.StrokeCap.BUTT,
                ),
            )
            for index in range(segment_count)
        ]

    def _segment_count(self, value: float) -> int:
        arc_length = self._size * math.pi * value
        return max(8, min(96, math.ceil(arc_length / 3)))

    def _color_at(self, position: float) -> str:
        colors = self._gradient_colors
        if len(colors) == 1:
            return colors[0]

        scaled_position = self._clamp_progress(position) * (len(colors) - 1)
        start_index = min(math.floor(scaled_position), len(colors) - 2)
        end_index = start_index + 1
        local_position = scaled_position - start_index

        return self._interpolate_hex_color(
            colors[start_index],
            colors[end_index],
            local_position,
        )

    @staticmethod
    def _clamp_progress(value: float) -> float:
        return max(0, min(1, value))

    @staticmethod
    def _interpolate_hex_color(start: str, end: str, position: float) -> str:
        start_rgb = CircularMetric._hex_to_rgb(start)
        end_rgb = CircularMetric._hex_to_rgb(end)
        rgb = tuple(
            round(start_channel + (end_channel - start_channel) * position)
            for start_channel, end_channel in zip(start_rgb, end_rgb)
        )

        return "#{:02X}{:02X}{:02X}".format(*rgb)

    @staticmethod
    def _hex_to_rgb(color: str) -> tuple[int, int, int]:
        normalized = color.removeprefix("#")
        if len(normalized) == 3:
            normalized = "".join(channel * 2 for channel in normalized)

        return (
            int(normalized[0:2], 16),
            int(normalized[2:4], 16),
            int(normalized[4:6], 16),
        )

    def set_show_number(self, show_number: bool) -> None:
        self._show_number = show_number
        self.content = self._build_content()
        self.update()

    def _handle_click(self, _: ft.ControlEvent) -> None:
        if self._center_content is None or self._toggle_center_content:
            self._show_number = not self._show_number
        self.content = self._build_content()
        if self._on_click is not None:
            self._on_click(self.metric)
        self.update()
