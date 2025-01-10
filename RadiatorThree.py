import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant

#Code written by Jorrit
#This class is used for more detailed radiator sizing

class Radiator:
    def __init__(self,BalanceOfPlant,Vtest=1):
        #Inputs previous classes
        self.IVCurves = IVCurves if IVCurves else IVCurves()
        self.CellParameters = CellParameters if CellParameters else CellParameters()
        self.BalanceOfPlant = BalanceOfPlant if BalanceOfPlant else BalanceOfPlant()

        #Temperatures
        self.T_c_in = 273.15+35 #Coolant in temperature [K]
        self.T_c_out = 273.15+25 #Coolant out temperature [K]
        self.T_a_in = 273.15+20 #Air in temperature (ambient) [K]

        #Air properties
        self.rho_a = 1.204 #[kg/m^3]
        self.c_pa = 1.006e3 #[J/kg K]

        #Heat
        self.Q_rad = 130e3  #Heat to be rejected by radiator, calculated in BalanceOfPlant

    def RadiatorSizing(self):
        self.T_a_out = np.linspace(273.15+20,323.15,500)
        self.LMTD = ((self.T_c_in-self.T_a_out)-(self.T_c_out-self.T_a_in))/(np.log((self.T_c_in-self.T_a_out)/(self.T_c_out-self.T_a_in)))

        self.V_a = np.linspace(0,25,len(self.T_a_out))

        self.T_a_out_point = np.zeros(len(self.V_a))
        for n in range(len(self.V_a)):
            self.air_balance = self.rho_a*self.V_a[n]*self.c_pa*abs(self.T_a_in-self.T_a_out)
            self.rad_balance = (1269*self.V_a[n] + 99.9)*self.LMTD

            tolerance = 1000
            for i in range(len(self.T_a_out)):
                if self.rad_balance[i]-tolerance <= self.air_balance[i] <= self.rad_balance[i] +tolerance:
                    self.T_a_out_point[n] = self.T_a_out[i]
        
        print(self.T_a_out_point)

        self.A_r = self.Q_rad/(self.rho_a*self.V_a*self.c_pa*abs(self.T_a_in-self.T_a_out_point))
        print(self.A_r)



        plt.figure(figsize=(10, 6))
        plt.plot(self.T_a_out, self.air_balance, label='Air side', color='blue')
        plt.plot(self.T_a_out, self.rad_balance, label='Radiator side', color='green')

        plt.title(f"Radiator balance")
        plt.legend(loc='upper left', fontsize='large')
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Air out T [K]")
        plt.ylabel("Q/A [W/m^2]")

        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(self.V_a, self.A_r, label='Relation', color='blue')

        plt.title(f"Radiator Size vs Air Speed")
        plt.legend(loc='upper left', fontsize='large')
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Air speed [m/s]")
        plt.ylabel("Radiator area [m^2]")

        plt.tight_layout()
        plt.show()


    



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
Rad.RadiatorSizing()
