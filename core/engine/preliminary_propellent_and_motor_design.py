import math

GRAVITY = 32.2  # ft/s²

def calculate_motor_parameters(
    acceleration: float,                  # g (gravity units)
    bore_factor: float,                   # dimensionless
    burn_time: float,                     # seconds
    burnrate_coefficient: float,          # in/s · psi^(-burnrate_exponent)
    burnrate_exponent: float,             # unitless
    chamber_pressure: float,              # psi
    combustion_efficiency: float,         # 0–1 (dimensionless)
    c_star_theoretical: float,            # ft/s
    thrust_coefficient: float,            # dimensionless
    exit_cone_angle_deg: float,           # degrees
    exit_cone_efficiency: float,          # 0–1 (dimensionless)
    density: float,                       # lb/in³
    empty_rocket_weight: float,           # lbs
    propellant_mass_fraction: float,      # 0–1 (dimensionless)
) -> dict:

    thrust_weight_ratio = acceleration + 1  # dimensionless

    denominator = (propellant_mass_fraction / thrust_weight_ratio) - (burn_time / c_star_theoretical)
    if denominator == 0:
        raise ValueError("Division by zero in thrust calculation. Check inputs.")

    # Basic thrust parameters
    thrust = (propellant_mass_fraction * empty_rocket_weight) / denominator
    liftoff_weight = thrust / thrust_weight_ratio
    motor_weight = liftoff_weight - empty_rocket_weight
    propellant_weight = motor_weight * propellant_mass_fraction

    # Exit cone and divergence
    exit_angle_rad = math.radians(exit_cone_angle_deg)
    divergence_factor = 1 + (math.cos(exit_angle_rad) * exit_cone_efficiency)
    delivered_thrust_coefficient = thrust_coefficient * divergence_factor * exit_cone_efficiency
    delivered_specific_impulse = (delivered_thrust_coefficient * c_star_theoretical * combustion_efficiency) / GRAVITY

    # Throat properties
    propellant_weight_flow = thrust / delivered_thrust_coefficient
    throat_area = thrust / (delivered_thrust_coefficient * chamber_pressure)
    throat_radius = math.sqrt(throat_area / math.pi)
    throat_diameter = 2 * throat_radius

    # Bore and burn properties
    bore_diameter = throat_diameter * bore_factor
    burnrate = burnrate_coefficient * (chamber_pressure ** burnrate_exponent)
    web_thickness = burn_time * burnrate
    propellant_outer_diameter = (2 * web_thickness) + bore_diameter

    # Propellant length and ablation
    initial_propellant_length = (
        (propellant_outer_diameter - bore_diameter +
         ((propellant_outer_diameter ** 2 - bore_diameter ** 2) /
          (2 * propellant_outer_diameter)))
        / (1 - (bore_diameter / propellant_outer_diameter))
    )
    final_propellant_length = initial_propellant_length - (2 * web_thickness)

    initial_cartridge_ablation = (
        2 * ((math.pi / 4) * (propellant_outer_diameter ** 2 - bore_diameter ** 2)) +
        math.pi * initial_propellant_length * bore_diameter
    )
    final_cartridge_ablation = math.pi * propellant_outer_diameter * final_propellant_length

    target_ablation = propellant_weight_flow / (density * burnrate)
    no_of_propellant_cartridge = target_ablation / final_cartridge_ablation

    return {
        "Acceleration (ft/s²)": acceleration,
        "Thrust-to-Weight Ratio": thrust_weight_ratio,
        "Thrust (lbf)": thrust,
        "Liftoff Weight (lbs)": liftoff_weight,
        "Motor Weight (lbs)": motor_weight,
        "Propellant Weight (lbs)": propellant_weight,
        "Divergence Factor": divergence_factor,
        "Delivered Thrust Coefficient": delivered_thrust_coefficient,
        "Delivered Specific Impulse (s)": delivered_specific_impulse,
        "Propellant Weight Flow (lb/s)": propellant_weight_flow,
        "Throat Area (in²)": throat_area,
        "Throat Radius (in)": throat_radius,
        "Throat Diameter (in)": throat_diameter,
        "Bore Diameter (in)": bore_diameter,
        "Burn Rate (in/s)": burnrate,
        "Web Thickness (in)": web_thickness,
        "Propellant Outer Diameter (in)": propellant_outer_diameter,
        "Initial Propellant Length (in)": initial_propellant_length,
        "Final Propellant Length (in)": final_propellant_length,
        "Initial Cartridge Ablation (in²)": initial_cartridge_ablation,
        "Final Cartridge Ablation (in²)": final_cartridge_ablation,
        "Target Ablation (in²)": target_ablation,
        "No. of Propellant Cartridges": no_of_propellant_cartridge,
    }
