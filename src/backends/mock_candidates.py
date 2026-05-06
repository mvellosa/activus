from models import MetricName, UserDetails


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    def get_candidates(self) -> list[UserDetails]:
        return [
            UserDetails(
                user_id="a1",
                name="AUsuario1",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.72,
                metrics={
                    MetricName.M1: 0.64,
                    MetricName.M2: 0.81,
                    MetricName.M3: 0.48,
                },
                final_score=0.76,
            ),
            UserDetails(
                user_id="b2",
                name="BUsuario2",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.58,
                metrics={
                    MetricName.M1: 0.51,
                    MetricName.M2: 0.62,
                    MetricName.M3: 0.74,
                },
                final_score=0.68,
            ),
            UserDetails(
                user_id="c3",
                name="CUsuario3",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.84,
                metrics={
                    MetricName.M1: 0.78,
                    MetricName.M2: 0.92,
                    MetricName.M3: 0.66,
                },
                final_score=0.88,
            ),
            UserDetails(
                user_id="d4",
                name="DUsuario4",
                subtitle="infos adicionais",
                image_url=None,
                main_metric=0.43,
                metrics={
                    MetricName.M1: 0.35,
                    MetricName.M2: 0.46,
                    MetricName.M3: 0.57,
                },
                final_score=0.52,
            ),
        ]
