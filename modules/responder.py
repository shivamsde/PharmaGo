from modules.inventory import best_match_med

GREETING = (
    "👋 Hello! Welcome to PharmaBot.\n"
    "Ask me about availability, price, or to place an order.\n"
    "e.g., 'Do you have Paracetamol 500mg?' or 'Price of Vitamin C?'."
)


def build_response(intent: str, user_text: str) -> str:
    intent = (intent or "").lower().strip()

    if intent == "greeting":
        return GREETING

    if intent in {"check_inventory", "check_price"}:
        med, score = best_match_med(user_text)
        if not med:
            return (
                "❌ I couldn't find that medicine in our inventory.\n"
                "Please send the exact name (e.g., 'Paracetamol 500mg')."
            )
        if intent == "check_inventory":
            return (
                f"✅ {med['name']} is available.\n"
                f"Stock: {med['stock']} units.\n"
                f"💡 You can ask: 'price of {med['name']}' or 'order {med['name']} x2'"
            )
        else:
            return (
                f"💰 Price of {med['name']}: ₹{med['price']}.\n"
                f"Stock available: {med['stock']} units."
            )

    if intent == "place_order":
        med, score = best_match_med(user_text)
        if not med:
            return (
                "🛒 To place an order, please include the medicine name and quantity.\n"
                "Example: 'Order Paracetamol 500mg x 2'"
            )
        # Minimal order capture (demo). In production, persist to DB and collect details.
        return (
            f"🧾 Draft order created for {med['name']}.\n"
            "Please share quantity, delivery address, and preferred payment method."
        )

    # Fallback
    return (
        "🤔 I didn't quite get that.\n"
        "You can say: 'hi', 'do you have <medicine>', 'price of <medicine>', or 'order <medicine>'."
    )