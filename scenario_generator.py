from __future__ import annotations

from dataclasses import dataclass

from exim_document_truth_bench import Action, TradeDocument, validate


@dataclass(frozen=True)
class Scenario:
    name: str
    documents: tuple[TradeDocument, ...]
    today_day: int
    expected: Action


def scenarios() -> tuple[Scenario, ...]:
    base = {"shipment_id": "S-1", "consignee": "ACME", "gross_weight_kg": "1000"}

    consistent = (
        TradeDocument("invoice", base, "commercial", 10),
        TradeDocument("packing_list", base, "warehouse", 10),
        TradeDocument("declaration", base, "broker", 11),
    )

    mismatch = (
        consistent[0],
        consistent[1],
        TradeDocument(
            "declaration",
            {**base, "gross_weight_kg": "1300"},
            "broker",
            11,
        ),
    )

    correlated = (
        TradeDocument("invoice", base, "same-pipeline", 10),
        TradeDocument("packing_list", base, "same-pipeline", 10),
        TradeDocument("declaration", base, "broker", 11),
    )

    stale = (
        consistent[0],
        consistent[1],
        TradeDocument("declaration", base, "broker", 11, authorization_expires_day=11),
    )

    return (
        Scenario("consistent", consistent, 11, Action.ACT),
        Scenario("missing", consistent[:2], 11, Action.VERIFY),
        Scenario("mismatch", mismatch, 11, Action.ESCALATE),
        Scenario("correlated", correlated, 11, Action.VERIFY),
        Scenario("stale", stale, 12, Action.ESCALATE),
    )


def run_benchmark(items: tuple[Scenario, ...] | None = None) -> dict:
    items = scenarios() if items is None else items
    rows = []
    correct = 0
    for item in items:
        report = validate(list(item.documents), today_day=item.today_day)
        ok = report.action == item.expected
        correct += int(ok)
        rows.append({
            "name": item.name,
            "expected": item.expected.value,
            "actual": report.action.value,
            "mismatches": report.mismatches,
            "missing": report.missing_kinds,
            "stale": report.stale_authorizations,
            "correlated": report.correlated_source_groups,
            "correct": ok,
        })
    return {
        "total": len(rows),
        "correct": correct,
        "accuracy": correct / len(rows) if rows else 0.0,
        "rows": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
