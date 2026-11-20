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


@dataclass(frozen=True)
class TruthReport:
    action: Action
    mismatches: tuple[str, ...]
    missing_kinds: tuple[str, ...]
    stale_authorizations: tuple[str, ...]
    correlated_source_groups: tuple[str, ...]
    duplicate_document_kinds: tuple[str, ...] = ()
    future_documents: tuple[str, ...] = ()


REQUIRED = ("invoice", "packing_list", "declaration")
CROSS_FIELDS = ("shipment_id", "consignee", "gross_weight_kg")


def _duplicates(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    dup: set[str] = set()
    for value in values:
        if value in seen:
            dup.add(value)
        seen.add(value)
    return tuple(sorted(dup))


def validate(documents: list[TradeDocument], *, today_day: int) -> TruthReport:
    if isinstance(today_day, bool) or not isinstance(today_day, int):
        raise ValueError("today_day must be an integer day index")
    kinds = [doc.kind for doc in documents]
    duplicate_kinds = _duplicates(kinds)
    by_kind = {doc.kind: doc for doc in documents}
    missing = tuple(kind for kind in REQUIRED if kind not in by_kind)

    mismatches: list[str] = []
    for field in CROSS_FIELDS:
        values = {
            doc.fields.get(field)
            for doc in documents
            if doc.fields.get(field) is not None
        }
        if len(values) > 1:
            mismatches.append(field)

    stale = tuple(
        doc.kind
        for doc in documents
        if doc.authorization_expires_day is not None
        and today_day > doc.authorization_expires_day
    )

    groups = [doc.source_group for doc in documents]
    correlated = _duplicates(groups)
    future = tuple(sorted(doc.kind for doc in documents if doc.issued_day > today_day))

    # Duplicate primary document kinds and future-dated records are ambiguous
    # evidence states, not safe last-write-wins updates.
    if mismatches or stale or duplicate_kinds or future:
        action = Action.ESCALATE
    elif missing or correlated:
        action = Action.VERIFY
    else:
        action = Action.ACT

    return TruthReport(
        action=action,
        mismatches=tuple(sorted(mismatches)),
        missing_kinds=missing,
        stale_authorizations=tuple(sorted(stale)),
        correlated_source_groups=correlated,
        duplicate_document_kinds=duplicate_kinds,
        future_documents=future,
    )


def synthetic_consistent_case() -> list[TradeDocument]:
    shared = {"shipment_id": "S-100", "consignee": "ACME", "gross_weight_kg": "1200"}
    return [
        TradeDocument("invoice", shared, "commercial", 100),
        TradeDocument("packing_list", shared, "warehouse", 100),
        TradeDocument("declaration", shared, "broker", 101),
    ]


if __name__ == "__main__":
    print(validate(synthetic_consistent_case(), today_day=102))
