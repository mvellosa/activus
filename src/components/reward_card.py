from __future__ import annotations

import flet as ft

from models import Reward
from theme import CARD_SHADOW, SURFACE_COLOR, TEXT_MUTED_COLOR, TEXT_PRIMARY_COLOR


REWARD_TYPE_ICONS: dict[str, ft.IconData] = {
    "podium": ft.Icons.EMOJI_EVENTS_OUTLINED,
    "completion": ft.Icons.DONE_OUTLINE,
    "top_three": ft.Icons.MILITARY_TECH_OUTLINED,
    "participation": ft.Icons.CARD_GIFTCARD,
    "streak": ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED,
}


class RewardCard(ft.Container):
    """Card displaying a single competition reward."""

    def __init__(self, reward: Reward) -> None:
        super().__init__()
        self.bgcolor = SURFACE_COLOR
        self.border_radius = 14
        self.shadow = CARD_SHADOW
        self.padding = ft.Padding(left=12, top=12, right=16, bottom=12)
        self.height = 118
        self.content = ft.Row(
            spacing=18,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self._build_picture(reward.picture_url),
                ft.Column(
                    expand=True,
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            reward.title,
                            size=19,
                            weight=ft.FontWeight.W_700,
                            color=TEXT_PRIMARY_COLOR,
                            no_wrap=True,
                        ),
                        ft.Text(
                            reward.condition,
                            size=12,
                            color=TEXT_MUTED_COLOR,
                            max_lines=2,
                        ),
                        ft.Icon(
                            REWARD_TYPE_ICONS.get(
                                reward.type,
                                ft.Icons.REDEEM_OUTLINED,
                            ),
                            size=18,
                            color="#FF8A00",
                        ),
                    ],
                ),
            ],
        )

    def _build_picture(self, picture_url: str) -> ft.Container:
        return ft.Container(
            width=104,
            height=92,
            border_radius=14,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor="#F3EEFA",
            content=ft.Image(
                src=picture_url,
                fit=ft.BoxFit.COVER,
            ),
        )
