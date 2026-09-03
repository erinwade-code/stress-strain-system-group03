from properties import MaterialProperties

class Material:
    def __init__(self, name: str, properties: MaterialProperties):
        self.name = name
        self.properties = properties

    def __str__(self) -> str:
        return f"{self.name} (Density: {self.properties.density} kg/m³)"

    def can_withstand_stress(self, stress: float) -> bool:
        return stress < self.properties.yield_strength

class Metal(Material):
    def __init__(self, name: str, properties: MaterialProperties, is_ferrous: bool = False):
        super().__init__(name, properties)
        self.is_ferrous = is_ferrous

class Plastic(Material):
    def __init__(self, name: str, properties: MaterialProperties, polymer_type: str):
        super().__init__(name, properties)
        self.polymer_type = polymer_type

class Composite(Material):
    def __init__(self, name: str, properties: MaterialProperties, fiber_type: str):
        super().__init__(name, properties)
        self.fiber_type = fiber_type