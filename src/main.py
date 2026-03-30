import flet as ft

from components.Achievments import AchievementList

# -------------------------------------------------------------------
# 1. Custom Component: Achievement Card
# ------------------------------------------------------------------



# -------------------------------------------------------------------
# 3. App Entry Point
# -------------------------------------------------------------------
def main(page: ft.Page):
    # Setup page properties (Modern App feel)
    page.title = "Achievements"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 25
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Using dynamic string token instead of missing Enum value
    page.bgcolor = "background" 
    
    # Custom fonts can be added here, but Flet's default works well for the bold weight setup
    
    # ---------------------------------------------------------------
    # The Parameterized List of Items
    # ---------------------------------------------------------------
    my_achievements = [
        {
            "title": "Sharpshooter", 
            "description": "Complete 10 flawless lessons in a row without any mistakes.", 
            "progress": 10, 
            "target": 10, 
            "icon": ft.Icons.STAR_ROUNDED, 
            "color": ft.Colors.RED
        },
        {
            "title": "Early Bird", 
            "description": "Practice before 8 AM for 5 days.", 
            "progress": 3, 
            "target": 5, 
            "icon": ft.Icons.WB_SUNNY_ROUNDED, 
            "color": ft.Colors.ORANGE
        },
        {
            "title": "Night Owl", 
            "description": "Complete a session after 10 PM.", 
            "progress": 1, 
            "target": 1, 
            "icon": ft.Icons.NIGHTLIGHT_ROUND, 
            "color": ft.Colors.DEEP_PURPLE
        },
        {
            "title": "Weekend Warrior", 
            "description": "Study on both Saturday and Sunday.", 
            "progress": 1, 
            "target": 2, 
            "icon": ft.Icons.FITNESS_CENTER_ROUNDED, 
            "color": ft.Colors.BLUE
        },
        {
            "title": "Social Butterfly", 
            "description": "Follow 3 friends.", 
            "progress": 0, 
            "target": 3, 
            "icon": ft.Icons.PEOPLE_ALT_ROUNDED, 
            "color": ft.Colors.GREEN
        },
        {
            "title": "Legendary", 
            "description": "Finish first in the Diamond League.", 
            "progress": 25, 
            "target": 100, 
            "icon": ft.Icons.DIAMOND_ROUNDED, 
            "color": ft.Colors.CYAN
        }
    ]

    # Header UI
    header = ft.Row(
        controls=[
            ft.Text("Achievements", size=28, weight=ft.FontWeight.W_900),
            ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color=ft.Colors.AMBER, size=32)
        ],
        alignment=ft.MainAxisAlignment.START,
    )
    
    # Subtitle
    subtitle = ft.Text(
        "Complete tasks to earn rewards and badges!",
        size=16,
        color="onSurfaceVariant",
        weight=ft.FontWeight.W_500
    )

    # Render the dynamic list
    achievements_view = AchievementList(items=my_achievements)
    
    # Add everything to a constrained central column (looks great on desktop/web too)
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                header,
                subtitle,
                ft.Container(height=10), # Spacer
                achievements_view
            ],
            expand=True
        ),
        width=600, # Max width for desktop viewing to simulate mobile/tablet app look
        expand=True
    )

    page.add(main_container)

if __name__ == "__main__":
    ft.run(main)