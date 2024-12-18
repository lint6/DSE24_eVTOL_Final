import numpy as np
import matplotlib.pyplot as plt


class Performance:

    def __init__(self, mtow, n_bl, R, chord, V_tip, n_elements, a_airfoil):

        # conversions  
        self.celsius_to_kelvin = 273.15     # addition
        self.RPM_to_rad = np.pi / 30      # multiply
        self.deg_to_rad = np.pi / 180     # multiply
        self.ft_to_m = 0.3048               # multiply

        # ambient constants 
        self.g = 9.80665        # [m/s^2]
        self.rho = 1.225        # [kg/m^3]
        self.temperature = 15   # [celsius] 
        self.speed_of_sound = np.sqrt(1.4 * 287 * (self.temperature + self.celsius_to_kelvin))

        # inputs
        self.mtow = mtow # [kg]
        self.n_bl = n_bl # number of blades
        self.R = R # radius in [m]
        self.chord = chord # [m]
        self.V_tip = V_tip # tip speed in [m/s]
        self.omega = V_tip / R # angular velocity in [rad/s]
        self.a_airfoil = a_airfoil # lift curve slope [1/rad]

        # blade element theory
        self.n_elements = n_elements

        # to be added: twist, cutout, airfoil data

    
    def power_hover(self):

        # hover power calculation using blade elemnet theory mixed with momentum theory 

        # Initialize lists to store results
        r_over_R = []
        c_over_R = []
        M = []
        a_slope = []

        # Calculate segment size
        segment_size = self.R / self.n_elements

        # Loop through each segment and calculate values
        for i in range(self.n_elements):
            # Midpoint of the blade element segment
            r_mid = (i + 0.5) * segment_size
            # Normalized position
            r_R = r_mid / self.R
            r_over_R.append(r_R)  # calculates r/R
            # Constant chord-to-radius ratio (5% of radius)
            c_R = self.chord / self.R
            c_over_R.append(c_R)
            # Local Mach number
            mach = r_R * ((self.omega * self.R) / self.speed_of_sound)
            M.append(mach)
            # Lift curve slope
            a = self.a_airfoil
            a_slope.append(a)

        return r_over_R, c_over_R, M
    

if __name__ == "__main__":
    # Initialize the Performance instance
    perf = Performance(
        mtow=709,          # Maximum takeoff weight [kg]
        n_bl=4,            # Number of blades
        R=3,               # Rotor radius [m]
        chord=0.2,         # Chord length [m]
        V_tip=167.64,      # Tip speed [m/s]
        n_elements=5       # Number of blade elements
        a_airfoil=5.73     # Lift curve slope
    )

    # Call the power_hover method
    r_over_R, c_over_R, M = perf.power_hover()
    print(r_over_R, c_over_R, M)

