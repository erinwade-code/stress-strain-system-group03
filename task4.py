def calculate_stress(force: float, area: float) -> float:
  if area <= 0: 
    raise ValueError("Cross-sectional area must be greater than zero.")
  return force / area
  
def calculate_strain(change_in_length: float, original_length: float) -> float:
  if orignal_length <= 0:
    raise ValueError("Original length must be greater than zero.")
  return change_in_length / original_length
  
def calculate_youngs_modulus(stress: float, strain: float) -> float:
    if strain <= 0:
        raise ValueError("Strain must be greater than zero.")
    return (stress / strain) / 1000.0

def calculate_factor_of_safety(yield_strength: float, applied_stress: float) -> float:
    if applied_stress <= 0:
        raise ValueError("Applied stress must be greater than zero.")
    return yield_strength / applied_stress

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val <= 0:
                print("Error: Value must be strictly greater than zero.")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input.")

def select_material() -> tuple[str, float]:
    materials = {
        "1": ("Structural Steel (A36)", 250.0),
        "2": ("Aluminum Alloy (6061-T6)", 276.0),
        "3": ("Titanium Alloy (Ti-6Al-4V)", 880.0),
        "4": ("Custom Material", None)
    }
print("\nSelect Material:")
    for key, (name, strength) in materials.items():
        if strength:
            print(f"  [{key}] {name} - Yield Strength: {strength} MPa")
        else:
            print(f"  [{key}] {name}")
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice in materials:
            name, strength = materials[choice]
            if strength is None:
                strength = get_positive_float("Enter custom yield strength (MPa): ")
            return name, strength
        print("Error: Selection out of range.")

def create_test_record(sample_id: str, material: str, stress: float, strain: float, modulus: float, fos: float) -> dict:
    return {
        "sample_id": sample_id,
        "material": material,
        "stress_mpa": round(stress, 2),
        "strain": round(strain, 6),
        "youngs_modulus_gpa": round(modulus, 2),
        "factor_of_safety": round(fos, 2),
        "status": "SAFE" if fos >= 1.0 else "FAILED"
    }
def add_record_to_history(history_list: list, record: dict) -> None:
    history_list.append(record)

