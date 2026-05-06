import flet as ft

from models import Metric, UserDetails


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    def get_candidates(self) -> list[UserDetails]:
        return [
            UserDetails(
                user_id="u1",
                name="Usuario1",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.72,
                metrics=[
                    Metric(label="M1", value=0.64, icon=ft.Icons.TIMER_OUTLINED),
                    Metric(label="M2", value=0.81, icon=ft.Icons.SPEED_OUTLINED),
                    Metric(label="M3", value=0.48, icon=ft.Icons.STAR_BORDER_OUTLINED),
                ],
                final_score=0.76,
            ),
            UserDetails(
                user_id="u2",
                name="Usuario2",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.58,
                metrics=[
                    Metric(label="M1", value=0.51, icon=ft.Icons.TIMER_OUTLINED),
                    Metric(label="M2", value=0.62, icon=ft.Icons.SPEED_OUTLINED),
                    Metric(label="M3", value=0.74, icon=ft.Icons.STAR_BORDER_OUTLINED),
                ],
                final_score=0.68,
            ),
            UserDetails(
                user_id="u3",
                name="Usuario3",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.84,
                metrics=[
                    Metric(label="M1", value=0.78, icon=ft.Icons.TIMER_OUTLINED),
                    Metric(label="M2", value=0.92, icon=ft.Icons.SPEED_OUTLINED),
                    Metric(label="M3", value=0.66, icon=ft.Icons.STAR_BORDER_OUTLINED),
                ],
                final_score=0.88,
            ),
            UserDetails(
                user_id="u4",
                name="Usuario4",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.43,
                metrics=[
                    Metric(label="M1", value=0.35, icon=ft.Icons.TIMER_OUTLINED),
                    Metric(label="M2", value=0.46, icon=ft.Icons.SPEED_OUTLINED),
                    Metric(label="M3", value=0.57, icon=ft.Icons.STAR_BORDER_OUTLINED),
                ],
                final_score=0.52,
            ),
        ]
