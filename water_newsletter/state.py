from __future__ import annotations

import json
from pathlib import Path


def load_state(path: Path, *, default_issue_number: int = 0) -> dict:
    if not path.exists():
        return {"last_issue_number": default_issue_number}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
