import random 
from material import Metal, Plastic, Composite
from properties import MaterialProperties

def get_material_database() -> dict:
    return {
        "Steel": Metal("Structural Steel", MaterialProperties(7850, 200e9, 250e6, 400e6), is_ferrous=True),
        "Aluminum": Metal("Aluminum 6061", MaterialProperties(2700, 69e9, 276e6, 310e6), is_ferrous=False),
        "PVC": Plastic("PVC Pipe", MaterialProperties(1380, 3e9, 52e6, 55e6), polymer_type="Thermoplastic"),
        "CarbonFiber": Composite("CFRP", MaterialProperties(1600, 150e9, 1200e6, 1500e6), fiber_type="Carbon")
    }

def generate_random_test_inputs():
    force = random.uniform(1000, 50000)  # Force in Newtons
    area = random.uniform(0.0001, 0.01)    # Area in
    orig_len = random.uniform(0.05, 0.5)
    delta_len = random.uniform(0.0001, 0.01)    # Change in length in meters
    return force, area, orig_len, delta_len