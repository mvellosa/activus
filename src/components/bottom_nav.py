import flet as ft


class BottomNav(ft.Container):
    """Bottom navigation for the competition screen."""

    def __init__(self) -> None:
        super().__init__()
        nav_icon_size = 24
        active_color = "#6322C6"
        inactive_color = "#1F1A2E"

        self.height = 78
        self.bgcolor = "#FFFFFF"
        self.border_radius = ft.BorderRadius.only(top_left=26, top_right=26)
        self.padding = ft.Padding(left=18, top=10, right=18, bottom=14)
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.HOME_OUTLINED, size=nav_icon_size, color=inactive_color),
                ft.Icon(ft.Icons.PERSON_OUTLINE, size=nav_icon_size, color=inactive_color),
                ft.Container(
                    width=48,
                    height=48,
                    border_radius=24,
                    bgcolor=active_color,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(
                        ft.Icons.EMOJI_EVENTS_OUTLINED,
                        size=26,
                        color="#FFFFFF",
                    ),
                ),
                ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=nav_icon_size, color=inactive_color),
            ],
        )
