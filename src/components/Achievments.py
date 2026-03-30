import flet as ft

class AchievementCard(ft.Container):
    def __init__(self, item: dict):
        super().__init__()
        
        # Extract data from the item dictionary
        title = item.get("title", "Unknown Achievement")
        description = item.get("description", "")
        progress = item.get("progress", 0)
        target = item.get("target", 1)
        icon_name = item.get("icon", ft.Icons.EMOJI_EVENTS)
        base_color = item.get("color", ft.Colors.BLUE)
        
        # Calculate completion
        is_completed = progress >= target
        progress_ratio = min(progress / target, 1.0)
        
        # UI Styling logic based on completion
        # Palette colors use ft.Colors Enum, Theme colors use string tokens
        card_border_color = ft.Colors.AMBER_400 if is_completed else "outlineVariant"
        icon_bg_color = ft.Colors.AMBER_100 if is_completed else "surfaceVariant"
        icon_color = ft.Colors.AMBER_600 if is_completed else base_color
        
        # Left side: Icon inside a rounded circular container
        icon_element = ft.Container(
            content=ft.Icon(icon_name, color=icon_color, size=32),
            bgcolor=icon_bg_color,
            width=64,
            height=64,
            border_radius=32,
            alignment=ft.Alignment.CENTER,
        )
        
        # Middle: Text and Progress Bar
        text_and_progress = ft.Column(
            controls=[
                ft.Text(title, size=18, weight=ft.FontWeight.W_800, color="onSurface"),
                ft.Text(description, size=14, color="onSurfaceVariant"),
                ft.Container(height=5), # Spacer
                ft.ProgressBar(
                    value=progress_ratio,
                    color=ft.Colors.AMBER if is_completed else base_color,
                    bgcolor="surfaceVariant",
                    height=12,
                    border_radius=6,
                )
            ],
            expand=True, # Takes up remaining middle space
            spacing=2,
        )
        
        # Right side: Status or Reward
        if is_completed:
            status_element = ft.Container(
                content=ft.Text("CLAIM", weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.AMBER,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                border_radius=12,
            )
        else:
            status_element = ft.Container(
                content=ft.Text(
                    f"{progress}/{target}", 
                    size=16, 
                    weight=ft.FontWeight.W_700, 
                    color="onSurfaceVariant"
                ),
                padding=ft.Padding.only(left=10, right=5),
            )
        
        # Assemble the Card Container
        self.content = ft.Row(
            controls=[icon_element, text_and_progress, status_element],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = "surface"
        # Duolingo style chunky border
        self.border = ft.Border.all(2, card_border_color)

class AchievementList(ft.Column):
    """
    Dynamically renders a list of AchievementCards based on a parameter list.
    """
    def __init__(self, items: list):
        super().__init__()
        self.spacing = 15
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        
        for item in items:
            self.controls.append(AchievementCard(item))