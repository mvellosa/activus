from __future__ import annotations

import flet as ft

from models import Metric, MetricName

METRIC_DEFINITIONS: tuple[tuple[MetricName, ft.IconData], ...] = (
    (MetricName.M1, ft.Icons.TIMER_OUTLINED),
    (MetricName.M2, ft.Icons.SPEED_OUTLINED),
    (MetricName.M3, ft.Icons.STAR_BORDER_OUTLINED),
)


def build_metrics(metric_values: dict[MetricName, float]) -> list[Metric]:
    """Convert backend metric values into UI metric view models."""

    return [
        Metric(label=metric_name.value, value=metric_values[metric_name], icon=icon)
        for metric_name, icon in METRIC_DEFINITIONS
        if metric_name in metric_values
    ]
