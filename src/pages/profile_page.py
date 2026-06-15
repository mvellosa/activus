from __future__ import annotations

from typing import Callable

import flet as ft

from app_state import AppState
from components import (
    CircularMetric,
    MetricSelector,
    MetricsGrid,
    ProfileHeader,
    SectionTitle,
    WeeklyPerformanceChart,
)
from components.metric_definitions import build_metrics
from models import Metric, MetricName, UserDetails
from theme import (
    BORDER_COLOR,
    CARD_SHADOW,
    PRIMARY_COLOR,
    RING_GRADIENT,
    SURFACE_COLOR,
    TEXT_MUTED_COLOR,
    TEXT_PRIMARY_COLOR,
)


CHART_PERIOD_OPTIONS: tuple[tuple[int, str], ...] = (
    (7, "7 dias"),
    (14, "14 dias"),
    (30, "1 mês"),
    (90, "3 meses"),
)


class ProfilePage(ft.Container):
    def __init__(
        self,
        state: AppState,
        on_edit_metrics: Callable[[], None],
        on_open_metrics_info: Callable[[], None],
    ) -> None:
        super().__init__()
        self._state = state
        self._on_edit_metrics = on_edit_metrics
        self._on_open_metrics_info = on_open_metrics_info
        self._selected_metric = self._default_metric(state)
        self._chart_period_days = CHART_PERIOD_OPTIONS[0][0]
        self._chart_toolbar_holder: ft.Container | None = None
        self._chart_holder: ft.Container | None = None
        self.expand = True
        self.padding = ft.Padding(left=8, top=0, right=8, bottom=0)
        self.content = self._build_page()

    def _build_page(self) -> ft.Stack:
        return ft.Stack(
            expand=True,
            controls=[
                self._build_content(self._state),
                self._build_edit_button(self._on_edit_metrics),
            ],
        )

    def _build_content(self, state: AppState) -> ft.Column:
        user = state.logged_user
        metrics = self._build_named_metrics(state)
        selected_metric = self._selected_metric_model(metrics)

        return ft.Column(
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ProfileHeader(user),
                self._build_metrics_header(self._on_open_metrics_info),
                MetricsGrid([metric for _, metric in metrics]),
                ft.Container(
                    padding=ft.Padding(left=18, top=8, right=18, bottom=16),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            SectionTitle("Desempenho"),
                            self._build_chart_toolbar_holder(metrics),
                            self._build_chart_holder(user, state, selected_metric),
                        ],
                    ),
                ),
                SectionTitle("Geral"),
                self._build_general_card(user),
            ],
        )

    def _build_metrics_header(self, on_open_metrics_info: Callable[[], None]) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                SectionTitle("Métricas"),
                ft.Container(
                    width=24,
                    height=24,
                    border_radius=12,
                    border=ft.Border.all(2, "#CFC9D9"),
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=lambda _: on_open_metrics_info(),
                    content=ft.Icon(
                        ft.Icons.QUESTION_MARK,
                        color="#B5AFBF",
                        size=14,
                    ),
                ),
            ],
        )

    def _build_chart_toolbar_holder(
        self,
        metrics: list[tuple[MetricName, Metric]],
    ) -> ft.Container:
        self._chart_toolbar_holder = ft.Container(
            content=self._build_chart_toolbar(metrics),
        )
        return self._chart_toolbar_holder

    def _build_chart_holder(
        self,
        user: UserDetails,
        state: AppState,
        selected_metric: Metric,
    ) -> ft.Container:
        self._chart_holder = ft.Container(
            content=WeeklyPerformanceChart(
                user=user,
                history=state.logged_user_history,
                selected_metric=self._selected_metric,
                metric=selected_metric,
                period_days=self._chart_period_days,
            ),
        )
        return self._chart_holder

    def _build_named_metrics(self, state: AppState) -> list[tuple[MetricName, Metric]]:
        metrics = build_metrics(state.logged_user.metrics)
        return [
            (metric_name, metric)
            for metric_name in MetricName
            for metric in metrics
            if metric.label == metric_name.value
        ]

    def _build_general_card(self, user: UserDetails) -> ft.Container:
        return ft.Container(
            bgcolor=SURFACE_COLOR,
            border_radius=16,
            shadow=CARD_SHADOW,
            padding=24,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    CircularMetric(
                        metric=Metric(
                            label="Geral",
                            value=user.main_metric,
                            icon=ft.Icons.EMOJI_EVENTS_OUTLINED,
                            color="#FF8A00",
                        ),
                        size=104,
                        stroke_width=8,
                        show_number=True,
                        interactive=False,
                        gradient_colors=RING_GRADIENT,
                    ),
                    ft.Text(
                        "readiness",
                        size=11,
                        weight=ft.FontWeight.W_500,
                        color="#FF8A00",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def _build_chart_toolbar(
        self,
        metrics: list[tuple[MetricName, Metric]],
    ) -> ft.Row:
        return ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self._build_period_menu(),
                ft.Container(
                    expand=True,
                    content=MetricSelector(
                        metrics=metrics,
                        selected_metric=self._selected_metric,
                        on_select=self._select_metric,
                        compact=True,
                    ),
                ),
            ],
        )

    def _build_period_menu(self) -> ft.PopupMenuButton:
        selected_label = self._period_label(self._chart_period_days)
        return ft.PopupMenuButton(
            padding=0,
            menu_padding=4,
            tooltip="Selecionar período",
            content=ft.Container(
                height=28,
                padding=ft.Padding(left=10, top=0, right=10, bottom=0),
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=14,
                alignment=ft.Alignment(0, 0),
                content=ft.Row(
                    spacing=4,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.ARROW_DROP_DOWN,
                            size=18,
                            color=TEXT_MUTED_COLOR,
                        ),
                        ft.Text(
                            selected_label,
                            size=11,
                            weight=ft.FontWeight.W_600,
                            color=TEXT_MUTED_COLOR,
                        ),
                    ],
                ),
            ),
            items=[
                ft.PopupMenuItem(
                    content=label,
                    checked=days == self._chart_period_days,
                    label_text_style=ft.TextStyle(
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=(
                            PRIMARY_COLOR
                            if days == self._chart_period_days
                            else TEXT_PRIMARY_COLOR
                        ),
                    ),
                    on_click=lambda _, selected_days=days: self._select_chart_period(
                        selected_days
                    ),
                )
                for days, label in CHART_PERIOD_OPTIONS
            ],
        )

    def _period_label(self, period_days: int) -> str:
        for days, label in CHART_PERIOD_OPTIONS:
            if days == period_days:
                return label

        return CHART_PERIOD_OPTIONS[0][1]

    def _default_metric(self, state: AppState) -> MetricName:
        return next(iter(state.logged_user.metrics), MetricName.VITALIDADE)

    def _selected_metric_model(self, metrics: list[tuple[MetricName, Metric]]) -> Metric:
        for metric_name, metric in metrics:
            if metric_name == self._selected_metric:
                return metric

        return Metric(
            label="Geral",
            value=self._state.logged_user.main_metric,
            icon=ft.Icons.EMOJI_EVENTS,
            color=TEXT_PRIMARY_COLOR,
        )

    def _select_metric(self, metric_name: MetricName) -> None:
        if self._selected_metric == metric_name:
            return

        self._selected_metric = metric_name
        self._refresh_chart()

    def _select_chart_period(self, period_days: int) -> None:
        if self._chart_period_days == period_days:
            return

        self._chart_period_days = period_days
        self._refresh_chart()

    def _refresh_chart(self) -> None:
        metrics = self._build_named_metrics(self._state)
        selected_metric = self._selected_metric_model(metrics)

        if self._chart_toolbar_holder is not None:
            self._chart_toolbar_holder.content = self._build_chart_toolbar(metrics)
            self._chart_toolbar_holder.update()

        if self._chart_holder is not None:
            self._chart_holder.content = WeeklyPerformanceChart(
                user=self._state.logged_user,
                history=self._state.logged_user_history,
                selected_metric=self._selected_metric,
                metric=selected_metric,
                period_days=self._chart_period_days,
            )
            self._chart_holder.update()

    def _build_edit_button(self, on_edit_metrics: Callable[[], None]) -> ft.Container:
        return ft.Container(
            right=10,
            bottom=16,
            width=58,
            height=58,
            border_radius=29,
            shadow=CARD_SHADOW,
            content=ft.FloatingActionButton(
                icon=ft.Icons.EDIT_NOTE,
                bgcolor="#FF8A00",
                foreground_color="#FFFFFF",
                on_click=lambda _: on_edit_metrics(),
            ),
        )
