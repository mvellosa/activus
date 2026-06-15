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

_MOCK_CANDIDATE_COUNT = 20
_MOCK_HISTORY_DAYS = 90
_MOCK_HISTORY_DAILY_DELTA = 0.055
_MOCK_HISTORY_NOISE_DELTA = 0.025
_MOCK_HISTORY_TREND_DELTA = 0.012
_MOCK_HISTORY_MAX_TREND = 0.03

_MOCK_USERS: tuple[tuple[str, str, int], ...] = (
    ("Matheus Oliveira", "Equipe comercial", 12),
    ("Renata Martins", "Time de produto", 47),
    ("Pedro Henrique", "Operações", 33),
    ("Juliana Costa", "Marketing", 48),
    ("Lucas Almeida", "Engenharia", 14),
    ("Camila Rocha", "Financeiro", 49),
    ("Bruno Ferreira", "Suporte ao cliente", 15),
    ("Fernanda Lima", "Recursos humanos", 50),
    ("Rafael Santos", "Vendas internas", 16),
    ("Mariana Azevedo", "Experiência do cliente", 51),
    ("Gustavo Pereira", "Logística", 17),
    ("Aline Carvalho", "Jurídico", 52),
    ("Felipe Souza", "Dados e BI", 18),
    ("Bianca Ribeiro", "Comunicação", 53),
    ("Thiago Moreira", "Planejamento", 19),
    ("Patrícia Gomes", "Administrativo", 54),
    ("André Nascimento", "Infraestrutura", 20),
    ("Letícia Barbosa", "Treinamento", 55),
    ("Diego Castro", "Projetos", 21),
    ("Larissa Mendes", "Qualidade", 56),
    ("Vinícius Araújo", "Parcerias", 22),
    ("Isabela Teixeira", "Design", 57),
    ("Caio Fernandes", "Atendimento", 23),
    ("Tatiane Correia", "Compras", 58),
    ("João Victor", "Gestão de contas", 24),
    ("Gabriela Cardoso", "Operações de campo", 59),
)


def _clamp_score(score: float) -> float:
    return max(0, min(100, score))


def _clamp_unit(value: float) -> float:
    return max(0, min(1, value))


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


def _next_history_value(value: float, trend: float) -> tuple[float, float]:
    next_trend = max(
        -_MOCK_HISTORY_MAX_TREND,
        min(
            _MOCK_HISTORY_MAX_TREND,
            trend + random.uniform(-_MOCK_HISTORY_TREND_DELTA, _MOCK_HISTORY_TREND_DELTA),
        ),
    )
    noise = random.uniform(-_MOCK_HISTORY_NOISE_DELTA, _MOCK_HISTORY_NOISE_DELTA)
    daily_delta = max(
        -_MOCK_HISTORY_DAILY_DELTA,
        min(_MOCK_HISTORY_DAILY_DELTA, next_trend + noise),
    )
    next_value = _clamp_unit(value + daily_delta)
    return next_value, next_trend


def _build_metric_history_snapshots(
    metrics: dict[MetricName, float],
) -> list[dict[MetricName, float]]:
    current_metrics = metrics.copy()
    trends = {
        metric_name: random.uniform(-_MOCK_HISTORY_MAX_TREND, _MOCK_HISTORY_MAX_TREND)
        for metric_name in MetricName
    }
    snapshots: list[dict[MetricName, float]] = []

    for _ in range(1, _MOCK_HISTORY_DAYS):
        next_metrics: dict[MetricName, float] = {}
        for metric_name in MetricName:
            next_value, trends[metric_name] = _next_history_value(
                current_metrics.get(metric_name, 0),
                trends[metric_name],
            )
            next_metrics[metric_name] = next_value

        snapshots.append(next_metrics)
        current_metrics = next_metrics

    return snapshots


def _history_score_from_metrics(metrics: dict[MetricName, float]) -> float:
    return _clamp_unit(
        (metrics.get(MetricName.VITALIDADE, 0) * 0.35)
        + (metrics.get(MetricName.CARGA, 0) * 0.30)
        + (metrics.get(MetricName.REPOUSO, 0) * 0.20)
        + (metrics.get(MetricName.ANIMO, 0) * 0.15)
    )


class MockCandidatesBackend:
    """Mocked backend for local development and tests."""

    def __init__(self) -> None:
        self._users = [self.create_candidate(i) for i in range(_MOCK_CANDIDATE_COUNT)]
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
                    condition="1º lugar",
                ),
                Reward(
                    title="Kit Fitness",
                    type="completion",
                    picture_url="https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&w=320&q=80",
                    condition="Completar a competição",
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
                    condition="Maior sequência de atividade",
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
                    condition="Manter frequência acima de 80%",
                ),
                Reward(
                    title="Troféu da equipe",
                    type="podium",
                    picture_url="https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?auto=format&fit=crop&w=320&q=80",
                    condition="Equipe com maior pontuação",
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
        name, subtitle, avatar_id = _MOCK_USERS[i % len(_MOCK_USERS)]
        metric_inputs = _random_metric_inputs()
        metrics, score = _readiness_inputs_to_scores(metric_inputs)

        return UserDetails(
            user_id=f"id_{i}",
            name=name,
            subtitle=subtitle,
            image_url=f"https://api.dicebear.com/9.x/lorelei/png?seed=activus-{avatar_id}&size=200",
            metric_inputs=metric_inputs,
            main_metric=score,
            metrics=metrics,
            final_score=score,
        )

    @staticmethod
    def _build_history(metric_inputs: DailyMetricInputs) -> list[MetricHistoryEntry]:
        today = date.today()
        entries: list[MetricHistoryEntry] = []
        current_metrics, _ = _readiness_inputs_to_scores(metric_inputs)
        metric_snapshots = _build_metric_history_snapshots(current_metrics)

        for days_ago, metric_snapshot in enumerate(metric_snapshots, start=1):
            entries.append(
                MetricHistoryEntry(
                    date=(today - timedelta(days=days_ago)).isoformat(),
                    metrics=metric_snapshot,
                    final_score=_history_score_from_metrics(metric_snapshot),
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
