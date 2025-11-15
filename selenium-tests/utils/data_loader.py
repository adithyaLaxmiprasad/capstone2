# utils/data_loader.py
import csv
from pathlib import Path
from typing import List, Dict

def load_csv_as_dicts(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]
