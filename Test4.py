import numpy as np
import matplotlib.pyplot as plt

def get_user_input(prompt, fields):
    print(prompt)
    return {field: float(input(f"Enter {field}: ")) for field in fields}

def calculate_performance(params, thrust_known, min_reynolds_mode, desired_reynolds_number=None):
    # Extract parameters
    diameter_inch = params['Propeller Diameter (inches)']
    velocity = params['Propeller forward velocity (m/s)']
    prop_RPM = params['Propeller RPM']
    density = params['Air Density (kg/m^3)']
    number_of_blades = params['Number Of Blades']
    airfoil_cl = params['Airfoil C_l']
    airfoil_cd = params['Airfoil C_d']
    hub_radius = params['Hub Radius']
    AoA = params['Angle of Attack (AoA)']
    number_blade_elements = int(params['Number of blade elements'])

    if thrust_known:
        thrust = params['Thrust (N)']
    else:
        consumed_power = params['Shaft Power (W)']

    # Derived parameters
    diameter_m = diameter_inch * 0.0254
    prop_ang_velocity = prop_RPM * 0.10472
    prop_radius = diameter_m / 2
    lamda = velocity / (prop_ang_velocity * prop_radius)
    epsilon = airfoil_cd / airfoil_cl
    dr = prop_radius / number_blade_elements
    zeta, zeta_new = 0, 1

    while abs(zeta - zeta_new) > 0.1:
        zeta = zeta_new
        phi_tip = np.degrees(np.arctan(lamda * (1 + zeta / 2)))

        rR, c, beta, dT, dQ = [], [], [], [], []
        for i in range(1, number_blade_elements + 1):
            r = i / number_blade_elements
            phi = np.degrees(np.arctan(np.tan(np.radians(phi_tip)) / r))
            f = (number_of_blades / 2) * ((1 - r) / np.sin(np.radians(phi_tip)))
            F = (2 / np.pi) * np.degrees(np.arccos(np.exp(-f)))
            G = F * r / lamda * np.cos(np.radians(phi)) * np.sin(np.radians(phi))
            Wc = (4 * np.pi * lamda * G * velocity * prop_radius * zeta) / (airfoil_cl * number_of_blades)

            term1 = 1 - epsilon * np.tan(np.radians(phi))
            term2 = 1 + epsilon / np.tan(np.radians(phi))
            A = 0.5 * zeta * np.cos(np.radians(phi)) ** 2 * term1
            W = velocity * (1 + A) / np.sin(np.radians(phi))
            chord = Wc / W

            beta.append(AoA + phi)
            c.append(chord)
            dT.append(density * W ** 2 * G * dr)
            dQ.append(2 * np.pi * r * prop_radius * density * W * dr)
            rR.append(r)

        if thrust_known:
            I1 = np.trapz(dT, rR)
            I2 = np.trapz(dQ, rR)
            zeta_new = (I1 / (2 * I2)) - np.sqrt((I1 / (2 * I2)) ** 2 - params['Thrust (N)'] / I2)
        else:
            J1 = np.trapz(dT, rR)
            J2 = np.trapz(dQ, rR)
            zeta_new = (-J1 / (2 * J2)) + np.sqrt((J1 / (2 * J2)) ** 2 + consumed_power / J2)

    # Performance calculations
    if thrust_known:
        P = 0.5 * I1 * density * velocity ** 3 * np.pi * prop_radius ** 2
        prop_efficiency = lamda * I1 / I2
    else:
        T = 0.5 * J1 * density * velocity ** 2 * np.pi * prop_radius ** 2
        prop_efficiency = lamda * J1 / J2

    print(f"Propeller Efficiency: {prop_efficiency:.2f}")

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(rR, c, label='Chord Distribution (c/R)')
    plt.plot(rR, beta, label='Twist Distribution (degrees)')
    plt.xlabel('r/R')
    plt.ylabel('Distribution')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example input and calculation
params = get_user_input('Enter Propeller Parameters:', [
    'Propeller Diameter (inches)', 'Propeller RPM', 'Propeller forward velocity (m/s)',
    'Thrust (N)', 'Air Density (kg/m^3)', 'Number Of Blades', 'Airfoil C_l',
    'Airfoil C_d', 'Angle of Attack (AoA)', 'Number of blade elements', 'Hub Radius'
])
calculate_performance(params, thrust_known=True, min_reynolds_mode=False)
