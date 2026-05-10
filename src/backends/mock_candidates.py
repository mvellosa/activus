from __future__ import annotations

import random
from datetime import date, timedelta

from models import MetricHistoryEntry, MetricName, UserDetails


def _score_from_metrics(metrics: dict[MetricName, float]) -> float:
    if not metrics:
        return 0

    return sum(metrics.values()) / len(metrics)


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    def __init__(self) -> None:
        self._users = [self.create_candidate(i) for i in range(10)]
        self._history = {
            user.user_id: self._build_history(user.metrics)
            for user in self._users
        }

    @staticmethod
    def create_candidate(i: int) -> UserDetails:
        user_letter = chr(ord("A") + i)
        metrics = {
            MetricName.M1: random.random(),
            MetricName.M2: random.random(),
            MetricName.M3: random.random(),
            MetricName.M4: random.random(),
        }
        score = _score_from_metrics(metrics)

        return UserDetails(
            user_id=f"id_{i}",
            name=f"{user_letter}Usuario{i}",
            subtitle="infos adicionais",
            image_url=f"https://picsum.photos/200?random={i}",
            main_metric=score,
            metrics=metrics,
            final_score=score,
        )

    @staticmethod
    def _build_history(metrics: dict[MetricName, float]) -> list[MetricHistoryEntry]:
        today = date.today()
        entries: list[MetricHistoryEntry] = []

        for days_ago in range(1, 5):
            metric_snapshot = {
                metric_name: max(0, min(1, value + random.uniform(-0.18, 0.18)))
                for metric_name, value in metrics.items()
            }
            entries.append(
                MetricHistoryEntry(
                    date=(today - timedelta(days=days_ago * 7)).isoformat(),
                    metrics=metric_snapshot,
                )
            )

        return entries

    def _upsert_history_entry(
        self,
        user_id: str,
        metrics: dict[MetricName, float],
    ) -> None:
        today = date.today().isoformat()
        history = self._history.setdefault(user_id, [])
        entry = MetricHistoryEntry(date=today, metrics=metrics)

        for index, history_entry in enumerate(history):
            if history_entry.date == today:
                history[index] = entry
                return

        history.insert(0, entry)

    def get_candidates(self) -> list[UserDetails]:
        print("MockCandidatesBackend.get_candidates called")
        return self._users.copy()

    def update_user_info(
        self,
        user_id: str,
        metrics: dict[MetricName, float],
    ) -> UserDetails:
        score = _score_from_metrics(metrics)

        for index, user in enumerate(self._users):
            if user.user_id != user_id:
                continue

            updated_user = UserDetails(
                user_id=user.user_id,
                name=user.name,
                subtitle=user.subtitle,
                image_url=user.image_url,
                main_metric=score,
                metrics=metrics,
                final_score=score,
            )
            self._users[index] = updated_user
            self._upsert_history_entry(user_id, metrics)
            return updated_user

        raise ValueError(f"User with id {user_id} was not found.")

    def get_history(self, user_id: str) -> list[MetricHistoryEntry]:
        return self._history.get(user_id, []).copy()
