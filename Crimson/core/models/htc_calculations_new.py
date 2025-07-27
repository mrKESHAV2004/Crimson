# imperial

ATM_PRESSURE = 14.7         # psi, atmospheric pressure
PSI_TO_PSF = 144            # psi to psf conversion
GAS_CONSTANT = 1545         # universal gas constant (ft·lb/(lb-mol·°R))
DITTUS_BOELTER_COEFF = 0.023
INCHES_TO_FEET = 12
SECONDS_PER_HOUR = 3600


def thermal_boundary_conditions(
        location_diameter,           # inches
        gas_velocity,                # ft/sec
        avg_chamber_pressure,        # psi or lbf/in²
        flame_temp,                  # (°R) Rankine
        gas_molecular_wt,            # lbmol
        prandtl_number,              # Pr
        gas_conductivity,            # Btu/Hr-ft-R
        gas_viscosity                # Lb/ft-sec

):
    """
    Calculate thermal boundary conditions including gas density, Reynolds number, and heat transfer coefficient.
    Inputs:
        location_diameter: Diameter at the location (inches)
        gas_velocity: Velocity of the gas (ft/sec)
        avg_chamber_pressure: Average chamber pressure (psi or lbf/in²)
        flame_temp: Flame temperature (°R) Rankine
        gas_molecular_wt: Molecular weight of the gas (lbmol)
        prandtl_number: Prandtl number (Pr)
        gas_conductivity: Thermal conductivity of the gas (Btu/Hr-ft-R)
        gas_viscosity: Viscosity of the gas (Lb/ft-sec)
    Returns:
        Dictionary with gas density, Reynolds number, and heat transfer coefficient
    """
    gas_density = ((avg_chamber_pressure + ATM_PRESSURE) * PSI_TO_PSF) / (flame_temp * (GAS_CONSTANT / gas_molecular_wt))
    reynolds_number = (gas_density * gas_velocity * (location_diameter / INCHES_TO_FEET)) / gas_viscosity
    heat_transfer_coeff = (gas_conductivity / (location_diameter / INCHES_TO_FEET)) * DITTUS_BOELTER_COEFF * (reynolds_number ** 0.8) * (prandtl_number ** 0.4) / SECONDS_PER_HOUR

    return {
        "Gas Density (lbm/ft³)": gas_density,
        "Reynolds Number (Re)": reynolds_number,
        "Heat Transfer Coefficient (Btu/sec-ft²-°R)": heat_transfer_coeff
    }
