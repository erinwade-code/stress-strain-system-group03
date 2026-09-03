from dataclasses import dataclass

@dataclass
class MaterialProperties:
    density: float         
    youngs_modulus: float  
    yield_strength: float  
    ultimate_strength: float 