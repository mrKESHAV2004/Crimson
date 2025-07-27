import math
#SI 

GRAVITY = 9.806650

def to_be_named(
        motor_total_impulse, #Ns
        average_thrust,      #N
        propellant_mass,     #kg
        dead_mass,           #kg
        drag_coefficient,    #(dimensionless)
        diameter             #m
):
        burn_time = motor_total_impulse / average_thrust                 # t = I / F (s)
        total_mass = dead_mass + 0.5 * propellant_mass                   # m = md + 1/2 mp (kg)
        acceleration = average_thrust / total_mass - GRAVITY             # a = F/m - g (m/s²)
        burnout_displacement = 0.5 * acceleration * burn_time ** 2       # z1 = 1/2 a t² (m)
        burnout_velocity = acceleration * burn_time                       # V1 = a t (m/s)
        equivalent_displacement = (average_thrust * burnout_displacement) / (total_mass * GRAVITY)  # z2 = F z1 / (m g) (m)
        adjusted_time = burn_time + math.sqrt(2 * (equivalent_displacement - burnout_displacement) / GRAVITY)  # t2 = t + sqrt[2 (z2 - z1) / g] (s)
        drag_influence_number = (drag_coefficient * diameter ** 2 * burnout_velocity ** 2) / (1000 * dead_mass)  # N = Cd D² V1² / (1000 md) (dimensionless)

        drag_reduction_factor_peak_altitude = math.exp(-0.000650 * drag_influence_number)     # fz(N) (dimensionless)
        drag_reduction_factor_burnout_velocity = math.exp(-0.000300 * drag_influence_number)  # fv(N) (dimensionless)
        drag_reduction_factor_time_to_apogee = math.exp(-0.000700 * drag_influence_number)    # ft(N) (dimensionless)

        ideal_peak_altitude = drag_reduction_factor_peak_altitude * equivalent_displacement  # zpeak = fz(N) * z2 (m)
        corrected_burnout_velocity = drag_reduction_factor_burnout_velocity * burnout_velocity # Vmax = fv(N) * V1 (m/s)
        corrected_time_to_apogee = drag_reduction_factor_time_to_apogee * adjusted_time       # tpeak = ft(N) * t2 (s)

        return {
        "Burn Time (sec)": burn_time,
        "Total Mass (kg)": total_mass,
        "Acceleration (m/s^2)": acceleration,
        "Burnout Displacement (m)": burnout_displacement,
        "Burnout Velocity (m/s)": burnout_velocity,
        "Equivalent Displacement (m)": equivalent_displacement,
        "Adjusted Time (sec)": adjusted_time,
        "Drag Influence Number (dimensionless)": drag_influence_number,
        "Drag Reduction Factor Peak Altitude (dimensionless)": drag_reduction_factor_peak_altitude,
        "Drag Reduction Factor Burnout Velocity (dimensionless)": drag_reduction_factor_burnout_velocity,
        "Drag Reduction Factor Time to Apogee (dimensionless)": drag_reduction_factor_time_to_apogee,
        "Ideal Peak Altitude (m)": ideal_peak_altitude,
        "Corrected Burnout Velocity (m/s)": corrected_burnout_velocity,
        "Corrected Time to Apogee (sec)": corrected_time_to_apogee
    }

def test_to_be_named():
    test_values = {
        "motor_total_impulse": 100.0,
        "average_thrust": 50.0,
        "propellant_mass": 0.2,
        "dead_mass": 0.8,
        "drag_coefficient": 0.75,
        "diameter": 0.05
    }
    result = to_be_named(
        test_values["motor_total_impulse"],
        test_values["average_thrust"],
        test_values["propellant_mass"],
        test_values["dead_mass"],
        test_values["drag_coefficient"],
        test_values["diameter"]
    )
    print("Test results for to_be_named with given values:")
    for key, value in result.items():
        print(f"{key}: {value}")


test_to_be_named()