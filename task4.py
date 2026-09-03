def get_positive_float(prompt: str, allow_zero: bool = False) -> float:
    """Validates user input ensuring numerical and range requirements (Task 2/3)."""
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Error: Value must be positive.")
                continue
            if val == 0 and not allow_zero:
                print("Error: Value cannot be zero!")
                continue
            return val
        except ValueError:
            print("Error: Invalid numeric input. Please enter a valid number.")

def select_material(materials_db: dict) -> tuple[str, float, float]:
    """Handles material selection including database options and custom entries (Task 2/3)."""
    print("\n=== Material Selection ===")
    keys = list(materials_db.keys())
    for idx, key in enumerate(keys, 1):
        ys_mpa = materials_db[key]["yield_strength"] / 1e6
        ym_gpa = materials_db[key]["youngs_modulus"] / 1e9
        print(f"{idx}. {key} (Yield: {ys_mpa:.0f} MPa, Modulus: {ym_gpa:.0f} GPa)")
    
    custom_option = len(keys) + 1
    print(f"{custom_option}. Custom Material")

    while True:
        choice = input(f"Choose a material (1-{custom_option}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                name = keys[idx]
                props = materials_db[name]
                return name, props["yield_strength"], props["youngs_modulus"]
            elif idx == len(keys):
                name = input("Enter custom material name: ").strip().capitalize()
                ys_mpa = get_positive_float("Enter yield strength (MPa): ")
                ym_gpa = get_positive_float("Enter Young's modulus (GPa): ")
                return name, ys_mpa * 1e6, ym_gpa * 1e9
        print(f"Invalid option. Please enter a number between 1 and {custom_option}.")

def calculate_stress(force: float, area: float) -> float:
    """Calculates stress in Pascals (Task 1/4)."""
    return force / area

def calculate_strain(change_in_length: float, original_length: float) -> float:
    """Calculates dimensionless strain (Task 1/4)."""
    return change_in_length / original_length

def calculate_youngs_modulus_gpa(stress_pa: float, strain: float) -> float:
    """Calculates Young's Modulus in GPa from stress and strain (Task 4)."""
    if strain <= 0:
        return 0.0
    return (stress_pa / strain) / 1e9

def calculate_factor_of_safety(yield_strength_pa: float, stress_pa: float) -> float:
    """Calculates factor of safety (Task 2/3/4)."""
    if stress_pa <= 0:
        return float('inf')
    return yield_strength_pa / stress_pa

def create_test_record(sample_id: str, material: str, force: float, area: float,
                       orig_len: float, dl: float, stress: float, strain: float,
                       modulus_gpa: float, fos: float) -> dict:
    """Packages calculation results into a record dictionary (Task 3/4)."""
    return {
        "sample_id": sample_id,
        "material": material,
        "force": force,
        "area": area,
        "original_length": orig_len,
        "change_in_length": dl,
        "stress_pa": stress,
        "stress_mpa": stress / 1e6,
        "strain": strain,
        "youngs_modulus_gpa": modulus_gpa,
        "factor_of_safety": fos,
        "status": "SAFE" if fos >= 1.5 else ("CAUTION" if fos >= 1.0 else "FAILED")
    }

def display_test_results(record: dict) -> None:
    """Outputs structured result for an individual sample run (Task 1/2/4)."""
    print("\n" + "=" * 45)
    print(f"TEST RESULTS: {record['sample_id']} ({record['material']})")
    print("=" * 45)
    print(f"Applied Force      : {record['force']:.2f} N")
    print(f"Cross Section Area : {record['area']:.6f} m²")
    print(f"Original Length    : {record['original_length']:.4f} m")
    print(f"Change in Length   : {record['change_in_length']:.6f} m")
    print("-" * 45)
    print(f"Calculated Stress  : {record['stress_mpa']:.2f} MPa ({record['stress_pa']:.2f} Pa)")
    print(f"Calculated Strain  : {record['strain']:.6f}")
    print(f"Young's Modulus    : {record['youngs_modulus_gpa']:.2f} GPa")
    print(f"Factor of Safety   : {record['factor_of_safety']:.2f} [{record['status']}]")
    print("=" * 45)

def display_session_summary(history: list, unique_materials: set) -> None:
    """Displays aggregate statistics across all runs in the session (Task 3/4)."""
    print("\n" + "#" * 70)
    print("SESSION HISTORY SUMMARY")
    print("#" * 70)
    if not history:
        print("No records saved in this session.")
        print("#" * 70 + "\n")
        return

    print(f"Total calculations performed : {len(history)}")
    print(f"Unique materials tested      : {', '.join(unique_materials)} ({len(unique_materials)})")
    
    highest_stress = max(history, key=lambda x: x["stress_pa"])
    avg_strain = sum(r["strain"] for r in history) / len(history)

    print("\nStatistical Analysis:")
    print(f"- Highest Stress : {highest_stress['stress_mpa']:.2f} MPa ({highest_stress['material']})")
    print(f"- Average Strain : {avg_strain:.6f}")

    print("\nDetailed History Table:")
    header = f"{'Sample ID':<12} | {'Material':<18} | {'Stress (MPa)':<12} | {'FoS':<6} | {'Status'}"
    print(header)
    print("-" * len(header))
    for r in history:
        print(f"{r['sample_id']:<12} | {r['material']:<18} | {r['stress_mpa']:<12.2f} | {r['factor_of_safety']:<6.2f} | {r['status']}")
    print("#" * 70 + "\n")

def main():
    print("=== Integrated Stress & Strain Session Manager (Task 4) ===")
    
    materials_db = {
        "Steel": {"yield_strength": 250_000_000.0, "youngs_modulus": 200_000_000_000.0},
        "Aluminum": {"yield_strength": 276_000_000.0, "youngs_modulus": 69_000_000_000.0},
        "Titanium": {"yield_strength": 880_000_000.0, "youngs_modulus": 114_000_000_000.0}
    }
    
    calculations_history = []
    unique_materials = set()
    test_counter = 1

    while True:
        sample_id = f"SAMPLE-{test_counter:03d}"
        print(f"\n--- Starting Analysis for {sample_id} ---")

        material_name, yield_strength, _ = select_material(materials_db)
        
        force = get_positive_float("Enter applied force (N): ")
        area = get_positive_float("Enter cross-sectional area (m²): ")
        orig_len = get_positive_float("Enter original length (m): ")
        dl = get_positive_float("Enter change in length (m): ", allow_zero=True)

        stress = calculate_stress(force, area)
        strain = calculate_strain(dl, orig_len)
        modulus_gpa = calculate_youngs_modulus_gpa(stress, strain)
        fos = calculate_factor_of_safety(yield_strength, stress)

        record = create_test_record(
            sample_id, material_name, force, area, orig_len, dl, 
            stress, strain, modulus_gpa, fos
        )

        calculations_history.append(record)
        unique_materials.add(material_name)

        display_test_results(record)
        test_counter += 1

        again = input("Perform another calculation? (y/n): ").strip().lower()
        while again not in ("y", "n", "yes", "no"):
            again = input("Please enter 'y' or 'n': ").strip().lower()

        if again in ("n", "no"):
            break

    display_session_summary(calculations_history, unique_materials)
    print("Thank you for using the Stress & Strain Calculator.")

if __name__ == "__main__":
    main()

