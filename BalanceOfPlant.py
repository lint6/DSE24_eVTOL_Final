import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties

#Code written by Jorrit
#This class does the power calculations for all the BOP components.

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
        self.C_p_stack = ThermoDynamicProperties(T=self.IVCurves.T).C_p  #Specific heat of air at stack T [J/kg-K]
        self.stack_gamma = ThermoDynamicProperties(T=self.IVCurves.T).gamma  #Ratio of specific heat of air at stack T
        self.p_s = self.IVCurves.p_s #Stack pressure
        self.T_s = self.IVCurves.T
        self.p_s_drop = self.CellParameters.p_s_drop

        #Constants
        self.SB_constant = 5.670367e-8 #Stefan-Boltzmann constant [W/m^2 K^4]


    def AirPower(self): #Assumes ISA SL conditions for now
        #Calculate compressor power
        self.eta_comp = 0.75    #Compressor efficiency, assumed value for now
        self.delta_T_comp = ((self.p_s/self.p_ambient)**((self.air_gamma-1)/self.air_gamma)-1)*self.T_ambient*(1/self.eta_comp) #Temperature change, assumes isentropic compression
        self.P_comp = self.C_p * self.air_in_flow * self.delta_T_comp #Compressor power [W]
        self.P_comp_max = self.C_p * max(self.air_in_flow) * self.delta_T_comp #Max compressor power [W], check if working correctly
        # print(f"Max compressor power is {self.P_comp_max} W")
        
        #Calculate turbine power
        self.eta_turb = 0.65    #Turbine efficiency, assumed value for now
        self.delta_T_turb = ((self.p_ambient/(self.p_s-self.p_s_drop))**((self.stack_gamma-1)/self.stack_gamma)-1)*self.T_s*self.eta_turb #Temperature change, assumes isentropic expansion
        self.P_turb = self.C_p_stack * self.air_out_flow * self.delta_T_turb #Turbine power [W]
        self.P_turb_max = self.C_p_stack * max(self.air_out_flow) * self.delta_T_turb   #Max turbine power [W]
        # print(f"Max turbine power is {self.P_turb_max} W")

        self.P_air = self.P_comp + self.P_turb
        self.P_air_max = max(self.P_air)
        print(f"Max CEM power is {self.P_air_max:.2f} W")

    def HTCPower(self):
        #Calculate heat to be rejected

        #Stack
        self.Q_s = (self.IVCurves.E_h - self.IVCurves.v)*(self.CellParameters.P_D/self.IVCurves.v) #Stack heat [W]
        print(f"Max stack heat is {self.Q_s[-1]}")

        #Air flow
        self.Q_htc_out = self.C_p_stack*self.air_out_flow*(self.T_s-self.T_ambient) #Heat carried out by air [W]
        print(f"Heat carried out by air {self.Q_htc_out[-1]}")

        #Dissipation
        self.f_s = 0.6 #Fraction of stack active area that is exposed, assumed value
        self.emissivity_s = 0.8 #Stack emissivity, assumed value
        self.convec_coeff = 3 #Overall convection heat transfer coefficient [W/m^2 K], assumed value 
        self.A_s = self.f_s * self.CellParameters.n_c * self.CellParameters.A_c * 1e-4 #Exposed stack area [m^2], 1e-3 for conversion from cm^2

        self.Q_htc_d = self.A_s*self.convec_coeff*(self.T_s-self.T_ambient) + self.A_s*self.emissivity_s*self.SB_constant*(self.T_s**4-self.T_ambient**4)
        print(f"Heat dissipated by stack {self.Q_htc_d[-1]}")

        #Total heat to be rejected [W], if statement to avoid negative values
        self.Q_htc = np.zeros(len(self.Q_htc_d))
        for i in range(len(self.Q_s)):
            self.Q_htc[i] = self.Q_s[i] - self.Q_htc_d[i] - self.Q_htc_out[i]  
            if self.Q_htc[i] < 0:
                self.Q_htc[i] = 0
        print(f"The heat to be rejected is {self.Q_htc[-1]:.2f} W")
        
        #Calculate required coolant mass flow [kg/s]
        self.C_p_HTC_coolant = 4.18e3 #Specific heat of coolant (assumed to be water) [J/kg-K]
        self.delta_T_HTC_coolant = 10 #Rise in coolant temp as it absorbs stack heat [K], assumed value
        self.HTC_coolant_flow = self.Q_htc/(self.C_p_HTC_coolant*self.delta_T_HTC_coolant) #Required mass flow of HTC coolant [kg/s]

        #Calculate radiator area.
        self.HTC_rad_convec_coeff = 1015+273.15 #HTC radiator heat transfer coefficient [W/m^2-K]
        self.HTC_rad_Tr = 273.15+95 #HTC radiator temperature [K]
        self.HTC_rad_emissivity = 0.8 #HTC radiator emissivity

        self.HTC_A_r = self.Q_htc/(self.HTC_rad_convec_coeff*(self.HTC_rad_Tr-self.T_ambient)+self.HTC_rad_emissivity*self.SB_constant*(self.HTC_rad_Tr**4-self.T_ambient**4)) #HTC Radiator area [m^2]
        print(f"HTC Radiator area {self.HTC_A_r[-1]:.2f} m^2")

        #Set up coefficients & exponents, from Datta
        self.k_HTCPower = 300
        self.e_HTCPower = 0
        self.f_HTCPower = 1

        #Calculate HTC power [W]
        self.P_HTC = self.k_HTCPower*(self.Q_htc**self.e_HTCPower)*(self.HTC_coolant_flow**self.f_HTCPower) 
        print(f"Max HTC Power is {max(self.P_HTC):.2f} W")


    def LTCPower(self):
        #Calculate heat to be rejected
        self.T_output_comp = self.T_ambient + self.delta_T_comp #Temperature at compressor output [K]
        self.C_p_output_comp = ThermoDynamicProperties(T=self.T_output_comp).C_p #Specific heat of air at compressor output, [J/kg-K]
        self.delta_T_output_comp_stack = self.T_output_comp - self.T_s  #Temperature change from compressor output to stack [K]
        self.Q_ltc = self.C_p_output_comp * self.air_in_flow * self.delta_T_output_comp_stack  #Heat to be rejected by LTC system [W]
        #Avoid negative values
        for i in range(len(self.Q_ltc)):
            if self.Q_ltc[i] < 0:
                self.Q_ltc[i] = 0
        print(f"Mean heat to be rejected {np.mean(self.Q_ltc):.2f} W")

        self.C_p_LTC_coolant = 4.18e3 #Specific heat of coolant (assumed to be water) [J/kg-K]
        self.delta_T_LTC_coolant = 10 #Rise in coolant temp as it absorbs heat from air [K], assumed value

        #Total heat to be rejected by LTC [W].
        self.LTC_coolant_flow = self.Q_ltc/(self.C_p_LTC_coolant*self.delta_T_LTC_coolant) #Required mass flow of LTC coolant [kg/s]
        print(f"Mean coolant flow {np.mean(self.LTC_coolant_flow):.2f} kg/s")

         #Calculate radiator area. 
        self.LTC_rad_convec_coeff = 1015+273.15 #HTC radiator heat transfer coefficient [W/m^2-K]
        self.LTC_rad_Tr = 273.15+95 #HTC radiator temperature [K]
        self.LTC_rad_emissivity = 0.8 #HTC radiator emissivity

        self.LTC_A_r = self.Q_ltc/(self.LTC_rad_convec_coeff*(self.LTC_rad_Tr-self.T_ambient)+self.LTC_rad_emissivity*self.SB_constant*(self.LTC_rad_Tr**4-self.T_ambient**4)) #LTC Radiator area [m^2]
        print(f"LTC Radiator area {np.mean(self.LTC_A_r):.2f} m^2")

        #Set up coefficients & exponents, from Datta
        self.k_LTCPower = 300
        self.e_LTCPower = 0
        self.f_LTCPower = 1

        #Calculate LTC power [W]
        self.P_LTC = self.k_LTCPower*(self.Q_ltc**self.e_LTCPower)*(self.LTC_coolant_flow**self.f_LTCPower) 
        print(f"Max LTC Power is {max(self.P_LTC):.2f} W")
    
    def WaterPower(self):
        #Set up coefficients & exponents
        self.k_WaterPower = 1e3 #Coefficient to liquid water flow, CHECK THIS VALUE

        #Calculate water power [W]
        self.P_Water = self.k_WaterPower*(max(self.CellParameters.water_liquid_flow)) #Power to circulate water [W]
        # print(max(self.CellParameters.water_liquid_flow))
        # print(f"Max water power is {max(self.P_Water):.2f} W")
    
    def ElecPower(self):
        #Set up coefficients & exponents
        self.k_ElecPower = 0.02
        self.e_ElecPower = 1

        self.P_Elec = self.k_ElecPower*(self.CellParameters.P_D**self.e_ElecPower)
        # print(f"Electric power is {self.P_Elec:.2f} W")
    
    def BOPPower(self):
        #Calculate total power required for BOP systems [W]
        self.P_BOP = self.P_air+self.P_HTC+self.P_LTC+self.P_Water+self.P_Elec
        # print(f"Mean BOP power is {np.mean(self.P_BOP):.2f} W, which is {(np.mean(self.P_BOP)/self.CellParameters.P_D)*100:.2f} % of total cell power")
    
    def BOPPieChart(self):
        labels = ["Air", "HTC", "LTC", "Water", "Electronics"]
        values = [np.median(self.P_air)/self.CellParameters.P_D, np.median(self.P_HTC)/self.CellParameters.P_D, np.median(self.P_LTC)/self.CellParameters.P_D, np.median(self.P_Water)/self.CellParameters.P_D, np.median(self.P_Elec)/self.CellParameters.P_D]

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("BOP Power Components")
        plt.axis("equal")
        plt.show()







#Just stuff for code checking
inputIV = IVCurves(p_s=2.50)
# inputIV.PlotCurves()
inputCell = CellParameters(IVCurves=inputIV)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
# BOP.AirPower()
# BOP.HTCPower()
# BOP.LTCPower()
BOP.WaterPower()
# BOP.ElecPower()
# BOP.BOPPower()
# BOP.BOPPieChart()

