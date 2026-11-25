import re

KNOWLEDGE_BASE = {
    "DOC-REFUND": "Customers may return unused items within 30 days of delivery for a full refund.",
    "DOC-SHIPPING": "Standard shipping takes 3 to 5 business days. Express shipping takes 1 business day.",
    "DOC-PASSWORD": "To reset your password, click Forgot Password on the login page and verify via email.",
}

STOP_WORDS = {"a", "an", "the", "do", "you", "is", "to", "for", "of", "on", "and", "in", "i", "my", "how", "what"}

def retrieve(query: str, top_k: int = 1) -> list[str]:
    query_words = set(re.findall(r"\w+", query.lower())) - STOP_WORDS
    scored = []
    for doc_id, text in KNOWLEDGE_BASE.items():
        doc_words = set(re.findall(r"\w+", text.lower())) - STOP_WORDS
        overlap = len(query_words & doc_words)
        if overlap > 0:
            scored.append((overlap, doc_id))
    scored.sort(reverse=True)
    return [doc_id for _, doc_id in scored[:top_k]]


def answer_question(query: str, mode: str = "normal") -> dict:
    doc_ids = retrieve(query)

    if mode == "hallucinate":
        return {
            "retrieved_doc_ids": doc_ids,
            "answer": "You have 90 days to return items and we include free gift wrap.",
            "abstained": False,
        }

    if not doc_ids:
        return {
            "retrieved_doc_ids": [],
            "answer": "I don't have information about that in our policies.",
            "abstained": True,
        }

    top_doc = doc_ids[0]
    return {
        "retrieved_doc_ids": doc_ids,
        "answer": f"According to {top_doc}: {KNOWLEDGE_BASE[top_doc]}",
        "abstained": False,
    }