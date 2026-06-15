from __future__ import annotations

from datetime import date, timedelta

import flet as ft
import flet.canvas as cv

from models import Metric, MetricHistoryEntry, MetricName, UserDetails
from theme import BORDER_COLOR, TEXT_MUTED_COLOR


class WeeklyPerformanceChart(ft.Container):
    _WIDTH = 320
    _HEIGHT = 196
    _LEFT = 36
    _RIGHT = 12
    _TOP = 12
    _BOTTOM = 30
    _Y_TICKS = (0, 25, 50, 75, 100)
    _WEEKDAY_LABELS = ("S", "T", "Q", "Q", "S", "S", "D")

    def __init__(
        self,
        user: UserDetails,
        history: list[MetricHistoryEntry],
        selected_metric: MetricName,
        metric: Metric,
        period_days: int = 7,
    ) -> None:
        super().__init__()
        self.alignment = ft.Alignment(0, 0)
        self.height = self._HEIGHT
        self.content = cv.Canvas(
            width=self._WIDTH,
            height=self._HEIGHT,
            shapes=self._build_shapes(user, history, selected_metric, metric, period_days),
        )

    def _build_shapes(
        self,
        user: UserDetails,
        history: list[MetricHistoryEntry],
        selected_metric: MetricName,
        metric: Metric,
        period_days: int,
    ) -> list[cv.Shape]:
        points = self._build_points(user, history, selected_metric, period_days)
        shapes: list[cv.Shape] = []
        plot_width = self._WIDTH - self._LEFT - self._RIGHT
        plot_height = self._HEIGHT - self._TOP - self._BOTTOM

        grid_paint = ft.Paint(
            color=BORDER_COLOR,
            stroke_width=1,
            style=ft.PaintingStyle.STROKE,
        )
        label_style = ft.TextStyle(size=11, color=TEXT_MUTED_COLOR)

        for tick in self._Y_TICKS:
            y = self._value_to_y(tick / 100, plot_height)
            shapes.append(cv.Line(self._LEFT, y, self._LEFT + plot_width, y, paint=grid_paint))
            shapes.append(
                cv.Text(
                    0,
                    y - 7,
                    str(tick),
                    style=label_style,
                    text_align=ft.TextAlign.RIGHT,
                    max_width=self._LEFT - 8,
                )
            )

        if len(points) == 1:
            points = [points[0], points[0]]

        coordinates = [
            (
                self._LEFT + (plot_width * index / max(1, len(points) - 1)),
                self._value_to_y(value, plot_height),
                entry_date,
            )
            for index, (entry_date, value) in enumerate(points)
        ]

        if coordinates:
            line_elements: list[cv.Path.PathElement] = [
                cv.Path.MoveTo(coordinates[0][0], coordinates[0][1])
            ]
            line_elements.extend(
                cv.Path.LineTo(x, y)
                for x, y, _ in coordinates[1:]
            )
            shapes.append(
                cv.Path(
                    line_elements,
                    paint=ft.Paint(
                        color=metric.color,
                        stroke_width=3,
                        style=ft.PaintingStyle.STROKE,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                )
            )

        point_paint = ft.Paint(color=metric.color, style=ft.PaintingStyle.FILL)
        for x, y, _ in coordinates:
            shapes.append(cv.Circle(x, y, 3.4, paint=point_paint))

        label_step = max(1, (len(coordinates) + 6) // 7)
        for index, (x, _, entry_date) in enumerate(coordinates):
            if index % label_step != 0 and index != len(coordinates) - 1:
                continue

            weekday = self._WEEKDAY_LABELS[entry_date.weekday()]
            shapes.append(
                cv.Text(
                    x - 8,
                    self._HEIGHT - 18,
                    weekday,
                    style=label_style,
                    text_align=ft.TextAlign.CENTER,
                    max_width=16,
                )
            )

        return shapes

    def _value_to_y(self, value: float, plot_height: float) -> float:
        bounded_value = max(0, min(1, value))
        return self._TOP + ((1 - bounded_value) * plot_height)

    def _build_points(
        self,
        user: UserDetails,
        history: list[MetricHistoryEntry],
        selected_metric: MetricName,
        period_days: int,
    ) -> list[tuple[date, float]]:
        snapshots: dict[date, float] = {}
        today = date.today()
        earliest_date = today - timedelta(days=max(0, period_days - 1))

        for entry in history:
            try:
                entry_date = date.fromisoformat(entry.date)
            except ValueError:
                continue

            if entry_date < earliest_date:
                continue

            snapshots[entry_date] = entry.metrics.get(selected_metric, 0)

        snapshots[today] = user.metrics.get(selected_metric, 0)
        return sorted(snapshots.items())
