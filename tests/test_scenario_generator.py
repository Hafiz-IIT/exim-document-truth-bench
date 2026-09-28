import unittest

from scenario_generator import run_benchmark


class ScenarioBenchmarkTests(unittest.TestCase):
    def test_reference_scenarios(self):
        result = run_benchmark()
        self.assertEqual(result["total"], 5)
        self.assertEqual(result["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
