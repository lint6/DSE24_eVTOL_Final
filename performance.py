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
        self.A_eq = 0.75

        # mission inputs
        self.gamma_climb = climb_angle #degrees
        self.gamma_descent = descent_angle #degrees
        self.vertical_climb = vertical_climb #m/s
        self.vertical_descent = vertical_descent #m/s
        self.steep_descent = steep_descent #m/s

        self.V_point = 13 # m/s, random assumed cruise speed

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


    def hover_powers(self):

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

        self.P_i_hov = self.MTOW_N * self.v_i_hov # k factor is 1 as rotors are away from fuselage, assumed that Thrust = Weight; TODO: CHANGE WHEN ROTOR IS FINISHED

        # profile power
        self.C_D_p_bar = 0.02 # TODO: CHANGE LATER based on airfoil tools

        self.P_p_hov = ((self.solidity*self.C_D_p_bar)/8) * self.rho *((self.omega*self.rotor_radius)**3)*(self.pi*(self.rotor_radius**2)) * self.number_of_rotors

        self.P_hoge = self.P_i_hov + self.P_p_hov

    def vertical_climb_descent_powers(self):
        # vertical climb and descent powers
        self.P_vertical_climb = self.P_hoge + (self.MTOW_N * self.vertical_climb) / 2  # diktaat
        self.P_vertical_descent = self.P_hoge + (self.MTOW_N * self.vertical_descent) / 2  # diktaat

    def forward_flight_powers(self):

        self.advance_ratio = self.V_point / (self.rotor_radius * self.omega) # advance ratio

        # Parasitic power
        self.P_par_ff = self.A_eq * 0.5 * self.rho * self.V_point**3 # TODO: UPDATE A_eq

        # Induced power
        self.T = self.MTOW_N
        self.V_bar = self.V_point / self.v_i_hov
        self.D_par = self.P_par_ff / self.V_point
        self.alpha = math.asin((self.D_par/self.MTOW_N) + math.sin(math.radians(self.gamma_climb)))
        array = np.array([0.0,0.0,0.0,0.0,0.0])
        array[0] = 1
        array[1] = 2*self.V_bar*math.sin(self.alpha)
        array[2] = (self.V_bar**2)
        array[3] = 0
        array[4] = -1
        self.roots = np.roots(array)[3]
        self.v_i_bar = np.real(self.roots) 
        self.v_i_ff = self.v_i_bar*self.v_i_hov

        self.P_i_ff = self.T * self.v_i_ff

        # Profile + Drag power
        self.P_p_ff = self.P_p_hov * (1 + 4.65*(self.advance_ratio**2)) # TODO: LOOK FOR A BETTER VALUE THAN 4.65

        # Total power
        self.P_ff = self.P_par_ff + self.P_i_ff + self.P_p_ff

    def climb_descent_powers(self):	

        # climb power
        self.ROC = self.V_point * math.tan(math.radians(self.gamma_climb)) # rate of climb
        self.P_loss_climb = self.MTOW_N * self.ROC # power loss due to climb
        self.P_climb = self.P_loss_climb * 1.045 # TODO: CHECK THIS FACTOR

        self.P_total_climb = self.P_ff + self.P_climb

        # descent power
        self.ROC_descent = self.V_point * math.tan(math.radians(self.gamma_descent)) # rate of descent
        self.P_loss_descent = self.MTOW_N * self.ROC_descent # power loss due to descent
        self.P_descent = self.P_loss_descent * 1.045 # TODO: CHECK THIS FACTOR

        self.P_total_descent = self.P_ff + self.P_descent

        # steep descent power
        self.P_loss_steep_descent = self.MTOW_N * self.steep_descent # power loss due to steep descent
        self.P_steep_descent = self.P_loss_steep_descent * 1.045 # TODO: CHECK THIS FACTOR

        self.P_total_steep_descent = self.P_ff + self.P_steep_descent

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

        self.hover_powers()
        self.vertical_climb_descent_powers()    
        self.forward_flight_powers()
        self.climb_descent_powers()

    def plot_forward_flight(self):
        V = np.linspace(0.01, 85, 1000)
        AV = []
        P_p = []
        P_i = []
        P_par = []
        P_total_level = []
        P_hoge = []

        for velocity in V:
            self.iterate_design(new_V_point=velocity)
            AV.append(self.advance_ratio)
            P_p.append(self.P_p_ff / 1000)
            P_i.append(self.P_i_ff / 1000)
            P_par.append(self.P_par_ff / 1000)
            P_total_level.append(self.P_ff / 1000)
            P_hoge.append(self.P_hoge / 1000)


        # Identify velocity corresponding to minimum flight-level power
        self.min_power = min(P_total_level)
        self.min_power_watts = self.min_power * 1000
        self.min_power_velocity = V[P_total_level.index(self.min_power)]

        # Find the induced power corresponding to the min_power_velocity
        self.min_power_induced = P_i[V.tolist().index(self.min_power_velocity)] * 1000

        # Find the profile power corresponding to the min_power_velocity
        self.min_power_profile = P_p[V.tolist().index(self.min_power_velocity)] * 1000

        # Find the parasitic power corresponding to the min_power_velocity
        self.min_power_parasitic = P_par[V.tolist().index(self.min_power_velocity)] * 1000

        # plot forward flight powers
        plt.plot(V, P_p, label="Profile drag power", linestyle='-', color='b', linewidth=1)
        plt.plot(V, P_i, label="Induced power", linestyle='-', color='c', linewidth=1)
        plt.plot(V, P_par, label="Parasitic power", linestyle='-', color='r', linewidth=1)
        plt.plot(V, P_total_level, label="Total power (level flight)", linestyle='-', color='k', linewidth=2)
        plt.scatter(self.min_power_velocity, self.min_power, color='red', label=f'Min Forward Flight Power: ({self.min_power_velocity*3.6:.2f} km/h, {self.min_power:.2f} kW)')
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Power (kW)')
        plt.title('Level Flight Power Components vs Velocity')
        plt.legend(loc='best', fontsize='small')
        plt.grid(True)
        plt.show()

    def plot_CD_power(self):

        V = np.linspace(0.01, 85, 1000)
        AV = []
        P_total_CD = []
        P_total_descent = []
        P_total_CD_steep = []

        for velocity in V:
            self.iterate_design(new_V_point=velocity)
            AV.append(self.advance_ratio)
            P_total_CD.append(self.P_total_climb / 1000)
            P_total_descent.append(self.P_total_descent / 1000)
            P_total_CD_steep.append(self.P_total_steep_descent / 1000)

        # plot climb and descent in forward flight

        # Identify velocity corresponding to minimum climb power
        self.min_power_climb = min(P_total_CD)
        self.min_power_climb_watts = self.min_power_climb * 1000
        self.min_power_velocity_climb = V[P_total_CD.index(self.min_power_climb)]

        # Identify velocity corresponding to minimum descent power
        self.min_power_descent = min(P_total_descent)
        self.min_power_descent_watts = self.min_power_descent * 1000
        self.min_power_velocity_descent = V[P_total_descent.index(self.min_power_descent)]

        # Identify velocity corresponding to minimum steep descent power
        self.power_steep_descent = P_total_CD_steep[V.tolist().index(self.min_power_velocity_climb)]
        self.power_steep_descent_watts = self.power_steep_descent * 1000
        self.power_velocity_steep_descent = self.min_power_velocity_climb

        # Plot climb, descent, and steep descent powers in the same graph
        plt.figure()
        plt.plot(V, P_total_CD, label="Total power (climb)", linestyle='-', color='g', linewidth=1.5)
        plt.plot(V, P_total_descent, label="Total power (descent)", linestyle='-', color='orange', linewidth=1.5)
        plt.plot(V, P_total_CD_steep, label="Total power (steep descent)", linestyle='-', color='purple', linewidth=1.5)
        plt.scatter(self.min_power_velocity_climb, self.min_power_climb, color='blue', label=f'Min Climb Power: ({self.min_power_velocity_climb*3.6:.2f} km/h, {self.min_power_climb:.2f} kW)')
        plt.scatter(self.min_power_velocity_descent, self.min_power_descent, color='green', label=f'Min Descent Power: ({self.min_power_velocity_descent*3.6:.2f} km/h, {self.min_power_descent:.2f} kW)')
        plt.scatter(self.power_velocity_steep_descent, self.power_steep_descent, color='purple', label=f'Min Steep Descent Power: ({self.power_velocity_steep_descent*3.6:.2f} km/h, {self.power_steep_descent:.2f} kW)')
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Power (kW)')
        plt.title('Climb, Descent, and Steep Descent Power Components vs Velocity')
        plt.legend(loc='best', fontsize='small')
        plt.grid(True)
        plt.show()

    def plot_power_pie_chart(self):
        # Draw a pie chart showing the composition of the total level flight power
        labels = [
            f'Induced Power: {self.min_power_induced/1000:.2f} kW', 
            f'Parasitic Power: {self.min_power_parasitic/1000:.2f} kW', 
            f'Profile Power: {self.min_power_profile/1000:.2f} kW',
            f'Total Power: {self.min_power:.2f} kW'
        ]
        sizes = [self.min_power_induced, self.min_power_parasitic, self.min_power_profile]
        colors = ['c', 'r', 'b']
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels[:-1], colors=colors, autopct=lambda p: f'{p:.1f}%\n({p * sum(sizes) / 100 / 1000:.2f} kW)', startangle=140, textprops={'color': 'w'})
        plt.title('Composition of Total Level Flight Power')
        plt.legend(labels, loc="upper center", bbox_to_anchor=(0.5, 0.1), ncol=1)
        plt.show()

    def plot_power_breakdown(self):

        # Power Breakdown at Different Velocities
        velocities = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80]  # velocities in m/s
        profile_power = []
        induced_power = []
        parasitic_power = []
        total_power = []

        for velocity in velocities:
            self.iterate_design(new_V_point=velocity)
            profile_power.append(self.P_p_ff / 1000)  # convert to kW
            induced_power.append(self.P_i_ff / 1000)  # convert to kW
            parasitic_power.append(self.P_par_ff / 1000)  # convert to kW
            total_power.append(self.P_ff / 1000)  # convert to kW

        velocities_kmh = [v * 3.6 for v in velocities]  # convert velocities to km/h

        plt.figure()
        bar_width = 0.35
        index = np.arange(len(velocities_kmh))
        p1 = plt.bar(index, profile_power, bar_width, label='Profile Power')
        p2 = plt.bar(index, induced_power, bar_width, bottom=profile_power, label='Induced Power')
        p3 = plt.bar(index, parasitic_power, bar_width, bottom=np.array(profile_power) + np.array(induced_power), label='Parasitic Power')
        plt.plot(index, total_power, label='Total Power', color='grey', linestyle='-', linewidth=2, alpha=0.7)

        plt.xlabel('Velocity (km/h)')
        plt.ylabel('Power (kW)')
        plt.title('Power Breakdown at Different Velocities in Forward Flight')
        plt.xticks(index, velocities_kmh)
        plt.legend()
        plt.grid(True)

        # Add percentages inside the bars
        for i in range(len(velocities_kmh)):
            plt.text(index[i], profile_power[i] / 2, f'{profile_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)
            plt.text(index[i], profile_power[i] + induced_power[i] / 2, f'{induced_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)
            plt.text(index[i], profile_power[i] + induced_power[i] + parasitic_power[i] / 2, f'{parasitic_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)

        plt.show()

    def print_results(self):
        # Create a table of flight phases and corresponding power usage, vertical speed, and horizontal speed
        flight_phases = ["HOGE","Vertical Climb", "Vertical Descent", "Forward Flight", "Angled Climb", "Angled Descent", "Steep Descent"]
        power_usage = [
            f"{self.P_hoge/1000:.2f}",
            f"{self.P_vertical_climb/1000:.2f}",
            f"{self.P_vertical_descent/1000:.2f}",
            f"{self.min_power:.2f}",
            f"{self.min_power_climb:.2f}",
            f"{self.power_steep_descent:.2f}",
            f"{self.min_power_descent:.2f}"
        ]
        vertical_speed = [
            "0.00",
            f"{self.vertical_climb:.2f}",
            f"{self.vertical_descent:.2f}",
            "0.00",
            f"{self.ROC:.2f}",
            f"{self.steep_descent:.2f}",
            f"{self.ROC_descent:.2f}",
        ]
        horizontal_speed = [
            "0.00",
            "0.00",
            "0.00",
            f"{self.min_power_velocity:.2f}",
            f"{self.min_power_velocity_climb:.2f}",
            f"{self.power_velocity_steep_descent:.2f}",
            f"{self.min_power_velocity_descent:.2f}"
        ]
        horizontal_speed_kmh = [
            "0.00",
            "0.00",
            "0.00",
            f"{self.min_power_velocity*3.6:.2f}",
            f"{self.min_power_velocity_climb*3.6:.2f}",
            f"{self.power_velocity_steep_descent*3.6:.2f}",
            f"{self.min_power_velocity_descent*3.6:.2f}"
        ]

        print(f"{'Flight Phase':<20} | {'Power Usage [kW]':<20} | {'Vertical Speed [m/s]':<20} | {'Horizontal Speed [m/s]':<20} | {'Horizontal Speed [km/h]':<20}")
        print(f"{'-'*109}")
        for phase, power, v_speed, h_speed, h_speed_kmh in zip(flight_phases, power_usage, vertical_speed, horizontal_speed, horizontal_speed_kmh):
            print(f"{phase:<20} | {power:<20} | {v_speed:<20} | {h_speed:<20} | {h_speed_kmh:<20}")


        # Print results seperately (not table)

        # print(f"--------------------------------------")
        # print(f"\033[1mVertical flight results:\033[0m")
        # print(f"Hover out of ground effect power: {self.P_hoge/1000:.2f} kW")
        # print(f"Vertical climb power: {self.P_vertical_climb/1000:.2f} kW")
        # print(f"Vertical descent power: {self.P_vertical_descent/1000:.2f} kW")
        # print(f"--------------------------------------")
        # print(f"\033[1mForward level flight results:\033[0m")
        # print(f"The velocity corresponding to the minimum flight-level power {self.min_power:.2f} kW is {self.min_power_velocity*3.6:.2f} km/h")
        # print(f"The corresponding induced power is {self.min_power_induced/1000:.2f} kW")
        # print(f"The corresponding profile power is {self.min_power_profile/1000:.2f} kW")
        # print(f"The corresponding parasitic power is {self.min_power_parasitic/1000:.2f} kW")
        # print(f"--------------------------------------")
        # print(f"\033[1mClimb and descent results:\033[0m")
        # print(f"The velocity corresponding to the minimum climb power {self.min_power_climb:.2f} kW is {self.min_power_velocity_climb*3.6:.2f} km/h")
        # print(f"The velocity corresponding to the minimum descent power {self.min_power_descent:.2f} kW is {self.min_power_velocity_descent*3.6:.2f} km/h")
        # print(f"The velocity corresponding to the minimum steep descent power {self.power_steep_descent:.2f} kW is {self.power_velocity_steep_descent*3.6:.2f} km/h")

    def final_power(self):

        self.hige_factor = 0.7 # TODO: CHANGE LATER

        self.P = {
            'HIGE1': self.P_hoge * self.hige_factor,
            'V_climb': self.P_vertical_climb, #0.76 m/s
            'HOGE1': self.P_hoge,
            'Climb1': self.min_power_climb_watts, # 9deg climb
            'Cruise1': self.min_power_watts,
            'Descent1': self.power_steep_descent_watts, # steep descent, 0 for compound
            'HOGE2': self.P_hoge,
            'Loiter': self.min_power_watts,
            'Climb2': self.min_power_climb_watts, # second climb 
            'Cruise2': self.min_power_watts, 
            'Descent2': self.min_power_descent_watts, # second descent
            'HOGE3': self.P_hoge,
            'V_Descent': self.P_vertical_descent, # 0.5 m/s
            'HIGE2': self.P_hoge * self.hige_factor
        }
        return self.P
    

class EnergyAnalysis:
    def __init__(self, performance = None, eta_p=0.9, Volts=840, motor_eta=0.85):
        
        # Initialize the Power object
        #self.rotorsizing = rotorsizing if rotorsizing else RotorSizing()
        self.performance = performance if performance else PerformanceAnalysis()

        #self.power = PowerAnalysis(rotorsizing)

        # Assigning the input parameters
        self.Vroc = self.performance.vertical_climb # vertical climb velocity
        self.eta_p = eta_p # what is this
        self.rho = self.performance.rho
        self.Volts = Volts # max volts of the system ig?
        self.V_climb1 = self.performance.min_power_velocity_climb # first climb velocity 
        self.V_cruise = self.performance.min_power_velocity # cruise velocity 
        self.V_loiter = self.performance.min_power_velocity # loiter velocity 
        self.V_descent = self.performance.min_power_velocity_descent #input descent velocity 
        self.V_climb2 = self.performance.min_power_velocity_climb  # second climb velocity, same as for climb 1
        self.motor_eta = motor_eta  # motor efficiency i think
        self.gamma_1 = self.performance.gamma_climb  # climb angle 
        self.gamma_2 = self.performance.gamma_descent # descent angle
        
        # Create a dictionary to hold times, powers, energies, and amps
        self.mission_data = {
            'times': { 'HIGE1': None, 'V_climb': None, 'HOGE1': None, 'Climb1': None, 'Cruise1': None, 'Descent1': None, 'HOGE2': None, 
                      'Loiter': None, 'Climb2': None, 'Cruise2': None, 'Descent2': None, 'HOGE3': None, 'V_Descent': None, 'HIGE2': None, 'total': None },
            'powers': self.performance.P,
            'energies': { 'HIGE1': None, 'V_climb': None, 'HOGE1': None, 'Climb1': None, 'Cruise1': None, 'Descent1': None, 'HOGE2': None, 
                          'Loiter': None, 'Climb2': None, 'Cruise2': None, 'Descent2': None, 'HOGE3': None, 'V_Descent': None, 'HIGE2': None, 'total': None },
            'amps': { 'HIGE1': None, 'V_climb': None, 'HOGE1': None, 'Climb1': None, 'Cruise1': None, 'Descent1': None, 'HOGE2': None, 
                      'Loiter': None, 'Climb2': None, 'Cruise2': None, 'Descent2': None, 'HOGE3': None, 'V_Descent': None, 'HIGE2': None, 'max': None }
        }
    
    def calculate_missionphase_time(self):
        # Define given constants
        h1, h2, h3 = 60.0, 300.0, 30.0  # Altitudes (m)
        delta_h2 = h2 - h1
        delta_h3 = h2 - h3
        d_tothalf = 30000  # Distance to half
        
        # Calculate times using loops
        times_dict = self.mission_data['times']
        
        # HIGE 1 time
        times_dict['HIGE1'] = 15 
        
        # Vertical Climb time (T2)
        times_dict['V_climb'] = h1 / self.Vroc
        
        # HOGE 1 time
        times_dict['HOGE1'] = 10
        
        # Steady Climb 1 time (T4)
        #!!!!!!!is the climb velocity the horizontal velocity? if not, change this
        d_cl1 = delta_h2 / np.tan(np.radians(self.gamma_1))
        times_dict['Climb1'] = d_cl1 / self.V_climb1
        
        # Descent 1 time (T6)
        roc_descent = 7.6 # m/s
        times_dict['Descent1'] = delta_h3 / roc_descent

        # Cruise 1 time (T5)
        d_cr1 = d_tothalf - d_cl1 - (self.V_climb1 * times_dict['Descent1'])
        times_dict['Cruise1'] = d_cr1 / self.V_cruise
        
        # HOGE 2 time
        times_dict['HOGE2'] = 30
        
        # Loiter time
        times_dict['Loiter'] = 1800 # Dependent on max endurance
        
        # Steady Climb 2 time (T9)
        d_cl2 = delta_h3 / np.tan(np.radians(self.gamma_1))
        times_dict['Climb2'] = d_cl2 / self.V_climb2
        
        # Descent 2 time (T11)
        d_des2 = delta_h2 / np.tan(np.radians(self.gamma_2))
        times_dict['Descent2'] = abs(d_des2) / self.V_descent

        # Cruise 2 time (T10)
        d_cr2 = d_tothalf - d_cl2 - (self.V_descent * times_dict['Descent2'])
        times_dict['Cruise2'] = d_cr2 / self.V_cruise
        
        # HOGE 3 time
        times_dict['HOGE3'] = 10
        
        # Vertical Descent time (T13)
        Vrod = 0.5
        times_dict['V_Descent'] = h1 / Vrod
        
        # HIGE 2 time
        times_dict['HIGE2'] = 15
        
        # Total time
        # Initialize sum to 0
        total_time = 0
        # Iterate through the 'times' dictionary and sum values excluding 'total'
        for key, value in self.mission_data['times'].items():
            if key != 'total' and value is not None:
                total_time += value
    
        #total_time = sum(times_dict.values()[:-1]) 
        times_dict['total'] = total_time
        
        # Update mission data
        self.mission_data['times'] = times_dict

        return self.mission_data['times']
    
    def calculate_energy_required(self):
        energies_dict = self.mission_data['energies']
        times_dict = self.mission_data['times']
        
        for phase, time in times_dict.items():
            if phase != 'total':
                # Calculate energy (Wh)
                power = self.performance.P.get(phase, 0)
                energies_dict[phase] = (time / 3600) * power / self.motor_eta
        
        # Calculate total energy
        # Initialize sum to 0
        total_energy = 0

        # Iterate through the 'energies' dictionary and sum values excluding 'total'
        for key, value in self.mission_data['energies'].items():
            if key != 'total' and value is not None:
                total_energy += value

        energies_dict['total'] = total_energy
        
        # Update mission data
        self.mission_data['energies'] = energies_dict

        return self.mission_data['energies']
    
    def calculate_amps(self):
        amps_dict = self.mission_data['amps']
        powers_dict = self.performance.P
        
        for phase, power in powers_dict.items():
            amps_dict[phase] = power / (self.Volts * self.motor_eta)
        
        #amps_dict['max'] = max(amps_dict.values())
        # Initialize max_amps to store the maximum value
        max_amps = None

        # Iterate through the 'amps' dictionary, excluding 'max' and None values
        for key, value in self.mission_data['amps'].items():
            if key != 'max' and value is not None:
                if max_amps is None or value > max_amps:
                    max_amps = value

        amps_dict['max'] = max_amps
        # Update mission data
        self.mission_data['amps'] = amps_dict

        return self.mission_data['amps']

    def visual_PEMFC_power(self):
        self.performance.final_power()
        power_per_phase = self.performance.P
        time_per_phase = self.calculate_missionphase_time()

        phases = list(power_per_phase.keys())
        power_values = list(power_per_phase.values())
        time_values = [int(time) for time in time_per_phase.values()]
        
        # remove 'total' in time_values
        time_values = time_values[:-1]

        # calculate bar positions and widths
        bar_positions = []
        widths = []
        start_time = 0
        for time in time_values:
            bar_positions.append(start_time)
            widths.append(time)
            start_time += time

        # define average and peak power
        average_power = sum(power_values) / len(power_values)
        peak_power = max(power_values)

        colors = ['black', 'lightgreen', 'black', 'lightcoral', 'skyblue', 
                'silver', 'black', 'skyblue', 'lightcoral', 'skyblue', 
                'purple', 'black', 'pink', 'black']

        # create bar plot
        plt.bar(bar_positions, power_values, width=widths, align='edge', color=colors, edgecolor='black', alpha=0.9)

        # average and peak power lines
        plt.axhline(average_power, color='red', linestyle='--', label=f'Average Power ({average_power:.2f} W)')
        plt.axhline(peak_power, color='blue', linestyle='--', label=f'Peak Power ({peak_power:.2f} W)')

        # labels and title
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Power (W)', fontsize=12)
        plt.title('Power vs Time for Mission Phases', fontsize=14)

        # legend
        for i, phase in enumerate(phases):
            plt.bar(0, 0, color=colors[i], label=phase)  # Dummy bars for legend
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, title="Phases")
    
        # show the plot
        plt.tight_layout()
        plt.show()

    def visual_PEMFC_energy(self):
        self.performance.final_power()
        energy_per_phase = self.calculate_energy_required()

        # phase and energy values
        phases = list(energy_per_phase.keys())
        energy_values = list(energy_per_phase.values())

        # remove 'total' in phases and energy values
        phases = phases[:-1]
        energy_values = energy_values[:-1]

        print(f'Phases: {phases}')
        print(f'Phases length: {len(phases)}')
        print(f'Energy Values length: {len(energy_values)}')

        # sizing the bars
        bar_positions = range(len(phases)) 
        bar_width = 0.8

        colors = [
            'skyblue', 'skyblue', 'skyblue', 'skyblue', 'skyblue', 
            'skyblue', 'skyblue', 'skyblue', 'skyblue', 'skyblue', 
            'skyblue', 'skyblue', 'skyblue', 'skyblue'
        ]

        # bar plot
        plt.bar(bar_positions, energy_values, width=bar_width, color=colors, edgecolor='black', alpha=0.9)
        
        # labels and title
        plt.xlabel('Mission Phase', fontsize=12)
        plt.ylabel('Energy (Wh)', fontsize=12)
        plt.title('Energy vs Mission Phase', fontsize=14)
        plt.xticks(bar_positions, phases, rotation=45, ha='right', fontsize=10)

        # show the plot
        plt.tight_layout()
        plt.show()


def run():

    print(f"------------------------------------------------------")
    print(f"\033[1mPerformance Analysis:\033[0m")
    # Create an instance of PerformanceAnalysis
    analysis = PerformanceAnalysis()
    
    # Call functions
    analysis.hover_powers()
    analysis.vertical_climb_descent_powers()
    analysis.forward_flight_powers()

    # Plot
    analysis.plot_forward_flight()
    analysis.plot_CD_power()
    analysis.plot_power_pie_chart()
    analysis.plot_power_breakdown()

    # Print
    analysis.print_results()

    # Final power
    analysis.final_power()

    print(f"------------------------------------------------------")
    print(f"\033[1mEnergy Analysis:\033[0m")


    # Instantiate the EnergyAnalysis class
    energy_analysis = EnergyAnalysis(performance=analysis)

    # Calculate mission phase times
    times = energy_analysis.calculate_missionphase_time()

    # Calculate energies
    energies = energy_analysis.calculate_energy_required()

    # Calculate amps
    amps = energy_analysis.calculate_amps()

    #print("Mission Phase Times:")
    #print(times)
    total_time = times['total']/60
    print(f'Total Mission time = {total_time:.2f} [min]')

    #print("\nMission Energies (Wh):")
    #print(energies)
    total_energy = energies['total']
    loiter_energy = energies['Loiter']
    loiter_time = times['Loiter']/60
    print(f'Total Energy Consumption = {total_energy:.2f} [Wh]')

    print(f'Loiter power required = {analysis.min_power:.2f} [kW] at a speed of {analysis.min_power_velocity*3.6:.2f} [km/h]')
    print(f'Loiter time = {loiter_time} [min]')
    print(f'Energy Consumption during loiter = {loiter_energy:.2f} [Wh]')

    #print("\nMission Amps:")
    #print(amps)
    max_amps = amps['max']
    print(f'Max amps = {max_amps:.2f} [A]')

    # plot the PEMFC power vs mission phase/time
    #energy_analysis.visual_PEMFC_power()
    #energy_analysis.visual_PEMFC_energy()

# Execute the run function
if __name__ == "__main__":
    run()
