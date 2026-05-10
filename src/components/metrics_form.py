from __future__ import annotations

from typing import Callable

import flet as ft

from models import MetricName
from theme import (
    BORDER_COLOR,
    PRIMARY_COLOR,
    SURFACE_COLOR,
    TEXT_MUTED_COLOR,
    TEXT_PRIMARY_COLOR,
)


class MetricsForm(ft.Container):
    """Numeric form for editing all user metric values."""

    def __init__(
        self,
        values: dict[MetricName, float],
        on_submit: Callable[[dict[MetricName, float]], None],
        on_cancel: Callable[[], None],
    ) -> None:
        super().__init__()
        self._on_submit = on_submit
        self._fields = {
            metric_name: self._build_field(metric_name, values.get(metric_name, 0))
            for metric_name in MetricName
        }

        self.bgcolor = SURFACE_COLOR
        self.border_radius = 18
        self.padding = 18
        self.content = ft.Column(
            spacing=14,
            controls=[
                ft.Text(
                    "Atualizar metricas",
                    size=18,
                    weight=ft.FontWeight.W_700,
                    color=TEXT_PRIMARY_COLOR,
                ),
                ft.Text(
                    "Informe valores de 0 a 100 para M1, M2, M3 e M4.",
                    size=12,
                    color=TEXT_MUTED_COLOR,
                ),
                ft.Column(spacing=10, controls=list(self._fields.values())),
                ft.Row(
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.TextButton(
                            "Cancelar",
                            on_click=lambda _: on_cancel(),
                        ),
                        ft.ElevatedButton(
                            "Salvar",
                            icon=ft.Icons.SAVE_OUTLINED,
                            bgcolor=PRIMARY_COLOR,
                            color="#FFFFFF",
                            on_click=self._handle_submit,
                        ),
                    ],
                ),
            ],
        )

    def _build_field(self, metric_name: MetricName, value: float) -> ft.TextField:
        return ft.TextField(
            label=metric_name.value,
            value=f"{round(value * 100)}",
            suffix="%",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=BORDER_COLOR,
            focused_border_color=PRIMARY_COLOR,
            border_radius=12,
            text_size=16,
        )

    def _handle_submit(self, _: ft.ControlEvent) -> None:
        metrics: dict[MetricName, float] = {}
        is_valid = True

        for metric_name, field in self._fields.items():
            raw_value = (field.value or "").strip().replace(",", ".")
            try:
                numeric_value = float(raw_value)
            except ValueError:
                field.error = "Use um numero"
                is_valid = False
                continue

            if not 0 <= numeric_value <= 100:
                field.error = "Entre 0 e 100"
                is_valid = False
                continue

            field.error = None
            metrics[metric_name] = numeric_value / 100

        if not is_valid:
            self.update()
            return

        self._on_submit(metrics)
