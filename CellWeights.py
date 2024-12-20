import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant

#Code written by Jorrit
#This class focuses on calculating the weights of all the PEMFC components.

class CellWeights:
    def __init__(self,IVCurves,CellParameters,BalanceOfPlant,missiontime=3600):
        #Inputs previous classes
        self.IVCurves = IVCurves if IVCurves else IVCurves()
        self.CellParameters = CellParameters if CellParameters else CellParameters()
        self.BalanceOfPlant = BalanceOfPlant if BalanceOfPlant else BalanceOfPlant()
        self.missiontime = missiontime

    
    def StackWeight(self):
        self.kappa_stack = 4 #Stack weight design factor [kg/m^2], assumed value (Datta)
        self.W_stack = self.kappa_stack*(self.CellParameters.A_c*1e-4)*self.CellParameters.n_c
        # print(f"Stack weight is {min(self.W_stack)} to {max(self.W_stack)} kg")
    
    def HydrogenWeight(self):
        self.W_hydrogen = self.CellParameters.H2_flow*self.missiontime #Calculate weight of hydrogen based on hydrogen mass flow and mission time [kg]
        # print(f"Required Hydrogen weight is {np.median(self.W_hydrogen):.2f} kg")
    
    def TankWeight(self):
        self.W_tank = 13.4*self.W_hydrogen + 13.3 #Hydrogen tank weight, based on regression from Powertrain sheet [kg], assumes 700 bar 
        # print(f"Required hydrogen tank weight is {np.median(self.W_tank)} kg") 
    
    def AirWeight(self): #Calculates the weights of the air system, based on fractions from Datta
        #Compressor weight [kg]
        self.k_W_comp = 7e-4 #Coefficient for compressor weight
        self.e_W_comp = 1 #Exponent for compressor weight
        self.W_comp = self.k_W_comp*(self.BalanceOfPlant.P_comp_max**self.e_W_comp) #Compressor-expander module weight, assumes single compressor-expander unit
        # print(f"Compressor weight is {self.W_comp} kg")

        self.f_air_filter = 0.01 #Air system filter weight fraction, Datta
        self.W_air_filter = self.f_air_filter*self.W_comp #Air system filter weight [kg]

        self.f_air_regulator = 0.01 #Air system regulator weight fraction, Datta
        self.W_air_regulator = self.f_air_regulator*self.W_comp #Air system regulator weight [kg]

        self.f_air_powersupply = 0.05 #Air system power supply weight fraction, Datta
        self.W_air_powersupply = self.f_air_powersupply*self.W_comp #Air system power supply weight [kg]

        self.f_air_humidifier = 0.05 #Humidifier weight fraction, Datta
        self.W_air_humdifier = self.f_air_humidifier*self.W_comp #Humidifier weight [kg]

        #No plumbing weight yet

        #Total air system weight [kg]
        self.W_air = self.W_comp + self.W_air_filter + self.W_air_regulator + self.W_air_powersupply + self.W_air_humdifier
        # print(f"Air system weight is {self.W_air} kg")
    
    def HTCWeight(self):
        #Coolant weight [kg]
        self.k_W_HTC_coolant = 1e-6 #Coefficient for coolant weight, Datta
        self.W_HTC_coolant = self.k_W_HTC_coolant*self.BalanceOfPlant.Q_htc

        #HTC radiator weight [kg]
        self.k_HTC_radiator = 3.5405 #Coefficient for HTC radiator weight [kg/m^2], Datta
        self.W_HTC_radiator = self.k_HTC_radiator*self.BalanceOfPlant.HTC_A_r
        # print(f"Radiator weight is {np.median(self.W_HTC_radiator)} kg")

        self.f_HTC_filter = 0.01 #HTC system filter weight fraction, Datta
        self.W_HTC_filter = self.f_HTC_filter*(self.W_HTC_coolant+self.W_HTC_radiator) #HTC system filter weight [kg]

        self.f_HTC_regulator = 0.01 #HTC system regulator weight fraction, Datta
        self.W_HTC_regulator = self.f_HTC_regulator*(self.W_HTC_coolant+self.W_HTC_radiator) #HTC system regulator weight [kg]

        self.f_HTC_powersupply = 0.05 #HTC system power supply weight fraction, Datta
        self.W_HTC_powersupply = self.f_HTC_powersupply*(self.W_HTC_coolant+self.W_HTC_radiator) #HTC system power supply weight [kg]

        #No plumbing weight yet

        #Total HTC system weight [kg]
        self.W_HTC = self.W_HTC_coolant + self.W_HTC_radiator + self.W_HTC_filter + self.W_HTC_regulator + self.W_HTC_powersupply
        # print(f"HTC system weight is {np.median(self.W_HTC)} kg")

    def LTCWeight(self):
        #Cooler weight [kg]
        self.k_W_LTC_Cooler = 1e-6 #LTC Cooler coefficient, Datta
        self.W_LTC_Cooler = self.k_W_LTC_Cooler*self.BalanceOfPlant.Q_ltc 

        #Coolant weight [kg]
        self.k_W_LTC_Coolant = 1e-6 #LTC Coolant coefficient, Datta
        self.W_LTC_coolant = self.k_W_LTC_Coolant*self.BalanceOfPlant.Q_ltc

        #LTC radiator weight [kg]
        self.k_LTC_radiator = 3.5405 #Coefficient for HTC radiator weight [kg/m^2], Datta
        self.W_LTC_radiator = self.k_LTC_radiator*self.BalanceOfPlant.LTC_A_r
        # print(f"Radiator weight is {np.median(self.W_LTC_radiator)} kg")

        self.f_LTC_filter = 0.01 #LTC system filter weight fraction, Datta
        self.W_LTC_filter = self.f_LTC_filter*(self.W_LTC_coolant+self.W_LTC_radiator) #LTC system filter weight [kg]

        self.f_LTC_regulator = 0.01 #LTC system regulator weight fraction, Datta
        self.W_LTC_regulator = self.f_LTC_regulator*(self.W_LTC_coolant+self.W_LTC_radiator) #LTC system regulator weight [kg]

        self.f_LTC_powersupply = 0.05 #LTC system power supply weight fraction, Datta
        self.W_LTC_powersupply = self.f_LTC_powersupply*(self.W_LTC_coolant+self.W_LTC_radiator) #LTC system power supply weight [kg]

        #No plumbing weight yet

        #Total LTC system weight [kg]
        self.W_LTC = self.W_LTC_Cooler+ self.W_LTC_coolant + self.W_LTC_radiator + self.W_LTC_filter + self.W_LTC_regulator + self.W_LTC_powersupply
        # print(f"LTC system weight is {np.median(self.W_LTC)} kg")
    
    def WaterWeight(self):
        #Current assumption is that we do not have a water tank as we just piss out the water, maybe estimate some plumbing and filter weights here?
        pass

    def ElectricalWeight(self):
        #Controller weight [kg]
        self.k_W_Elec_controller = 0.01 #Coefficient for electrical system controller weight, Datta
        self.W_Elec_controller = self.k_W_Elec_controller*(self.CellParameters.I_D) 

        #Power electronics weight [kg]
        self.f_Elec_power = 0.01
        self.W_Elec_power = self.f_Elec_power*self.W_Elec_controller

        #No plumbing weight yet

        #Total Electrical system weight [kg]
        self.W_Elec = self.W_Elec_controller + self.W_Elec_power 
        # print(f"Electrical system weight is {self.W_Elec} kg")

    def TotalWeight(self):
        #Calculate total PEMFC system weight [kg]
        self.W_PEMFC = self.W_stack + self.W_hydrogen + self.W_tank + self.W_air + self.W_HTC + self.W_LTC + self.W_Elec
        # print(f"Min PEMFC weight is {min(self.W_PEMFC)} kg")

    def WeightsPieChart(self):
        #Create pie chart of the weight components
        labels = ["Stack", "H2", "H2 Tank", "Air", "HTC", "LTC", "Electrical"]
        index = 0
        for i in range(len(self.W_PEMFC)):
            if self.W_PEMFC[i] == min(self.W_PEMFC):
                index = i
        values = [self.W_stack[i],self.W_hydrogen[i],self.W_tank[i],self.W_air,self.W_HTC[i],self.W_LTC[i],self.W_Elec]

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("PEMFC System Weight Components")
        plt.axis("equal")
        plt.show()
        
    def FindDesignPoint(self):
        #Find and plot design point on IV curves
        #Find index of design point that gives min weight
        index = 0
        for i in range(len(self.W_PEMFC)):
            if self.W_PEMFC[i] == min(self.W_PEMFC):
                index = i
        
        self.i_d, self.v_d, self.p_d, self.q_d = self.IVCurves.i[index], self.IVCurves.v[index], self.IVCurves.p[index], self.IVCurves.q[index]

        #Find max power point index
        maxpin = 0
        for i in range(len(self.IVCurves.p)):
            if self.IVCurves.p[i] == max(self.IVCurves.p):
                maxpin = i

        plt.figure(figsize=(10, 6))
        plt.plot(self.IVCurves.i, self.IVCurves.v, label='Cell voltage', color='blue')
        plt.plot(self.IVCurves.i, self.IVCurves.p, label='Power Density', color='green')
        plt.plot(self.IVCurves.i, self.IVCurves.q, label='Heat', color='red')

        plt.axvline(x=self.i_d, color='black', label='Design Point', linestyle='--', linewidth=1)

        plt.scatter(self.i_d, self.v_d, color='orange', zorder=5)
        plt.scatter(self.i_d, self.p_d, color='orange', zorder=5)
        plt.scatter(self.i_d, self.q_d, color='orange', zorder=5)

        plt.scatter(self.IVCurves.i[maxpin],self.IVCurves.p[maxpin], color='black', label='Max P',zorder=5)

        plt.title(f"IV Curves for {self.IVCurves.p_s/101325} atm")
        plt.legend(loc='upper left', fontsize='large')
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Current density [A/cm^2]")
        plt.ylabel("Cell voltage [V], Power density [A/cm^2], Heat [A/cm^2]")

        plt.tight_layout()
        plt.show()

    def OutputCharacteristics(self):
        index = 0
        for i in range(len(self.W_PEMFC)):
            if self.W_PEMFC[i] == min(self.W_PEMFC):
                index = i

        print(f"======GENERAL CHARACTERISTICS=====")
        print(f"Design power [kW]: {self.CellParameters.P_D*1e-3:.2f}")
        print(f"Net power [kW]: {(self.CellParameters.P_D-self.BalanceOfPlant.P_BOP[index])*1e-3:.2f}")
        print(f"Design voltage [V]: {self.CellParameters.V_D:.2f}")
        print(f"Stack temperature [K]: {self.IVCurves.T:.2f}")
        print(f"Stack pressure [atm]: {self.IVCurves.p_s/101325:.2f}")
        print(f"Pressure drop [Pa]: {self.CellParameters.p_s_drop:.2f}")
        print(f"Number of cells: {self.CellParameters.n_c[index]:.2f}")
        print(f"Active cell area [cm^2]: {self.CellParameters.A_c[index]:.2f}")

        print(f"======MASS FLOWS=====")
        print(f"H2 flow [kg/s]: {self.CellParameters.H2_flow[index]:.4f}")
        print(f"O2 flow [kg/s]: {self.CellParameters.O2_flow[index]:.4f}")
        print(f"Air in flow [kg/s]: {self.CellParameters.air_in_flow[index]:.4f}")
        print(f"Air out flow [kg/s]: {self.CellParameters.air_out_flow[index]:.4f}")
        print(f"Water flow [kg/s]: {self.CellParameters.water_flow[index]:.4f}")
        print(f"Water vapour flow [kg/s]: {self.CellParameters.water_vapour_flow[index]:.4f}")
        print(f"Water liquid flow [kg/s]: {self.CellParameters.water_liquid_flow[index]:.4f}")
        print(f"HTC coolant flow [kg/s]: {self.BalanceOfPlant.HTC_coolant_flow[index]:.4f}")
        print(f"LTC coolant flow [kg/s]: {self.BalanceOfPlant.LTC_coolant_flow[index]:.4f}")

        print(f"======HEAT CHARACTERISTICS=====")
        print(f"Total heat to be rejected (HTC) [W]: {self.BalanceOfPlant.Q_htc[index]:.2f} ")
        print(f"Total heat to be rejected (LTC) [W]: {self.BalanceOfPlant.Q_ltc[index]:.2f} ")
        print(f"HTC radiator area [m^2]: {self.BalanceOfPlant.HTC_A_r[index]:.2f}")
        print(f"LTC radiator area [m^2]: {self.BalanceOfPlant.LTC_A_r[index]:.2f}")

        print(f"======BALANCE OF PLANT=====")
        print(f"Compressor power [W]: {self.BalanceOfPlant.P_comp[index]:.2f}")
        print(f"Turbine power [W]: {self.BalanceOfPlant.P_turb[index]:.2f}")
        print(f"HTC power [W]: {self.BalanceOfPlant.P_HTC[index]:.2f}")
        print(f"LTC power [W]: {self.BalanceOfPlant.P_LTC[index]:.2f}")
        print(f"Water power [W]: {self.BalanceOfPlant.P_Water:.2f}")
        print(f"Electrical power [W]: {self.BalanceOfPlant.P_Elec:.2f}")
        print(f"Total BOP power [W]: {self.BalanceOfPlant.P_BOP[index]:.2f}")

        print(f"======WEIGHTS=====")
        print(f"Stack weight [kg]: {self.W_stack[index]:.2f}")
        print(f"Air system weight [kg]: {self.W_air:.2f}")
        print(f"H2 weight [kg]: {self.W_hydrogen[index]:.2f}")
        print(f"Tank weight [kg]: {self.W_tank[index]:.2f}")
        print(f"HTC weight [kg]: {self.W_HTC[index]:.2f}")
        print(f"LTC weight [kg]: {self.W_LTC[index]:.2f}")
        print(f"Electrical weight [kg]: {self.W_Elec:.2f}")
        print(f"Total PEMFC weight [kg]: {self.W_PEMFC[index]:.2f}")






#Testing
inputIV = IVCurves(p_s=2.50)
inputCell = CellParameters(IVCurves=inputIV,P_D=105000,V_D=840)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
BOP.AirPower()
BOP.HTCPower()
BOP.LTCPower()
BOP.WaterPower()
BOP.ElecPower()
BOP.BOPPower()
Weights = CellWeights(IVCurves=inputIV,CellParameters=inputCell,BalanceOfPlant=BOP)
Weights.StackWeight()
Weights.HydrogenWeight()
Weights.TankWeight()
Weights.AirWeight()
Weights.HTCWeight()
Weights.LTCWeight()
Weights.WaterWeight()
Weights.ElectricalWeight()
Weights.TotalWeight()
Weights.WeightsPieChart()
Weights.FindDesignPoint()
Weights.OutputCharacteristics()
    
