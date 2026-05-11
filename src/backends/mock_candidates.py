from __future__ import annotations

import random
from datetime import date, timedelta

from models import MetricHistoryEntry, MetricName, Reward, UserDetails


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
        self._rewards_by_competition = {
            "competition_main": [
                Reward(
                    title="Smartwatch",
                    type="podium",
                    picture_url="https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=320&q=80",
                    condition="1o lugar",
                ),
                Reward(
                    title="Kit Fitness",
                    type="completion",
                    picture_url="https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&w=320&q=80",
                    condition="Completar a competicao",
                ),
                Reward(
                    title="Garrafa esportiva",
                    type="top_three",
                    picture_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=320&q=80",
                    condition="Top 3 colocados",
                ),
                Reward(
                    title="Vale-presente",
                    type="participation",
                    picture_url="https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?auto=format&fit=crop&w=320&q=80",
                    condition="Participar de todos os desafios",
                ),
                Reward(
                    title="Medalha especial",
                    type="streak",
                    picture_url="https://images.unsplash.com/photo-1567427018141-0584cfcbf1b8?auto=format&fit=crop&w=320&q=80",
                    condition="Maior sequencia de atividade",
                ),
                Reward(
                    title="Fone Bluetooth",
                    type="top_three",
                    picture_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=320&q=80",
                    condition="Top 5 no ranking geral",
                ),
                Reward(
                    title="Mochila esportiva",
                    type="completion",
                    picture_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=320&q=80",
                    condition="Concluir 4 semanas seguidas",
                ),
                Reward(
                    title="Camiseta premium",
                    type="participation",
                    picture_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=320&q=80",
                    condition="Registrar atividade em 10 dias",
                ),
                Reward(
                    title="Assinatura fitness",
                    type="streak",
                    picture_url="https://images.unsplash.com/photo-1571019613914-85f342c6a11e?auto=format&fit=crop&w=320&q=80",
                    condition="Manter frequencia acima de 80%",
                ),
                Reward(
                    title="Trofeu da equipe",
                    type="podium",
                    picture_url="https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?auto=format&fit=crop&w=320&q=80",
                    condition="Equipe com maior pontuacao",
                ),
                Reward(
                    title="Cupom nutricional",
                    type="participation",
                    picture_url="https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=320&q=80",
                    condition="Participar dos desafios semanais",
                ),
            ]
        }

    @staticmethod
    def create_candidate(i: int) -> UserDetails:
        user_letter = chr(ord("A") + i)
        metrics = {
            MetricName.VITALIDADE: random.random(),
            MetricName.CARGA: random.random(),
            MetricName.REPOUSO: random.random(),
            MetricName.ANIMO: random.random(),
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

    def get_rewards(self, competition_id: str) -> list[Reward]:
        return self._rewards_by_competition.get(competition_id, []).copy()
