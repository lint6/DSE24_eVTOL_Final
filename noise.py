import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class RotorSizing:

    def __init__(self, MTOW=718.89, n_blades=4, n_rotor = 6, DL = 34.2, bank_angle = 30, cto_fl = 0.12, cto_turn = 0.15, cto_turb = 0.17, co_ax = 1, d_fact = 0.05, max_v = 50, k_int = 1, A_eq = 0.48, FM = 0.7):

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
        self.N_rotors = n_rotor
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

    def iterate_design(self, new_MTOW=None, new_n_blades=None):
        if new_MTOW:
            self.MTOW = new_MTOW 
        if new_n_blades:
            self.n_blades = new_n_blades 
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



class SoundAnalysis:
    def __init__(self, rotorsizing = None):
        #Conversions
        self.m_to_f = 1/0.3048 #Conversion factor from meter to feet
        self.N_to_lbs = (1/9.80665)*2.20462

        #Input
        self.rotorsizing = rotorsizing if rotorsizing else RotorSizing()

        #Observer position relative to rotor, UNUSED 
        self.x = np.linspace(0,10000,10) #Measured in direction of motion of helicopter [ft]
        self.x = np.array(self.x)
        self.y = np.full(10, 0) #np.linspace(-100,100,1000) #Measured at 90 deg to x in disc plane [ft]
        self.z = np.full(10, 492) #Flyover height [ft]
        self.r = (self.x**2+self.y**2+self.z**2)**0.5

        #Inputs for rotational noise
        self.R = 1 #self.rotorsizing.rotor_radius*self.m_to_f #Get rotor radius in [f]
        self.A = np.pi*(self.R**2) #Rotor area [ft^2]
        self.n = 180 #self.rotorsizing.omega #Rotor rotational speed [rad/s] 
        self.V = 25*self.m_to_f #self.rotorsizing.V_max*self.m_to_f [ft/s] -> VH is defined as the airspeed in level flight obtained using the minimum specification engine power corresponding to maximum continuous power available
        self.c = self.rotorsizing.speed_of_sound*self.m_to_f #Speed of sound [ft/s]
        self.B = 5 #self.rotorsizing.n_blades
        self.T = 7900*self.N_to_lbs/self.rotorsizing.N_rotors #self.rotorsizing.T_forward_flight*self.N_to_lbs/self.rotorsizing.N_rotors #Thrust [lbs]

        #Inputs for vortex noise
        self.D = 2*self.R #Rotor diameter [ft]
        self.V_07 = 0.7*((self.n*np.pi*self.D)/60) #Linear speed of 0.7 radius section
        self.chord = self.rotorsizing.chord*self.m_to_f #Chord [ft]
        self.A_b = self.B*self.R*self.chord #Total blade area [ft^2]

        #Input for noise conversion/addition
        self.n_rotors = self.rotorsizing.N_rotors*self.rotorsizing.coaxial

        #Initialize
        self.rotational_noise()
        self.vortex_noise()

    def rotational_noise(self):
        #Calculate rotational Mach number
        self.M = (0.8*self.n*self.R)/(self.c)

        #Calculate flight Mach number
        self.M_f = self.V/self.c

        #Calculate theta dash UNUSED
        #self.theta_dash = np.arccos(self.x/self.r)
        self.theta_dash = np.linspace(np.pi / 4, np.pi / 2, 10)

        # Ensure theta_dash is a NumPy array
        self.theta_dash = np.array(self.theta_dash)

        # Calculate effective rotational Mach number
        self.M_E_list = self.M / (1 - self.M_f * self.x / self.r)

        # Print the results
        print("M_E_list = ", self.M_E_list)

        #Calculate theta UNUSED
        self.theta = np.pi/2 #Set to angle that gives max noise for now (unused)

        #Interpolate all values for SPL for the critical theta

        #This commented part is Jorrits old code
        
        # #Interpolate from graph of 1st harmonic (45deg)
        # M_series = np.linspace(0.2,1,9)
        # noise_series = np.array([77,82,85,88,91,93,95,96,97])
        # interpolator = np.polyfit(M_series, noise_series,3)

        # self.rotational_SPL_uncorrected = interpolator[0]*(self.M_E)**3  + interpolator[1]*(self.M_E)**2 + interpolator[2]*(self.M_E) + interpolator [3]



        #SPL as a function of M_E for all 12 harmonics:

        def calculate_rotational_SPL_uncorrected(M_E, noise_series):
            """
            Calculate the rotational SPL uncorrected based on the given Mach number M_E and noise series.

            Parameters:
            M_E (float): The Mach number for which the SPL is to be calculated.
            noise_series (array-like): The noise levels corresponding to the Mach series.

            Returns:
            float: The calculated rotational SPL uncorrected value.
            """
            # Define the Mach series
            M_series = np.linspace(0.2, 1, 9)

            # Fit a 3rd degree polynomial to the data
            interpolator = np.polyfit(M_series, noise_series, 3)

            # Calculate the rotational SPL uncorrected for the given M_E
            rotational_SPL_uncorrected = (
                interpolator[0] * (M_E) ** 3 +
                interpolator[1] * (M_E) ** 2 +
                interpolator[2] * (M_E) +
                interpolator[3]
            )

            return rotational_SPL_uncorrected

        # Example numbered functions for different noise series
        def calculate_rotational_SPL_uncorrected_1(M_E):
            noise_series = np.array([77, 82, 85, 88, 91, 93, 95, 96, 97])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_2(M_E):
            noise_series = np.array([68.5,74,79.5,84.5,89,92.5,95.5,97.5,100])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_3(M_E):
            noise_series = np.array([65,71,78, 82.5, 87.5, 91, 95, 97.5, 100])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_4(M_E):
            noise_series = np.array([57.5, 63, 69, 75, 83, 88, 93, 96, 102])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_5(M_E):
            noise_series = np.array([53, 57, 63, 69.5, 77, 84, 91, 96, 101])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_6(M_E):
            noise_series = np.array([48, 54, 60, 65, 74, 83, 92, 98, 103])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_7(M_E):
            noise_series = np.array([46, 53, 56, 63, 70, 80, 90, 97, 103])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_8(M_E):
            noise_series = np.array([43, 46, 53, 56, 64, 75, 86, 96, 104])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_9(M_E):
            noise_series = np.array([40, 45, 50, 55, 59, 69, 83, 95, 104])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_10(M_E):
            noise_series = np.array([25, 30, 42, 46, 53, 60, 76, 93, 105])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_11(M_E):
            noise_series = np.array([24, 33, 37, 43, 47, 55, 69, 91, 107])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        def calculate_rotational_SPL_uncorrected_12(M_E):
            noise_series = np.array([15, 20, 31, 36, 40, 47, 58, 86, 109])
            return calculate_rotational_SPL_uncorrected(M_E, noise_series)

        M_E = np.max(self.M_E_list)
        print("M_E =", M_E)
        SPL_array_uncorrected = np.array([calculate_rotational_SPL_uncorrected_1(M_E),
                              calculate_rotational_SPL_uncorrected_2(M_E),
                              calculate_rotational_SPL_uncorrected_3(M_E),
                              calculate_rotational_SPL_uncorrected_4(M_E),
                              calculate_rotational_SPL_uncorrected_5(M_E),
                              calculate_rotational_SPL_uncorrected_6(M_E),
                              calculate_rotational_SPL_uncorrected_7(M_E),
                              calculate_rotational_SPL_uncorrected_8(M_E),
                              calculate_rotational_SPL_uncorrected_9(M_E),
                              calculate_rotational_SPL_uncorrected_10(M_E),
                              calculate_rotational_SPL_uncorrected_11(M_E),
                              calculate_rotational_SPL_uncorrected_12(M_E)])
        print("SPL uncorrected =", SPL_array_uncorrected)
            
        # Example usage:
        # M_E = 0.5
        # print(calculate_rotational_SPL_uncorrected_1(M_E))
        # print(calculate_rotational_SPL_uncorrected_12(M_E))


        #Apply SPL correction
        SPL_corrected_list = []
        for i in range(10):
            self.rotational_SPL = SPL_array_uncorrected + 11 + 10*np.log10((self.T/(self.r[i]**2))*(self.T/self.A))
            SPL_corrected_list.append(max(self.rotational_SPL))

        print(' SPL corrected:', SPL_corrected_list)

        plt.plot(self.r,SPL_corrected_list)
        plt.show()
    
    
        #Convert to sound intensity
        self.one_rotor_intensity = (10e-12) * 10**(self.rotational_SPL/10)
        
        #Add sound intensities
        self.all_rotor_intensity = self.one_rotor_intensity * self.n_rotors

        #Convert back to dB
        self.rotational_SPL_total = 10*np.log10(self.all_rotor_intensity/(10e-12))

        print("Rotational SPL tot", self.rotational_SPL_total)

        #Calculate fundamental frequency
        self.f_rotational = (self.n*self.B)/(2*np.pi*(1-self.M_f*np.cos(self.theta)))

    def vortex_noise(self):
        #Calculate SPL for 300 ft distance
        self.vortex_SPL_uncorrected = 10*(2*np.log10(self.V_07)+2*np.log10(self.T)-np.log10(self.A_b)-3.57)

        #Correct for distance (500 ft)
        self.vortex_SPL = self.vortex_SPL_uncorrected - 20*np.log10(self.z/300)

        #Convert to sound intensity
        self.one_rotor_intensity_vortex = (10e-12) * 10**(self.vortex_SPL/10)
        
        #Add sound intensities
        self.all_rotor_intensity_vortex = self.one_rotor_intensity_vortex * self.n_rotors

        #Convert back to dB
        self.vortex_SPL_total = 10*np.log10(self.all_rotor_intensity_vortex/(10e-12))

        print("Vortex Noise is", self.vortex_SPL_total ,  "dB")

        #Calculate frequency
        self.thickness = 0.12*self.chord #NACA0012 airfoil thickness to chord
        self.f_vortex = (self.V_07*0.28)/self.thickness  #Only valid for small AoA

    def display_parameters_rotor(self):
        print(f"This configuration has {self.n_rotors} rotors")
        print(f"Equivalent M: {self.M_E :.4f}")
        print(f"Single rotor SPL: {self.rotational_SPL:.4f} dB")
        #print(f"Correction factor: {self.rotational_SPL-self.rotational_SPL_uncorrected:.4f} dB")
        print(f"All rotor SPL: {self.rotational_SPL_total:.4f} dB")
        print(f"Fundamental frequency: {self.f_rotational:.4f} Hz")
        
    def display_paramenters_vortex(self):
        print(f"Single rotor SPL: {self.vortex_SPL:.4f} dB")
        print(f"All rotor SPL: {self.vortex_SPL_total:.4f} dB")
        print(f"Vortex frequency: {self.f_vortex:.4f} Hz")


def run():
    # Create an instance of PerformanceAnalysis
    analysis = SoundAnalysis()

    analysis.rotational_noise()
    analysis.vortex_noise()


# Execute the run function
if __name__ == "__main__":
    run()
