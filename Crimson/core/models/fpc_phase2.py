import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
GRAVITY = 9.806650
RHO0 = 1.225  # kg/m³ at sea level
PI = np.pi

class Phase2RocketSimulator:
    def __init__(self, md, mp, D, burn_time, thrust_func, dt=0.01):
        self.md = md                          # Dead mass (kg)
        self.mp = mp                          # Propellant mass (kg)
        self.D = D                            # Diameter (m)
        self.A = PI * (D ** 2) / 4            # Cross-sectional area (m²)
        self.burn_time = burn_time            # Burn duration (s)
        self.F = thrust_func                  # Thrust function F(t)
        self.dt = dt                          # Time step for evaluation

    def g(self, z):
        return GRAVITY - 0.000030 * z         # Gravity as a function of altitude

    def rho(self, z):
        return RHO0 * np.exp(-z / 8500)       # Atmospheric density

    def Cd(self, z):
        return 0.75 + 0.01 * (z / 1000)        # Drag coefficient

    def mass(self, t):
        if t <= self.burn_time:
            return self.md + self.mp * (1 - t / self.burn_time)
        return self.md

    def acceleration(self, t, y):
        z, v = y
        m = self.mass(t)
        F = self.F(t) if t <= self.burn_time else 0.0
        Cd = self.Cd(z)
        rho = self.rho(z)
        g = self.g(z)
        drag = 0.5 * Cd * rho * self.A * v ** 2 / m
        drag *= np.sign(v)
        return [v, (F / m) - g - drag]

    def simulate(self):
        y0 = [0, 0]  # Initial conditions: [altitude, velocity]

        # --- Burn Phase ---
        sol_burn = solve_ivp(
            self.acceleration,
            [0, self.burn_time],
            y0,
            t_eval=np.arange(0, self.burn_time, self.dt),
            rtol=1e-8,
            atol=1e-8
        )

        z_burn, v_burn = sol_burn.y[0][-1], sol_burn.y[1][-1]
        t_burnout = sol_burn.t[-1]

        # --- Coast Phase ---
        def stop_at_apogee(t, y): return y[1]
        stop_at_apogee.terminal = True
        stop_at_apogee.direction = -1

        sol_coast = solve_ivp(
            self.acceleration,
            [t_burnout, t_burnout + 30],
            [z_burn, v_burn],
            events=stop_at_apogee,
            rtol=1e-8,
            atol=1e-8
        )

        z_peak = sol_coast.y[0][-1]
        t_apogee = sol_coast.t[-1]

        return {
            "Burnout Altitude (m)": z_burn,
            "Burnout Velocity (m/s)": v_burn,
            "Time to Burnout (s)": t_burnout,
            "Peak Altitude (m)": z_peak,
            "Time to Apogee (s)": t_apogee,
            "Burn Profile": sol_burn,
            "Coast Profile": sol_coast
        }

# Example thrust function — linearly decreasing thrust
def linear_thrust(t):
    F0 = 50.0  # N
    return F0 * (1 - 0.2 * t) if t <= 2.0 else 0.0

# Example usage
if __name__ == "__main__":
    sim = Phase2RocketSimulator(
        md=0.8,
        mp=0.2,
        D=0.05,
        burn_time=2.0,
        thrust_func=linear_thrust
    )

    results = sim.simulate()

    # Print results
    print("\nPhase 2 Rocket Simulation Results:")
    for key, value in results.items():
        if not isinstance(value, dict):
            print(f"{key}: {value:.6f}" if isinstance(value, float) else f"{key}: {value}")

    # Plot Altitude vs Time
    plt.plot(results['Burn Profile'].t, results['Burn Profile'].y[0], label="Burn Phase Altitude")
    plt.plot(results['Coast Profile'].t, results['Coast Profile'].y[0], label="Coast Phase Altitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Rocket Altitude Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
