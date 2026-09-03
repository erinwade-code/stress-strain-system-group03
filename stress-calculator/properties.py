from dataclasses import dataclass


@dataclass
class MaterialProperties:
    density: float
    youngs_modulus: float
    yield_strength: float
    ultimate_strength: float    

    def __post_init__(self):
        if self.density <= 0:
            raise ValueError("Density must be positive")
        if self.youngs_modulus <= 0:
            raise ValueError("Young's modulus must be positive")
        if self.yield_strength <= 0:
            raise ValueError("Yield strength must be positive")
        if self.ultimate_strength <= 0:
            raise ValueError("Ultimate strength must be positive")
        if self.ultimate_strength < self.yield_strength:
            raise ValueError("Ultimate strength cannot be less than yield strength")
