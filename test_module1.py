import json
from pathlib import Path
import pytest
from mock_llm import mock_llm

GOLDEN_PATH = Path(__file__).parent / "golden_set.jsonl"


def load_golden_cases():
    cases = []
    for line in GOLDEN_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(json.loads(line))
    return cases


@pytest.mark.parametrize("case", load_golden_cases(), ids=lambda c: c["id"])
def test_golden_output_rules(case):
    raw = mock_llm(case["prompt"], mode="normal")

    # 1. Schema / JSON check
    data = json.loads(raw)
    assert isinstance(data, dict)

    text = json.dumps(data).lower()

    # 2. Required and forbidden terms
    for term in case["required_terms"]:
        assert term.lower() in text, f"Missing required term: {term}"

    for term in case["forbidden_terms"]:
        assert term.lower() not in text, f"Found forbidden term: {term}"

    # 3. Length / word-budget check
    word_count = len(text.split())
    assert word_count <= case["max_words"], f"Too wordy: {word_count} > {case['max_words']}"


def test_metamorphic_rephrase_consistency():
    prompt_a = "Summarize order #1042 status as shipped"
    prompt_b = "Give me a quick summary: order #1042 is shipped"

    data_a = json.loads(mock_llm(prompt_a, mode="normal"))
    data_b = json.loads(mock_llm(prompt_b, mode="normal"))

    assert data_a.get("order_id") == data_b.get("order_id")
    assert data_a.get("status") == data_b.get("status")