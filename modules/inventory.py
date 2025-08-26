import json
from pathlib import Path
from rapidfuzz import process, fuzz

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "inventory.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _INVENTORY = json.load(f)

# Build a lookup list of names for fuzzy matching
_MED_NAMES = [m["name"] for m in _INVENTORY]


def best_match_med(query: str, score_cutoff: int = 70):
    """Return (med_dict, score) fuzzy-matched by name, or (None, 0)."""
    if not query:
        return None, 0
    match = process.extractOne(
        query,
        _MED_NAMES,
        scorer=fuzz.WRatio,
        score_cutoff=score_cutoff,
    )
    if not match:
        return None, 0
    name, score, idx = match
    return _INVENTORY[idx], score


def find_by_name_exact(name: str):
    for med in _INVENTORY:
        if med["name"].lower() == name.lower():
            return med
    return None