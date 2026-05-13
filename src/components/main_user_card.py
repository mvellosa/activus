import flet as ft

from models import Metric, UserDetails
from theme import SURFACE_COLOR, TEXT_MUTED_COLOR

from .circular_metric import CircularMetric
from .metric_definitions import build_metrics
from .user_avatar import UserAvatar


class MainUserCard(ft.Card):
    """Main card showing the selected user and primary metrics."""

    def __init__(self, user: UserDetails) -> None:
        super().__init__()
        self.user = user
        self._compression = 0.0
        self.elevation = 4
        self.color = SURFACE_COLOR
        self.surface_tint_color = SURFACE_COLOR
        self.shape = ft.RoundedRectangleBorder(radius=24)
        self.content = self._build_content()

    def _build_content(self) -> ft.Container:
        compression = self._compression
        padding = round(self._lerp(18, 10, compression))
        height = round(self._lerp(246, 80, compression))

        return ft.Container(
            padding=ft.Padding(left=padding, top=padding, right=padding, bottom=padding),
            width=340,
            height=height,
            animate_size=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
            content=self.__metrics_stack(340 - (padding * 2), height - (padding * 2)),
        )

    def __metrics_stack(self, width: int, height: int) -> ft.Stack:
        compression = self._compression
        big_size = round(self._lerp(138, 58, compression))
        big_avatar_size = round(self._lerp(92, 34, compression))
        big_stroke_width = max(4, round(big_size * 0.07))
        big_left = self._lerp((width - big_size) / 2, 0, compression)
        big_top = self._lerp(0, 0, compression)

        metrics = build_metrics(self.user.metrics)
        compact_start = self._lerp(0, 104, compression)
        metric_size = round(self._lerp(58, 38, compression))
        metric_stroke_width = round(self._lerp(5, 4, compression))
        expanded_gap = (width - (len(metrics) * metric_size)) / max(1, len(metrics) + 1)
        compact_gap = 12
        metric_top = self._lerp(154, 4, compression)
        value_top = metric_top + metric_size + self._lerp(5, -1, compression)

        controls: list[ft.Control] = [
            ft.Container(
                left=big_left,
                top=big_top,
                content=CircularMetric(
                    metric=Metric(
                        label="Main",
                        value=self.user.main_metric,
                        icon=ft.Icons.PERSON,
                    ),
                    size=big_size,
                    stroke_width=big_stroke_width,
                    center_content=UserAvatar(self.user, size=big_avatar_size),
                    toggle_center_content=True,
                    gradient_colors=("#6322C6", "#07484D"),
                    interactive=True,
                ),
            ),
        ]

        for index, metric in enumerate(metrics):
            expanded_left = expanded_gap + (index * (metric_size + expanded_gap))
            compact_left = compact_start + (index * (metric_size + compact_gap))
            left = self._lerp(expanded_left, compact_left, compression)

            controls.extend(
                [
                    ft.Container(
                        left=left,
                        top=metric_top,
                        content=CircularMetric(
                            metric=metric,
                            size=metric_size,
                            stroke_width=metric_stroke_width,
                            toggle_center_content=True,
                            interactive=True,
                        ),
                    ),
                    ft.Container(
                        left=left,
                        top=value_top,
                        width=metric_size,
                        opacity=compression,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(
                            str(round(metric.value * 10)),
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_MUTED_COLOR,
                        ),
                    ),
                ]
            )

        return ft.Stack(
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            controls=controls,
        )

    def set_compression(self, compression: float) -> None:
        normalized = self._clamp(compression)
        if abs(normalized - self._compression) < 0.02:
            return

        self._compression = normalized
        self.content = self._build_content()
        self._update_if_mounted()

    def update_user(self, user: UserDetails) -> None:
        self.user = user
        self.content = self._build_content()
        self._update_if_mounted()

    def _update_if_mounted(self) -> None:
        try:
            self.update()
        except RuntimeError:
            pass

    @staticmethod
    def _lerp(start: float, end: float, progress: float) -> float:
        return start + ((end - start) * progress)

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0, min(1, value))
