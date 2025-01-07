import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class PerformanceAnalysis:

    def __init__(self, MTOW = 709, climb_angle = 9, descent_angle = -5, vertical_climb = 0.76, vertical_descent = -0.5, steep_descent = -7.6):
        
        # constants
        self.g = 9.80665
        self.rho = 1.225
        self.pi = np.pi

        # conversions
        self.RPM_to_rad = (np.pi / 30)

        #vehicle inputs
        self.MTOW = MTOW #kg
        self.MTOW_N = self.MTOW * self.g #N

        # rotor inputs, TODO: INPUT CORRECT VALUES LATER
        self.rotor_radius = 2 #m
        self.number_of_blades = 4
        self.number_of_rotors = 4
        self.omega = 70 #rad/s
        self.C_l_alpha = 5.73 #1/rad
        self.solidity = 0.12
        self.pitch_x = 8 # pitch angle variation over span aqs a function of x

        # structural inputs, TODO: INPUT CORRECT VALUES LATER
        self.A_eq = 0.5

        # mission inputs
        self.gamma_climb = climb_angle #degrees
        self.gamma_descent = descent_angle #degrees
        self.vertical_climb = vertical_climb #m/s
        self.vertical_descent = vertical_descent #m/s
        self.steep_descent = steep_descent #m/s

        self.V_point = 13 # m/s, random assumed cruise speed

        # calculated values, TODO: CHANGE LATER
        # self.min_power = None
        # self.min_power_velocity = None

        # self.min_power_CD = None
        # self.min_power_velocity_CD = None

        # self.gamma_CD_steep = None
        # self.power_steep_descent = None
 
        # self.P_vertical_climb = None
        # self.min_power_watts = None
        # self.min_power_CD_watts = None
        # self.power_steep_descent_watts = None
        # self.min_power_descent_watts = None
        # self.min_power_velocity_descent = None

        self.P = {
            'HIGE1': None,
            'V_climb': None,
            'HOGE1': None,
            'Climb1': None,
            'Cruise1': None,
            'Descent1': None,
            'HOGE2': None,
            'Loiter': None,
            'Climb2': None,
            'Cruise2': None,
            'Descent2': None,
            'HOGE3': None,
            'V_Descent': None,
            'HIGE2': None
        }


    def powers_in_flight(self):
        self.advance_ratio = self.V_point / (self.rotor_radius * self.omega) # advance ratio

        # hover induced power

        def lambda_equation(lambda_i, x):
            return self.solidity * self.C_l_alpha * ((self.pitch_x *(np.pi/180)) - lambda_i / x) * x - 8 * lambda_i**2

        # Function to solve for lambda_i at a given x
        def solve_lambda(x, initial_guess=0.1):
            lambda_i_solution = fsolve(lambda_equation, initial_guess, args=(x,))
            return lambda_i_solution[0]

        # Solve for lambda_i over a range of x
        x_values = np.linspace(0.01, 1, 100)  # range over blade from 0 to 1 (if 0 is input it breaks the equation)
        lambda_values = np.array([solve_lambda(x) for x in x_values])  # Solve for lambda_i at each x
        hover_vi_values = lambda_values * (self.omega * self.rotor_radius)

        delta_x = x_values[1] - x_values[0]  # Assuming evenly spaced x values
        self.v_i_hov = np.sum(hover_vi_values) * delta_x  # Approximate integral

        # plot induced velocity
        # plt.plot(x_values, hover_vi_values, label=r'$v_i-hov$')
        # plt.xlabel('x')
        # plt.ylabel(r'$v_i-hov$')
        # plt.title('v_i-hov along blade span')
        # plt.legend()
        # plt.grid()
        # plt.show()

        # this should be lower then the same calculation using pure momentum disk theory
        self.P_i_hov = self.MTOW_N * self.v_i_hov # k factor is 1 as rotors are away from fuselage, assumed that Thrust = Weight; TODO: CHANGE WHEN ROTOR IS FINISHED
        #print(f"Hover induced power: {self.P_i_hov/1000:.2f} kW")
        # profile power

        self.C_D_p_bar = 0.01 # TODO: CHANGE LATER based on airfoil tools

        self.P_p_hov = ((self.solidity*self.C_D_p_bar)/8) * self.rho *((self.omega*self.rotor_radius)**3)*(self.pi*(self.rotor_radius**2)) * self.number_of_rotors

        self.P_hoge = self.P_i_hov + self.P_p_hov
        print(f"Hover out of ground effect power: {self.P_hoge/1000:.2f} kW")

        self.P_vertical_climb = self.P_hoge + (self.MTOW_N * self.vertical_climb)/2 # diktaat

        self.P_vertical_descent = self.P_hoge + (self.MTOW_N * self.vertical_descent)/2 # diktaat

