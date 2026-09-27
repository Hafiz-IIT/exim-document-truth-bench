# EXIM Document Truth Bench

> **Correct extraction is not the same thing as correct evidence.**

Trade-document automation can perfectly extract multiple documents while the documents themselves disagree, omit required evidence, rely on stale authorization, or originate from correlated sources. This benchmark isolates that reliability problem before any downstream customs or logistics action.

## Implemented

- synthetic invoice/packing-list/declaration records
- required-document detection
- cross-document shipment/consignee/weight consistency checks
- stale-authorization detection
- correlated-source-group warning
- ACT / VERIFY / ESCALATE outcome
- deterministic tests

## Repository map

| Path | Purpose |
|---|---|
| `exim_document_truth_bench.py` | Core implementation |
| `tests/` | Deterministic tests |
| `examples/` | Reproducible synthetic/example case |
| `docs/architecture.md` | Architecture |
| `docs/research-agenda.md` | Experiments and research lineage |
| `STATUS.md` | Claims boundary and maturity |
| `CITATION.cff` | Citation metadata |

## Quick start

```bash
python -m unittest discover -s tests -v
python exim_document_truth_bench.py
```

## Architecture

**trade documents → field extraction representation → required-document check → cross-document consistency → freshness + source checks → ACT / VERIFY / ESCALATE**

## Research lineage

This repository is a direct descendant of the multi-year EXIM AI work: document ingestion, extraction, discrepancy handling, correction/revalidation, evidence verification, and escalation. It is intentionally narrower than the full product vision.

The historical titles named in this repository are research directions, not claims that those manuscripts have already been published.

## Evaluation direction

Create controlled synthetic corruption regimes and compare naive 'all fields parsed' automation with explicit truth/consistency gating. Later add de-identified or public-domain trade-document datasets if legally and ethically usable.

## Status

**Reproducible research prototype.** No real customs records, production OCR, ICEGATE/DGFT integration, legal compliance certification, or operational clearance decision is represented.
