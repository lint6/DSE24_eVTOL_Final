import numpy as np
import matplotlib.pyplot as plt

class HubStress:
    
    def __init__(self, g_0=9.80665, m_R=10, d=100, T=150, G=80, L=200, D=10, r_R=1.2, b=6):
        # Initialize the HubStress Class
        # Input m in [kg], d in [mm], T in [Nm], G in [GPa], L in [N], D in [N], R in [m], and b in [-]
        self.g_0 = g_0  # Acceleration due to gravity in [m/s^2]
        self.W_R = m_R * g_0 # Weight of 1 blade in [N]
        self.d = d / 1000  # Diameter of the hub in [m]
        self.T = T  # Torque in [Nm]
        self.G = G * 10**9  # Shear Modulus in [Pa]
        self.L = L  # Lift in [N]
        self.D = D  # Drag in [N]
        self.r_R = r_R  # Radius of the rotor in [m]
        self.b = b  # Number of blades [-]
        
    def calculate_polar_moment_of_inertia(self):
        return (np.pi / 32) * (self.d**4) # returns in [m^4]
    
    def calculate_moment_of_inertia(self):
        return (np.pi / 64) * (self.d**4) # returns in [m^4]
    
    def calculate_moment_lift(self):
        return self.L * self.r_R  # returns in [Nm]
    
    def calculate_moment_weight(self):
        return self.W_R * self.r_R  # returns in [Nm]
    
    def calculate_moment_drag(self):
        return self.D * self.r_R  # returns in [Nm]
    
    def calculate_shear_stress(self):
        J = self.calculate_polar_moment_of_inertia()
        M_D = self.calculate_moment_drag()
        r = self.d / 2
        return ((self.T - (self.b * M_D)) * r) / J  # returns in [Pa]
    
    def calculate_bending_stress(self, r_i=50):
        # Input x and y in [mm]
        I = self.calculate_moment_of_inertia()
        M_L = self.calculate_moment_lift()
        M_W = self.calculate_moment_weight()
        M_x = M_L - M_W
        self.r_i = r_i / 1000   # Location on the cross section along the hub's radius in [m]
        return ((M_x * self.r_i) / I)   # returns in [Pa]

if __name__ == "__main__":
    hub = HubStress()
    polar_moment_of_inertia = hub.calculate_polar_moment_of_inertia()
    moment_of_inertia = hub.calculate_moment_of_inertia()
    moment_lift = hub.calculate_moment_lift()
    moment_weight = hub.calculate_moment_weight()
    moment_drag = hub.calculate_moment_drag()
    shear_stress = hub.calculate_shear_stress()
    bending_stress = hub.calculate_bending_stress()
    print(f"The polar moment of inertia (J) of the hub is {polar_moment_of_inertia} [m^4]")
    print(f"The moment of inertia (I) of the hub is {moment_of_inertia} [m^4]")
    print(f"The moment due to lift (M_L) of 1 blade is {moment_lift} [Nm]")
    print(f"The moment due to weight (M_W) of 1 blade is {moment_weight} [Nm]")
    print(f"The moment due to drag (M_D) of 1 blade is {moment_drag} [Nm]")
    print(f"The maximum shear stress in the hub is {shear_stress / 10**6} [MPa]")
    print(f"The bending stress in the hub at r = {hub.r_i} [m] is {bending_stress / 10**6} [MPa]")
