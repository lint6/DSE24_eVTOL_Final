import numpy as np
import matplotlib.pyplot as plt


class RotorAnalysis:
    def __init__(self, mtow_kg=718.89, n_rotors=4, bank_angle=30, v_max_kmh=150):
        # Constants
        self.MTOW_KG = mtow_kg  # Maximum Takeoff Weight in kg
        self.N_rotors = n_rotors  # Number of rotors
       # self.DL_IMPERIAL = dl_imperial  # Disc loading in lb/ft²
        self.bank_angle = bank_angle  # Bank angle during turn [deg]
        self.V_MAX_KMH = v_max_kmh  # Maximum forward speed in km/h

        # Physical constants
        self.POUNDS_PER_KG = 2.205  # Conversion factor from kg to pounds
        self.FT_TO_M = 3.281  # Conversion factor from ft to m
        self.SPEED_OF_SOUND = 343  # Speed of sound in m/s
        self.rho = 1.225  # Air density [kg/m³]
        self.g = 9.80665  # Gravitational acceleration [m/s²]

        # Derived values
        self.D_v = 0.05 * self.MTOW_KG  # Drag penalty [kg]
        self.k_dl = (1 + (self.D_v / self.MTOW_KG))  # Drag load factor
        self.V_ne = (self.V_MAX_KMH / 3.6) * 1.1  # Never exceed speed [m/s]
        self.V_gust = 30 / self.FT_TO_M
        self.C_lalpha = 5.73  # 1/rad; NACA0012
       
    def calculate_radius(self):
        dl_imperial = []
        radius_m_list = []
        for i in range(0, 100):
            x = i+1
            dl_imperial.append(x)
            mtow_pounds = self.MTOW_KG * self.POUNDS_PER_KG
            radius_ft = np.sqrt((mtow_pounds / self.N_rotors) / (dl_imperial[i] * np.pi))
            radius_m = radius_ft / self.FT_TO_M
            radius_m_list.append(radius_m)
            dl_metric = [x * 4.88243 for x in dl_imperial]
    
        plt.plot(dl_metric, radius_m_list)
        plt.xlabel('dl_metric')
        plt.ylabel('radius_m')
        plt.title('dl_metric vs radius_m')
        plt.show()

if __name__ == "__main__":
    rotor_analysis = RotorAnalysis()
    rotor_analysis.calculate_radius()
        # mtow_pounds = self.MTOW_KG * self.POUNDS_PER_KG
        # radius_ft = np.sqrt((mtow_pounds / self.N_rotors) / (self.DL_IMPERIAL * np.pi))
        # radius_m = radius_ft / self.FT_TO_M
        # return radius_m