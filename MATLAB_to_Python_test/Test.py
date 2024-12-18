import numpy as np
import matplotlib.pyplot as plt

# Code converted from MATLAB file provided by Stephen D. Prior and Daniel Newman-Sanders

# CLEAR ALL VARIABLES

# TAKE INPUTS FROM USER
thrust_or_power = input("Is thrust or shaft power known? (Thrust/Shaft Power): ").strip().lower()
if thrust_or_power == 'thrust':
    inputs = [
        "Propeller Diameter (inches)", "Propeller RPM", "Propeller forward velocity (m/s)",
        "Thrust (N)", "Air Density (kg/m^3)", "Number Of Blades", "Airfoil C_l",
        "Airfoil C_d", "Angle of Attack (AoA)", "Number of blade elements", "Hub Radius"
    ]
else:
    inputs = [
        "Propeller Diameter (inches)", "Propeller RPM", "Propeller forward velocity (m/s)",
        "Shaft Power (W)", "Air Density (kg/m^3)", "Number Of Blades", "Airfoil C_l",
        "Airfoil C_d", "Angle of Attack (AoA)", "Number of blade elements", "Hub Radius"
    ]

input_values = [float(input(f"{prompt}: ")) for prompt in inputs]

# DEFINE INPUTS
diameter_inch, prop_RPM, velocity, primary_input, density, num_blades, cl, cd, AoA, num_elements, hub_radius = input_values

diameter_m = diameter_inch * 0.0254
prop_ang_velocity = prop_RPM * 0.10472
prop_radius = diameter_m / 2
prop_area = np.pi * prop_radius ** 2
lamda = velocity / (prop_ang_velocity * prop_radius)
advance_ratio = lamda * np.pi
epsilon = cd / cl
dr = prop_radius / num_elements

if thrust_or_power == 'thrust':
    TC = 2 * primary_input / (density * velocity**2 * np.pi * prop_radius**2)
else:
    PC = 2 * primary_input / (density * velocity**3 * np.pi * prop_radius**2)

zeta = 0
zeta_new = 1
while abs(zeta_new - zeta) > 0.1:
    zeta = zeta_new
    tan_phi_tip = lamda * (1 + (zeta / 2))
    phi_tip = np.degrees(np.arctan(tan_phi_tip))

    rR = np.linspace(hub_radius, 1, num_elements)
    phi = np.degrees(np.arctan(np.tan(np.radians(phi_tip)) / rR))
    F = (2 / np.pi) * np.arccos(np.exp(-num_blades * (1 - rR) / (2 * np.sin(np.radians(phi_tip)))))
    G = F * rR / lamda * np.cos(np.radians(phi)) * np.sin(np.radians(phi))
    Wc = (4 * np.pi * lamda * G * velocity * prop_radius * zeta) / (cl * num_blades)

    term1 = 1 - epsilon * np.tan(np.radians(phi))
    term2 = 1 + epsilon / np.tan(np.radians(phi))

    A = 0.5 * zeta * np.cos(np.radians(phi))**2 * term1
    W = velocity * (1 + A) / np.sin(np.radians(phi))
    c = Wc / W
    beta = AoA + phi

    dI1 = 4 * rR * G * term1
    dI2 = lamda * dI1 * term2 * np.sin(np.radians(phi)) * np.cos(np.radians(phi)) / (2 * rR)

    I1 = np.trapz(dI1, rR)
    I2 = np.trapz(dI2, rR)

    if thrust_or_power == 'thrust':
        d = (I1 / (2 * I2))**2 - (TC / I2)
        zeta_new = (I1 / (2 * I2)) - np.sqrt(d)
    else:
        d = (I1 / (2 * I2))**2 + (PC / I2)
        zeta_new = (-I1 / (2 * I2)) + np.sqrt(d)

# Final Calculations and Plotting
if thrust_or_power == 'thrust':
    PC = I1 * zeta_new + I2 * zeta_new**2
    P = 0.5 * PC * density * velocity**3 * np.pi * prop_radius**2
    CT = primary_input / (density * (prop_RPM / 60)**2 * diameter_m**4)
    CP = P / (density * (prop_RPM / 60)**3 * diameter_m**5)
else:
    TC = I1 * zeta_new - I2 * zeta_new**2
    T = 0.5 * TC * density * velocity**2 * np.pi * prop_radius**2
    CT = T / (density * (prop_RPM / 60)**2 * diameter_m**4)
    CP = primary_input / (density * (prop_RPM / 60)**3 * diameter_m**5)

Propeller_Efficiency = advance_ratio * CT / CP

print(f"Propeller Efficiency: {Propeller_Efficiency:.2f}")

plt.figure()
plt.plot(rR, c, label='Chord Distribution')
plt.plot(rR, beta, label='Twist Distribution')
plt.xlabel('r/R')
plt.ylabel('Distribution')
plt.legend()
plt.show()
