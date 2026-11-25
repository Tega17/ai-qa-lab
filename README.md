# AI QA Lab (`ai-qa-lab`)

[![AI QA CI Gate](https://github.com/Tega17/ai-qa-lab/actions/workflows/ai-qa-ci.yml/badge.svg)](https://github.com/Tega17/ai-qa-lab/actions/workflows/ai-qa-ci.yml)

A fast, zero-API-key test harness demonstrating practical Quality Assurance patterns for LLM, RAG (Retrieval-Augmented Generation), and tool-calling agent systems using Python and `pytest`.

## Overview

Traditional software tests rely on exact string matching (`assert actual == expected`), which fails on non-deterministic AI outputs. This repository implements a three-layer AI testing strategy:

1. **Deterministic & Metamorphic Assertions** — Structural JSON validation, required/forbidden term rules, length budgets, and rephrase consistency checks.
2. **RAG Failure Isolation & Rubric Grading** — Separating retrieval misses from generation hallucinations and verifying proper abstention on unanswerable queries.
3. **Agent Tool Validation, Red Teaming & CI Release Gates** — Verifying tool selection, step limits, direct/indirect prompt injection defenses, and automated deployment gating.

## Project Structure

```text
ai-qa-lab/
├── golden_set.jsonl      # Golden dataset of test prompts and output constraints
├── mock_llm.py           # Simulated LLM supporting normal and fault-injection modes
├── test_module1.py       # Module 1: Schema, rule, budget, and metamorphic tests
├── rag_pipeline.py       # Local knowledge base, stop-word retriever, and RAG responder
├── test_module2.py       # Module 2: Retrieval precision, groundedness, and abstention tests
├── mock_agent.py         # Simulated tool-calling agent with order/ticket tools and guardrails
├── test_module3.py       # Module 3: Tool-call, loop-cap, and red-team security tests
├── gate.py               # CI release gate enforcing pass rate, security, and latency thresholds
└── eval_report.json      # Generated evaluation metrics consumed by gate.py
ß
```

Quickstart

1. Create a Virtual Environment & Install pytest
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install pytest

2. Run the Full Test Suite & CI Release Gate
   pytest -v && python gate.py

Expected output:
14 passed in 0.07s
Release Gate Report: {"total": 4, "passed": 4, "pass_rate": 1.0, "security_failures": 0, "avg_latency_ms": 112.5}
GATE PASSED: Ready for deployment.

**Module Breakdown**

**Module 1: Deterministic Checks & Golden Datasets (test_module1.py)**
JSON & Schema Checks: Catches malformed JSON before downstream parsing fails (mode="broken_json").

Content & Budget Rules: Enforces required_terms, forbidden_terms, and max_words bounds (mode="missing_field", mode="too_wordy").

Metamorphic Testing: Verifies that rephrased prompts asking the same question produce identical structured fields.

**Module 2: RAG Failure Isolation & Rubrics (test_module2.py)**
Retrieval Precision: Filters stop words to prevent false-positive document matches on out-of-scope queries.

Groundedness & Hallucination Detection: Flags fabricated claims that contradict retrieved source documents (mode="hallucinate").

Abstention Verification: Ensures the system explicitly abstains when no matching policy exists in the knowledge base.

**Module 3: Agent Guardrails, Red Teaming & CI Gate (test_module3.py, gate.py)**
Execution Trace Assertions: Validates exact tool names, arguments, and max_steps loop caps (mode="infinite_loop").

Security & Red Teaming: Tests defenses against direct prompt injection and indirect injection embedded inside tool data (mode="leak_secret").

Release Gate (gate.py): Blocks deployment (exit code 1) if security_failures > 0, pass_rate < 0.85, or avg_latency_ms > 300.
