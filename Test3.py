import numpy as np
import matplotlib.pyplot as plt

# Clear variables: implicit in Python

# User Input Section
def get_user_inputs():
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
    return indx, input1

def blade_element_analysis(indx, input1):
    # Define inputs
    diameter_inch, prop_RPM, velocity, thrust_or_power, density, blades, cl, cd, AoA, elements, hub_radius = input1
    
    # Derived parameters
    diameter_m = diameter_inch * 0.0254
    prop_ang_velocity = prop_RPM * 0.10472
    prop_radius = diameter_m / 2
    prop_area = np.pi * prop_radius**2
    lamda = velocity / (prop_ang_velocity * prop_radius)
    epsilon = cd / cl
    dr = prop_radius / elements
    
    # Initialize variables
    zeta = 0
    zeta_new = 1
    zeta_difference = zeta_new - zeta
    
    if indx == 1:
        TC = 2 * thrust_or_power / (density * velocity**2 * prop_area)
    else:
        PC = 2 * thrust_or_power / (density * velocity**3 * prop_area)

    # Iterative Zeta Calculation Loop
    while abs(zeta_difference) > 0.1:
        zeta = zeta_new
        
        # Blade Element Calculations
        rR = np.linspace(hub_radius, 1, elements)
        X = rR / lamda
        phi_tip = np.degrees(np.arctan(lamda * (1 + zeta / 2)))
        phi = np.degrees(np.arctan(np.tan(np.radians(phi_tip)) / rR))
        
        F = (2 / np.pi) * np.arccos(np.exp(-0.5 * blades * (1 - rR) / np.sin(np.radians(phi_tip))))
        G = F * X * np.cos(np.radians(phi)) * np.sin(np.radians(phi))

        # Aerodynamic Calculations
        Wc = (4 * np.pi * lamda * G * velocity * prop_radius * zeta) / (cl * blades)
        W = velocity * (1 + 0.5 * zeta * np.cos(np.radians(phi))**2 * (1 - epsilon * np.tan(np.radians(phi))))
        c = Wc / W
        dT = density * W**2 * cl * c * dr * np.cos(np.radians(phi))
        dQ = 2 * np.pi * rR * prop_radius * density * W**2 * 0.5 * zeta * np.sin(np.radians(phi)) * dr
        
        I1 = np.trapz(dT, rR)
        I2 = np.trapz(dT * lamda * np.sin(np.radians(phi)) * np.cos(np.radians(phi)), rR)
        J1 = np.trapz(dQ, rR)
        J2 = np.trapz(dQ * lamda * np.cos(np.radians(phi))**2, rR)

        # Update zeta
        if indx == 1:
            d = (I1 / (2 * I2))**2 - (TC / I2)
            zeta_new = (I1 / (2 * I2)) - np.sqrt(d)
        else:
            d = (J1 / (2 * J2))**2 + (PC / J2)
            zeta_new = (-J1 / (2 * J2)) + np.sqrt(d)

        zeta_difference = zeta - zeta_new
    
    # Final Calculations
    if indx == 1:
        PC = J1 * zeta_new + J2 * zeta_new**2
        P = 0.5 * PC * density * velocity**3 * prop_area
        CT = thrust_or_power / (density * (prop_RPM / 60)**2 * diameter_m**4)
        CP = P / (density * (prop_RPM / 60)**3 * diameter_m**5)
        Propeller_Efficiency = lamda * CT / CP
    else:
        TC = I1 * zeta_new - I2 * zeta_new**2
        T = 0.5 * TC * density * velocity**2 * prop_area
        CT = T / (density * (prop_RPM / 60)**2 * diameter_m**4)
        CP = thrust_or_power / (density * (prop_RPM / 60)**3 * diameter_m**5)
        Propeller_Efficiency = lamda * CT / CP

    return rR, c, dT, dQ, Propeller_Efficiency

def plot_results(rR, c, dT, dQ, Propeller_Efficiency):
    print(f"Propeller Efficiency: {Propeller_Efficiency:.4f}")

    # Chord and Twist Distribution
    plt.figure(1)
    plt.plot(rR, c, label="Chord Distribution")
    plt.xlabel("r/R")
    plt.ylabel("Chord (c/R)")
    plt.grid(True)
    plt.legend()

    # Radial Thrust and Torque Distribution
    plt.figure(2)
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

if __name__ == "__main__":
    indx, input1 = get_user_inputs()
    rR, c, dT, dQ, Propeller_Efficiency = blade_element_analysis(indx, input1)
    plot_results(rR, c, dT, dQ, Propeller_Efficiency)
