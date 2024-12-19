import math
import numpy as np
import matplotlib.pyplot as plt


# class DLvsRadius:
#     def __init__(self, mtow_kg=718.89, n_rotors=4, bank_angle=30, v_max_kmh=150):
#         # Constants
#         self.MTOW_KG = mtow_kg  # Maximum Takeoff Weight in kg
#         self.N_rotors = n_rotors  # Number of rotors
#        # self.DL_IMPERIAL = dl_imperial  # Disc loading in lb/ft²
#         self.bank_angle = bank_angle  # Bank angle during turn [deg]
#         self.V_MAX_KMH = v_max_kmh  # Maximum forward speed in km/h

#         # Physical constants
#         self.POUNDS_PER_KG = 2.205  # Conversion factor from kg to pounds
#         self.FT_TO_M = 3.281  # Conversion factor from ft to m
#         self.SPEED_OF_SOUND = 343  # Speed of sound in m/s
#         self.rho = 1.225  # Air density [kg/m³]
#         self.g = 9.80665  # Gravitational acceleration [m/s²]

#         # Derived values
#         self.D_v = 0.05 * self.MTOW_KG  # Drag penalty [kg]
#         self.k_dl = (1 + (self.D_v / self.MTOW_KG))  # Drag load factor
#         self.V_ne = (self.V_MAX_KMH / 3.6) * 1.1  # Never exceed speed [m/s]
#         self.V_gust = 30 / self.FT_TO_M
#         self.C_lalpha = 5.73  # 1/rad; NACA0012
       
#     def calculate_radius(self):
#         dl_imperial = []
#         radius_m_list = []
#         for i in range(0, 100):
#             x = i+1
#             dl_imperial.append(x)
#             mtow_pounds = self.MTOW_KG * self.POUNDS_PER_KG
#             radius_ft = np.sqrt((mtow_pounds / self.N_rotors) / (dl_imperial[i] * np.pi))
#             radius_m = radius_ft / self.FT_TO_M
#             radius_m_list.append(radius_m)
#             dl_metric = [x * 4.88243 for x in dl_imperial]
    
#         plt.plot(dl_metric, radius_m_list)
#         plt.xlabel('dl_metric')
#         plt.ylabel('radius_m')
#         plt.title('dl_metric vs radius_m')
#         plt.show()

# if __name__ == "__main__":
#     DLRadius = DLvsRadius()
#     DLRadius.calculate_radius()
#         # mtow_pounds = self.MTOW_KG * self.POUNDS_PER_KG
#         # radius_ft = np.sqrt((mtow_pounds / self.N_rotors) / (self.DL_IMPERIAL * np.pi))
#         # radius_m = radius_ft / self.FT_TO_M
#         # return radius_m


