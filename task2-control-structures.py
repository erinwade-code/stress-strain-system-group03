materials = {
    "steel": {"yield_strength": 250, "youngs_modulus":200 },
    "aluminum":{"yield_strength": 95, "youngs_modulus":69},
    "titanium":{"yield_strenght": 880, "youngs_modulus":114}
}

def get_positive_float(prompt, allow_zero=False):

    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number")
            continue

        if value < 0:
            print("Value must be positive")
        elif value == 0 and not allow_zero:
            print("Value cannot be zero!")
        else: 
            return value

def select_material():

    print()
    print("=== Material Selection ===")
    print("1. Steel")
    print("2. Aluminum ")
    print("3. Titanium")
    print("4. Custom materials")

    while True:
        choice = input("Choose a material (1-4): ").strip()

        if choice == '1':
            name, props = "Steel", materials["steel"]
        elif choice == '2':
            name, props = "Aluminum", materials["aluminum"]
        elif choice == '3': 
            name, props = "Titanium", materials["titanium"]
        elif choice == '4':
            name = input("Enter a custom material name: ").strip()
            yield_strength = get_positive_float("Enter yield strength MPa")
            youngs_modulus = get_positive_float("Enter Young's modulus GPa ")
            props = {"yield_strength": yield_strength, "youngs_modulus": youngs_modulus}
        else:
            print("Invalid. Enter 1, 2, 3, or 4.")
            continue

        selected = {
            "name": name, 
            "yield_strength": props["yield_strength"],
            "youngs_modulus": props["youngs_modulus"],
        }
        print(f"\nSelected maeerial: {selected['name']}")
        print(f" Yield strenght: {selected['yield_strength']} MPa")
        print(f" Young's modulus: {selected['youngs_modulus']} GPa")
        return selected

    
def analyze_safety(stress_pa, material):
    stress_mpa = stress_pa / 1_000_000
    yield_strength = material["yield_strength"]
    factor_of_safety = yield_strength / stress_mpa 

    print()
    print(f"Calculated stress: {stress_mpa::.2f} MPa")
    print(f"{material['name']} yield strength: {yield_strength} MPa")
    print(f"Factor of safety: {factor_of_safety:.2f}")

    if stress_mpa >= yield_strength:
        print("Failure! stress meets / exceeds yield strength. Material will fail")
    elif factor_of_safety < 1.5:
        print("Caution! Factor of safety is low. Design margin is thin.")
    else:
        print("Safe! Loading is within safe design limits.")

def main():
    print(" === Stress and Strain Calculator (Part 2) ===")
    print()

    while True:
        material = select_material()
        print()

        force = get_poisitive_float("Enter applied force (N): ")
        area = get_poisitive_float("Enter cross-sectional area (m^2):")
        original_length = get_poisitive_float("Enter original length (m):")
        change_in_length = get_poisitive_float("Enter change in length (m): ", allow_zero=True)

        stress = force / area
        strain = change_in_length / original_length

        print()
        print("=== RESULTS ====")
        print(f"Force: {force:2f} N")
        print(f"Area: {area:.4f} m^2")
        print(f"Original Length: {original_length:.2f} m")
        print(f"Change in Length: {change_in_length:.4f} m")
        print()
        print(f"Stress: {stress:.2f} Pa")
        print(f"Strain: {strain:.6f}")

        analyze_safety(stress, material)

        print()
        print("=== Analysis Complete ===")

        again = input("\nPerform another calculation (y/n):").strip().lower()

        while again not in ("y", "n", "yes", "no"):
            again = input("Pleaase enter 'y' or 'n': ").strip().lower()

        if again in ("n", "no"):
            print("\n Thank you for using the Stress & Strain Calculator.")

if __name__ == "__main__":
    main()
            
        
        
              
