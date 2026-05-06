from __future__ import annotations

from typing import Callable

import flet as ft

from models import Metric


class CircularMetric(ft.Container):
    """Reusable clickable circular progress component."""

    def __init__(
        self,
        metric: Metric,
        size: int = 54,
        stroke_width: int = 4,
        show_number: bool = False,
        on_click: Callable[[Metric], None] | None = None,
    ) -> None:
        super().__init__()
        self.metric = metric
        self._size = size
        self._stroke_width = stroke_width
        self._show_number = show_number
        self._on_click = on_click
        self.width = size
        self.height = size
        self.border_radius = size // 2
        self.content = self._build_content()
        self.on_click = lambda e: self._handle_click(e)
        self.ink = True

    def _build_content(self) -> ft.Stack:
        center_content: ft.Control
        if self._show_number:
            center_content = ft.Text(
                f"{round(self.metric.value * 100)}",
                size=max(10, self._size // 5),
                weight=ft.FontWeight.BOLD,
                color="#1F1A2E",
            )
        else:
            center_content = ft.Icon(
                self.metric.icon,
                size=max(14, self._size // 3),
                color=self.metric.color,
            )

        return ft.Stack(
            width=self._size,
            height=self._size,
            alignment=ft.Alignment(0, 0),
            controls=[
                ft.ProgressRing(
                    value=self.metric.value,
                    width=self._size,
                    height=self._size,
                    stroke_width=self._stroke_width,
                    color=self.metric.color,
                    bgcolor="#ECE9F4",
                ),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=center_content,
                ),
            ],
        )

    def set_show_number(self, show_number: bool) -> None:
        self._show_number = show_number
        self.content = self._build_content()
        self.update()

    def _handle_click(self, _: ft.ControlEvent) -> None:
        self._show_number = not self._show_number
        self.content = self._build_content()
        if self._on_click is not None:
            self._on_click(self.metric)
        self.update()
