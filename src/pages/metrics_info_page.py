from __future__ import annotations

from typing import Callable

import flet as ft

from components import CircularMetric
from components.metric_definitions import METRIC_DEFINITIONS
from models import Metric, MetricName
from theme import APP_BG_COLOR, CARD_SHADOW, TEXT_MUTED_COLOR, TEXT_PRIMARY_COLOR


METRIC_DESCRIPTIONS: dict[MetricName, str] = {
    MetricName.VITALIDADE: (
        "Mostra como o corpo esta respondendo ao estresse e a recuperacao. "
        "Ela usa a variacao da frequencia cardiaca para indicar sua prontidao."
    ),
    MetricName.CARGA: (
        "Compara o esforco recente com sua carga habitual. Ajuda a entender "
        "se o treino esta equilibrado, leve demais ou exigente demais."
    ),
    MetricName.REPOUSO: (
        "Resume a qualidade do sono, incluindo duracao, eficiencia e sono "
        "profundo. Quanto melhor o descanso, maior a pontuacao."
    ),
    MetricName.ANIMO: (
        "Representa sua percepcao subjetiva do dia. Esse sinal ajuda a ajustar "
        "a leitura fisica com como voce realmente esta se sentindo."
    ),
}


class MetricsInfoPage(ft.Container):
    def __init__(self, on_back: Callable[[], None]) -> None:
        super().__init__()
        self.expand = True
        self.bgcolor = APP_BG_COLOR
        self.padding = ft.Padding(left=14, top=16, right=20, bottom=0)
        self.content = ft.Column(
            spacing=28,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._build_header(on_back),
                ft.Column(
                    spacing=28,
                    controls=[
                        self._build_metric_info(metric_name, icon, color)
                        for metric_name, icon, color in METRIC_DEFINITIONS
                    ],
                ),
            ],
        )

    def _build_header(self, on_back: Callable[[], None]) -> ft.Row:
        return ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor="#FFFFFF",
                    shadow=CARD_SHADOW,
                    alignment=ft.Alignment(0, 0),
                    content=ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color="#5B15CE",
                        icon_size=28,
                        on_click=lambda _: on_back(),
                    ),
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "Metricas",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.Container(width=38, height=38),
            ],
        )

    def _build_metric_info(
        self,
        metric_name: MetricName,
        icon: ft.IconData,
        color: str,
    ) -> ft.Row:
        return ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=52,
                    alignment=ft.Alignment(0, 0),
                    content=CircularMetric(
                        metric=Metric(
                            label=metric_name.value,
                            value=1,
                            icon=icon,
                            color=color,
                        ),
                        size=50,
                        stroke_width=4,
                        interactive=False,
                        gradient_colors=(color, color),
                    ),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                metric_name.value,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=color,
                            ),
                            ft.Text(
                                METRIC_DESCRIPTIONS[metric_name],
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=TEXT_MUTED_COLOR,
                            ),
                        ],
                    ),
                ),
            ],
        )
