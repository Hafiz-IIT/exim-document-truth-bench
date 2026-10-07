# EXIM Document Truth Bench

<p align="center">
  <strong>From Document Extraction to Document Truth</strong><br/>
  <sub>Synthetic benchmark for conflicts, missing evidence, stale authorization and correlated verification.</sub>
</p>

<p align="center">
  <a href="https://github.com/Hafiz-IIT/exim-document-truth-bench/actions"><img src="https://img.shields.io/github/actions/workflow/status/Hafiz-IIT/exim-document-truth-bench/ci.yml?label=CI" alt="CI"/></a>
  <img src="https://img.shields.io/badge/status-reproducible%20prototype-blue" alt="Prototype"/>
  <img src="https://img.shields.io/badge/domain-EXIM%20%2B%20AI-orange" alt="EXIM"/>
</p>

## Research question

**Can an AI system distinguish “the document was extracted correctly” from “the evidence supports the decision”?**

That distinction is central to high-stakes document automation.

## Benchmark pipeline

```
Invoice / Packing List / Declaration
              ↓
       Normalized fields
              ↓
  ┌───────────┼────────────┐
  mismatch   missing   stale/correlated
              ↓
       evidence analysis
              ↓
       ACT / VERIFY / ESCALATE
```

## Try it

```bash
python exim_document_truth_bench.py
python scenario_generator.py
python -m unittest discover -s tests -v
```

The reproducible scenario suite includes:

| Scenario | Expected behavior |
|---|---|
| consistent evidence | ACT |
| missing document | VERIFY |
| conflicting declaration | ESCALATE |
| correlated source pipeline | VERIFY |
| stale authorization | ESCALATE |

## Implemented

- synthetic trade-document records
- cross-document field consistency
- required-document checks
- stale authorization detection
- correlated-source analysis
- action validation
- deterministic benchmark scenarios
- CI

## Why EXIM?

The project comes from sustained exposure to export-import documentation and logistics workflows. The engineering contribution here is not a claim to automate customs law; it is a testable framework for **evidence quality before operational action**.

## Research boundary

Synthetic data only. No claim of customs/regulatory approval, production deployment or real scanner integration.

Related work: [EXIM Copilot Core](https://github.com/Hafiz-IIT/exim-copilot-core) · [Secure Document RAG Agent](https://github.com/Hafiz-IIT/secure-doc-rag-agent) · [Cargo Scan Consistency Lab](https://github.com/Hafiz-IIT/cargo-scan-consistency-lab)
