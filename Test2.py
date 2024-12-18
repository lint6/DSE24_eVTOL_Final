import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Clear variables (implicit in Python)

# Inputs from user
indx = int(input("Is thrust (1) or shaft power (2) known? "))

if indx == 1:
    input1 = [
        float(input("Propeller Diameter (inches): ")),
        float(input("Propeller RPM: ")),
        float(input("Propeller forward velocity (m/s): ")),
        float(input("Thrust (N): ")),
        float(input("Air Density (kg/m^3): ")),
        int(input("Number Of Blades: ")),
        float(input("Airfoil C_l: ")),
        float(input("Airfoil C_d: ")),
        float(input("Angle of Attack (AoA): ")),
        int(input("Number of blade elements: ")),
        float(input("Hub Radius: "))
    ]
else:
    input1 = [
        float(input("Propeller Diameter (inches): ")),
        float(input("Propeller RPM: ")),
        float(input("Propeller forward velocity (m/s): ")),
        float(input("Shaft Power (W): ")),
        float(input("Air Density (kg/m^3): ")),
        int(input("Number Of Blades: ")),
        float(input("Airfoil C_l: ")),
        float(input("Airfoil C_d: ")),
        float(input("Angle of Attack (AoA): ")),
        int(input("Number of blade elements: ")),
        float(input("Hub Radius: "))
    ]

# Define inputs
diameter_inch, prop_RPM, velocity, thrust_or_power, density, blades, cl, cd, AoA, elements, hub_radius = input1

# Derived parameters
diameter_m = diameter_inch * 0.0254
prop_ang_velocity = prop_RPM * 0.10472
prop_radius = diameter_m / 2
prop_area = np.pi * prop_radius**2
lamda = velocity / (prop_ang_velocity * prop_radius)
advance_ratio = lamda * np.pi
epsilon = cd / cl
dr = prop_radius / elements

zeta = 0
zeta_new = 1
zeta_difference = zeta_new - zeta

if indx == 1:
    TC = 2 * thrust_or_power / (density * velocity**2 * np.pi * prop_radius**2)
else:
    PC = 2 * thrust_or_power / (density * velocity**3 * np.pi * prop_radius**2)

# Begin iteration loop
while abs(zeta_difference) > 0.1:
    zeta = zeta_new
    tan_phi_tip = lamda * (1 + zeta / 2)
    phi_tip = np.degrees(np.arctan(tan_phi_tip))

    # Variables at all blade sections
    rR = np.linspace(hub_radius, 1, elements)
    X = rR / lamda
    phi = np.degrees(np.arctan(np.tan(np.radians(phi_tip)) / rR))
    F = (2 / np.pi) * np.arccos(np.exp(-0.5 * blades * (1 - rR) / np.sin(np.radians(phi_tip))))
    G = F * X * np.cos(np.radians(phi)) * np.sin(np.radians(phi))

    # Aerodynamic parameters
    Wc = (4 * np.pi * lamda * G * velocity * prop_radius * zeta) / (cl * blades)
    W = velocity * (1 + 0.5 * zeta * np.cos(np.radians(phi))**2 * (1 - epsilon * np.tan(np.radians(phi))))
    c = Wc / W
    beta = AoA + phi

    # Initialize arrays
    dT = np.zeros(elements)
    dQ = np.zeros(elements)

    # Corrected Blade Element Calculations
    for i in range(elements):
        term1 = 1 - epsilon * np.tan(np.radians(phi[i]))
        term2 = 1 + epsilon / np.tan(np.radians(phi[i]))
        A = 0.5 * zeta_new * np.cos(np.radians(phi[i]))**2 * term1
        A_prime = 0.5 * zeta_new * np.cos(np.radians(phi[i])) * np.sin(np.radians(phi[i])) * term2 / X[i]

    # Calculate inflow velocity and chord
    W = velocity * (1 + A) / np.sin(np.radians(phi[i]))
    c[i] = Wc[i] / W

    # Thrust and torque differentials
    dL = density * W**2 * cl * c[i] * dr
    dT[i] = dL * np.cos(np.radians(phi[i])) * term1
    dQ[i] = 2 * np.pi * rR[i] * prop_radius * density * W**2 * A_prime * F[i] * dr


    # Update zeta
    if indx == 1:
        I1 = np.trapz(dT, rR)
        I2 = np.trapz(dQ * lamda * (1 + epsilon / np.tan(np.radians(phi))) * np.sin(np.radians(phi)) * np.cos(np.radians(phi)), rR)
        d = (I1 / (2 * I2))**2 - (TC / I2)
        zeta_new = (I1 / (2 * I2)) - np.sqrt(d)
    else:
        J1 = np.trapz(dJ1, rR)
        J2 = np.trapz(dJ1 * lamda * (1 - epsilon * np.tan(np.radians(phi))) * np.cos(np.radians(phi))**2, rR)
        d = (J1 / (2 * J2))**2 + (PC / J2)
        zeta_new = (-J1 / (2 * J2)) + np.sqrt(d)

    zeta_difference = zeta - zeta_new

# Calculate final performance parameters
if indx == 1:
    PC = I1 * zeta_new + I2 * zeta_new**2
    P = 0.5 * PC * density * velocity**3 * np.pi * prop_radius**2  # Shaft Power in W
    CT = thrust_or_power / (density * (prop_RPM / 60)**2 * diameter_m**4)
    CP = P / (density * (prop_RPM / 60)**3 * diameter_m**5)
    Propeller_Efficiency = advance_ratio * CT / CP
else:
    TC = I1 * zeta_new - I2 * zeta_new**2
    T = 0.5 * TC * density * velocity**2 * np.pi * prop_radius**2  # Thrust in N
    CT = T / (density * (prop_RPM / 60)**2 * diameter_m**4)
    CP = thrust_or_power / (density * (prop_RPM / 60)**3 * diameter_m**5)
    Propeller_Efficiency = advance_ratio * CT / CP

# Display results
print(f"Propeller Efficiency: {Propeller_Efficiency:.4f}")

# Plot chord and twist distribution
plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(rR, beta, label="Twist distribution (degrees)")
plt.ylabel("Twist distribution (degrees)")
plt.xlabel("r/R")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(rR, c, label="Chord distribution (c/R)")
plt.ylabel("Chord distribution (c/R)")
plt.xlabel("r/R")
plt.grid(True)
plt.legend()

# Plot Reynolds number distribution
plt.figure(2)
Re = density * (rR * prop_radius * prop_ang_velocity) * c / 1.81e-5
plt.plot(rR, Re, label="Reynolds number")
plt.axhline(y=100000, color='m', linestyle='--', label="Re = 100,000")
plt.xlabel("r/R")
plt.ylabel("Reynolds number")
plt.grid(True)
plt.legend()

# Plot radial thrust and torque distribution
plt.figure(3)
plt.subplot(2, 1, 1)
plt.plot(rR, dT, label="dT (N)")
plt.ylabel("Thrust (N)")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(rR, dQ, label="dQ (Nm)")
plt.ylabel("Torque (Nm)")
plt.xlabel("r/R")
plt.grid(True)
plt.legend()

plt.show()
