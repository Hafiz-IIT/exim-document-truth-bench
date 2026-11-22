from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class Action(str, Enum):
    ACT = "ACT"
    VERIFY = "VERIFY"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class TradeDocument:
    kind: str
    fields: Mapping[str, str | None]
    source_group: str
    issued_day: int
    authorization_expires_day: int | None = None

    def __post_init__(self):
        for name in ("kind", "source_group"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if isinstance(self.issued_day, bool) or not isinstance(self.issued_day, int) or self.issued_day < 0:
            raise ValueError("issued_day must be a non-negative integer")
        expiry = self.authorization_expires_day
        if expiry is not None and (
            isinstance(expiry, bool) or not isinstance(expiry, int) or expiry < 0
        ):
            raise ValueError("authorization_expires_day must be a non-negative integer or None")
        if not isinstance(self.fields, Mapping):
            raise TypeError("fields must be a mapping")
        clean = {}
        for key, value in self.fields.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("field names must be non-empty strings")
            if value is not None and not isinstance(value, str):
                raise ValueError("field values must be strings or None")
            clean[key] = value
        object.__setattr__(self, "fields", MappingProxyType(clean))


@dataclass(frozen=True)
class TruthReport:
    action: Action
    mismatches: tuple[str, ...]
    missing_kinds: tuple[str, ...]
    stale_authorizations: tuple[str, ...]
    correlated_source_groups: tuple[str, ...]
    duplicate_kinds: tuple[str, ...] = ()
    unknown_kinds: tuple[str, ...] = ()
    future_documents: tuple[str, ...] = ()
    stale_documents: tuple[str, ...] = ()


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


def validate(
    documents: list[TradeDocument],
    *,
    today_day: int,
    max_document_age_days: int | None = None,
) -> TruthReport:
    if not isinstance(documents, list) or any(not isinstance(doc, TradeDocument) for doc in documents):
        raise TypeError("documents must be a list of TradeDocument instances")
    if isinstance(today_day, bool) or not isinstance(today_day, int) or today_day < 0:
        raise ValueError("today_day must be a non-negative integer")
    if max_document_age_days is not None and (
        isinstance(max_document_age_days, bool)
        or not isinstance(max_document_age_days, int)
        or max_document_age_days <= 0
    ):
        raise ValueError("max_document_age_days must be a positive integer or None")

    kinds = [doc.kind for doc in documents]
    duplicate_kinds = _duplicates(kinds)
    unknown_kinds = tuple(sorted(set(kinds) - set(REQUIRED)))
    by_kind = {}
    for doc in documents:
        by_kind.setdefault(doc.kind, doc)
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

    stale_authorizations = tuple(sorted({
        doc.kind
        for doc in documents
        if doc.authorization_expires_day is not None
        and today_day > doc.authorization_expires_day
    }))
    future_documents = tuple(sorted({
        doc.kind for doc in documents if doc.issued_day > today_day
    }))
    stale_documents = ()
    if max_document_age_days is not None:
        stale_documents = tuple(sorted({
            doc.kind
            for doc in documents
            if today_day - doc.issued_day > max_document_age_days
        }))

    correlated = _duplicates([doc.source_group for doc in documents])

    if mismatches or stale_authorizations or duplicate_kinds or future_documents:
        action = Action.ESCALATE
    elif missing or correlated or unknown_kinds or stale_documents:
        action = Action.VERIFY
    else:
        action = Action.ACT

    return TruthReport(
        action=action,
        mismatches=tuple(sorted(mismatches)),
        missing_kinds=missing,
        stale_authorizations=stale_authorizations,
        correlated_source_groups=correlated,
        duplicate_kinds=duplicate_kinds,
        unknown_kinds=unknown_kinds,
        future_documents=future_documents,
        stale_documents=stale_documents,
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
