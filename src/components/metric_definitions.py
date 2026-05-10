from __future__ import annotations

import flet as ft

from models import Metric, MetricName

METRIC_DEFINITIONS: tuple[tuple[MetricName, ft.IconData, str], ...] = (
    (MetricName.M1, ft.Icons.TIMER_OUTLINED, "#29B6F6"),
    (MetricName.M2, ft.Icons.SPEED_OUTLINED, "#FF9800"),
    (MetricName.M3, ft.Icons.STAR_BORDER_OUTLINED, "#FFD54F"),
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
