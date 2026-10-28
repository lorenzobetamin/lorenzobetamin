#!/usr/bin/env python3
"""Atualiza o semestre acadêmico exibido no README do perfil."""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


BASE_YEAR = 2026
BASE_PERIOD = 2
BASE_SEMESTER = 5
MAX_SEMESTER = 10
TIMEZONE = ZoneInfo("America/Fortaleza")

README_PATH = Path(__file__).resolve().parents[2] / "README.md"
START_MARKER = "<!-- SEMESTER:START -->"
END_MARKER = "<!-- SEMESTER:END -->"


def academic_period(current_date: date) -> tuple[int, int]:
    """Retorna o ano e o período acadêmico correspondentes à data informada."""
    if current_date.month == 1:
        return current_date.year - 1, 2
    if current_date.month <= 7:
        return current_date.year, 1
    return current_date.year, 2


def calculate_semester(current_date: date) -> int:
    """Calcula o semestre a partir do período-base, limitado ao máximo do curso."""
    year, period = academic_period(current_date)
    elapsed_periods = (year - BASE_YEAR) * 2 + (period - BASE_PERIOD)
    return min(BASE_SEMESTER + elapsed_periods, MAX_SEMESTER)


def update_readme(semester: int) -> bool:
    """Atualiza somente o conteúdo entre os marcadores e informa se houve mudança."""
    content = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"({re.escape(START_MARKER)}\n).*?(\n{re.escape(END_MARKER)})",
        re.DOTALL,
    )

    matches = pattern.findall(content)
    if len(matches) != 1:
        raise RuntimeError(
            "O README deve conter exatamente um par de marcadores de semestre."
        )

    semester_text = (
        f"🎓 Atualmente no **{semester}º semestre** de Engenharia da Computação "
        "na **Universidade de Fortaleza (UNIFOR)**."
    )
    updated_content = pattern.sub(
        lambda match: f"{match.group(1)}{semester_text}{match.group(2)}",
        content,
        count=1,
    )

    if updated_content == content:
        return False

    README_PATH.write_text(updated_content, encoding="utf-8")
    return True


def main() -> None:
    today = datetime.now(TIMEZONE).date()
    semester = calculate_semester(today)
    changed = update_readme(semester)

    print(f"Semestre atual: {semester}º")
    print("README atualizado." if changed else "README já está atualizado.")


if __name__ == "__main__":
    main()
