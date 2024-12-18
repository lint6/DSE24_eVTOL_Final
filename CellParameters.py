import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves

#Class explanation goes here

class CellParameters():
    def __init__(self,IVCurves,P_D=96000,V_D=840):

        #Inputs
        self.IVCurves = IVCurves if IVCurves else IVCurves()   #Get values from IV curves
        self.P_D = P_D              #Design power [W]
        self.V_D = V_D              #Design voltage [V]

        self.n_c = self.V_D/self.IVCurves.v   #Number of cells

        self.A_c = self.P_D/(self.n_c*self.IVCurves.p) #Active cell area

        
        
            


