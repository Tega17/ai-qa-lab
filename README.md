# AI QA Lab (`ai-qa-lab`)

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

# AI QA Lab (`ai-qa-lab`)

[![AI QA CI Gate](https://github.com/Tega17/ai-qa-lab/actions/workflows/ai-qa-ci.yml/badge.svg)](https://github.com/Tega17/ai-qa-lab/actions/workflows/ai-qa-ci.yml)
