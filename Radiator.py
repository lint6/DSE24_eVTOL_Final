import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant

#USE RadiatorThree FOR RADIATOR SIZING, THIS IS JUST IN CASE I MIGHT NEED IT LATER

class Radiator:
    def __init__(self,BalanceOfPlant,Vtest=15.83):
        #Inputs previous classes
        self.IVCurves = IVCurves if IVCurves else IVCurves()
        self.CellParameters = CellParameters if CellParameters else CellParameters()
        self.BalanceOfPlant = BalanceOfPlant if BalanceOfPlant else BalanceOfPlant()

        #Air properties (assumes 20 degrees C), values from Engineering Toolbox
        self.dynamic_viscosity = 18.13e-6 #[kg/m s]
        self.density = 1.204 #[kg/m^3]
        self.specific_heat = 1.006e3 #[J/kg K]
        self.thermal_conductivity = 25.86e-3 #[W/m K]

        self.V = Vtest
    
    def HydraulicDiameter(self):
        #Calculates the effective hydraulic diameter

        #Flat plate
        self.plate_area = 1.38 #Radiator area [m^2] calculated in PEMFC model

        #For a given area, find the lowest (i.e. best) hydraulic diameter value
        self.a = np.linspace(0.01,self.plate_area/2,100)
        # print(self.a)
        self.b = np.zeros(len(self.a))
        self.a_plus_b = np.zeros(len(self.a))

        #Placeholders 
        self.a_t = 0
        self.b_t = 0

        for i in range(len(self.a)): 
            self.b[i] = self.plate_area/self.a[i] #Generate the options
            self.a_plus_b[i] = self.a[i] + self.b[i] #Get the sums
        
        for i in range(len(self.a_plus_b)): #Get combination that gives lowest sum, likely redundant
            if self.a_plus_b[i] == min(self.a_plus_b):
                self.a_t = self.a[i]
                self.b_t = self.b[i]
                
        # self.d = (2*(self.a_t*self.b_t))/(self.a_t+self.b_t)
        self.d = 1.32e-3

        print(self.a_t, self.b_t)
    
    def AirNumbers(self):
        self.Prandtl_number = (self.dynamic_viscosity*self.specific_heat)/self.thermal_conductivity
        self.Reynolds_number = (self.V*self.density*self.d)/(self.dynamic_viscosity)
        print(self.Reynolds_number)

        if self.Reynolds_number >= 5e5:
            self.Nusselt_number = (0.3387*self.Reynolds_number**(1/2)*self.Prandtl_number**(1/3))/(1+(0.0468/self.Prandtl_number)**(2/3))**(1/4)
        if self.Reynolds_number < 5e5:
            self.Nusselt_number = 0.0296*(self.Reynolds_number**(4/5))*(self.Prandtl_number**(1/3))

        print(self.Nusselt_number)

        self.convec_coefficient = (self.Nusselt_number*self.thermal_conductivity)/self.d

        print(self.convec_coefficient)



inputIV = IVCurves(p_s=1.50)
inputIV.PlotCurves()
inputCell = CellParameters(IVCurves=inputIV)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
BOP.AirPower()
BOP.HTCPower()
BOP.LTCPower()
BOP.WaterPower()
BOP.ElecPower()
BOP.BOPPower()
Rad = Radiator(BalanceOfPlant=BOP)
Rad.HydraulicDiameter()
Rad.AirNumbers()