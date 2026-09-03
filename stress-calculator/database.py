from material import Metal, Plastic, Composite
from properties import MaterialProperties

def get_material_database() -> dict:
    return {
        "Steel": Metal("Structural Steel", MaterialProperties(7850, 200e9, 250e6, 400e6), is_ferrous=True),
        "Aluminum": Metal("Aluminum 6061", MaterialProperties(2700, 69e9, 276e6, 310e6), is_ferrous=False),
        "PVC": Plastic("PVC Pipe", MaterialProperties(1380, 3e9, 52e6, 55e6), polymer_type="Thermoplastic"),
        "CarbonFiber": Composite("CFRP", MaterialProperties(1600, 150e9, 1200e6, 1500e6), fiber_type="Carbon")
    }