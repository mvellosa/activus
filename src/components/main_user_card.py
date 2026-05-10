import flet as ft

from models import Metric, UserDetails
from theme import SURFACE_COLOR

from .circular_metric import CircularMetric
from .metric_definitions import build_metrics
from .user_avatar import UserAvatar


class MainUserCard(ft.Card):
    """Main card showing the selected user and primary metrics."""

    def __init__(self, user: UserDetails) -> None:
        super().__init__()
        self.user = user
        self.elevation = 4
        self.color = SURFACE_COLOR
        self.surface_tint_color = SURFACE_COLOR
        self.shape = ft.RoundedRectangleBorder(radius=24)
        self.content = self._build_content()

    def _build_content(self) -> ft.Container:
        return ft.Container(
            padding=ft.Padding(left=18, top=18, right=18, bottom=18),
            width=340,
            content=ft.Column(
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.__big_user_metric(),
                    self.__small_user_metrics(),
                ],
            ),
        )

    def __big_user_metric(self) -> ft.Row:
        _size = 138
        _stroke_width = int(_size * 0.07)
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                CircularMetric(
                    metric=Metric(
                        label="Main",
                        value=self.user.main_metric,
                        icon=ft.Icons.PERSON,
                    ),
                    size=_size,
                    stroke_width=(_stroke_width),
                    center_content=UserAvatar(self.user, size=92),
                    toggle_center_content=True,
                    gradient_colors=("#6322C6", "#07484D"),
                    interactive=True,
                )
            ],
        )

    def __small_user_metrics(self) -> ft.Row:
        metrics = build_metrics(self.user.metrics)
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                CircularMetric(metric=metric, size=58, stroke_width=5)
                for metric in metrics
            ],
        )

    def update_user(self, user: UserDetails) -> None:
        self.user = user
        self.content = self._build_content()
        self.update()
