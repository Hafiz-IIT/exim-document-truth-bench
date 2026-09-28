# Evaluation Protocol

## Question
How often can apparently correct document extraction still lead to unsafe downstream action because the evidence set is inconsistent or weak?

## Metrics
- Mismatch recall
- Unsafe ACT rate
- Missing-document handling
- Correlated-evidence warnings
- Stale-authorization detection

## Falsification
- Known conflicts pass as ACT.
- Missing required documents are ignored.
- Stale authorization evidence is treated as current.

Run:
```bash
python -m unittest discover -s tests -v
```
