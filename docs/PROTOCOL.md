# Protocol and limitations

This repository is a deterministic synthetic benchmark for cross-document consistency checks. It compares a small fixed set of shipment fields across invoice, packing-list and declaration records and checks authorization expiry and coarse source-group reuse.

## Interpretation

- ACT means the configured toy checks passed; it is not customs clearance or a legal compliance determination.
- VERIFY means required documents are missing or the supplied source groups are correlated.
- ESCALATE means a cross-document mismatch, expired authorization, or future-dated document was found.
- issued_day and today_day are integer fixture-day counters, not wall-clock timestamps.
- Source-group equality is a simple correlation proxy, not cryptographic provenance verification.

## Limitations

The benchmark does not parse PDFs, verify signatures, query official customs or sanctions systems, interpret HS codes, establish document authenticity, model jurisdiction-specific law, or validate the truth of a field that appears consistently across all documents. A compromised common source can make mutually consistent documents wrong. Results from these fixtures are not real shipment outcomes.
