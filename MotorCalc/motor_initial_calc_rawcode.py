# Constants
GRAVITY_CONSTANT = 32.2    # ft/s², standard gravity constant on Earth
LBS_TO_NEWTON = 4.445      # Conversion factor: 1 lb·s = 4.445 N·s

def Motor_Initial_Parameters_Calculater(
    Rocket_Velocity,             # ft/s (velocity off rod)
    Rod_Length,                  # ft (length of launch rod)
    Propellant_Mass_Fraction,    # unitless (typically 0.5 to 0.85)
    Burn_time,                   # seconds (motor burn duration)
    Weight_Of_Rocket,            # lbs (dry weight of the rocket)
    Specific_Impulse             # seconds (Isp, performance of propellant)
):
    # Kinematics and Thrust Calculations
    Initial_Rocket_Acceleration = (Rocket_Velocity ** 2) / (2 * Rod_Length)    # ft/s²
    Acceleration_G = Initial_Rocket_Acceleration / GRAVITY_CONSTANT            # g's
    Initial_Thrust_To_Weight_Ratio = Acceleration_G + 1                        # unitless

    # Initial thrust required for liftoff
    Initial_Thrust = (Propellant_Mass_Fraction * Weight_Of_Rocket) / (
        (Propellant_Mass_Fraction / Initial_Thrust_To_Weight_Ratio) -
        (Burn_time / Specific_Impulse)
    )                                                                          # lbs

    # Calculating derived mass properties
    Liftoff_Rocket_Weight = Initial_Thrust / Initial_Thrust_To_Weight_Ratio    # lbs
    Motor_Weight = Liftoff_Rocket_Weight - Weight_Of_Rocket                    # lbs
    Propellant_Weight = Motor_Weight * Propellant_Mass_Fraction                # lbs

    # Motor impulse metrics
    Motor_Impulse = Specific_Impulse * Propellant_Weight                       # lb·s
    Motor_Impulse_Newton = Motor_Impulse * LBS_TO_NEWTON                       # N·s

    return {
        "Initial_Rocket_Acceleration": Initial_Rocket_Acceleration,   # ft/s²
        "Acceleration_G": Acceleration_G,                             # g
        "Initial_Thrust_To_Weight_Ratio": Initial_Thrust_To_Weight_Ratio,  # unitless
        "Initial_Thrust": Initial_Thrust,                             # lbs
        "Liftoff_Rocket_Weight": Liftoff_Rocket_Weight,               # lbs
        "Motor_Weight": Motor_Weight,                                 # lbs
        "Propellant_Weight": Propellant_Weight,                       # lbs
        "Motor_Impulse": Motor_Impulse,                               # lb·s
        "Motor_Impulse_Newton": Motor_Impulse_Newton                  # N·s
    }
