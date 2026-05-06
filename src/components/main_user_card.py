import flet as ft

from models import Metric, UserDetails

from .circular_metric import CircularMetric
from .user_avatar import UserAvatar


class MainUserCard(ft.Card):
    """Main card showing the selected user and primary metrics."""

    def __init__(self, user: UserDetails) -> None:
        super().__init__()
        self.user = user
        self.elevation = 4
        self.color = "#FFFFFF"
        self.surface_tint_color = "#FFFFFF"
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
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            CircularMetric(
                                metric=Metric(
                                    label="Main",
                                    value=self.user.main_metric,
                                    icon=ft.Icons.PERSON,
                                ),
                                size=138,
                                stroke_width=15,
                                center_content=UserAvatar(self.user, size=92),
                                gradient_colors=("#6322C6", "#07484D"),
                                interactive=False,
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            CircularMetric(metric=metric, size=58, stroke_width=7)
                            for metric in self.user.metrics
                        ],
                    ),
                ],
            ),
        )

    def update_user(self, user: UserDetails) -> None:
        self.user = user
        self.content = self._build_content()
        self.update()
