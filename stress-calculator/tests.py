from datetime import datetime
from material import Material
import json
import csv
from pathlib import Path
from typing import List
 
class StressStrainTest:
    """A single stress-strain test."""
 
    def __init__(
        self,
        material: Material,
        force: float,
        area: float,
        original_length: float,
        change_in_length: float,
    ):
        if force <= 0:
            raise ValueError("Force must be positive")
        if area <= 0:
            raise ValueError("Area must be positive")
        if original_length <= 0:
            raise ValueError("Original length must be positive")
        # Change in length can be negative (compression)
 
        self.material = material
        self._force = force
        self._area = area
        self._original_length = original_length
        self._change_in_length = change_in_length
 
    @property
    def stress(self) -> float:
        """Calculate stress in MPa."""
        return self._force / self._area
 
    @property
    def strain(self) -> float:
        """Calculate strain (dimensionless)."""
        return self._change_in_length / self._original_length
 
    @property
    def youngs_modulus(self) -> float:
        """Calculate Young's modulus in GPa."""
        # Convert from MPa to GPa
        return (self.stress / self.strain) / 1000
 
    def will_fail(self) -> bool:
        """Determine if the material is likely to fail under this test."""
        return not self.material.can_withstand_stress(self.stress)
 
    def to_dict(self) -> dict:
        """Flat, JSON/CSV-friendly representation of this test.
 
        Using this instead of __dict__ directly avoids trying to
        serialize the Material object itself.
        """
        return {
            "material_name": self.material.name,
            "force": self._force,
            "area": self._area,
            "original_length": self._original_length,
            "change_in_length": self._change_in_length,
            "stress": round(self.stress, 4),
            "strain": round(self.strain, 6),
            "youngs_modulus": round(self.youngs_modulus, 4),
            "will_fail": self.will_fail(),
        }
 
    def __str__(self) -> str:
        return (
            f"Test on {self.material.name}: "
            f"Stress={self.stress:.2f} MPa, "
            f"Strain={self.strain:.6f}, "
            f"Young's Modulus={self.youngs_modulus:.2f} GPa"
        )
 
    def __eq__(self, other):
        if not isinstance(other, StressStrainTest):
            return False
        return (
            self.material.name == other.material.name
            and self.stress == other.stress
            and self.strain == other.strain
        )
 
    def __lt__(self, other):
        return self.stress < other.stress
        
class TestCollection:
    def __init__(self):
        self.tests = []

    def add_test(self, test: StressStrainTest):
        self.tests.append(test)

    def save_to_json(self, filename="results.json"):
        data = [t.__dict__ for t in self.tests]
        Path(filename).write_text(json.dumps(data, indent =4))
      

    def export_to_csv(self, filename="results.csv"):
        if not self.tests:
            return
        keys = self.tests[0].__dict__.keys()
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows([t.__dict__ for t in self.tests])

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
        strength for each test"""
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
