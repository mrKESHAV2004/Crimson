import numpy as np

# Constants
GRAVITY_CONSTANT = 32.2           # ft/s², standard gravity
THROAT_AREA_FACTOR = 1.274        # dimensionless, area-to-diameter conversion factor

def load_pepc_csv(filepath):
    """
    Load PEPC data from CSV file. Assumes 5 columns:
    [0] PEPC (unitless), [2] Expansion Ratio (unitless), [4] Thrust Coefficient (unitless)
    """
    data = np.genfromtxt(filepath, delimiter=',', skip_header=1)
    pepc_column = data[:, 0]               # unitless
    expansion_ratio_column = data[:, 2]    # unitless
    thrust_coeff_column = data[:, 4]       # unitless
    pepc_index_map = {val: idx for idx, val in enumerate(pepc_column)}
    return pepc_column, expansion_ratio_column, thrust_coeff_column, pepc_index_map

def motor_ballistic_performance_numpy(
    Propellant_Weight,      # lbs
    Burn_Time,              # seconds
    C_Star,                 # ft/s (characteristic velocity)
    Chamber_Pressure,       # psi
    Exit_Pressure,          # psia
    filepath='PEPC.csv'     # path to CSV table
):
    # Load data
    pepc_column, expansion_column, thrust_column, pepc_index_map = load_pepc_csv(filepath)

    # Core calculations
    Propellant_Weight_Flow = Propellant_Weight / Burn_Time                      # lb/s
    Throat_Area = (Propellant_Weight_Flow * C_Star) / (Chamber_Pressure * GRAVITY_CONSTANT)  # in²
    Throat_Diameter = np.sqrt(THROAT_AREA_FACTOR * Throat_Area)                # inches
    PEPC = Exit_Pressure / Chamber_Pressure                                    # unitless

    # Closest PEPC search via vectorized difference
    differences = np.abs(pepc_column - PEPC)
    min_diff = np.min(differences)

    candidate_plus = PEPC + min_diff
    candidate_minus = PEPC - min_diff

    # Choose corrected PEPC based on available match
    if candidate_plus in pepc_index_map:
        New_PEPC = candidate_plus
    elif candidate_minus in pepc_index_map:
        New_PEPC = candidate_minus
    else:
        New_PEPC = pepc_column[np.argmin(differences)]

    D = pepc_index_map.get(New_PEPC, np.argmin(np.abs(pepc_column - New_PEPC)))

    Expansion_Ratio = expansion_column[D]              # unitless
    Thrust_Coefficient = thrust_column[D]              # unitless
    Exit_Pressure_Corrected = New_PEPC * Chamber_Pressure      # psia
    Thrust = Chamber_Pressure * Throat_Area * Thrust_Coefficient  # lbs
    Exit_Diameter = Throat_Diameter * np.sqrt(Expansion_Ratio)    # inches

    return {
        "Propellant_Weight": Propellant_Weight,                        # lbs
        "Burn_Time": Burn_Time,                                        # s
        "C_Star": C_Star,                                              # ft/s
        "Chamber_Pressure": Chamber_Pressure,                          # psi
        "Exit_Pressure": Exit_Pressure_Corrected,                      # psia
        "Propellant_Weight_Flow": Propellant_Weight_Flow,              # lb/s
        "Throat_Area": Throat_Area,                                    # in²
        "Throat_Diameter": Throat_Diameter,                            # inches
        "PEPC": PEPC,                                                  # unitless
        "Corrected_PEPC": New_PEPC,                                    # unitless
        "Expansion_Ratio": Expansion_Ratio,                            # unitless
        "Thrust_Coefficient": Thrust_Coefficient,                      # unitless
        "Thrust": Thrust,                                              # lbs
        "Exit_Diameter": Exit_Diameter                                 # inches
    }
