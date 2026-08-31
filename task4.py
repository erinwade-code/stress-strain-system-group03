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
