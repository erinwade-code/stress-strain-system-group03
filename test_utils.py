test_utils.py - Unit tests verifying all 10 rubric requirements
for Task 6 integration.

import json
import os
import unittest
from material import get_material_database
from utils import StressStrainTest, TestCollection, ResultTestAnalysis

class TestUtilsRubric(unittest.TestCase):

    def setUp(self):
        self.db = get_material_database()
        self.json_file = "results.json"
        self.csv_file = "results.csv"

    def tearDown(self):
        """Clean up generated files after tests complete."""
        if os.path.exists(self.json_file):
            os.remove(self.json_file)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_01_invalid_numeric_inputs(self):
        """Rubric Check 1: Invalid numeric inputs"""
        with self.assertRaises(TypeError):
            StressStrainTest(self.db["Steel"], "invalid_text", 0.01, 10.0, 0.005)

    def test_02_negative_inputs(self):
        """Rubric Check 2: Negative inputs"""
        with self.assertRaises(ValueError):
            StressStrainTest(self.db["Steel"], -50000.0, 0.01, 10.0, 0.005)

    def test_03_zero_area(self):
        """Rubric Check 3: Zero area"""
        with self.assertRaises(ValueError):
            StressStrainTest(self.db["Steel"], 50000.0, 0, 10.0, 0.005)

    def test_04_zero_original_length(self):
        """Rubric Check 4: Zero original length"""
        with self.assertRaises(ValueError):
            StressStrainTest(self.db["Steel"], 50000.0, 0.01, 0, 0.005)

    def test_05_different_material_selections(self):
        """Rubric Check 5: Different material selections"""
        steel_test = StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005)
        pvc_test = StressStrainTest(self.db["PVC"], 100.0, 0.001, 2.0, 0.01)
        self.assertEqual(steel_test.material.name, "Structural Steel")
        self.assertEqual(pvc_test.material.name, "PVC Pipe")

    def test_06_multiple_test_records(self):
        """Rubric Check 6: Multiple test records"""
        collection = TestCollection()
        collection.add_test(StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005))
        collection.add_test(StressStrainTest(self.db["Aluminum"], 10000.0, 0.002, 1.0, 0.0015))
        self.assertEqual(len(collection.tests), 2)

    def test_07_file_saving(self):
        """Rubric Check 7: File saving (JSON)"""
        collection = TestCollection()
        collection.add_test(StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005))
        collection.save_to_json(self.json_file)
        self.assertTrue(os.path.exists(self.json_file))

    def test_08_file_loading(self):
        """Rubric Check 8: File loading (JSON)"""
        collection = TestCollection()
        collection.add_test(StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005))
        collection.save_to_json(self.json_file)

        with open(self.json_file, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["material_name"], "Structural Steel")

    def test_09_csv_export(self):
        """Rubric Check 9: CSV export"""
        collection = TestCollection()
        collection.add_test(StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005))
        collection.export_to_csv(self.csv_file)
        self.assertTrue(os.path.exists(self.csv_file))

    def test_10_execution_of_modular_application(self):
        """Rubric Check 10: Execution of the modular application"""
        t1 = StressStrainTest(self.db["Steel"], 50000.0, 0.01, 10.0, 0.005)
        t2 = StressStrainTest(self.db["PVC"], 1000000.0, 0.001, 2.0, 0.01)
        analysis = ResultTestAnalysis([t1, t2])
        report = analysis.generate_summary_report()
        self.assertIn("Test Summary Report", report)


if __name__ == "__main__":
    unittest.main()

