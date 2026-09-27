# Architecture

```mermaid
flowchart LR
    N0[trade documents] --> N1
    N1[field extraction representation] --> N2
    N2[required-document check] --> N3
    N3[cross-document consistency] --> N4
    N4[freshness + source checks] --> N5
    N5[ACT / VERIFY / ESCALATE]
```

## Document objects
Represent document kind, normalized fields, source group, issue date, and authorization expiry.

## Consistency layer
Checks shared shipment identifiers, consignee identity, and gross-weight agreement.

## Evidence completeness
Verifies required document kinds are present.

## Decision gate
Escalates conflicts/staleness, verifies incomplete/correlated evidence, and acts only on clean synthetic cases.

## Design principle

Never let extraction success silently substitute for evidence consistency.
