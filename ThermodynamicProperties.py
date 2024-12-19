import numpy as np
import matplotlib.pyplot as plt

#Code written by Jorrit
#To calculate C_p and gamma of air at different temperatures. Need to actually integrate this to replace placeholder C_p and gamma values. 

class ThermoDynamicProperties():
    def __init__(self,T=293.15):
        self.T = T

        T_base = [175,200,225,250,275,300,325,350,375,400,450,500]
        C_p_base = [1.0023, 1.0025, 1.0027, 1.0031, 1.0038, 1.0049, 1.0063, 1.0082, 1.0106, 1.0135, 1.0206, 1.0295]
        gamma_base = [1.401, 1.401, 1.401, 1.401, 1.401, 1.400, 1.400, 1.398, 1.397, 1.395, 1.391, 1.387]
    
        self.C_p = np.interp(self.T,T_base,C_p_base)*1000 #Output Cp in [J/kg-K]
        self.gamma = np.interp(self.T,T_base,gamma_base) #Output gamma
        # print(f"The Cp of air at {self.T} K is {self.C_p}")
        # print(f"The gamma of air at {self.T} K is {self.gamma}")


object = ThermoDynamicProperties(T=393.15)



        

