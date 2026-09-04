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

    force = float(input("Enter force (N): "))
    area = float(input("Enter area (m^2): "))
    orig_l = float(input("Enter original length (m): "))
    delta_l = float(input("Enter delta length (m): "))

    stress = calculate_stress(force, area)
    strain = calculate_strain(delta_l, orig_l)

    print(f"\nCalculated Stress: {stress:.2f} Pa ({pa_to_mpa(stress):.2f} MPa)")
    print(f"Calculated Strain: {strain:.6f}")

    test_entry = StressStrainTest(material, force, area, orig_l, delta_l)
    print(test_entry)
    print("FAILS under this load!" if test_entry.will_fail() else "Passes safely.")

    history.add_test(test_entry)
    history.save_to_json()
    print("Test logged and saved to results.json!")

if __name__ == "__main__":
    main()
