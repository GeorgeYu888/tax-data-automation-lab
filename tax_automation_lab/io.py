from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def read_csv(path: Path | str) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)


def read_yaml(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Rules config not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Rules config must be a mapping: {path}")
    return data


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
