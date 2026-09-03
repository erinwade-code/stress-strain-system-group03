# Part 1: Basic Stress and Strain Calculator Template
# TODO: Complete this template by filling in the missing code


def main():
    """Main function for the stress and strain calculator."""

    # TODO: Print a header for your program
    print("=== Stress and Strain Calculator ===")
    print()

    # TODO: Get user input for the four required values
    # Hint: Use input() to get strings, then convert with float()
    force = float(input("Enter applied force (N): "))
    area = float(input("Enter cross-sectional area (M^2): "))
    original_length = float(input("Enter original length (m): "))
    change_in_length = float(input("Enter change in length (m): "))
    
    # TODO: Calculate stress and strain
    # Hint: Stress = Force / Area, Strain = Change in Length / Original Length
    stress = force/area
    strain = change_in_length/original_length


    # TODO: Display the input values using f-string formatting
    print()
    print("=== RESULTS ===")
    # TODO: Print each input value with appropriate formatting
    print(f"Applied Force: {force:.2f} N")
    print(f"Cross sectional area: {area:.4f} m^2")
    print(f"Original length: {original_length:.2f} m")
    print(f"Change in length: {change_in_length:.4f} m")


    print()

    # TODO: Display the calculated results
    print(f"Calculated stress: {stress:.2f} Pa")
    print(f"Calculated strain: {strain:.6f}")

    print()

    stress_mpa = stress/1000000
    print(f"Stress in MPa: {stress_mpa:.2f} MPa")
    if change_in_length >= 0:
        print("Loading type: Tension")
    else:
        print("Loading type: Compression")

    print()
    print("=== Analysis Complete ===")


# TODO: Add the standard Python execution pattern
if __name__ == "__main__":
    main()