# EXIM Document Truth Bench

A synthetic benchmark for studying an important failure mode in document automation: **the documents may be extracted correctly while the underlying evidence is inconsistent, stale, incomplete, or jointly wrong.**

## Implemented
- synthetic invoice / packing-list / declaration records
- field-level extraction comparisons
- cross-document mismatch checks
- missing-document detection
- stale-authorization flags
- correlated-evidence warning
- action validator returning ACT / VERIFY / ESCALATE

## Run
```bash
python -m unittest discover -s tests -v
python exim_document_truth_bench.py
```

## What this does not claim
No real customs records, ICEGATE integration, production OCR system, or scanner hardware is represented here. The benchmark is synthetic by design so reliability logic can be tested without exposing business or personal documents.
