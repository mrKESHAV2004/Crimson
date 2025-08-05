import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# === Constants ===
GRAVITY = 32.2
C_STAR_REF = 500

# === Initial Parameters ===
initial_mass = 5.0
initial_pressure = 100.0
initial_temperature = 3000.0
rho = 0.06
bore_d = 1.0
a = 0.05
n = 0.3
At0 = 0.5
Vc = 100.0
ce0 = 0.95
T_crit = 6000.0
T_decay_rate = 0.01
efficiency_decay = 0.05

# === Supporting Functions ===
def throat_area(t):
    return At0 + 0.005 * t

def burn_rate(P, a, n):
    return a * (P ** n)

def burn_area(bore_d, web, grain_type="multi"):
    if grain_type == "multi":
        return np.pi * bore_d * web * (1 + 0.05 * web)
    elif grain_type == "star":
        return np.pi * bore_d * web * 1.25
    return np.pi * bore_d * web

def temperature_decay(t, T0):
    return max(T0 - T_decay_rate * t * T0, 1000)

def combustion_efficiency(t, ce0):
    return max(ce0 - efficiency_decay * t, 0.5)

def specific_impulse(c_star, ce, T):
    return (ce * c_star) / GRAVITY * (T / T_crit)

def chamber_ode(t, y, params):
    m_p, P, T = y
    rho, bore_d, a, n, Vc, ce0 = params

    r = burn_rate(P, a, n)
    web = r * t
    Ab = burn_area(bore_d, web)
    At = throat_area(t)
    ce = combustion_efficiency(t, ce0)
    T_new = temperature_decay(t, T)

    mdot = rho * Ab * r
    C_STAR = C_STAR_REF * (T_new / T_crit)

    dPdt = (GRAVITY * mdot * C_STAR * ce) / Vc - (P * At / Vc)
    dmpdt = -mdot
    dTdt = -T_decay_rate * T

    return [dmpdt, dPdt, dTdt]

# === Integration ===
params = (rho, bore_d, a, n, Vc, ce0)
y0 = [initial_mass, initial_pressure, initial_temperature]
t_eval = np.linspace(0, 2, 500)

sol = solve_ivp(
    lambda t, y: chamber_ode(t, y, params),
    [0, 2],
    y0,
    t_eval=t_eval,
    rtol=1e-8,
    atol=1e-8
)

# === Extract Results ===
time = sol.t
mass, pressure, temperature = sol.y
throat_areas = np.array([throat_area(t) for t in time])
efficiencies = np.array([combustion_efficiency(t, ce0) for t in time])
isp_values = specific_impulse(C_STAR_REF, efficiencies, temperature)

# === Plotting in 2x2 Grid ===
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), sharex=True)

# Top Left
axs[0, 0].plot(time, pressure, color='red', label='Chamber Pressure')
axs[0, 0].set_ylabel("Pressure (psi)")
axs[0, 0].set_title("Chamber Pressure vs Time")
axs[0, 0].grid(True)
axs[0, 0].legend()

# Top Right
axs[0, 1].plot(time, mass, color='blue', label='Propellant Mass')
axs[0, 1].set_ylabel("Mass (lb)")
axs[0, 1].set_title("Propellant Mass vs Time")
axs[0, 1].grid(True)
axs[0, 1].legend()

# Bottom Left
axs[1, 0].plot(time, throat_areas, color='green', label='Throat Area')
axs[1, 0].set_ylabel("Area (in²)")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_title("Throat Area vs Time")
axs[1, 0].grid(True)
axs[1, 0].legend()

# Bottom Right
axs[1, 1].plot(time, isp_values, color='purple', label='Delivered ISP')
axs[1, 1].set_ylabel("ISP (s)")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_title("Delivered ISP vs Time")
axs[1, 1].grid(True)
axs[1, 1].legend()

plt.suptitle("Advanced Internal Ballistics Simulation")
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave room for suptitle
plt.show()
