import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz

# Function to get user input
def get_user_input():
    thrust_or_power = input("Is thrust or shaft power known? (Thrust/Shaft Power): ").strip()
    if thrust_or_power.lower() == "thrust":
        input_labels = ["Propeller Diameter (inches)", "Propeller RPM", "Propeller forward velocity (m/s)", 
                        "Thrust (N)", "Air Density (kg/m^3)", "Number Of Blades", "Airfoil C_l", "Airfoil C_d", 
                        "Angle of Attack (AoA)", "Number of blade elements", "Hub Radius"]
    else:
        input_labels = ["Propeller Diameter (inches)", "Propeller RPM", "Propeller forward velocity (m/s)", 
                        "Shaft Power (W)", "Air Density (kg/m^3)", "Number Of Blades", "Airfoil C_l", "Airfoil C_d", 
                        "Angle of Attack (AoA)", "Number of blade elements", "Hub Radius"]
    inputs = [float(input(f"Enter {label}: ")) for label in input_labels]

    min_reynolds_mode = input("Minimum Re. number mode? (Yes/No): ").strip().lower() == "yes"
    min_reynolds_number = float(input("Enter Minimum Reynolds number: ")) if min_reynolds_mode else None

    return thrust_or_power.lower(), inputs, min_reynolds_number

# Main function
def main():
    thrust_or_power, inputs, min_reynolds_number = get_user_input()

    # Extract input variables
    diameter_inch, prop_RPM, velocity, power_or_thrust, density, num_blades, airfoil_cl, airfoil_cd, AoA, num_blade_elements, hub_radius = inputs

    # Calculated parameters
    diameter_m = diameter_inch * 0.0254
    prop_ang_velocity = prop_RPM * 0.10472
    prop_radius = diameter_m / 2
    lamda = velocity / (prop_ang_velocity * prop_radius)
    advance_ratio = lamda * np.pi
    epsilon = airfoil_cd / airfoil_cl
    dr = prop_radius / num_blade_elements
    
    # Initial guess
    zeta = 0
    zeta_new = 1
    while abs(zeta_new - zeta) > 0.1:
        zeta = zeta_new
        tan_phi_tip = lamda * (1 + zeta / 2)
        phi_tip = np.degrees(np.arctan(tan_phi_tip))

        rR, phi, F, G, Wc, W, c, beta = ([] for _ in range(8))
        dT, dQ, dI1, dI2, dJ1, dJ2 = ([] for _ in range(6))

        for i in range(1, num_blade_elements + 1):
            rR_val = i / num_blade_elements
            phi_val = np.degrees(np.arctan(np.tan(np.radians(phi_tip)) / rR_val))
            f_val = (num_blades / 2) * ((1 - rR_val) / np.sin(np.radians(phi_tip)))
            F_val = (2 / np.pi) * np.degrees(np.arccos(np.exp(-f_val)))
            G_val = F_val * rR_val / lamda * np.cos(np.radians(phi_val)) * np.sin(np.radians(phi_val))
            Wc_val = (4 * np.pi * lamda * G_val * velocity * prop_radius * zeta) / (airfoil_cl * num_blades)
            term1 = 1 - epsilon * np.tan(np.radians(phi_val))
            term2 = 1 + epsilon / np.tan(np.radians(phi_val))

            A = 0.5 * zeta * np.cos(np.radians(phi_val))**2 * term1
            A_prime = 0.5 * zeta * np.cos(np.radians(phi_val)) * np.sin(np.radians(phi_val)) * term2 / rR_val

            W_val = velocity * (1 + A) / np.sin(np.radians(phi_val))
            c_val = Wc_val / W_val
            beta_val = AoA + phi_val

            dI1_val = 4 * rR_val * G_val * term1
            dI2_val = lamda * dI1_val * term2 * np.sin(np.radians(phi_val)) * np.cos(np.radians(phi_val)) / (2 * rR_val)
            dJ1_val = 4 * rR_val * G_val * term2
            dJ2_val = 0.5 * dJ1_val * term1 * np.cos(np.radians(phi_val))**2
            dT_val = density * W_val * (2 * np.pi * velocity**2 * zeta * G_val / prop_ang_velocity) * dr
            dQ_val = 2 * np.pi * rR_val * prop_radius * density * velocity * (1 + A) * (2 * prop_ang_velocity * rR_val * prop_radius * A_prime * F_val) * dr

            rR.append(rR_val)
            phi.append(phi_val)
            F.append(F_val)
            G.append(G_val)
            Wc.append(Wc_val)
            W.append(W_val)
            c.append(c_val)
            beta.append(beta_val)
            dI1.append(dI1_val)
            dI2.append(dI2_val)
            dJ1.append(dJ1_val)
            dJ2.append(dJ2_val)
            dT.append(dT_val)
            dQ.append(dQ_val)

        I1, I2 = trapz(dI1, rR), trapz(dI2, rR)
        J1, J2 = trapz(dJ1, rR), trapz(dJ2, rR)
        
        if thrust_or_power == "thrust":
            d = (I1 / (2 * I2))**2 - (2 * power_or_thrust / (density * velocity**2 * np.pi * prop_radius**2)) / I2
            zeta_new = (I1 / (2 * I2)) - np.sqrt(d)
        else:
            d = (J1 / (2 * J2))**2 + (2 * power_or_thrust / (density * velocity**3 * np.pi * prop_radius**2)) / J2
            zeta_new = (-J1 / (2 * J2)) + np.sqrt(d)

    # Display results and plots
    print(f"Final Zeta: {zeta_new:.4f}")
    plt.figure()
    plt.plot(rR, c, label="Chord Distribution (c/R)")
    plt.plot(rR, beta, label="Twist Distribution (degrees)")
    plt.legend()
    plt.xlabel("r/R")
    plt.show()

if __name__ == "__main__":
    main()
