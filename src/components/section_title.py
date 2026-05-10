import flet as ft

from theme import TEXT_PRIMARY_COLOR


class SectionTitle(ft.Container):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.padding = ft.Padding(left=8, top=0, right=8, bottom=0)
        self.content = ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=TEXT_PRIMARY_COLOR,
        )
