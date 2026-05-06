from __future__ import annotations

from typing import Callable

import flet as ft

from models import UserDetails

from .user_list_item import UserListItem


class UsersList(ft.Column):
    """Reusable users list component."""

    def __init__(
        self,
        users: list[UserDetails],
        selected_user_id: str,
        on_select: Callable[[UserDetails], None],
    ) -> None:
        super().__init__()
        self.users = users
        self.selected_user_id = selected_user_id
        self._on_select = on_select
        self.spacing = 10
        self.controls = self._build_items()

    def _build_items(self) -> list[ft.Control]:
        return [
            UserListItem(
                user=user,
                selected=user.user_id == self.selected_user_id,
                on_select=self._on_select,
            )
            for user in self.users
        ]

    def update_selection(self, selected_user_id: str) -> None:
        self.selected_user_id = selected_user_id
        self.controls = self._build_items()
        self.update()
