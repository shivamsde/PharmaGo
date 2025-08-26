import os

# WhatsApp / Meta
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

# Intent labels supported in the bot
INTENT_LABELS = [
    "greeting",
    "check_inventory",
    "check_price",
    "place_order",
    "fallback",
]

# HuggingFace zero-shot model (small & free)
INTENT_MODEL = os.environ.get(
    "INTENT_MODEL",
    "typeform/distilbert-base-uncased-mnli",  # light alternative to bart-large-mnli
)