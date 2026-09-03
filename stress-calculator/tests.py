from datetime import datetime
import json
import csv

class StressStrainTest:
    def __init__(self, material_name: str, force: float, area: float, orig_len: float, delta_len: float):
        self.material_name = material_name
        self.force = force
        self.area = area
        self.orig_len = orig_len
        self.delta_len = delta_len
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TestCollection:
    def __init__(self):
        self.tests = []

    def add_test(self, test: StressStrainTest):
        self.tests.append(test)

    def save_to_json(self, filename="results.json"):
        data = [t.__dict__ for t in self.tests]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def export_to_csv(self, filename="results.csv"):
        if not self.tests:
            return
        keys = self.tests[0].__dict__.keys()
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerow([t.__dict__ for t in self.tests])

class ResultTestAnalysis:
    """Aggregates and analyzes a collection of stress-strain tests."""
 
    def __init__(self, tests: List[StressStrainTest]):
        self.tests = tests
 
    def average_stress_by_material(self):
        stress_by_material = {}
        for test in self.tests:
            name = test.material.name
            stress_by_material.setdefault(name, []).append(test.stress)
        return {
            name: sum(stresses) / len(stresses)
            for name, stresses in stress_by_material.items()
        }
 
    def generate_summary_report(self) -> str:
        averages = self.average_stress_by_material()
        passed = sum(1 for test in self.tests if not test.will_fail())
        failed = sum(1 for test in self.tests if test.will_fail())
        averages_text = "".join(
            f"  {name}: {avg:.2f} MPa\n" for name, avg in averages.items()
        )
        report = (
            f"Test Summary Report\n"
            f"Total tests: {passed + failed}\n"
            f"Passed: {passed}\n"
            f"Failed: {failed}\n"
            f"Average stress by material:\n"
            f"{averages_text}"
        )
        return report
 
    def describe_results(self, bar_width: int = 30) -> str:
        """A simple text-based 'visualization' of stress relative to yield
        strength for each test."""
        if not self.tests:
            return "No tests to describe."
        max_stress = max(test.stress for test in self.tests)
        scale = bar_width / max_stress if max_stress else 0
        lines = ["Stress vs. Yield Strength"]
        for test in self.tests:
            yield_strength = test.material.properties.yield_strength
            filled = round(test.stress * scale)
            bar = "#" * filled
            pct_of_yield = (test.stress / yield_strength) * 100
            status = "FAIL" if test.will_fail() else "OK"
            lines.append(
                f"{test.material.name:>12} | {bar} "
                f"{test.stress:.1f} MPa ({pct_of_yield:.0f}% of yield) [{status}]"
            )
        return "\n".join(lines)
