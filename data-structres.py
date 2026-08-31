def main():
    print("=== Stress and Strain Calculator - Session Manager ===\n")

    calculations_history = [] 
    unique_materials = set() 
    UNITS = ("N", "m²", "m", "Pa") 

    materials_db = {
        "Steel": {"yield_strength": 250000000, "youngs_modulus": 200000000000},
        "Aluminum": {"yield_strength": 276000000, "youngs_modulus": 69000000000},
        "Titanium": {"yield_strength": 830000000, "youngs_modulus": 114000000000}
    }
    
