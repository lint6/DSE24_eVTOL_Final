import numpy as np 
import matplotlib.pyplot as plt 

class SquareBeamShearFlow:  

    def __init__(self, b, t, Vx, Vy):
        self.b = b 
        self.t = t 
        self.Vx = Vx 
        self.Vy = Vy 

    def calculate_Ixx(self):
        I_xx_outer =  1/12 * self.b**4
        I_xx_inner = 1/12 * (self.b - 2 * self.t)**4
        return I_xx_outer - I_xx_inner 
    
    def calculate_Iyy(self):
        return self.calculate_Ixx()
    
    def calculate_shear_flow_Vx(self):


    def calculate_shear_flow_Vy(self):


    def plot_shear_flow_Vx(self):

        

