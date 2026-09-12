# Security-AI Reports & Evaluation Audits

This directory contains technical reports, incident analyses, benchmark results, and Architecture Decision Records (ADRs) for the Security-AI platform.

---

## Available Reports

| Report ID | Date | Subject | Status | Document |
| :--- | :--- | :--- | :--- | :--- |
| **ADR-001** | 2026-09-12 | Evaluation of `llama3.2:1b` failure (hallucination & tool calling collapse) and architectural migration to `Qwen3.5-4B`. | **Approved** | [`adr_001_llm_hallucination_and_migration.md`](./adr_001_llm_hallucination_and_migration.md) |

---

## Report Structure Guidelines
All future evaluation reports added to this directory should document:
1. **Timestamp & Test Environment** (Model version, runtime, temperature).
2. **Exact Prompts & System Traces**.
3. **Observed vs Expected Ground Truth**.
4. **Root Cause Analysis** (Context drift, token degeneration, tool parsing failures).
5. **Mitigation & Architectural Decisions**.
