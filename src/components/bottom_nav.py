import flet as ft
from typing import Callable

from app_state import AppTab
from theme import PRIMARY_COLOR, SURFACE_COLOR, TEXT_PRIMARY_COLOR


class BottomNav(ft.Container):
    """Bottom navigation shared between app sections."""

    def __init__(self, selected_tab: AppTab, on_change: Callable[[AppTab], None]) -> None:
        super().__init__()
        self._selected_tab = selected_tab
        self._on_change = on_change

        self.height = 78
        self.bgcolor = SURFACE_COLOR
        self.border_radius = ft.BorderRadius.only(top_left=26, top_right=26)
        self.padding = ft.Padding(left=18, top=10, right=18, bottom=14)
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self._build_icon_button(ft.Icons.HOME_OUTLINED, selected=False),
                self._build_icon_button(
                    ft.Icons.PERSON_OUTLINE,
                    selected=self._selected_tab == AppTab.PROFILE,
                    on_click=lambda _: self._on_change(AppTab.PROFILE),
                ),
                self._build_icon_button(
                    ft.Icons.EMOJI_EVENTS_OUTLINED,
                    selected=self._selected_tab == AppTab.COMPETITION,
                    on_click=lambda _: self._on_change(AppTab.COMPETITION),
                    emphasized=True,
                ),
                self._build_icon_button(ft.Icons.SETTINGS_OUTLINED, selected=False),
            ],
        )

    def _build_icon_button(
        self,
        icon: ft.IconData,
        selected: bool,
        on_click: Callable | None = None,
        emphasized: bool = False,
    ) -> ft.Control:
        return ft.Container(
            width=48,
            height=48,
            border_radius=24,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=PRIMARY_COLOR if selected else None,
            alignment=ft.Alignment(0, 0),
            ink=on_click is not None,
            on_click=on_click,
            content=ft.Icon(
                icon,
                size=26 if emphasized and selected else 24,
                color="#FFFFFF" if selected else TEXT_PRIMARY_COLOR,
            ),
        )
