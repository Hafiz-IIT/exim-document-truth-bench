from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Mapping

class Action(str, Enum):
    ACT = "ACT"
    VERIFY = "VERIFY"
    ESCALATE = "ESCALATE"

@dataclass(frozen=True)
class TradeDocument:
    kind: str
    fields: Mapping[str, str]
    source_group: str
    issued_day: int
    authorization_expires_day: int | None = None
    def __post_init__(self):
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("document kind must be non-empty")
        if not isinstance(self.source_group, str) or not self.source_group.strip():
            raise ValueError("source_group must be non-empty")
        if not isinstance(self.fields, Mapping) or any(
            not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip()
            for k, v in self.fields.items()
        ):
            raise ValueError("document fields must map non-empty strings to non-empty strings")
        if isinstance(self.issued_day, bool) or not isinstance(self.issued_day, int) or self.issued_day < 0:
            raise ValueError("issued_day must be a non-negative integer")
        expiry = self.authorization_expires_day
        if expiry is not None and (isinstance(expiry, bool) or not isinstance(expiry, int) or expiry < self.issued_day):
            raise ValueError("authorization expiry must be an integer on or after issue day")

@dataclass(frozen=True)
class TruthReport:
    action: Action
    mismatches: tuple[str, ...]
    missing_kinds: tuple[str, ...]
    stale_authorizations: tuple[str, ...]
    correlated_source_groups: tuple[str, ...]
    future_issued_documents: tuple[str, ...]
    missing_fields: tuple[str, ...]
    duplicate_kinds: tuple[str, ...]

REQUIRED = ("invoice", "packing_list", "declaration")
CROSS_FIELDS = ("shipment_id", "consignee", "gross_weight_kg")

def _duplicates(values: list[str]) -> tuple[str, ...]:
    seen, dup = set(), set()
    for value in values:
        if value in seen: dup.add(value)
        seen.add(value)
    return tuple(sorted(dup))

def validate(documents: list[TradeDocument], *, today_day: int) -> TruthReport:
    if not isinstance(documents, list) or any(not isinstance(doc, TradeDocument) for doc in documents):
        raise ValueError("documents must be a list of TradeDocument values")
    if isinstance(today_day, bool) or not isinstance(today_day, int) or today_day < 0:
        raise ValueError("today_day must be a non-negative integer")
    duplicate_kinds = _duplicates([doc.kind for doc in documents])
    by_kind = {doc.kind: doc for doc in documents}
    missing = tuple(kind for kind in REQUIRED if kind not in by_kind)
    mismatches = []
    missing_fields = []
    for kind in REQUIRED:
        doc = by_kind.get(kind)
        if doc is None:
            continue
        for field in CROSS_FIELDS:
            if field not in doc.fields:
                missing_fields.append(f"{kind}.{field}")
    for field in CROSS_FIELDS:
        values = {doc.fields[field] for doc in documents if field in doc.fields}
        if len(values) > 1: mismatches.append(field)
    stale = tuple(sorted(doc.kind for doc in documents
        if doc.authorization_expires_day is not None and today_day > doc.authorization_expires_day))
    future = tuple(sorted(doc.kind for doc in documents if doc.issued_day > today_day))
    correlated = _duplicates([doc.source_group for doc in documents])
    if mismatches or stale or future or duplicate_kinds: action = Action.ESCALATE
    elif missing or missing_fields or correlated: action = Action.VERIFY
    else: action = Action.ACT
    return TruthReport(action, tuple(sorted(mismatches)), missing, stale, correlated, future,
                       tuple(sorted(missing_fields)), duplicate_kinds)

def synthetic_consistent_case() -> list[TradeDocument]:
    shared = {"shipment_id": "S-100", "consignee": "ACME", "gross_weight_kg": "1200"}
    return [TradeDocument("invoice", shared, "commercial", 100),
            TradeDocument("packing_list", shared, "warehouse", 100),
            TradeDocument("declaration", shared, "broker", 101)]

if __name__ == "__main__":
    print(validate(synthetic_consistent_case(), today_day=102))
