import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties

#Code written by Jorrit
#Just a quick something to check the air temperature at compressor exit
class DeltaTtest:
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
        self.T_ambient = np.linspace(273.15,313.15,1000) #Ambient temperature [K]
        self.p_ambient = 101325 #Ambient pressure [Pa]

        #Stack conditions
        self.C_p_stack = ThermoDynamicProperties(T=self.IVCurves.T).C_p  #Specific heat of air at stack T [J/kg-K]
        self.stack_gamma = ThermoDynamicProperties(T=self.IVCurves.T).gamma  #Ratio of specific heat of air at stack T
        self.p_s = self.IVCurves.p_s #Stack pressure
        self.T_s = self.IVCurves.T
        self.p_s_drop = self.CellParameters.p_s_drop

        #Constants
        self.SB_constant = 5.670367e-8 #Stefan-Boltzmann constant [W/m^2 K^4]

        #Converter
        self.converter_efficiency = 0.981


    def AirPower(self): #Assumes ISA SL conditions for now
        #Calculate compressor power
        self.eta_comp = 0.80    #Compressor efficiency, assumed value for now
        self.delta_T_comp = ((self.p_s/self.p_ambient)**((self.air_gamma-1)/self.air_gamma)-1)*self.T_ambient*(1/self.eta_comp) #Temperature change, assumes isentropic compression
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.T_ambient-273.15, self.T_ambient+self.delta_T_comp-273.15, label='Relation', color='blue')
        plt.axhline(y=80, color='black', label='Stack Temperature', linestyle='--', linewidth=1)

        plt.title(f"Compressor Temperature change for {self.p_s/101325} atm")
        plt.legend(loc='upper left', fontsize='large')
    
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Ambient Air Temperature")
        plt.ylabel("Air Temperature at Compressor Exit")

        plt.tight_layout()
        plt.show()







#Just stuff for code checking
inputIV = IVCurves(p_s=1.50)
inputIV.PlotCurves()
inputCell = CellParameters(IVCurves=inputIV)
test = DeltaTtest(IVCurves=inputIV,CellParameters=inputCell)
test.AirPower()


