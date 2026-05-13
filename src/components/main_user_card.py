import flet as ft

from models import Metric, UserDetails
from theme import SURFACE_COLOR

from .circular_metric import CircularMetric
from .metric_definitions import build_metrics
from .user_avatar import UserAvatar


class MainUserCard(ft.Card):
    """Main card showing the selected user and primary metrics."""

    _COMPRESSION_STEP = 0.05
    _SMOOTHING_AMOUNT = 0.5

    def __init__(self, user: UserDetails) -> None:
        super().__init__()
        self.user = user
        self._metrics = build_metrics(user.metrics)
        self._compression = 0.0
        self.elevation = 4
        self.color = SURFACE_COLOR
        self.surface_tint_color = SURFACE_COLOR
        self.shape = ft.RoundedRectangleBorder(radius=24)
        self.content = self._build_content()

    def _build_content(self) -> ft.Container:
        compression = self._smooth(self._compression)
        padding = round(self._lerp(18, 10, compression))
        height = round(self._lerp(256, 80, compression))

        return ft.Container(
            padding=ft.Padding(left=padding, top=padding, right=padding, bottom=padding),
            width=340,
            height=height,
            content=self.__metrics_stack(340 - (padding * 2), height - (padding * 2)),
        )

    def __metrics_stack(self, width: int, height: int) -> ft.Stack:
        compression = self._smooth(self._compression)
        big_progress = self._smooth(self._progress_between(self._compression, 0.0, 0.68))
        metrics_progress = self._smooth(self._progress_between(self._compression, 0.18, 1.0))

        big_size = round(self._lerp(138, 58, big_progress))
        big_avatar_size = round(self._lerp(92, 34, big_progress))
        big_stroke_width = max(4, round(big_size * 0.07))
        big_left = self._lerp((width - big_size) / 2, 0, big_progress)
        big_top = self._lerp(0, 0, compression)

        metrics = self._metrics
        metric_size = round(self._lerp(58, 38, metrics_progress))
        metric_stroke_width = round(self._lerp(5, 4, compression))
        expanded_gap = (width - (len(metrics) * metric_size)) / max(1, len(metrics) + 1)
        compact_gap = 14
        compact_total_width = (len(metrics) * metric_size) + ((len(metrics) - 1) * compact_gap)
        compact_start = width - compact_total_width - 4
        metric_top = self._lerp(150, (height - metric_size) / 2, metrics_progress)

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
            left = self._lerp(expanded_left, compact_left, metrics_progress)

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
                ]
            )

        return ft.Stack(
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            controls=controls,
        )

    def set_compression(self, compression: float) -> None:
        normalized = self._quantize(self._clamp(compression), self._COMPRESSION_STEP)
        if normalized == self._compression:
            return

        self._compression = normalized
        self.content = self._build_content()
        self._update_if_mounted()

    def update_user(self, user: UserDetails) -> None:
        self.user = user
        self._metrics = build_metrics(user.metrics)
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

    @staticmethod
    def _quantize(value: float, step: float) -> float:
        return round(value / step) * step

    @classmethod
    def _progress_between(cls, value: float, start: float, end: float) -> float:
        if end <= start:
            return 1

        return cls._clamp((value - start) / (end - start))

    @classmethod
    def _smooth(cls, value: float) -> float:
        linear = cls._clamp(value)
        smooth = linear * linear * (3 - (2 * linear))
        amount = cls._clamp(cls._SMOOTHING_AMOUNT)
        return cls._lerp(linear, smooth, amount)
