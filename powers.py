import numpy as np
import matplotlib.pyplot as plt
from Aero.airfoil import AirfoilData
from scipy.integrate import quad

class Performance:

    def __init__(self, mtow, n_bl, R, chord, V_tip, n_elements, a_airfoil, pitch_tip):

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
        self.n_elements = n_elements # number of elements used
        self.pitch_tip = pitch_tip * self.deg_to_rad # pitch at the tip in [rad]

        # to be added: twist, cutout, airfoil data
        self.airfoil_data = AirfoilData()


    
    def power_hover(self):

        # hover power calculation using blade elemnet theory mixed with momentum theory 

        # Initialize lists to store results of each element
        r_over_R = []
        c_over_R = []
        M = []
        a_slope = []
        pitch = []
        inflow = []
        aoa = []
        cl_local = []
        cd_local = []
        #ct_noloss = []
        #ct_final = []
        running_thrust = []
        running_torque_profile = []
        running_torque_induced = []

        # Calculate segment size
        segment_size = self.R / self.n_elements
        dr = segment_size / self.R              # Normalized segment length

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

            # Calculate pitch of each blade element, in [rad]
            # !!!assumes ideal twist distribution!!!
            pitch_calc = self.pitch_tip / r_R #!!! ideal twist assumed
            pitch.append(pitch_calc)

            # Calculate local inflow angle
            # a and pitch must be in [rad]]
            inflow_angle = (a*self.n_bl)/(16*np.pi) * (c_R/r_R) * (-1 + np.sqrt(1+((32*np.pi*pitch_calc*r_R)/(a*self.n_bl*c_R))))
            inflow.append(inflow_angle)

            # Calculate local angle of attack
            alpha = pitch_calc - np.arctan(inflow_angle)
            aoa.append(alpha)

            # Calculate corresponding local CL and CD
            cl = self.airfoil_data.interpolate_cl_cd(alpha)[0]
            cl_local.append(cl)
            cd = self.airfoil_data.interpolate_cl_cd(alpha)[1]
            cd_local.append(cd)

            r_thurst = (self.n_bl * (r_R**2) * c_R * cl) / (2 * np.pi)
            running_thrust.append(r_thurst)

            # Calculate local torques
            r_torque_profile = (self.n_bl * (r_R**3) * c_R * cd) / (2 * np.pi)
            running_torque_profile.append(r_torque_profile)
            r_torque_induced = (self.n_bl * (r_R**3) * c_R * cl * inflow_angle) / (2 * np.pi)
            running_torque_induced.append(r_torque_induced)
    

            #SOMETHING IS WRONG FROM NOW ON
            # maybe i should just be adding all ct's at the end, instead of integrating?

            # Define thrust loading function inside the loop
            # thrust_loading = lambda r_R: (self.n_bl * (r_R**2) * c_R * cl) / (2 * np.pi)

            # # Integrate thrust loading over the blade segment using `quad`
            # t_noloss, error = quad(thrust_loading, 0.15, 1) # assume blade starts at 15% radius
            # ct_noloss.append(t_noloss)

            # # Calculate tip loss factor
            # B = 1 - np.sqrt(2*t_noloss)/self.n_bl

            # # Calculate corrected thrust coefficient
            # t_loss, error = quad(thrust_loading, B, 1)
            # ct = t_noloss - t_loss
            # ct_final.append(ct)

    
        total_c_t = sum(running_thrust) * dr  # Numerical integration thrust
        total_c_q_p = sum(running_torque_profile) * dr  # Numerical integration profile torque
        total_c_q_i = sum(running_torque_induced) * dr   # Numerical integration induced torque
        total_c_q = total_c_q_p + total_c_q_i

            # Convert total thrust coefficient to physical thrust
        rotor_area = np.pi * self.R**2
        total_thrust = total_c_t * self.rho * rotor_area * self.V_tip**2
        total_power = total_c_q * self.rho * rotor_area * self.V_tip**3

        DL = total_c_t * self.rho * self.V_tip**2


        return r_over_R, running_thrust, total_c_t, total_thrust, total_power, DL
    
# run file
if __name__ == "__main__":
    # Initialize the Performance instance
    perf = Performance(
        mtow=709,          # Maximum takeoff weight [kg]
        n_bl=4,            # Number of blades
        R=5,               # Rotor radius [m]
        chord=0.2,         # Chord length [m]
        V_tip=167.64,      # Tip speed [m/s]
        n_elements=10,       # Number of blade elements
        a_airfoil=5.73,     # Lift curve slope	[1/rad]
        pitch_tip=8         # Collective pitch angle [deg]
    )

    # Call the power_hover method
    r_over_R, running_thrust, total_c_t, total_thrust, total_power, DL = perf.power_hover()

    #print(r_over_R, running_thrust)
    print(total_c_t, total_thrust, total_power, DL)
    #Plot the results
    # plt.figure()
    # plt.plot(r_over_R, running_thrust, marker='o')
    # plt.xlabel("r/R")
    # plt.ylabel("Thrust")
    # plt.title("Thrust Distribution in Hover")
    # plt.grid()
    # plt.show()

