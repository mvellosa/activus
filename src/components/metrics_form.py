from __future__ import annotations

from typing import Callable

import flet as ft

from models import DailyMetricInputs, MoodLevel
from theme import (
    BORDER_COLOR,
    PRIMARY_COLOR,
    SURFACE_COLOR,
    TEXT_MUTED_COLOR,
    TEXT_PRIMARY_COLOR,
)


class MetricsForm(ft.Container):
    """Form for collecting raw values used to calculate readiness metrics."""

    def __init__(
        self,
        values: DailyMetricInputs,
        on_submit: Callable[[DailyMetricInputs], None],
        on_cancel: Callable[[], None],
    ) -> None:
        super().__init__()
        self._on_submit = on_submit
        self._fields = {
            "rmssd_day": self._build_number_field("RMSSD do dia", values.rmssd_day, "ms"),
            "rmssd_baseline": self._build_number_field("RMSSD baseline", values.rmssd_baseline, "ms"),
            "acute_load": self._build_number_field("Carga aguda", values.acute_load),
            "chronic_load": self._build_number_field("Carga crônica", values.chronic_load),
            "total_sleep_hours": self._build_number_field("TST", values.total_sleep_hours, "h"),
            "sleep_efficiency": self._build_number_field("Eficiência do sono", values.sleep_efficiency, "%"),
            "deep_sleep_percent": self._build_number_field("Sono N3", values.deep_sleep_percent, "%"),
        }
        self._mood_field = self._build_mood_field(values.mood)

        self.bgcolor = SURFACE_COLOR
        self.border_radius = 18
        self.padding = 18
        self.content = ft.Column(
            spacing=14,
            controls=self._build_form_controls(on_cancel),
        )

    def _build_form_controls(self, on_cancel: Callable[[], None]) -> list[ft.Control]:
        return [
            ft.Text(
                "Atualizar métricas",
                size=18,
                weight=ft.FontWeight.W_700,
                color=TEXT_PRIMARY_COLOR,
            ),
            ft.Text(
                "Informe os dados de coleta. O app calcula Vitalidade, Carga, Repouso, Ânimo e readiness.",
                size=12,
                color=TEXT_MUTED_COLOR,
            ),
            self._build_section("Vitalidade", ["rmssd_day", "rmssd_baseline"]),
            self._build_section("Carga", ["acute_load", "chronic_load"]),
            self._build_section(
                "Repouso",
                ["total_sleep_hours", "sleep_efficiency", "deep_sleep_percent"],
            ),
            self._build_mood_section(),
            ft.Row(
                spacing=10,
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.TextButton(
                        "Cancelar",
                        on_click=lambda _: on_cancel(),
                    ),
                    ft.Button(
                        "Salvar",
                        icon=ft.Icons.SAVE_OUTLINED,
                        bgcolor=PRIMARY_COLOR,
                        color="#FFFFFF",
                        on_click=self._handle_submit,  # pyright: ignore[reportArgumentType]
                    ),
                ],
            ),
        ]

    def _build_section(self, title: str, field_names: list[str]) -> ft.Container:
        return ft.Container(
            border_radius=14,
            border=ft.Border.all(1, BORDER_COLOR),
            padding=12,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        title,
                        size=13,
                        weight=ft.FontWeight.W_700,
                        color=TEXT_PRIMARY_COLOR,
                    ),
                    *[self._fields[field_name] for field_name in field_names],
                ],
            ),
        )

    def _build_mood_section(self) -> ft.Container:
        return ft.Container(
            border_radius=14,
            border=ft.Border.all(1, BORDER_COLOR),
            padding=12,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        "Ânimo",
                        size=13,
                        weight=ft.FontWeight.W_700,
                        color=TEXT_PRIMARY_COLOR,
                    ),
                    self._mood_field,
                ],
            ),
        )

    def _build_number_field(
        self,
        label: str,
        value: float,
        suffix: str | None = None,
    ) -> ft.TextField:
        return ft.TextField(
            label=label,
            value=f"{value:.1f}".rstrip("0").rstrip("."),
            suffix=suffix,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=BORDER_COLOR,
            focused_border_color=PRIMARY_COLOR,
            border_radius=12,
            text_size=15,
        )

    def _build_mood_field(self, value: MoodLevel) -> ft.Dropdown:
        return ft.Dropdown(
            label="Percepção subjetiva",
            value=value.value,
            options=[
                ft.dropdown.Option(key=mood.value, text=mood.value)
                for mood in MoodLevel
            ],
            border_color=BORDER_COLOR,
            focused_border_color=PRIMARY_COLOR,
            border_radius=12,
            text_size=15,
        )

    def _parse_positive_field(self, field_name: str) -> float | None:
        field = self._fields[field_name]
        raw_value = (field.value or "").strip().replace(",", ".")

        try:
            numeric_value = float(raw_value)
        except ValueError:
            field.error = "Use um número"
            return None

        if numeric_value < 0:
            field.error = "Use valor positivo"
            return None

        field.error = None
        return numeric_value

    def _handle_submit(self, _: ft.ControlEvent) -> None:
        values: dict[str, float] = {}
        is_valid = True

        for field_name in self._fields:
            numeric_value = self._parse_positive_field(field_name)
            if numeric_value is None:
                is_valid = False
                continue
            values[field_name] = numeric_value

        if values.get("rmssd_baseline") == 0:
            self._fields["rmssd_baseline"].error = "Maior que zero"
            is_valid = False

        if values.get("chronic_load") == 0:
            self._fields["chronic_load"].error = "Maior que zero"
            is_valid = False

        for percent_field in ("sleep_efficiency", "deep_sleep_percent"):
            if values.get(percent_field, 0) > 100:
                self._fields[percent_field].error = "Entre 0 e 100"
                is_valid = False

        try:
            mood = MoodLevel(self._mood_field.value)
            self._mood_field.error_text = None
        except ValueError:
            mood = MoodLevel.NEUTRO
            self._mood_field.error_text = "Escolha uma opção"
            is_valid = False

        if not is_valid:
            self.update()
            return

        self._on_submit(
            DailyMetricInputs(
                rmssd_day=values["rmssd_day"],
                rmssd_baseline=values["rmssd_baseline"],
                acute_load=values["acute_load"],
                chronic_load=values["chronic_load"],
                total_sleep_hours=values["total_sleep_hours"],
                sleep_efficiency=values["sleep_efficiency"],
                deep_sleep_percent=values["deep_sleep_percent"],
                mood=mood,
            )
        )
