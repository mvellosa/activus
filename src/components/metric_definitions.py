from __future__ import annotations

import flet as ft

from models import Metric, MetricName

METRIC_DEFINITIONS: tuple[tuple[MetricName, ft.IconData, str], ...] = (
    (MetricName.VITALIDADE, ft.Icons.FAVORITE, "#E90067"),
    (MetricName.CARGA, ft.Icons.FITNESS_CENTER, "#FF8A00"),
    (MetricName.REPOUSO, ft.Icons.HOTEL, "#5B15CE"),
    (MetricName.ANIMO, ft.Icons.MOOD, "#13B8B2"),
)


def build_metrics(metric_values: dict[MetricName, float]) -> list[Metric]:
    """Convert backend metric values into UI metric view models."""

    return [
        Metric(
            label=metric_name.value,
            value=metric_values[metric_name],
            icon=icon,
            color=color,
        )
        for metric_name, icon, color in METRIC_DEFINITIONS
        if metric_name in metric_values
    ]


def build_profile_metrics(main_value: float, metric_values: dict[MetricName, float]) -> list[Metric]:
    return [
        Metric(label="Principal", value=main_value, icon=ft.Icons.PERSON, color="#29B6F6"),
        *build_metrics(metric_values),
    ]
