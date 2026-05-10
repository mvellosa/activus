import flet as ft

from models import UserDetails
from theme import AVATAR_PLACEHOLDER_COLOR


class UserAvatar(ft.Container):
    """Reusable circular avatar with optional image fallback."""

    def __init__(self, user: UserDetails, size: int = 58) -> None:
        super().__init__()
        self.width = size
        self.height = size
        self.border_radius = size // 2
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        self.bgcolor = AVATAR_PLACEHOLDER_COLOR
        self.alignment = ft.Alignment(0, 0)
        self.content = self._build_content(user=user, size=size)

    def _build_content(self, user: UserDetails, size: int) -> ft.Control:
        if user.image_url:
            return ft.Image(
                src=user.image_url,
                width=size,
                height=size,
                fit=ft.BoxFit.COVER,
            )

        initials = "".join(part[:1] for part in user.name.split()).upper()[:2]
        return ft.Text(
            initials or "?",
            size=max(12, size // 4),
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
        )
