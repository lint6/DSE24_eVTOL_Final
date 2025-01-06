import math
import numpy as np
import matplotlib.pyplot as plt

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

        # rotor inputs, INPUT CORRECT VALUES LATER
        self.rotor_radius = 2 #m
        self.number_of_blades = 4
        self.number_of_rotors = 4
        self.omega = 70 #rad/s
        self.C_l_alpha = 5.73 #1/rad

        # structural inputs, INPUT CORRECT VALUES LATER
        self.A_eq = 0.5

        # mission inputs
        self.gamma_climb = climb_angle #degrees
        self.gamma_descent = descent_angle #degrees
        self.vertical_climb = vertical_climb #m/s
        self.vertical_descent = vertical_descent #m/s
        self.steep_descent = steep_descent #m/s

        # calculated values, CHANGE LATER
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

    def hover_flight(self):
