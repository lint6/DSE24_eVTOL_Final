import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves

#Code written by Jorrit
#This class is used to calculate some general cell parameters and the required mass flows. 

class CellParameters():
    def __init__(self,IVCurves,P_D=96000,V_D=840, p_s_drop=30000):

        #Inputs
        self.IVCurves = IVCurves if IVCurves else IVCurves()   #Get values from IV curves
        self.P_D = P_D              #Design power [W]
        self.V_D = V_D              #Design voltage [V]
        self.p_s_drop = p_s_drop    #Stack pressure drop at outlet [Pa]

        #General parameters
        self.I_D = self.P_D/self.V_D  #Design current [Ampere]
        self.n_c = self.V_D/self.IVCurves.v   #Number of cells
        self.A_c = self.P_D/(self.n_c*self.IVCurves.p) #Active cell area [cm^2]

        self.MassFlows()

    def MassFlows(self):
        #Constants
        self.m_h =  2.01588e-3  #Molecular mass of H2 [kg/mol]
        self.m_o = 31.9988e-3   #Molecular mass of O2 [kg/mol]
        self.m_a = 28.9655e-3   #Molecular mass of dry air [kg/mol]
        self.m_w = 18.0153e-3   #Molecular mass of water [kg/mol]
        self.x_o = 0.2095       #Mole fraction of oxygen in air
        self.f_a = 2.0          #Utilization fraction of air in, typically 1.5-2.5 according to Datta paper

        #Calculate hydrogen mass flow [kg/s]
        self.H2_flow = (1/2)*(self.m_h/self.IVCurves.F)*self.I_D*self.n_c #1/2 is from ratio of moles of hydrogen to moles of electrons

        #Calculate oxygen mass flow [kg/s]
        self.O2_flow = (1/4)*(self.m_o/self.IVCurves.F)*self.I_D*self.n_c #1/4 is from ratio of moles of oxygen to moles of electrons

        #Calculate air in flow [kg/s]
        self.air_in_flow = self.f_a*(1/4)*(self.m_o/(self.IVCurves.F*self.x_o))*self.I_D*self.n_c

        #Calculate air out flow [kg/s]
        self.air_out_flow = self.air_in_flow-self.O2_flow

        #Calculate air volume flow [m^3/s]
        self.air_in_volume_flow = (self.air_in_flow/self.m_a)*((self.IVCurves.R*self.IVCurves.T)/self.IVCurves.p_s)
        # print(f"Air in flow {self.air_in_flow}")

        #Calculate water flow [kg/s]
        self.water_flow = self.H2_flow + self.O2_flow

        #Calculate water products 
        self.alpha_p_ws = (18.678-self.IVCurves.T/234.5)*(self.IVCurves.T/(257.14+self.IVCurves.T)) #Empirical Arden Buck Equations
        self.p_ws = 611.21*(np.e**self.alpha_p_ws)  #Water saturation pressure [Pa]
        self.humidity_s = (self.m_w/self.m_a)*(self.p_ws/(self.IVCurves.p_s-self.p_s_drop-self.p_ws))   #Maximum saturation humidity ratio

        self.water_vapour_flow = []
        self.water_liquid_flow = []

        for i in range(len(self.air_out_flow)): #Check for every point on iv curve what the water products are

            if self.humidity_s*self.air_out_flow[i] >= self.water_flow[i]:
                self.water_vapour_flow.append(self.water_flow[i])
                self.water_liquid_flow.append(0)
                # print(f"A cathode humidifier is required")
            if self.humidity_s*self.air_out_flow[i] < self.water_flow[i]:
                self.water_vapour_flow.append(self.humidity_s*self.air_out_flow[i])
                self.water_liquid_flow.append(self.water_flow[i]-self.water_vapour_flow[i])
                # print(f"A cathode humidifier is not required")

        #Testing stuff
        print(f"Hydrogen mass flow is {np.mean(self.H2_flow)} kg/s")
        print(f"Oxygen mass flow is {np.mean(self.O2_flow)} kg/s")
        print(f"Air in mass flow is {np.mean(self.air_in_flow)} kg/s")
        print(f"Air out mass flow is {np.mean(self.air_out_flow)} kg/s")
        print(f"Water mass flow is {np.mean(self.water_flow)} kg/s")

        
#Just here for intermediate testing, move to UI later
# inputIV = IVCurves(p_s=2.5)
# Cell = CellParameters(IVCurves=inputIV)


        
        
            


