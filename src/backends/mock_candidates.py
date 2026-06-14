from __future__ import annotations

import random
from datetime import date, timedelta
from math import exp

from models import DailyMetricInputs, MetricHistoryEntry, MetricName, MoodLevel, Reward, UserDetails


_MOOD_BONUS = {
    MoodLevel.OTIMO: 25,
    MoodLevel.BEM: 18.75,
    MoodLevel.NEUTRO: 12.5,
    MoodLevel.MAL: 6.25,
    MoodLevel.PESSIMO: 0,
}


def _clamp_score(score: float) -> float:
    return max(0, min(100, score))


def _readiness_inputs_to_scores(
    metric_inputs: DailyMetricInputs,
) -> tuple[dict[MetricName, float], float]:
    vitality_score = _score_vitality(metric_inputs)
    load_score = _score_load(metric_inputs)
    rest_score = _score_rest(metric_inputs)
    mood_bonus = _MOOD_BONUS[metric_inputs.mood]

    base_score = (vitality_score * 0.35) + (load_score * 0.30) + (rest_score * 0.20)
    raw_score = base_score + mood_bonus
    daily_score = round((raw_score / 125) * 100, 1)

    metrics = {
        MetricName.VITALIDADE: vitality_score / 100,
        MetricName.CARGA: load_score / 100,
        MetricName.REPOUSO: rest_score / 100,
        MetricName.ANIMO: mood_bonus / 25,
    }
    return metrics, _clamp_score(daily_score) / 100


def _score_vitality(metric_inputs: DailyMetricInputs) -> float:
    if metric_inputs.rmssd_baseline <= 0:
        return 0

    delta_hrv = ((metric_inputs.rmssd_day - metric_inputs.rmssd_baseline) / metric_inputs.rmssd_baseline) * 100
    sigma = 13 if delta_hrv <= 7 else 20
    score = 100 * exp(-0.5 * ((delta_hrv - 7) / sigma) ** 2)

    if delta_hrv > 50:
        score = min(score, 40)

    return _clamp_score(score)


def _score_load(metric_inputs: DailyMetricInputs) -> float:
    if metric_inputs.chronic_load <= 0:
        return 0

    acwr = metric_inputs.acute_load / metric_inputs.chronic_load
    sigma = 0.22 if acwr <= 1.05 else 0.18
    score = 100 * exp(-0.5 * ((acwr - 1.05) / sigma) ** 2)

    if acwr >= 1.50:
        score = 0
    elif acwr < 0.60:
        score = min(score, 30)

    return _clamp_score(score)


def _score_rest(metric_inputs: DailyMetricInputs) -> float:
    tst = metric_inputs.total_sleep_hours
    score_tst = 100 * exp(-0.5 * ((tst - 8.0) / 1.0) ** 2)
    if tst < 6:
        score_tst = 0

    score_se = min(100, (metric_inputs.sleep_efficiency / 85) * 100)
    score_n3 = 100 * exp(-0.5 * ((metric_inputs.deep_sleep_percent - 20) / 6) ** 2)
    score = (score_tst * 0.50) + (score_se * 0.30) + (score_n3 * 0.20)

    if tst < 6:
        score = min(score, 50)

    return _clamp_score(score)


def _random_metric_inputs() -> DailyMetricInputs:
    rmssd_baseline = random.uniform(35, 70)
    return DailyMetricInputs(
        rmssd_day=rmssd_baseline * random.uniform(0.82, 1.28),
        rmssd_baseline=rmssd_baseline,
        acute_load=random.uniform(250, 650),
        chronic_load=random.uniform(280, 620),
        total_sleep_hours=random.uniform(5.4, 9.0),
        sleep_efficiency=random.uniform(72, 96),
        deep_sleep_percent=random.uniform(12, 28),
        mood=random.choice(list(MoodLevel)),
    )


def _jitter_metric_inputs(metric_inputs: DailyMetricInputs) -> DailyMetricInputs:
    return DailyMetricInputs(
        rmssd_day=max(1, metric_inputs.rmssd_day + random.uniform(-8, 8)),
        rmssd_baseline=max(1, metric_inputs.rmssd_baseline + random.uniform(-5, 5)),
        acute_load=max(0, metric_inputs.acute_load + random.uniform(-90, 90)),
        chronic_load=max(1, metric_inputs.chronic_load + random.uniform(-70, 70)),
        total_sleep_hours=max(0, metric_inputs.total_sleep_hours + random.uniform(-0.8, 0.8)),
        sleep_efficiency=max(0, min(100, metric_inputs.sleep_efficiency + random.uniform(-8, 8))),
        deep_sleep_percent=max(0, min(100, metric_inputs.deep_sleep_percent + random.uniform(-5, 5))),
        mood=random.choice(list(MoodLevel)),
    )


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    def __init__(self) -> None:
        self._users = [self.create_candidate(i) for i in range(26)]
        self._history = {
            user.user_id: self._build_history(user.metric_inputs)
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
        metric_inputs = _random_metric_inputs()
        metrics, score = _readiness_inputs_to_scores(metric_inputs)

        return UserDetails(
            user_id=f"id_{i}",
            name=f"{user_letter}Usuario{i}",
            subtitle="infos adicionais",
            image_url=f"https://picsum.photos/200?random={i}",
            metric_inputs=metric_inputs,
            main_metric=score,
            metrics=metrics,
            final_score=score,
        )

    @staticmethod
    def _build_history(metric_inputs: DailyMetricInputs) -> list[MetricHistoryEntry]:
        today = date.today()
        entries: list[MetricHistoryEntry] = []

        for days_ago in range(1, 7):
            metric_snapshot, final_score = _readiness_inputs_to_scores(
                _jitter_metric_inputs(metric_inputs)
            )
            entries.append(
                MetricHistoryEntry(
                    date=(today - timedelta(days=days_ago * 7)).isoformat(),
                    metrics=metric_snapshot,
                    final_score=final_score,
                )
            )

        return entries

    def _upsert_history_entry(
        self,
        user_id: str,
        metrics: dict[MetricName, float],
        final_score: float,
    ) -> None:
        today = date.today().isoformat()
        history = self._history.setdefault(user_id, [])
        entry = MetricHistoryEntry(date=today, metrics=metrics, final_score=final_score)

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
        metric_inputs: DailyMetricInputs,
    ) -> UserDetails:
        metrics, score = _readiness_inputs_to_scores(metric_inputs)

        for index, user in enumerate(self._users):
            if user.user_id != user_id:
                continue

            updated_user = UserDetails(
                user_id=user.user_id,
                name=user.name,
                subtitle=user.subtitle,
                image_url=user.image_url,
                metric_inputs=metric_inputs,
                main_metric=score,
                metrics=metrics,
                final_score=score,
            )
            self._users[index] = updated_user
            self._upsert_history_entry(user_id, metrics, score)
            return updated_user

        raise ValueError(f"User with id {user_id} was not found.")

    def get_history(self, user_id: str) -> list[MetricHistoryEntry]:
        return self._history.get(user_id, []).copy()

    def get_rewards(self, competition_id: str) -> list[Reward]:
        return self._rewards_by_competition.get(competition_id, []).copy()
