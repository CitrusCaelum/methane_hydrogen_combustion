import cantera as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# Parameters
# ---------------------------------------

temperature = 300
pressure = ct.one_atm

h2_percentages = [0, 10, 20, 30, 40]

phis = np.arange(0.6, 1.5, 0.1)

results = []

# ---------------------------------------
# Main Simulation Loop
# ---------------------------------------

for h2 in h2_percentages:

    ch4 = 100 - h2

    fuel = f"CH4:{ch4}, H2:{h2}"

    for phi in phis:

        gas = ct.Solution("gri30.yaml")

        gas.set_equivalence_ratio(
            phi,
            fuel,
            "O2:1, N2:3.76"
        )

        gas.TP = temperature, pressure

        # --------------------------------
        # Adiabatic Flame Temperature
        # --------------------------------

        gas.equilibrate("HP")

        flame_temp = gas.T

        # --------------------------------
        # Flame Speed
        # --------------------------------

        gas = ct.Solution("gri30.yaml")

        gas.set_equivalence_ratio(
            phi,
            fuel,
            "O2:1, N2:3.76"
        )

        gas.TP = temperature, pressure

        flame = ct.FreeFlame(gas, width=0.03)

        flame.solve(loglevel=0, auto=True)

        flame_speed = flame.velocity[0]

        # Store results
        results.append([
            h2,
            phi,
            flame_speed,
            flame_temp
        ])

        print(
            f"H2={h2}% | "
            f"phi={phi:.2f} | "
            f"SL={flame_speed:.3f} m/s | "
            f"T={flame_temp:.1f} K"
        )

# ---------------------------------------
# Save Results
# ---------------------------------------

df = pd.DataFrame(
    results,
    columns=[
        "H2 Percentage",
        "Equivalence Ratio",
        "Flame Speed (m/s)",
        "Flame Temperature (K)"
    ]
)

df.to_csv("full_results.csv", index=False)

print(df)

# ---------------------------------------
# Plot Flame Speed
# ---------------------------------------

plt.figure(figsize=(8,6))

for h2 in h2_percentages:

    subset = df[df["H2 Percentage"] == h2]

    plt.plot(
        subset["Equivalence Ratio"],
        subset["Flame Speed (m/s)"],
        marker='o',
        label=f"{h2}% H2"
    )

plt.xlabel("Equivalence Ratio (ϕ)")
plt.ylabel("Laminar Flame Speed (m/s)")
plt.title("Flame Speed vs Equivalence Ratio")
plt.legend()
plt.grid(True)

plt.show()

# ---------------------------------------
# Plot Flame Temperature
# ---------------------------------------

plt.figure(figsize=(8,6))

for h2 in h2_percentages:

    subset = df[df["H2 Percentage"] == h2]

    plt.plot(
        subset["Equivalence Ratio"],
        subset["Flame Temperature (K)"],
        marker='s',
        label=f"{h2}% H2"
    )

plt.xlabel("Equivalence Ratio (ϕ)")
plt.ylabel("Adiabatic Flame Temperature (K)")
plt.title("Flame Temperature vs Equivalence Ratio")
plt.legend()
plt.grid(True)

plt.show()