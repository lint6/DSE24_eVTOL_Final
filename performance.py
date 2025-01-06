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