class RotorSizing:

    def __init__(self, MTOW=718.89, n_blades=4, n_rotors = 4, DL = 14.65, bank_angle = 30, cto_fl = 0.12, cto_turn = 0.15, cto_turb = 0.17, co_ax = 1, d_fact = 0.05, max_v = 50, k_int = 1, A_eq = 0.48, FM = 0.7):
        # conversions  
        self.celsius_to_kelvin = 273.15     # addition
        self.RPM_to_rad = np.pi / 30      # multiply
        self.deg_to_rad = np.pi / 180     # multiply
        self.ft_to_m = 0.3048               # multiply

        # ambient constants 
        self.g = 9.80665        # m / s^2
        self.rho = 1.225        # kg/m^3
        self.temperature = 15   # celsius 
        self.speed_of_sound = np.sqrt(1.4 * 287 * (self.temperature + self.celsius_to_kelvin))

        # physical constants
        self.MTOW = MTOW 
        self.n_blades = n_blades 
        self.max_tip_mach = 0.85
        self.N_rotors = n_rotors
        self.disc_loading = DL   # kg/m^2 
        self.c_t_o_fl = cto_fl #user defined depending on advance ratio
        self.c_t_o_turn = cto_turn # user defined
        self.c_t_o_turb = cto_turb # user defined
        self.roll_angle = bank_angle                                        # deg
        self.n_z_turn = 1 / np.cos(self.roll_angle * self.deg_to_rad)    # load factor in turn
        self.lift_slope = 5.73      # 1 / rad (from NACA0012)
        self.gust_velocity = 30 * self.ft_to_m # from FAA
        self.coaxial = co_ax # 1 if not coaxial, 2 if coaxial
        self.V_max = max_v
        self.V_ne = 1.1 * self.V_max

        download_factor = d_fact
        self.fuselage_download = download_factor * self.MTOW * self.g                 # N
        self.k_dl = 1 + (self.fuselage_download / (self.MTOW * self.g))    # --

        self.k_int = k_int
        self.A_eq = A_eq
        self.FM = FM

        # initialize the parameters 
        self.update_parameters()

    def update_parameters(self):
        # derived parameters 
        # Disc loading calcualtion, we assumed the disc loading relation, To be further discussed 
        #check the source of this 
        #for co-axial
        #self.disc_loading = 2.28 * ((self.MTOW)**(1/3) - 2.34)                      # kg/m^2

        self.rotor_radius = np.sqrt((self.MTOW / self.N_rotors) / (np.pi * self.disc_loading))    # m 
        self.rotor_diameter = 2 * self.rotor_radius                                 # m
        # marilena statistics for helicopters. quad assumed 550 ft/s (NASA paper), to be discussed
        #self.tip_speed = 140 * (self.rotor_diameter)**0.171                         # m / s, coaxial
        self.tip_speed = 550 * self.ft_to_m                                        # quad rotor

        #self.RPM = 2673 / ((self.rotor_diameter)**0.892)                            # rpm
        #self.omega = self.RPM_to_rad * self.RPM                                     # rad / s

        self.omega = self.tip_speed / self.rotor_radius # rad/s
        self.RPM = self.omega / self.RPM_to_rad # rpm

        # flight performance 
        self.max_forward_velocity = (self.max_tip_mach * self.speed_of_sound) - self.tip_speed  # m / s; choose max mach, calculate max velocity
        self.never_exceed_velocity = 1.1 * self.max_forward_velocity                            # m / s
        self.mu_ne = self.never_exceed_velocity / self.tip_speed                                # --; advance ratio

        #print(f'User chosen max velocity = {self.V_max * 3.6 :.2f} [km/h]')
        #print(f'Corresponding never exceed advance ratio = {self.V_ne / self.tip_speed} [-]')


        # forward flight solidity 
        self.T_forward_flight = self.k_dl * self.MTOW * self.g             # N
        self.C_T_forward_flight = self.T_forward_flight / (self.N_rotors * (self.rho * math.pi * self.rotor_radius**2 * (self.rotor_radius * self.omega)**2)) # --
        self.solidity_forward_flight = self.C_T_forward_flight / self.c_t_o_fl                    # --

        # turn solidity 
        self.T_turn = self.n_z_turn * self.k_dl * self.MTOW * self.g     # N 
        self.C_T_turn = self.T_turn / (self.N_rotors*(self.rho * math.pi * (self.rotor_radius**2) * (self.rotor_radius * self.omega)**2))   # -- 
        self.solidity_turn = self.C_T_turn / self.c_t_o_turn

        # turbulent solidity
        self.delta_n_turbulent = (0.25 * self.lift_slope * (self.gust_velocity/(self.rotor_radius * self.omega))) / self.c_t_o_turb
        self.n_z_turbulent = self.delta_n_turbulent + 2 # 2g pull up
        self.T_turbulence = self.n_z_turbulent * self.k_dl * self.MTOW * self.g
        self.C_T_turbulence = self.T_turbulence / (self.N_rotors * (self.rho * math.pi * (self.rotor_radius**2) * (self.rotor_radius * self.omega)**2))
        self.solidity_turbulent = self.C_T_turbulence / self.c_t_o_turb

        # chord and aspect ratio 
        self.maximum_solidity = np.max([self.solidity_forward_flight, self.solidity_turn, self.solidity_turbulent])
        self.chord = (self.maximum_solidity * np.pi * self.rotor_radius) / (self.coaxial * self.n_blades)
        self.aspect_ratio = self.rotor_radius**2 / (self.rotor_radius * self.chord)


    def display_parameters(self):
        print(f"MTOW: {self.MTOW} kg")
        print(f"Rotor Radius: {self.rotor_radius:.2f} m")
        print(f"Rotor Diameter: {self.rotor_diameter:.2f} m")
        print(f"Tip Speed: {self.tip_speed:.2f} m/s")
        print(f"Rad/s: {self.omega:.2f}")
        print(f"RPMs: {self.RPM:.2f}")
        print(f'Maximum Solidity: {self.maximum_solidity:.2f}')
        print(f"Blade Chord: {self.chord:.3f} m")
        print(f"Aspect Ratio: {self.aspect_ratio:.2f}")

        #next 2 not really used anymore
        #print(f"Max Forward Velocity: {self.max_forward_velocity:.2f} m/s")
        #print(f"Never Exceed Velocity: {self.never_exceed_velocity:.2f} m/s")

    def iterate_design(self, new_MTOW=None, new_n_blades=None, new_n_rotors=None, new_disc_loading=None):
        if new_MTOW:
            self.MTOW = new_MTOW 
        if new_n_blades:
            self.n_blades = new_n_blades 
        if new_n_rotors:
            self.N_rotors = new_n_rotors
        if new_disc_loading:
            self.disc_loading = new_disc_loading
        self.update_parameters()

    def visual_blade_vs_aspect_ratio(self):
        blade_numbers = [2, 3, 4, 5, 6, 7, 8]
        aspect_ratios = []
        for blades in blade_numbers:
            self.iterate_design(new_n_blades=blades)
            aspect_ratios.append(self.aspect_ratio)
        plt.figure(figsize=(10, 6))
        plt.plot(blade_numbers, aspect_ratios, marker='o', label='Aspect Ratio')
        plt.title('Effect of Blade Number on Aspect Ratio')
        plt.xlabel('Number of Blades')
        plt.ylabel('Aspect Ratio')

        #plt.axhspan(14, 20, color='green', alpha=0.2, label='Acceptable Range')
        #plt.axhspan(0, 14, color = 'red', alpha=0.2, label = 'Unacceptable Range')
        #plt.axhspan(20, 100, color = 'red', alpha = 0.2)

        plt.grid(True)
        plt.legend()
        plt.show()
    
    def visual_blade_vs_radius(self):
        blade_numbers = [2, 3, 4, 5, 6, 7, 8]
        rotor_radius = []
        for blades in blade_numbers:
            self.iterate_design(new_n_blades=blades)
            rotor_radius.append(self.rotor_radius)
        plt.figure(figsize=(10, 6))
        plt.plot(blade_numbers, rotor_radius, marker='o', label='Rotor Radius')
        plt.title('Effect of Blade Number on Rotor Radius')
        plt.xlabel('Number of Blades')
        plt.ylabel('Rotor Radius [m]')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def n_rotors_vs_radius(self):
        n_rotors = [4, 6, 8, 10, 12]
        rotor_radius = []
        for rotors in n_rotors:
            self.iterate_design(new_n_rotors=rotors)
            rotor_radius.append(self.rotor_radius)
        plt.figure(figsize=(10, 6))
        plt.plot(n_rotors, rotor_radius, marker='o', label='Rotor Radius')
        plt.title('Effect of Rotor Number on Rotor Radius')
        plt.xlabel('Number of Rotors')
        plt.ylabel('Rotor Radius [m]')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def disc_loading_vs_radius(self):
        disc_loading = np.arange(1, 50, 1)
        rotor_radius = []
        for dl in disc_loading:
            self.iterate_design(new_disc_loading=dl)
            rotor_radius.append(self.rotor_radius)
        plt.figure(figsize=(10, 6))
        plt.plot(disc_loading, rotor_radius, marker='o', label='Rotor Radius')
        plt.title('Effect of Disc Loading on Rotor Radius')
        plt.xlabel('Disc Loading [kg/m^2]')
        plt.ylabel('Rotor Radius [m]')
        plt.grid(True)
        plt.legend()
        plt.show()
    
    def disc_loading_vs_aspect_ratios(self):
        disc_loading = np.arange(1, 50, 1)
        aspect_ratios = []
        for dl in disc_loading:
            self.iterate_design(new_disc_loading=dl)
            aspect_ratios.append(self.aspect_ratio)
        plt.figure(figsize=(10, 6))
        plt.plot(disc_loading, aspect_ratios, marker='o', label='Aspect Ratio')
        plt.title('Effect of Disc Loading on Aspect Ratio')
        plt.xlabel('Disc Loading [kg/m^2]')
        plt.ylabel('Aspect Ratio')
        plt.grid(True)
        plt.legend()
        plt.show()

    def MTOW_vs_radius(self):
        MTOW = np.arange(500, 1500, 50)
        rotor_radius = []
        for mtow in MTOW:
            self.iterate_design(new_MTOW=mtow)
            rotor_radius.append(self.rotor_radius)
        plt.figure(figsize=(10, 6))
        plt.plot(MTOW, rotor_radius, marker='o', label='Rotor Radius')
        plt.title('Effect of MTOW on Rotor Radius')
        plt.xlabel('MTOW [kg]')
        plt.ylabel('Rotor Radius [m]')
        plt.grid(True)
        plt.legend()
        plt.show()

if __name__ == "__main__":
     RotorSize = RotorSizing()
     RotorSize.visual_blade_vs_aspect_ratio()
     #RotorSize.visual_blade_vs_radius()
     RotorSize.n_rotors_vs_radius()
     RotorSize.disc_loading_vs_radius()
     RotorSize.disc_loading_vs_aspect_ratios()
     RotorSize.MTOW_vs_radius()