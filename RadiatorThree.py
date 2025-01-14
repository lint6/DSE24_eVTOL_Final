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

        #Sizing speed [m/s]
        self.Vtest = Vtest

        #Temperatures
        self.T_c_in = 273.15+54.3 #Coolant in temperature [K]
        self.T_c_out = 273.15+58.9 #Coolant out temperature [K]
        self.T_a_in = 273.15+20 #Air in temperature (ambient) [K]

        #Air properties
        self.rho_a = 1.204 #[kg/m^3]
        self.c_pa = 1.006e3 #[J/kg K]

        #Heat
        self.Q_rad = 17.6e3  #Heat to be rejected by radiator, calculated in BalanceOfPlant

    def RadiatorSizing(self):
        self.T_a_out = np.linspace(273.15+20,323.15,500)
        self.LMTD = ((self.T_c_in-self.T_a_out)-(self.T_c_out-self.T_a_in))/(np.log((self.T_c_in-self.T_a_out)/(self.T_c_out-self.T_a_in)))

        self.V_a = np.linspace(0.01,25,len(self.T_a_out))

        self.T_a_out_point = np.zeros(len(self.V_a))
        for n in range(len(self.V_a)):
            self.air_balance = self.rho_a*self.V_a[n]*self.c_pa*abs(self.T_a_in-self.T_a_out)
            self.rad_balance = (1269*self.V_a[n] + 99.9)*self.LMTD

            tolerance = 1000
            for i in range(len(self.T_a_out)):
                if self.rad_balance[i]-tolerance <= self.air_balance[i] <= self.rad_balance[i] +tolerance:
                    self.T_a_out_point[n] = self.T_a_out[i]
        
        # print(self.T_a_out_point)

        self.A_r = self.Q_rad/(self.rho_a*self.V_a*self.c_pa*abs(self.T_a_in-self.T_a_out_point))
        # print(self.A_r)

        index = None
        tolerance2 = 0.05
        for n in range(len(self.V_a)):
            if self.Vtest-tolerance2 <= self.V_a[n] <= self.Vtest+tolerance2:
                index = n
                break
        
        self.A_r_point = self.Q_rad/(self.rho_a*self.V_a[index]*self.c_pa*abs(self.T_a_in-self.T_a_out_point[index]))
        self.k_radiator = 3.5405 #[kg/m^2], radiator density Datta
        self.W_radiator = self.A_r_point*self.k_radiator #Radiator weight [kg]
        print(f"Radiator size is {self.A_r_point:.2f} [m^2]")
        print(f"Radiator weight is {self.W_radiator:.2f} [kg]")


        # plt.figure(figsize=(10, 6))
        # plt.plot(self.T_a_out, self.air_balance, label='Air side', color='blue')
        # plt.plot(self.T_a_out, self.rad_balance, label='Radiator side', color='green')

        # plt.title(f"Radiator balance")
        # plt.legend(loc='upper left', fontsize='large')
        # plt.grid(color='gray', linestyle=':', linewidth=0.5)
        # plt.xlabel("Air out T [K]")
        # plt.ylabel("Q/A [W/m^2]")

        # plt.tight_layout()
        # plt.show()

        # plt.figure(figsize=(10, 6))
        # plt.plot(self.V_a, self.A_r, label='Relation', color='blue')

        # plt.title(f"Radiator Size vs Air Speed")
        # plt.legend(loc='upper left', fontsize='large')
        # plt.grid(color='gray', linestyle=':', linewidth=0.5)
        # plt.xlabel("Air speed [m/s]")
        # plt.ylabel("Radiator area [m^2]")

        # plt.tight_layout()
        # plt.show()
    def CoolantSystem(self): #Only for battery & infrastructure cooling system, assumes same as PEMFC HTC
        #Calculate required coolant mass flow [kg/s]
        self.C_p_HTC_coolant = 4.18e3 #Specific heat of coolant (assumed to be water) [J/kg-K]
        self.delta_T_HTC_coolant = 10 #Rise in coolant temp as it absorbs stack heat [K], assumed value
        self.HTC_coolant_flow = self.Q_rad/(self.C_p_HTC_coolant*self.delta_T_HTC_coolant) #Required mass flow of HTC coolant [kg/s]

        #Coolant weight [kg] 
        self.k_W_HTC_coolant = 5 #Coefficient for coolant weight, Datta
        self.W_HTC_coolant = self.k_W_HTC_coolant*self.HTC_coolant_flow

        self.f_HTC_filter = 0.01 #HTC system filter weight fraction, Datta
        self.W_HTC_filter = self.f_HTC_filter*(self.W_HTC_coolant+self.W_radiator) #HTC system filter weight [kg]

        self.f_HTC_regulator = 0.01 #HTC system regulator weight fraction, Datta
        self.W_HTC_regulator = self.f_HTC_regulator*(self.W_HTC_coolant+self.W_radiator) #HTC system regulator weight [kg]

        self.f_HTC_powersupply = 0.05 #HTC system power supply weight fraction, Datta
        self.W_HTC_powersupply = self.f_HTC_powersupply*(self.W_HTC_coolant+self.W_radiator) #HTC system power supply weight [kg]

        #No plumbing weight yet

        #Total HTC system weight [kg]
        self.W_HTC = self.W_HTC_coolant + self.W_radiator + self.W_HTC_filter + self.W_HTC_regulator + self.W_HTC_powersupply
        print(f"Total cooling system weight is {self.W_HTC:.2f} [kg]")



    



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
Rad = Radiator(BalanceOfPlant=BOP,Vtest=2.5)
Rad.RadiatorSizing()
Rad.CoolantSystem()

