from core.models.preliminary_propellent_and_motor_design.py import calculate_motor_parameters

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")

def main():
    print("Rocket Motor Design CLI — Imperial Units\n")

    # Input collection in correct order
    acceleration = get_float("Acceleration (g): ")
    bore_factor = get_float("Bore Factor (dimensionless): ")
    burn_time = get_float("Burn Time (s): ")
    burnrate_coefficient = get_float("Burnrate Coefficient (in/s·psi^(-exponent)): ")
    burnrate_exponent = get_float("Burnrate Exponent (unitless): ")
    chamber_pressure = get_float("Chamber Pressure (psi): ")
    combustion_efficiency = get_float("Combustion Efficiency (0–1): ")
    c_star_theoretical = get_float("Theoretical c* (ft/s): ")
    thrust_coefficient = get_float("Thrust Coefficient (dimensionless): ")
    exit_cone_angle_deg = get_float("Exit Cone Angle (°): ")
    exit_cone_efficiency = get_float("Exit Cone Efficiency (0–1): ")
    density = get_float("Propellant Density (lb/in³): ")
    empty_rocket_weight = get_float("Empty Rocket Weight (lbs): ")
    propellant_mass_fraction = get_float("Propellant Mass Fraction (0–1): ")

    try:
        result = calculate_motor_parameters(
            acceleration,
            bore_factor,
            burn_time,
            burnrate_coefficient,
            burnrate_exponent,
            chamber_pressure,
            combustion_efficiency,
            c_star_theoretical,
            thrust_coefficient,
            exit_cone_angle_deg,
            exit_cone_efficiency,
            density,
            empty_rocket_weight,
            propellant_mass_fraction,
        )

        print("\n--- Calculation Results ---")
        for key, value in result.items():
            print(f"{key}: {value:.4f}")

    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
