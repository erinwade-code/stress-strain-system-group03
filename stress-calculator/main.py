from database import get_material_database
from utils import calculate_stress, calculate_strain, pa_to_mpa
from tests import StressStrainTest, TestCollection

def main():
    db = get_material_database()
    history = TestCollection()

    print("=== Modular Stress and Strain System ===")
    print(f"Available materials: {', '.join(db.keys())}")
    material_key = input("Choose a material: ").strip()
    while material_key not in db:
        material_key = input(
            f"'{material_key}' not found. Choose one of {list(db.keys())}: "
        ).strip()
    material = db[material_key]

    force = read_positive_float("Enter force (N): ")
    area = read_positive_float("Enter area (m^2): ")
    orig_l = read_positive_float("Enter original length (m): ")
    delta_l = read_float("Enter delta length (m): ")

    stress = calculate_stress(force, area)
    strain = calculate_strain(delta_l, orig_l)

    print(f"\nCalculated Stress: {stress:.2f} Pa ({pa_to_mpa(stress):.2f} MPa)")
    print(f"Calculated Strain: {strain:.6f}")

    try:
        test_entry = StressStrainTest(material, force, area, orig_l, delta_l)
    except ValueError as exc:
        print(f"Could not create test record: {exc}")
        return
    
    test_entry = StressStrainTest(material, force, area, orig_l, delta_l)
    print(test_entry)
    print("FAILS under this load!" if test_entry.will_fail() else "Passes safely.")

    history.add_test(test_entry)
    history.save_to_json()
    print("Test logged and saved to results.json!")

def read_float(prompt: str) -> float:
    """Keep prompting until the user enters a value that parses as a float."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"'{raw}' is not a valid number. Please try again.")
 
 
def read_positive_float(prompt: str) -> float:
    """Keep prompting until the user enters a number greater than zero."""
    while True:
        value = read_float(prompt)
        if value <= 0:
            print("Value must be greater than zero. Please try again.")
            continue
        return value

if __name__ == "__main__":
    main()
