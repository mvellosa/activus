from __future__ import annotations

import flet as ft

from components import RewardCard
from models import Reward
from theme import TEXT_MUTED_COLOR, TEXT_PRIMARY_COLOR


class RewardsPage(ft.Container):
    def __init__(self, rewards: list[Reward]) -> None:
        super().__init__()
        self.expand = True
        self.padding = ft.Padding(left=28, top=48, right=28, bottom=0)
        self.content = ft.Column(
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Text(
                            "Recompensas",
                            size=30,
                            weight=ft.FontWeight.W_700,
                            color=TEXT_PRIMARY_COLOR,
                        ),
                        ft.Text(
                            "Participe das competicoes e ganhe\npremios exclusivos!",
                            size=17,
                            color=TEXT_MUTED_COLOR,
                            height=1.35,
                        ),
                    ],
                ),
                ft.Column(
                    spacing=14,
                    controls=[RewardCard(reward) for reward in rewards],
                ),
            ],
        )
