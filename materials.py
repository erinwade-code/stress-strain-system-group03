from dataclasses import dataclass, field
from typing import List


@dataclass
class MaterialProperties:
    """Properties of a material.

    Implemented as a dataclass since it's a plain, data-centric container.
    Validation happens in __post_init__ since dataclasses don't get
    property setters called during __init__.
    """

    density: float  # kg/m³
    yield_strength: float  # MPa
    typical_youngs_modulus: float  # GPa

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be positive")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive")
        if self.typical_youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive")


class Material:
    """Base class for all materials."""

    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return f"{self.name} (Density: {self.properties.density} kg/m³)"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Material):
            return False
        return self.name == other.name

    def __lt__(self, other) -> bool:
        """Compare materials by yield strength (useful for sorting/ranking)."""
        if not isinstance(other, Material):
            return NotImplemented
        return self.properties.yield_strength < other.properties.yield_strength

    def can_withstand_stress(self, stress: float) -> bool:
        """Check if the material can withstand the given stress.

        Both stress and yield_strength are already in MPa, so no
        unit conversion is needed here.
        """
        return stress < self.properties.yield_strength


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
        strength for each test, scaled to a fixed bar width so results can
        be scanned at a glance without needing a plotting library.
        """
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


class Metal(Material):
    """A metal material."""

    def __init__(
        self, name: str, properties: MaterialProperties, is_ferrous: bool = False
    ):
        super().__init__(name, properties)
        self.is_ferrous = is_ferrous

    def __str__(self) -> str:
        ferrous_text = "Ferrous" if self.is_ferrous else "Non-ferrous"
        return f"{self.name} ({ferrous_text} metal, Density: {self.properties.density} kg/m³)"


class Plastic(Material):
    """A plastic material."""

    VALID_POLYMER_TYPES = ("PVC", "Polyethylene", "Nylon")

    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        is_thermoplastic: bool = False,
        polymer_type: str = "",
    ):
        if polymer_type not in self.VALID_POLYMER_TYPES:
            raise ValueError(
                f"polymer_type must be one of {self.VALID_POLYMER_TYPES}"
            )
        super().__init__(name, properties)
        self.is_thermoplastic = is_thermoplastic
        self.polymer_type = polymer_type

    def __str__(self) -> str:
        thermoplastic = "Thermoplastic" if self.is_thermoplastic else "Thermosetting"
        return (
            f"{self.name} ({thermoplastic}, plastic, {self.polymer_type}, "
            f"Density: {self.properties.density} kg/m³)"
        )


class Composite(Material):
    """A composite material, composed of a matrix and a reinforcement material."""

    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        matrix_material: Material,
        reinforcement_material: Material,
    ):
        if not isinstance(matrix_material, Material):
            raise ValueError("matrix_material must be a Material instance")
        if not isinstance(reinforcement_material, Material):
            raise ValueError("reinforcement_material must be a Material instance")

        super().__init__(name, properties)
        self.matrix_material = matrix_material
        self.reinforcement_material = reinforcement_material

    def __str__(self) -> str:
        matrixm = self.matrix_material.name
        reinforce = self.reinforcement_material.name
        return (
            f"{self.name} (contains both {matrixm} and {reinforce}, "
            f"with its Density: {self.properties.density} kg/m³)"
        )


if __name__ == "__main__":
    # Example usage
    steel_properties = MaterialProperties(
        density=7850, yield_strength=250, typical_youngs_modulus=200
    )
    steel = Metal("Steel", steel_properties, is_ferrous=True)
    test = StressStrainTest(
        steel, force=5000, area=25, original_length=100, change_in_length=0.5
    )

    polymer_properties = MaterialProperties(
        density=32, yield_strength=100, typical_youngs_modulus=100
    )
    polymer = Plastic(
        "Polymer", polymer_properties, is_thermoplastic=True, polymer_type="PVC"
    )
    test2 = StressStrainTest(
        polymer, force=1200, area=20, original_length=60, change_in_length=1.0
    )

    fiberglass_properties = MaterialProperties(
        density=1800, yield_strength=600, typical_youngs_modulus=40
    )
    fiberglass = Composite(
        "Fiberglass",
        fiberglass_properties,
        matrix_material=polymer,
        reinforcement_material=steel,
    )
    test3 = StressStrainTest(
        fiberglass, force=200, area=30, original_length=150, change_in_length=1.5
    )

    print(fiberglass)
    print(test3)
    print(f"Will the material fail? {'Yes' if test.will_fail() else 'No'}")
    print(f"Calculated Young's modulus: {test.youngs_modulus:.2f} GPa")
    print(f"Typical Young's modulus: {steel.properties.typical_youngs_modulus:.2f} GPa")

    print()
    analysis = ResultTestAnalysis([test, test2, test3])
    print(analysis.generate_summary_report())
    print()
    print(analysis.describe_results())