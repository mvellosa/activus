from __future__ import annotations

import math
from typing import Callable, Sequence

import flet as ft

from models import Metric


class CircularMetric(ft.Container):
    """Reusable clickable circular progress component."""

    _TRACK_COLOR = "#ECE9F4"
    _DEFAULT_GRADIENT_COLORS = ("#6322C6", "#FF8A00")

    def __init__(
        self,
        metric: Metric,
        size: int = 54,
        stroke_width: int = 4,
        show_number: bool = False,
        center_content: ft.Control | None = None,
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
        if self._center_content is not None:
            return self._center_content

        if self._show_number:
            return ft.Text(
                f"{round(self.metric.value * 100)}",
                size=max(10, self._size // 3),
                weight=ft.FontWeight.BOLD,
                font_family="Roboto",
                color="#303030",
            )

        return ft.Icon(
            self.metric.icon,
            size=max(14, self._size // 2.5),
            color=self.metric.color,
        )

    def _build_progress_ring(self) -> ft.Stack:
        return ft.Stack(
            width=self._size,
            height=self._size,
            controls=[
                ft.ProgressRing(
                    value=1,
                    width=self._size,
                    height=self._size,
                    stroke_width=self._stroke_width,
                    color=self._TRACK_COLOR,
                    bgcolor="transparent",
                ),
                ft.ShaderMask(
                    blend_mode=ft.BlendMode.SRC_IN,
                    shader=ft.SweepGradient(
                        colors=list(self._gradient_colors),
                        rotation=-math.pi / 2,
                    ),
                    flip=None if self._clockwise else ft.Flip(flip_x=True),
                    content=ft.ProgressRing(
                        value=self.metric.value,
                        width=self._size,
                        height=self._size,
                        stroke_width=self._stroke_width,
                        color="#FFFFFF",
                        bgcolor="transparent",
                    ),
                ),
            ],
        )

    def set_show_number(self, show_number: bool) -> None:
        self._show_number = show_number
        self.content = self._build_content()
        self.update()

    def _handle_click(self, _: ft.ControlEvent) -> None:
        if self._center_content is None:
            self._show_number = not self._show_number
        self.content = self._build_content()
        if self._on_click is not None:
            self._on_click(self.metric)
        self.update()
