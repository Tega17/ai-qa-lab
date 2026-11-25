from rag_pipeline import KNOWLEDGE_BASE, answer_question, retrieve


def grade_rag_response(result: dict, expected_doc: str | None, required_fact: str | None) -> tuple[bool, str]:
    """Simple deterministic rubric scorer returning (passed, reason)."""
    # Unanswerable case: model must abstain and not invent facts
    if expected_doc is None:
        if not result["abstained"]:
            return False, "FAIL_ABSTENTION: Answered when no policy existed"
        return True, "PASS"

    # Answerable case: isolate retrieval vs. generation failure
    if expected_doc not in result["retrieved_doc_ids"]:
        return False, f"FAIL_RETRIEVAL: Expected {expected_doc}, got {result['retrieved_doc_ids']}"

    if result["abstained"]:
        return False, "FAIL_GENERATION: Abstained despite retrieving valid doc"

    if required_fact and required_fact.lower() not in result["answer"].lower():
        return False, f"FAIL_GROUNDEDNESS: Missing fact '{required_fact}' from {expected_doc}"

    return True, "PASS"


def test_retrieval_precision():
    assert retrieve("How many days do I have for a refund?") == ["DOC-REFUND"]
    assert retrieve("How fast is express shipping?") == ["DOC-SHIPPING"]


def test_grounded_answers():
    res = answer_question("What is the refund window?", mode="normal")
    passed, reason = grade_rag_response(res, expected_doc="DOC-REFUND", required_fact="30 days")
    assert passed, reason


def test_unanswerable_question_abstains():
    res = answer_question("Do you offer a student discount?", mode="normal")
    passed, reason = grade_rag_response(res, expected_doc=None, required_fact=None)
    assert passed, reason


def test_detects_hallucination():
    res = answer_question("What is the refund window?", mode="hallucinate")
    passed, reason = grade_rag_response(res, expected_doc="DOC-REFUND", required_fact="30 days")
    assert not passed
    assert "FAIL_GROUNDEDNESS" in reason