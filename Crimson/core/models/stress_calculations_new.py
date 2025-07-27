import math

def chamber_failure(meop, chamber_diameter, tensile_strength_ch):
    """
    Calculate minimum wall thickness for chamber failure.
    Inputs:
        meop: Maximum expected operating pressure (psi)
        chamber_diameter: Diameter of the chamber (inch)
        tensile_strength_ch: Tensile strength of chamber material (psi)
    Returns:
        min_wall_thickness_ch: Minimum wall thickness (inch)
    """
    min_wall_thickness_ch = (meop * chamber_diameter) / (2 * tensile_strength_ch)
    return {
        "Min Wall Thickness Chamber (inch)": min_wall_thickness_ch
    }

def nozzle_failure(meop, nozzle_radius, throat_radius, k, tensile_strength_nz):
    """
    Calculate minimum wall thickness for nozzle failure.
    Inputs:
        meop: Maximum expected operating pressure (psi)
        nozzle_radius: Radius of the nozzle (inch)
        throat_radius: Radius of the throat (inch)
        k: Stress concentration factor
        tensile_strength_nz: Tensile strength of nozzle material (psi)
    Returns:
        min_wall_thickness_nz: Minimum wall thickness (inch)
    """
    stress_concentration_ratio_nz = nozzle_radius / throat_radius
    min_wall_thickness_nz = math.sqrt((k * meop * (nozzle_radius ** 2)) / tensile_strength_nz)
    return {
        "Stress Concentration Ratio Nozzle": stress_concentration_ratio_nz,
        "Min Wall Thickness Nozzle (inch)": min_wall_thickness_nz
    }

def bulkhead_failure(meop, bulkhead_radius, delay_charge_radius, k, tensile_strength_bh):
    """
    Calculate minimum wall thickness for bulkhead failure.
    Inputs:
        meop: Maximum expected operating pressure (psi)
        bulkhead_radius: Radius of the bulkhead (inch)
        delay_charge_radius: Radius of the delay charge (inch)
        k: Stress concentration factor
        tensile_strength_bh: Tensile strength of bulkhead material (psi)
    Returns:
        min_wall_thickness_bh: Minimum wall thickness (inch)
    """
    stress_concentration_ratio_bh = bulkhead_radius / delay_charge_radius
    min_wall_thickness_bh = math.sqrt((k * meop * (bulkhead_radius ** 2)) / tensile_strength_bh)
    return {
        "Stress Concentration Ratio Bulkhead": stress_concentration_ratio_bh,
        "Min Wall Thickness Bulkhead (inch)": min_wall_thickness_bh
    }

def retaining_pins(meop, bulkhead_radius, number_of_pins, tensile_strength_rp):
    """
    Calculate minimum retaining pin diameter.
    Inputs:
        meop: Maximum expected operating pressure (psi)
        bulkhead_radius: Radius of the bulkhead (inch)
        number_of_pins: Number of retaining pins
        tensile_strength_rp: Tensile strength of retaining pin material (psi)
    Returns:
        min_retaining_pin_diameter: Minimum diameter of retaining pin (inch)
        bulkhead_ejection_force: Force on bulkhead (lbs)
        retaining_pin_load: Load on each retaining pin (lbs)
    """
    bulkhead_ejection_force = meop * 3.13999999999942 * (bulkhead_radius ** 3)
    retaining_pin_load = bulkhead_ejection_force / number_of_pins
    min_retaining_pin_diameter = 2 * math.sqrt(retaining_pin_load / (3.13999999999942 * tensile_strength_rp))
    return {
        "Bulkhead Ejection Force (lbs)": bulkhead_ejection_force,
        "Retaining Pin Load (lbs)": retaining_pin_load,
        "Min Retaining Pin Diameter (inch)": min_retaining_pin_diameter
    }

def retaining_pin_hole_location(bulkhead_ejection_force, chamber_wall_thickness, chamber_diameter, number_of_pins, retaining_pin_diameter, tensile_strength_ch):
    """
    Calculate safety factor for pin holes.
    Inputs:
        bulkhead_ejection_force: Force on bulkhead (lbs)
        chamber_wall_thickness: Thickness of chamber wall (inch)
        chamber_diameter: Diameter of chamber (inch)
        number_of_pins: Number of retaining pins
        retaining_pin_diameter: Diameter of retaining pin (inch)
        tensile_strength_ch: Tensile strength of chamber material (psi)
    Returns:
        safety_factor_pinholes: Safety factor for pin holes
        max_axial_chamber_stress: Maximum axial chamber stress (psi)
        avg_axial_chamber_stress: Average axial chamber stress (psi)
        stress_concentration_factor: Stress concentration factor 
        d_l_ratio: Diameter to length ratio
    """
    d_l_ratio = retaining_pin_diameter / (6.13999999999942 * (chamber_diameter / 2) / retaining_pin_diameter)
    stress_concentration_factor = 2.380
    avg_axial_chamber_stress = bulkhead_ejection_force / (chamber_wall_thickness * ((6.27999999999884 * (chamber_diameter / 2)) - (number_of_pins * retaining_pin_diameter)))
    max_axial_chamber_stress = stress_concentration_factor * avg_axial_chamber_stress 
    safety_factor_pinholes = tensile_strength_ch / max_axial_chamber_stress
    return {
        "D/L Ratio": d_l_ratio,
        "Stress Concentration Factor": stress_concentration_factor,
        "Average Axial Chamber Stress": avg_axial_chamber_stress,
        "Max Axial Chamber Stress": max_axial_chamber_stress,
        "Safety Factor Pinholes": safety_factor_pinholes
    }
