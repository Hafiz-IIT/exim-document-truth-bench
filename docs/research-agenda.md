# Research agenda

## Central question
**How often would an automated EXIM workflow act incorrectly if it checked extraction completeness but not cross-document truth and provenance?**

## Hypotheses
### H1
Cross-document consistency checks reduce incorrect downstream actions under synthetic mismatch regimes.

### H2
Correlated documents should not be treated as independent corroboration.

### H3
Stale authorization is a distinct failure mode from extraction error and should trigger escalation.

## Proposed experiments
1. Generate mismatch rates across weight, consignee, and shipment ID; compare naive vs gated action policies.
2. Vary missing-document probability and measure verification burden against unsafe-action reduction.
3. Simulate correlated source groups and test whether naive document-count rules overestimate support.

## Metrics
- incorrect ACT rate
- escalation rate
- verification rate
- mismatch-detection recall
- false escalation rate

## Historical paper lineage
- **EXIM AI Co-Pilot: A Multimodal Cargo Scanning & Customs Automation Framework (Concept & Prototype)**
- **AI in Customs & Logistics: State of the Art**

These are preserved from earlier research planning and are not publication claims.

## Preprint gate
Do not label a direction as a paper result until the protocol is frozen, baselines are reproduced, results include uncertainty/error analysis, negative cases are documented, and limitations are explicit.
