import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant

#Code written by Jorrit
#Class explanation goes here

class CellWeights:
    def __init__(self,IVCurves,CellParameters,BalanceOfPlant):
        #Inputs previous classes
        self.IVCurves = IVCurves if IVCurves else IVCurves()
        self.CellParameters = CellParameters if CellParameters else CellParameters()
        self.BalanceOfPlant = BalanceOfPlant if BalanceOfPlant else BalanceOfPlant()

    
    def StackWeight(self):
        self.kappa_stack = 5 #Stack weight design factor [kg/m^2], assumed value
        self.W_stack = self.kappa_stack*(self.CellParameters.A_c*1e-3)*self.CellParameters.n_c
        print(f"Stack weight is {min(self.W_stack)} to {max(self.W_stack)} kg")
    
    




#Testing
inputIV = IVCurves(p_s=2.50)
inputCell = CellParameters(IVCurves=inputIV,P_D=70000)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
BOP.AirPower()
BOP.HTCPower()
BOP.LTCPower()
BOP.WaterPower()
Weights = CellWeights(IVCurves=inputIV,CellParameters=inputCell,BalanceOfPlant=BOP)
Weights.StackWeight()
    