def run():
    # Create an instance of PerformanceAnalysis
    analysis = PerformanceAnalysis()

    # Call the powers_in_flight method to perform calculations and plot results
    print("Calculating powers in flight and plotting induced velocity distribution...")
    analysis.powers_in_flight()

    # Display some key results
    print(f"Hover induced velocity: {analysis.v_i_hov:.2f} m/s")


# Execute the run function
if __name__ == "__main__":
    run()


class PowerAnalysis:

    def __init__(self, rotorsizing, climb_angle = 9, descent_angle = -5, vertical_climb = 0.76, vertical_descent = -0.5):
        #conversion
        self.g = 9.80665
        self.pi = np.pi
        self.RPM_to_rad = (np.pi / 30)

        #input
        self.rotorsizing = rotorsizing if rotorsizing else RotorSizing()  # Use the provided object or create a default one
        self.FM = self.rotorsizing.FM
        self.solidity = self.rotorsizing.maximum_solidity
        self.rho = self.rotorsizing.rho
        self.omega = self.rotorsizing.omega
        self.rotor_radius = self.rotorsizing.rotor_radius
        self.MTOW = self.rotorsizing.MTOW
        self.MTOW_N = self.MTOW * self.g
        self.k = 1.15       # inflow correction, assumption: should be between 1.1 and 1.2
        self.k_dl = self.rotorsizing.k_dl # fuselage downlaod factor
        self.V_point = 13 # cruise speed, assumption for now
        self.k_int = self.rotorsizing.k_int # 1.28 for co axial
        self.ROC_VCD = 10
        self.C_l_alpha = self.rotorsizing.lift_slope # 1/rad NACA0012
        self.A_eq = self.rotorsizing.A_eq # equivalent flat plate area

        # basic gamma values
        self.gamma_CD = climb_angle # deg
        self.ROC_CD_steep = -7.6 # m/s

        self.hige_factor = 1  #power in hige / power hoge
        self.min_power = None
        self.min_power_velocity = None
        self.min_power_CD = None
        self.min_power_velocity_CD = None
        self.gamma_CD_steep = None
        self.power_steep_descent = None
        self.gamma_descent = descent_angle
        self.vertical_climb = vertical_climb # m/s
        self.vertical_descent = vertical_descent # m/s
        self.P_vertical_climb = None
        self.min_power_watts = None
        self.min_power_CD_watts = None
        self.power_steep_descent_watts = None
        self.min_power_descent_watts = None
        self.min_power_velocity_descent = None

        self.P = {
            'HIGE1': None,
            'V_climb': None,
            'HOGE1': None,
            'Climb1': None,
            'Cruise1': None,
            'Descent1': None,
            'HOGE2': None,
            'Loiter': None,
            'Climb2': None,
            'Cruise2': None,
            'Descent2': None,
            'HOGE3': None,
            'V_Descent': None,
            'HIGE2': None
        }

        self.forward_flight()

    def forward_flight(self):
        self.AV = self.V_point/(self.omega*self.rotor_radius) # advance ratio

        ## profile drag power calculation
        # thurst coefficient
        self.C_T = self.rotorsizing.T_forward_flight / (self.rho * (self.pi * (self.rotor_radius**2)) * self.rotorsizing.N_rotors * ((self.rotor_radius * self.omega)**2))
        # avg coefficient of lift
        self.C_L_bar = (6.6 * self.C_T)/self.solidity
        # AoA for max lift
        self.alpha_m = self.C_L_bar / self.C_l_alpha

        # estimate C_D_p_bar
        self.C_D_p_bar_1 = 0.0087 - 0.0216 * self.alpha_m + 0.4 * (self.alpha_m**2) #bailey
        self.C_D_p_bar_2 = 0.011 + 0.4 * (self.alpha_m**2) #marinescu
        self.C_D_p_bar_3 = 0.009 + 0.73 * (self.alpha_m**2) #talbot

        # pick the highest
        self.C_D_p_bar = max(self.C_D_p_bar_1,self.C_D_p_bar_2,self.C_D_p_bar_3)

        # compute hover profile power
        self.P_p_hov = ((self.solidity*self.C_D_p_bar)/8) * self.rho *((self.omega*self.rotor_radius)**3)*(self.pi*(self.rotor_radius**2)) * self.rotorsizing.N_rotors

        # compute forward flight profile power
        self.P_p = self.P_p_hov*(1 + 4.65*(self.AV**2))

        ## parasitic power calculation
        self.P_par = 0.5*self.A_eq*self.rho*(self.V_point**3)
        #parasitic drag
        self.D_par = self.P_par / self.V_point

        ## induced power calculation
        self.T = self.rotorsizing.T_forward_flight
        self.v_i_hov = np.sqrt((self.MTOW_N / self.rotorsizing.N_rotors)/(2*self.rho*self.pi*(self.rotor_radius**2)))
        self.V_bar = self.V_point / self.v_i_hov
        self.alpha = math.asin((self.D_par/self.MTOW_N) + math.sin(math.radians(self.gamma_CD)))
        array = np.array([0.0,0.0,0.0,0.0,0.0])
        array[0] = 1
        array[1] = 2*self.V_bar*math.sin(self.alpha)
        array[2] = (self.V_bar**2)
        array[3] = 0
        array[4] = -1
        self.roots = np.roots(array)[3]
        self.v_i_bar = np.real(self.roots) #aanname
        self.v_i = self.v_i_bar*self.v_i_hov

        #compute induced power
        self.P_i = self.k_int * self.k * self.T * self.v_i 

        ## total power
        self.P_total_level_loss = self.P_p + self.P_i + self.P_par

        # account for losses
        self.P_total_level = 1.045*self.P_total_level_loss

        ## compute climb/descent power
        #1.045 is a drag to fuselage kinda constant. 
        self.ROC_CD = self.V_point * math.sin(math.radians(self.gamma_CD))
        self.P_CD_loss = self.MTOW_N * self.ROC_CD
        self.P_CD = self.P_CD_loss * 1.045

        ## total power (including climb/descent)
        self.P_total_CD = self.P_total_level + self.P_CD

        #steep descent
        self.P_CD_loss_steep = self.MTOW_N * self.ROC_CD_steep
        self.P_CD_steep = self.P_CD_loss_steep * 1.045
        ## total power steep descent (including climb/descent)
        self.P_total_CD_steep = self.P_total_level + self.P_CD_steep


        ## compute climb/descent power
        #1.045 is a drag to fuselage kinda constant. 
        self.ROC_descent = self.V_point * math.sin(math.radians(self.gamma_descent))
        self.P_CD_loss_descent = self.MTOW_N * self.ROC_descent
        self.P_CD_descent = self.P_CD_loss_descent * 1.045

        ## total power (including climb/descent)
        self.P_total_descent = self.P_total_level + self.P_CD_descent

        ## hover power; what is this?? changed it to momentum theory (james wang adn stepiniewski)
        #self.P_hoge = self.k_int * self.k * self.T * self.v_i_hov + self.P_p_hov

        self.P_hoge = self.k_int * self.k * self.v_i_hov * self.T + self.P_p_hov

        #self.P_vertical_climb =  (self.MTOW_N / self.rotorsizing.N_rotors)*((self.vertical_climb / 2) + np.sqrt((self.vertical_climb / 2)**2 + ((self.MTOW_N / self.rotorsizing.N_rotors)) / (2 * self.rho * self.pi*(self.rotor_radius**2)))) 
        self.P_vertical_climb = self.P_hoge + (self.MTOW_N * self.vertical_climb)/2 
        #self.P_vertical_descent =  (self.MTOW_N / self.rotorsizing.N_rotors)*((self.vertical_descent / 2) + np.sqrt((self.vertical_descent / 2)**2 + ((self.MTOW_N / self.rotorsizing.N_rotors)) / (2 * self.rho * self.pi*(self.rotor_radius**2))))
        self.P_vertical_descent = self.P_hoge + (self.MTOW_N * self.vertical_descent)/2
        #print(f'P_req for vertical climb = {self.P_vertical_climb / 1000:.2f}kW')
        #print(f'P_req for vertical descent = {self.P_vertical_descent / 1000:.2f}kW')

        ## vertical climb/descent power
        #self.P_VCD = self.P_hoge + self.ROC_VCD*self.MTOW_N


    def iterate_design(self, new_MTOW_N=None, new_V_point=None, new_solidity=None, new_gamma_CD=None, new_rho=None, new_ROC_VCD=None, new_min_power_velocity_CD = None, new_min_power_velocity = None, new_min_power_velocity_descent = None, new_gamma_descent = None):
        if new_MTOW_N:
            self.MTOW_N = new_MTOW_N
        if new_V_point:
            self.V_point = new_V_point
        if new_solidity:
            self.solidity = new_solidity
        if new_gamma_CD:
            self.gamma_CD = new_gamma_CD
        if new_rho:
            self.rho = new_rho
        if new_ROC_VCD:
            self.ROC_VCD = new_ROC_VCD


        self.forward_flight()

    def display_parameters(self):
        print("----------------")


    def plot_power_components(self):
        V = np.linspace(0.01, 85, 1000)
        AV = []
        P_p = []
        P_i = []
        P_par = []
        P_total_level = []
        P_CD = []
        P_total_CD = []
        P_hoge = []
        P_total_CD_steep = []
        P_total_descent = []

        for velocity in V:
            self.iterate_design(new_V_point=velocity)
            AV.append(velocity / (self.omega * self.rotor_radius))
            P_p.append(self.P_p / 1000)
            P_i.append(self.P_i / 1000)
            P_par.append(self.P_par / 1000)
            P_total_level.append(self.P_total_level / 1000)
            P_CD.append(self.P_CD / 1000)
            P_total_CD.append(self.P_total_CD / 1000)
            P_hoge.append(self.P_hoge / 1000)
            P_total_CD_steep.append(self.P_total_CD_steep / 1000)
            P_total_descent.append(self.P_total_descent / 1000)

        # Identify velocity corresponding to minimum flight-level power
        self.min_power = min(P_total_level)
        self.min_power_watts = self.min_power * 1000
        self.min_power_velocity = V[P_total_level.index(self.min_power)]
        print(f"The velocity corresponding to the minimum flight-level power {self.min_power:.2f} kW is {self.min_power_velocity:.2f} m/s")

        #steep deescent angle
        #self.gamma_CD_steep = math.degrees(math.asin(self.ROC_CD_steep / self.min_power_velocity_CD))

        #climb min power
        self.min_power_CD = min(P_total_CD)
        self.min_power_CD_watts = self.min_power_CD * 1000
        self.min_power_velocity_CD = V[P_total_CD.index(self.min_power_CD)] # velocity of climb 1

        #second descent min power
        self.min_power_descent = min(P_total_descent)
        self.min_power_descent_watts = self.min_power_descent * 1000
        self.min_power_velocity_descent = V[P_total_descent.index(self.min_power_descent)] # second descent velocity

        self.power_steep_descent = P_total_CD_steep[V.tolist().index(self.min_power_velocity_CD)] # same velocity as climb 1
        self.power_steep_descent_watts = self.power_steep_descent * 1000

        #print(f"The velocity corresponding to the minimum climb power ({self.min_power_CD:.2f} kW) is {self.min_power_velocity_CD:.2f} m/s")
        plt.scatter(self.min_power_velocity_CD, self.min_power_CD, color='green', label='Climb Min. Power', zorder=5)
        plt.annotate(f'({self.min_power_velocity_CD:.2f} m/s, {self.min_power_CD:.2f} kW)',
                 (self.min_power_velocity_CD, self.min_power_CD),
                 textcoords="offset points",
                 xytext=(-30, 10),
                 ha='center',
                 fontsize=9,
                 color='green')
        
        plt.scatter(self.min_power_velocity_CD, self.power_steep_descent, color='purple', label='Descent Min. Power', zorder=5)
        plt.annotate(f'({self.min_power_velocity_CD:.2f} m/s, {self.power_steep_descent:.2f} kW)',
                 (self.min_power_velocity_CD, self.power_steep_descent),
                 textcoords="offset points",
                 xytext=(-30, 10),
                 ha='center',
                 fontsize=9,
                 color='purple')
        
        plt.scatter(self.min_power_velocity_descent, self.min_power_descent, color='yellow', label='Second descent min. Power', zorder=5)
        plt.annotate(f'({self.min_power_velocity_descent:.2f} m/s, {self.min_power_descent:.2f} kW)',
                 (self.min_power_velocity_descent, self.min_power_descent),
                 textcoords="offset points",
                 xytext=(-30, 10),
                 ha='center',
                 fontsize=9,
                 color='yellow')

        #plt.plot(V, P_p, label="Profile drag power", linestyle='-', color='b')
        #plt.plot(V, P_i, label="Induced power", linestyle='--', color='c')
        #plt.plot(V, P_par, label="Parasitic power", linestyle='-.', color='r')
        plt.plot(V, P_total_level, label="Total power (level flight)", linestyle='-', color='k')

        plt.plot(V, P_hoge, label="Power HOGE", linestyle=':', color='purple')

        # plotting min power point
        plt.scatter(self.min_power_velocity, self.min_power, color='red', label='Level Flight Min. Power', zorder=5)
        plt.annotate(f'({self.min_power_velocity:.2f} m/s, {self.min_power:.2f} kW)',
                 (self.min_power_velocity, self.min_power),
                 textcoords="offset points",
                 xytext=(-30, 10),
                 ha='center',
                 fontsize=9,
                 color='red')
        


        #plt.text(V[-1], P_p[-1], 'P_p', color='black', va='center', ha='left')
        #plt.text(V[-1], P_i[-1], 'P_i', color='black', va='center', ha='left')
        #plt.text(V[-1], P_par[-1], 'P_par', color='black', va='center', ha='left')
        plt.text(V[-1], P_total_level[-1], 'P_total_level', color='black', va='center', ha='left')
        plt.text(V[-1], P_hoge[-1], 'P_hoge', color='black', va='center', ha='left')
        plt.text(V[-1], P_total_CD_steep[-1], 'P_steep_descent', color='black', va='center', ha='left')
        plt.text(V[-1], P_total_descent[-1], 'P_second_descent', color='black', va='center', ha='left')

        #plt.plot(V, P_CD, label=f'Climb power ($\gamma$ = {self.gamma_CD}$^\circ$)', linestyle='-', color='m')
        plt.plot(V, P_total_CD, linestyle=':', label='Total power (climbing flight)', color='k')

        plt.plot(V, P_total_CD_steep, linestyle=':', label='Steep descent power', color='green')

        plt.plot(V, P_total_descent, linestyle='-', label='Second descent power', color='purple')

        #plt.text(V[-1], P_CD[-1], 'P_C', color='black', va='center', ha='left')
        plt.text(V[-1], P_total_CD[-1], 'P_total_CD', color='black', va='center', ha='left')

        #plt.axvline(x=0.4569090434, color='gray', linestyle='-', linewidth=1, label='Never Exceed AV')

        plt.title("Power Components vs. Advance Ratio")
        plt.legend(loc='upper left', fontsize='large')
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Velocity [m/s]")
        plt.ylabel("Power [kW]")
        plt.show()

    def plot_power_bucket(self): # co-axial by default?
        max_speed_constraint = self.rotorsizing.max_forward_velocity
        max_speed_mu_constraint = 0.4 * self.rotorsizing.tip_speed
        limiting_velocity = min(max_speed_constraint, max_speed_mu_constraint)

        V = np.linspace(0.01, 100, 1000)
        P_profile = []
        P_induced = []
        P_parasitic = []
        P_total = []

        for velocity in V:
            self.iterate_design(new_V_point=velocity)
            P_profile.append(self.P_p / 1000)
            P_induced.append(self.P_i / 1000)
            P_parasitic.append(self.P_par / 1000)
            # add climb power maybe
            P_total.append(self.P_total_level / 1000)
            
        self.min_power = min(P_total)
        self.min_power_velocity = V[P_total.index(self.min_power)]
        
        plt.figure(figsize=(10, 6))
        plt.plot(V, P_profile, label='Profile Power', color='blue')
        plt.plot(V, P_induced, label='Induced Power', color='green')
        plt.plot(V, P_parasitic, label='Parasitic Power', color='black')
        plt.plot(V, P_total, label='Total Power', color='red', linewidth=2)

        plt.scatter(self.min_power_velocity, self.min_power, color='black', label='Min Power', zorder=5)
        plt.axhline(y=self.min_power, color='black', linestyle='--', linewidth=1, label=f'Min Power = {self.min_power:2f} kW')
        plt.axvline(x=self.min_power_velocity, color='black', linestyle='--', linewidth=1, label=f'Min Velocity = {self.min_power_velocity:.2f} m/s')
        plt.axvline(x=limiting_velocity, color='gray', linestyle='--', linewidth=1, label=f'Max Speed = {limiting_velocity} m/s')

        plt.xlabel('Velocity [m/s]', fontsize=12)
        plt.ylabel('Power [kW]', fontsize=12)
        plt.title('Power vs Velocity', fontsize = 16)
        plt.legend(fontsize=10)
        plt.grid(True)

        plt.tight_layout()
        plt.show()


    def final_power(self):
        self.P = {
            'HIGE1': self.P_hoge * self.hige_factor,
            'V_climb': self.P_vertical_climb, #0.76 m/s
            'HOGE1': self.P_hoge,
            'Climb1': self.min_power_CD_watts, # 9deg climb
            'Cruise1': self.min_power_watts,
            'Descent1': self.power_steep_descent_watts, # steep descent, 0 for compound
            'HOGE2': self.P_hoge,
            'Loiter': self.min_power_watts,
            'Climb2': self.min_power_CD_watts, # second climb 
            'Cruise2': self.min_power_watts, 
            'Descent2': self.min_power_descent_watts, # second descent
            'HOGE3': self.P_hoge,
            'V_Descent': self.P_vertical_descent, # 0.5 m/s
            'HIGE2': self.P_hoge * self.hige_factor
        }
        return self.P
    
    def get_highest_power(self):
        # Find the maximum value
        max_key = max(self.P, key=self.P.get)
        max_value = self.P[max_key]

        print(f"The maximum power usage is {max_value / 1000:.2f} [kW], corresponding to {max_key}.")

    def print_all_powers(self):
        # Ensure the final_power method has been called to populate self.P
        if not hasattr(self, 'P'):
            self.final_power()
        
        # Print each power name and value
        for name, power in self.P.items():
            # Ensure correct formatting based on the type of `power`
            if isinstance(power, (int, float)):  # If the value is a number
                print(f"The Power usage is = {power / 1000:.2f} [kW] in {name} phase")
            else:  # For non-numeric types
                print(f"The Power usage in {name} phase is {power}")
    


        print(f"Single rotor SPL: {self.vortex_SPL:.4f} dB")
        print(f"All rotor SPL: {self.vortex_SPL_total:.4f} dB")
        print(f"Vortex frequency: {self.f_vortex:.4f} Hz")