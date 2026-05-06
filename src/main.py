import flet as ft

from backends import MockCandidatesBackend
from models import CandidatesBackend
from pages import CompetitionApp


def main(page: ft.Page, backend: CandidatesBackend | None = None) -> None:
    app = CompetitionApp(backend=backend or MockCandidatesBackend())
    app.build(page)


if __name__ == "__main__":
    ft.run(main, target=main)
