def calculate_stress(force: float, area: float) -> float:
    if area <= 0:
        raise ValueError("Cross-sectional area must be greater than zero.")
    return force / area

def calculate_strain(change_in_length: float, original_length: float) -> float:
    if original_length <= 0:
        raise ValueError("Original length must be greater than zero.")
    return change_in_length / original_length

def pa_to_mpa(stress_pa: float) -> float:
    return stress_pa / 1_000_000.0