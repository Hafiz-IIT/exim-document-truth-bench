# EXIM Document Truth Bench

> Synthetic EXIM benchmark for separating extraction accuracy from cross-document truth consistency and evidence quality.

## Status
**Reproducible prototype** with executable Python, deterministic tests, and CI. It does not claim production deployment, regulatory approval, or real-world validation.

## Problem
An OCR/extraction system can be locally correct while the documents themselves conflict, are incomplete, stale, or share a common failure source.

## Architecture
Trade documents → normalized fields → cross-document consistency checks → missing/stale/correlated evidence analysis → ACT / VERIFY / ESCALATE.

## Quick start
```bash
python -m unittest discover -s tests -v
python exim_document_truth_bench.py
```

## Implemented
- Synthetic trade-document records
- Cross-field mismatch detection
- Required-document checks
- Stale authorization detection
- Correlated-source warning
- ACT / VERIFY / ESCALATE report
- Tests and CI

## Evaluation
The benchmark focuses on downstream truth consistency rather than merely field-extraction correctness.

## Research lineage
- *The Future of Digital Trust: Secure Data Interactions in User-Centric Platforms*
- *Framework for Ethical AI Deployment in Consumer-Oriented Systems*
- *Scalable Architectures for Distributed Intelligent Agents*

## Limitations
- Synthetic records only
- No real customs data
- No OCR model bundled
- No ICEGATE/DGFT integration

## Structure
`exim_document_truth_bench.py` · `tests/` · `docs/` · `ROADMAP.md` · `CITATION.cff` · CI

## License
MIT.
