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
    
    while True:
        print("\nAvailable Materials:", ", ".join(materials_db.keys()))
        material_name = input("Enter material name (or 'quit' to exit): ").strip().capitalize()

        if material_name.lower() == 'quit':
            break

        if material_name not in materials_db:
            print("Error: Material not found in database!")
            continue

        try:
            force = float(input(f"Enter force in {UNITS[0]}: "))
            area = float(input(f"Enter area in {UNITS[1]}: "))
            length = float(input(f"Enter original length in {UNITS[2]}: "))
            change_in_length = float(input(f"Enter change in length in {UNITS[2]}: "))

            if area <= 0 or length <= 0:
                print("Error: Area and original length must be strictly positive!")
                continue

            stress = force / area
            strain = change_in_length / length

            yield_strength = materials_db[material_name]["yield_strength"]
            safety_factor = yield_strength / stress if stress > 0 else float('inf')

            record = {
                "material": material_name,
                "force": force,
                "area": area,
                "original_length": length,
                "change_in_length": change_in_length,
                "stress": stress,
                "strain": strain,
                "safety_factor": safety_factor
            }

            calculations_history.append(record)
            unique_materials.add(material_name)

            print(f"\nResults: Stress = {stress:.2f} {UNITS[3]}, Strain = {strain:.6f}")

        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")
        except ZeroDivisionError:
            print("Error: Area and original length cannot be zero!")

    print("\n=== Session Summary ===")
    print(f"Total calculations performed: {len(calculations_history)}")
