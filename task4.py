def calculate_stress(force: float, area: float) -> float:
  if area <= 0: 
    raise ValueError("Cross-sectional area must be greater than zero.")
  return force / area

