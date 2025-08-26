import re

def clean_text(t: str) -> str:
    if not t:
        return ""
    t = t.strip()
    # collapse whitespace
    t = re.sub(r"\s+", " ", t)
    return t