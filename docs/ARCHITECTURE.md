# Architecture

## Flow
Trade documents → normalized fields → cross-document consistency checks → missing/stale/correlated evidence analysis → ACT / VERIFY / ESCALATE.

## Invariants
1. Cross-document conflicts must be surfaced.
2. Missing required evidence cannot be treated as complete.
3. Shared-source correlation must reduce confidence in apparent agreement.

## Boundary
Adapters for OCR, government systems, sensors, databases or LLMs must preserve provenance and explicit failure states.
