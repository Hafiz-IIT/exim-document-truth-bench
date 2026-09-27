import unittest

from exim_document_truth_bench import Action, TradeDocument, synthetic_consistent_case, validate


class TruthBenchTests(unittest.TestCase):
    def test_consistent_independent_evidence_can_act(self):
        report = validate(synthetic_consistent_case(), today_day=102)
        self.assertEqual(report.action, Action.ACT)

    def test_cross_document_conflict_escalates(self):
        docs = synthetic_consistent_case()
        bad = TradeDocument(
            "declaration",
            {**docs[2].fields, "gross_weight_kg": "1500"},
            "broker",
            101,
        )
        report = validate([docs[0], docs[1], bad], today_day=102)
        self.assertEqual(report.action, Action.ESCALATE)
        self.assertIn("gross_weight_kg", report.mismatches)

    def test_missing_document_requires_verification(self):
        report = validate(synthetic_consistent_case()[:2], today_day=102)
        self.assertEqual(report.action, Action.VERIFY)
        self.assertIn("declaration", report.missing_kinds)

    def test_stale_authorization_escalates(self):
        docs = synthetic_consistent_case()
        docs[2] = TradeDocument(
            "declaration", docs[2].fields, "broker", 101, authorization_expires_day=101
        )
        self.assertEqual(validate(docs, today_day=102).action, Action.ESCALATE)


if __name__ == "__main__":
    unittest.main()
