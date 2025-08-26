from langgraph.graph import StateGraph
from transformers import pipeline
from typing import Dict, Any
from config import INTENT_MODEL, INTENT_LABELS
from modules.utils import clean_text

# Initialize zero-shot classifier once
_classifier = pipeline("zero-shot-classification", model=INTENT_MODEL)


class State(dict):
    """Simple dict-like state for LangGraph."""
    user_text: str
    intent: str


def classify_intent(state: Dict[str, Any]) -> Dict[str, Any]:
    text = clean_text(state.get("user_text", ""))
    if not text:
        state["intent"] = "fallback"
        return state

    result = _classifier(text, INTENT_LABELS)
    # labels are sorted by score desc; pick the top
    top_intent = (result.get("labels") or ["fallback"])[0]

    # Safety: if confidence too low, fallback
    scores = result.get("scores") or [0.0]
    if scores and scores[0] < 0.45:
        top_intent = "fallback"

    state["intent"] = top_intent
    return state


# Build & compile a tiny graph with one node (can be extended later)
_graph = StateGraph(State)
_graph.add_node("classify_intent", classify_intent)
_graph.set_entry_point("classify_intent")
_graph.set_finish_point("classify_intent")
_intent_graph = _graph.compile()


def get_intent(user_text: str) -> str:
    result = _intent_graph.invoke({"user_text": user_text})
    return result.get("intent", "fallback")