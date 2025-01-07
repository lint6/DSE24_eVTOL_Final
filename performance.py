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

        # this should be lower then the same calculation using pure momentum disk theory
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

        self.forward_flight_powers()

    def plot_power_components(self):
        V = np.linspace(0.01, 85, 1000)
        AV = []
        P_p = []
        P_i = []
        P_par = []
        P_total_level = []
        P_hoge = []

        # P_CD = []
        # P_total_CD = []
        # P_total_CD_steep = []
        # P_total_descent = []

        for velocity in V:
            self.iterate_design(new_V_point=velocity)
            AV.append(self.advance_ratio)
            P_p.append(self.P_p_ff / 1000)
            P_i.append(self.P_i_ff / 1000)
            P_par.append(self.P_par_ff / 1000)
            P_total_level.append(self.P_ff / 1000)
            P_hoge.append(self.P_hoge / 1000)

            # P_CD.append(self.P_CD / 1000)
            # P_total_CD.append(self.P_total_CD / 1000)
            # P_total_CD_steep.append(self.P_total_CD_steep / 1000)
            # P_total_descent.append(self.P_total_descent / 1000)


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

        # plot hoge power
        #plt.plot(V, P_hoge, label="Power HOGE", linestyle=':', color='purple')

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
        plt.title('Power Breakdown at Different Velocities')
        plt.xticks(index, velocities_kmh)
        plt.legend()
        plt.grid(True)

        # Add percentages inside the bars
        for i in range(len(velocities_kmh)):
            plt.text(index[i], profile_power[i] / 2, f'{profile_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)
            plt.text(index[i], profile_power[i] + induced_power[i] / 2, f'{induced_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)
            plt.text(index[i], profile_power[i] + induced_power[i] + parasitic_power[i] / 2, f'{parasitic_power[i] / total_power[i] * 100:.1f}%', ha='center', va='center', color='black', fontsize=8)

        plt.show()




def run():
    # Create an instance of PerformanceAnalysis
    analysis = PerformanceAnalysis()
    
    # Call functions
    analysis.hover_powers()
    analysis.vertical_climb_descent_powers()
    analysis.forward_flight_powers()
    analysis.plot_power_components()
    #analysis.plot_power_pie_chart()
    #analysis.plot_power_breakdown()

    # Print results
    print(f"--------------------------------------")
    print(f"Hover out of ground effect power: {analysis.P_hoge/1000:.2f} kW")
    print(f"--------------------------------------")
    print(f"Vertical climb power: {analysis.P_vertical_climb/1000:.2f} kW")
    print(f"--------------------------------------")
    print(f"Vertical descent power: {analysis.P_vertical_descent/1000:.2f} kW")
    print(f"--------------------------------------")
    print(f"The velocity corresponding to the minimum flight-level power {analysis.min_power:.2f} kW is {analysis.min_power_velocity*3.6:.2f} km/h")
    print(f"--------------------------------------")
    print(f"The corresponding induced power is {analysis.min_power_induced/1000:.2f} kW")
    print(f"--------------------------------------")
    print(f"The corresponding profile power is {analysis.min_power_profile/1000:.2f} kW")
    print(f"--------------------------------------")
    print(f"The corresponding parasitic power is {analysis.min_power_parasitic/1000:.2f} kW")




# Execute the run function
if __name__ == "__main__":
    run()
