import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp 

class MDOFVibrationForwardFlight: 

    def __init__(self, L=0.8, E=70, I=1000, T_min=400, T_max=540, C_damp=0.01, m=1, RPM=1000, gust_velocity=19, gust_time=0.0, impulse_duration=0.1, J=1000, G=25):
        self.L = L 
        self.E = E 
        self.I = I 
        self.T_min = T_min 
        self.T_max = T_max 
        self.C_damp = C_damp 
        self.m = m 
        self.RPM = RPM 
        self.gust_velocity = gust_velocity 
        self.gust_time = gust_time 
        self.impulse_duration = impulse_duration 
        self.J = J 
        self.G = G 

    def calculate_equivalent_mass(self):
        return self.m * 1/3