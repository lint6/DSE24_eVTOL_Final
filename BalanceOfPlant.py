import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters

#Class explanation goes here

class BalanceOfPlant:
    def __init__(self,IVCurves,CellParameters):
        #Inputs previous classes
        self.IVCurves = IVCurves if IVCurves else IVCurves()
        self.CellParameters = CellParameters if CellParameters else CellParameters()
        
        #Define inputs
        self.air_in_flow = self.CellParameters.air_in_flow
        self.air_out_flow = self.CellParameters.air_out_flow

        #Ambient conditions, assumes ISA SL for now
        self.C_p = 1005 #Specific heat of air [J/kg/K]
        self.air_gamma = 1.40 #Ratio of specific heat of air
        self.T_ambient = 288.15 #Ambient temperature [K]
        self.p_ambient = 101325 #Ambient pressure [Pa]

        #Stack conditions
        self.C_p_stack = 2000 #PLACEHOLDER 
        self.stack_gamma = 1.3 #PLACEHOLDER
        self.p_s = self.IVCurves.p_s #Stack pressure
        self.T_s = self.IVCurves.T
        self.p_s_drop = self.CellParameters.p_s_drop


    def AirPower(self): #Assumes ISA SL conditions for now
        #Calculate compressor power
        self.eta_comp = 0.75    #Compressor efficiency, assumed value for now
        self.delta_T_comp = ((self.p_s/self.p_ambient)**((self.air_gamma-1)/self.air_gamma)-1)*self.T_ambient*(1/self.eta_comp) #Temperature change, assumes isentropic compression
        self.P_comp = self.C_p * self.air_in_flow * self.delta_T_comp #Compressor power [W]
        self.P_comp_max = self.C_p * max(self.air_in_flow) * self.delta_T_comp #Max compressor power [W], check if working correctly
        print(f"Max compressor power is {self.P_comp_max} W")
        
        #Calculate turbine power
        self.eta_turb = 0.65    #Turbine efficiency, assumed value for now
        self.delta_T_turb = ((self.p_ambient/(self.p_s-self.p_s_drop))**((self.stack_gamma-1)/self.stack_gamma)-1)*self.T_s*self.eta_turb #Temperature change, assumes isentropic expansion
        self.P_turb = self.C_p_stack * self.air_out_flow * self.delta_T_turb #Turbine power [W]
        self.P_turb_max = self.C_p_stack * max(self.air_out_flow) * self.delta_T_turb   #Max turbine power [W]
        print(f"Max turbine power is {self.P_turb_max} W")

        self.P_air = self.P_comp + self.P_turb

    # def HTCPower(self):
        #Still working on rest of BOP

#Just stuff for code checking
inputIV = IVCurves(p_s=2.5)
inputCell = CellParameters(IVCurves=inputIV)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
BOP.AirPower()


