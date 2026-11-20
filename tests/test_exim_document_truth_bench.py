import unittest
from exim_document_truth_bench import Action, TradeDocument, synthetic_consistent_case, validate

class TruthBenchTests(unittest.TestCase):
    def test_consistent_independent_evidence_can_act(self):
        self.assertEqual(validate(synthetic_consistent_case(),today_day=102).action,Action.ACT)
    def test_cross_document_conflict_escalates(self):
        docs=synthetic_consistent_case()
        bad=TradeDocument("declaration",{**docs[2].fields,"gross_weight_kg":"1500"},"broker",101)
        report=validate([docs[0],docs[1],bad],today_day=102)
        self.assertEqual(report.action,Action.ESCALATE)
        self.assertIn("gross_weight_kg",report.mismatches)
    def test_missing_document_requires_verification(self):
        report=validate(synthetic_consistent_case()[:2],today_day=102)
        self.assertEqual(report.action,Action.VERIFY)
        self.assertIn("declaration",report.missing_kinds)
    def test_stale_authorization_escalates(self):
        docs=synthetic_consistent_case()
        docs[2]=TradeDocument("declaration",docs[2].fields,"broker",101,authorization_expires_day=101)
        self.assertEqual(validate(docs,today_day=102).action,Action.ESCALATE)
    def test_future_issued_document_escalates(self):
        docs=synthetic_consistent_case()
        docs[0]=TradeDocument("invoice",docs[0].fields,"commercial",103)
        report=validate(docs,today_day=102)
        self.assertEqual(report.action,Action.ESCALATE)
        self.assertEqual(report.future_issued_documents,("invoice",))
    def test_missing_cross_document_field_requires_verification(self):
        docs=synthetic_consistent_case()
        docs[1]=TradeDocument("packing_list", {"shipment_id":"S-100", "consignee":"ACME"}, "warehouse", 100)
        report=validate(docs,today_day=102)
        self.assertEqual(report.action,Action.VERIFY)
        self.assertIn("packing_list.gross_weight_kg",report.missing_fields)
    def test_duplicate_document_kind_escalates(self):
        docs=synthetic_consistent_case()
        report=validate(docs+[docs[0]],today_day=102)
        self.assertEqual(report.action,Action.ESCALATE)
        self.assertEqual(report.duplicate_kinds,("invoice",))
    def test_invalid_day_and_empty_field_rejected(self):
        with self.assertRaises(ValueError): validate(synthetic_consistent_case(),today_day=-1)
        with self.assertRaises(ValueError): TradeDocument("invoice",{"weight":" "},"issuer",1)
if __name__ == "__main__": unittest.main()
