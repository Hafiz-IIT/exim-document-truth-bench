import unittest

from scenario_generator import run_benchmark


class ScenarioBenchmarkTests(unittest.TestCase):
    def test_reference_scenarios(self):
        result = run_benchmark()
        self.assertEqual(result["total"], 7)
        self.assertEqual(result["accuracy"], 1.0)
        self.assertEqual(result["unsafe_action_rate"], 0.0)
        self.assertEqual(result["false_block_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
