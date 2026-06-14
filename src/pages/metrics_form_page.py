from __future__ import annotations

from typing import Callable

import flet as ft

from components import MetricsForm, SectionTitle
from components.metric_definitions import METRIC_DEFINITIONS
from models import DailyMetricInputs, MetricHistoryEntry, MetricName, UserDetails
from theme import (
    BORDER_COLOR,
    CARD_SHADOW,
    SURFACE_COLOR,
    TEXT_MUTED_COLOR,
    TEXT_PRIMARY_COLOR,
)


class MetricsFormPage(ft.Container):
    def __init__(
        self,
        user: UserDetails,
        history: list[MetricHistoryEntry],
        on_submit: Callable[[DailyMetricInputs], None],
        on_cancel: Callable[[], None],
    ) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=12, top=16, right=12, bottom=0)
        self.content = ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._build_header(on_cancel),
                MetricsForm(
                    values=user.metric_inputs,
                    on_submit=on_submit,
                    on_cancel=on_cancel,
                ),
                SectionTitle("Histórico"),
                self._build_history(history),
            ],
        )

    def _build_header(self, on_cancel: Callable[[], None]) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Editar perfil",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY_COLOR,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=TEXT_PRIMARY_COLOR,
                    on_click=lambda _: on_cancel(),
                ),
            ],
        )

    def _build_history(self, history: list[MetricHistoryEntry]) -> ft.Container:
        if not history:
            content: ft.Control = ft.Text(
                "Nenhum histórico disponível.",
                size=13,
                color=TEXT_MUTED_COLOR,
            )
        else:
            content = ft.Column(
                spacing=0,
                controls=[
                    self._build_history_row(entry, show_divider=index < len(history) - 1)
                    for index, entry in enumerate(history)
                ],
            )

        return ft.Container(
            bgcolor=SURFACE_COLOR,
            border_radius=16,
            shadow=CARD_SHADOW,
            padding=14,
            content=content,
        )

    def _build_history_row(
        self,
        entry: MetricHistoryEntry,
        show_divider: bool,
    ) -> ft.Control:
        row = ft.Column(
            spacing=10,
            controls=[
                ft.Text(
                    f"{entry.date} · Geral {round(entry.final_score * 100)}",
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_MUTED_COLOR,
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        self._build_history_chip(metric_name, entry.metrics.get(metric_name, 0), color)
                        for metric_name, _, color in METRIC_DEFINITIONS
                    ],
                ),
            ],
        )

        controls: list[ft.Control] = [
            ft.Container(
                padding=ft.Padding(left=0, top=8, right=0, bottom=10),
                content=row,
            )
        ]

        if show_divider:
            controls.append(ft.Divider(height=1, thickness=1, color=BORDER_COLOR))

        return ft.Column(spacing=0, controls=controls)

    def _build_history_chip(
        self,
        metric_name: MetricName,
        value: float,
        color: str,
    ) -> ft.Container:
        return ft.Container(
            expand=True,
            border_radius=12,
            padding=ft.Padding(left=8, top=8, right=8, bottom=8),
            bgcolor="#F8F6FC",
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text(
                        metric_name.value,
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=color,
                    ),
                    ft.Text(
                        f"{round(value * 100)}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY_COLOR,
                    ),
                ],
            ),
        )
