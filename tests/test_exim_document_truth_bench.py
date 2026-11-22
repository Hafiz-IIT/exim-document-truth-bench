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

    def test_duplicate_document_kind_escalates_instead_of_overwriting(self):
        docs = synthetic_consistent_case()
        duplicate = TradeDocument("invoice", {"shipment_id": "S-999"}, "other-source", 100)
        report = validate(docs + [duplicate], today_day=102)
        self.assertEqual(report.action, Action.ESCALATE)
        self.assertEqual(report.duplicate_kinds, ("invoice",))

    def test_future_dated_document_escalates(self):
        docs = synthetic_consistent_case()
        docs[1] = TradeDocument("packing_list", docs[1].fields, "warehouse", 103)
        report = validate(docs, today_day=102)
        self.assertEqual(report.action, Action.ESCALATE)
        self.assertEqual(report.future_documents, ("packing_list",))

    def test_stale_document_requires_verification_when_age_limit_supplied(self):
        docs = [
            TradeDocument("invoice", {"shipment_id": "S-100"}, "commercial", 1),
            TradeDocument("packing_list", {"shipment_id": "S-100"}, "warehouse", 99),
            TradeDocument("declaration", {"shipment_id": "S-100"}, "broker", 100),
        ]
        report = validate(docs, today_day=102, max_document_age_days=30)
        self.assertEqual(report.action, Action.VERIFY)
        self.assertEqual(report.stale_documents, ("invoice",))

    def test_unknown_document_kind_requires_verification(self):
        docs = synthetic_consistent_case() + [
            TradeDocument("unrecognized_attachment", {"shipment_id": "S-100"}, "other", 101)
        ]
        report = validate(docs, today_day=102)
        self.assertEqual(report.action, Action.VERIFY)
        self.assertEqual(report.unknown_kinds, ("unrecognized_attachment",))

    def test_trade_document_fields_are_immutable_after_construction(self):
        fields = {"shipment_id": "S-100"}
        doc = TradeDocument("invoice", fields, "commercial", 100)
        fields["shipment_id"] = "S-999"
        self.assertEqual(doc.fields["shipment_id"], "S-100")
        with self.assertRaises(TypeError):
            doc.fields["shipment_id"] = "S-777"

    def test_invalid_day_and_field_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "today_day"):
            validate(synthetic_consistent_case(), today_day=True)
        with self.assertRaisesRegex(ValueError, "max_document_age_days"):
            validate(synthetic_consistent_case(), today_day=102, max_document_age_days=0)
        with self.assertRaisesRegex(ValueError, "field values"):
            TradeDocument("invoice", {"gross_weight_kg": 1200}, "commercial", 100)

    def test_same_source_group_requires_verification(self):
        docs = synthetic_consistent_case()
        docs[1] = TradeDocument("packing_list", docs[1].fields, "commercial", 100)
        report = validate(docs, today_day=102)
        self.assertEqual(report.action, Action.VERIFY)
        self.assertIn("commercial", report.correlated_source_groups)


if __name__ == "__main__":
    unittest.main()
