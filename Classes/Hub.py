import numpy as np
import matplotlib.pyplot as plt

class HubStuff:
    
    def __init__(self, g_0=9.80665, r_R=1.2, b=6, m_R=5.705, d_sh=23.95, d=270, z=70, G=44, rho=4.43, T=213, L=426.6, D=15.66):
        # Initialize the HubStress Class
        # Input r_R in [m], b in [-], m_R (1 rotor) in [kg], d_sh in [mm], d in [mm], z in [mm], T in [Nm], G in [GPa], rho in [g/cc], L (1 blade) in [N], and D (1 rotor) in [N]
        
        "Material Selection"
        # Aluminium 7075-T6: G = 26.9 [GPa], rho = 2.81 [g/cc]
        # Ti-6Al-4V: G = 44 [GPa], rho = 4.43 [g/cc]
        # Steel AlSl 4130: G = 80 [GPa], rho = 7.85 [g/cc]

        self.g_0 = g_0  # Acceleration due to gravity in [m/s^2]
        self.r_R = r_R  # Radius of the rotor in [m]
        self.b = b  # Number of blades [-]
        self.W_R = (m_R * g_0) / self.b # Weight of 1 blade in [N]
        self.d_sh = d_sh / 1000 # Diameter of the shaft [m]
        self.d = d / 1000  # Diameter of the hub in [m]
        self.z = z / 1000  # Thickness of the hub in [m]
        self.G = G * 10**9  # Shear Modulus of the material in [Pa]
        self.rho = rho * 1000  # Density of the material in [kg/m^3]
        self.T = T  # Torque in [Nm]
        self.L = L  # Lift of 1 blade in [N]
        self.D = D / self.b  # Drag of 1 blade in [N]

        
    def calculate_polar_moment_of_inertia(self):
        return (np.pi / 32) * ((self.d**4) - (self.d_sh**4)) # returns in [m^4]
    
    def calculate_moment_of_inertia(self):
        return (np.pi / 64) * ((self.d**4) - (self.d_sh**4)) # returns in [m^4]
    
    def calculate_moment_lift(self):
        return self.L * self.r_R  # returns in [Nm]
    
    def calculate_moment_weight(self):
        return self.W_R * self.r_R  # returns in [Nm]
    
    def calculate_moment_drag(self):
        return self.D * self.r_R  # returns in [Nm]
    
    def calculate_rate_of_twist(self):
        J = self.calculate_polar_moment_of_inertia()
        M_D = self.calculate_moment_drag()
        return (self.T - (self.b * M_D)) / (self.G * J) # returns in [rad/m]
    
    def calculate_twist_angle(self):
        return self.calculate_rate_of_twist() * self.z  # returns in [rad]
    
    def calculate_shear_stress(self):
        J = self.calculate_polar_moment_of_inertia()
        M_D = self.calculate_moment_drag()
        r = self.d / 2
        return ((self.T - (self.b * M_D)) * r) / J  # returns in [Pa]
    
    def calculate_bending_stress(self):
        # Input location of bending stress (r_i) in [mm], default as the radius of the hub
        r_i = self.d / 2
        I = self.calculate_moment_of_inertia()
        M_L = self.calculate_moment_lift()
        M_W = self.calculate_moment_weight()
        M_x = M_L - M_W
        self.r_i = r_i / 1000   # Location on the cross section along the hub's radius in [m]
        return ((M_x * r_i) / I)   # returns in [Pa]

    def calculate_hub_mass(self):
        return np.pi * (((self.d**2) - self.d_sh**2) / 4) * self.z * self.rho  # returns in [kg]


if __name__ == "__main__":
    hub = HubStuff()
    polar_moment_of_inertia = hub.calculate_polar_moment_of_inertia()
    moment_of_inertia = hub.calculate_moment_of_inertia()
    moment_lift = hub.calculate_moment_lift()
    moment_weight = hub.calculate_moment_weight()
    moment_drag = hub.calculate_moment_drag()
    rate_of_twist = hub.calculate_rate_of_twist()
    twist_angle = hub.calculate_twist_angle()
    shear_stress = hub.calculate_shear_stress()
    bending_stress = hub.calculate_bending_stress()
    hub_mass = hub.calculate_hub_mass()
    print(f"The polar moment of inertia (J) of the hub is {polar_moment_of_inertia} [m^4]")
    print(f"The moment of inertia (I) of the hub is {moment_of_inertia} [m^4]")
    print(f"The moment due to lift (M_L) of 1 blade is {moment_lift} [Nm]")
    print(f"The moment due to weight (M_W) of 1 blade is {moment_weight} [Nm]")
    print(f"The moment due to drag (M_D) of 1 blade is {moment_drag} [Nm]")
    print(f"The rate of twist of the hub is {rate_of_twist} [rad/m]")
    print(f"The twist angle of the hub is {twist_angle} [rad] or {twist_angle * 180 / np.pi} [deg]")
    print(f"The maximum shear stress in the hub is {shear_stress / 10**6} [MPa]")
    print(f"The bending stress in the hub at r = {hub.r_i} [m] is {bending_stress / 10**6} [MPa]")
    print(f"The mass of the hub is {hub_mass} [kg]")
