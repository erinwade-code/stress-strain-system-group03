from properties import MaterialProperties

class Material:
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
        if not isinstance(other, Material):
            return NotImplemented
        return self.properties.yield_strength < other.properties.yield_strength
 
    def can_withstand_stress(self, stress: float) -> bool:
        return stress < self.properties.yield_strength
 
class Plastic(Material): 
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        is_thermoplastic: bool = False,
        polymer_type: str = "",
    ):
        if not polymer_type:
            raise ValueError("polymer_type must be provided")
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
    def __init__(
        self,
        name: str,
        properties: MaterialProperties,
        fiber_type: str = None,
        matrix_material: Material = None,
        reinforcement_material: Material = None,
    ):
        if matrix_material is not None and not isinstance(matrix_material, Material):
            raise ValueError("matrix_material must be a Material instance")
        if reinforcement_material is not None and not isinstance(
            reinforcement_material, Material
        ):
            raise ValueError("reinforcement_material must be a Material instance")
        if fiber_type is None and (
            matrix_material is None or reinforcement_material is None
        ):
            raise ValueError(
                "Composite requires either fiber_type, or both "
                "matrix_material and reinforcement_material"
            )
 
        super().__init__(name, properties)
        self.fiber_type = fiber_type
        self.matrix_material = matrix_material
        self.reinforcement_material = reinforcement_material
 
    def __str__(self) -> str:
        if self.matrix_material and self.reinforcement_material:
            matrixm = self.matrix_material.name
            reinforce = self.reinforcement_material.name
            return (
                f"{self.name} (contains both {matrixm} and {reinforce}, "
                f"with its Density: {self.properties.density} kg/m³)"
            )
        return (
            f"{self.name} ({self.fiber_type} fiber composite, "
            f"Density: {self.properties.density} kg/m³)"
        )
