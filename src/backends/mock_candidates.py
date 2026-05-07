import random

from models import MetricName, UserDetails


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    @staticmethod
    def createCandidate(i: int):
        userLetter = chr(ord('A') + i)
        return UserDetails(
            user_id=f"id_{i}",
            name=f"{userLetter}Usuario{i}",
            subtitle="infos adicionais",
            image_url=f"https://picsum.photos/200?random={i}",
            main_metric=random.random(),
            metrics={
                MetricName.M1: random.random(),
                MetricName.M2: random.random(),
                MetricName.M3: random.random(),
            },
            final_score=random.random(),
        )

    def get_candidates(self) -> list[UserDetails]:
        print("MockCandidatesBackend.get_candidates called")
        return [ self.createCandidate(i) for i in range(10)]
