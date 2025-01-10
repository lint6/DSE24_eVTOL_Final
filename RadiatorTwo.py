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
        self.mu_a = 18.13e-6 #[kg/m s]
        self.rho_a = 1.204 #[kg/m^3]
        self.c_pa = 1.006e3 #[J/kg K]
        self.k_a = 25.86e-3 #[W/m K]

        #Water properties (same units as above)
        self.mu_w = 7.98e-4	
        self.rho_w = 1000
        self.c_pw = 4.3e3 
        self.k_w = 0.58

        #Copper properties
        self.k_copper = 398

        #Radiator geometry [m], from Canazas paper
        self.l = 23e-3 #Fin length
        self.h = 5.8e-3 #Fin height
        self.s = 0.7e-3 #Fin spacing
        self.t = 0.2e-3 #Fin thickness
        self.d = 2e-3 #Inner tube thickness

    
    def HydraulicDiameter(self):
        #Water
        self.D_hw = 4*((self.d*(self.l-self.d)+np.pi*(self.d**2/4))/(2*(self.l-self.d)+2*np.pi*(self.d/2)))

        #Air
        self.D_ha = (4/2)*((self.s*self.h)/(2*(self.s+self.h))+(self.s*self.h)/(self.s+2*self.h))

        
    
    def WaterNumbers(self):
        self.Pr_w = self.c_pw*self.mu_w/self.k_w #Prandtl number
        self.V_w = np.mean(self.BalanceOfPlant.HTC_coolant_flow)*(1/self.rho_w)*(1/(np.pi*self.d**2)) #Water flow velocity through tube, uses mean just for testing
        self.Re_w = (self.rho_w*self.V_w*self.D_hw)/(self.mu_w) #Reynolds number
        self.Nu_w = 0.012*(self.Re_w**0.87-280)*(self.Pr_w**0.4) #Nusselt number
        self.h_w = (self.Nu_w*self.k_w)/(self.D_hw)
        print(self.Re_w,self.h_w)
    
    def AirNumbers(self):
        self.Pr_a = self.c_pa*self.mu_a/self.k_a #Prandtl number
        self.V_a = np.arange(0,101,1) #Air velocity input array
        self.Re_a = (self.rho_a*self.V_a*self.D_ha)/(self.mu_a) #Reynolds number
        
        # #Air Nusselt number using NASA relations
        # self.Nu_a = np.zeros(len(self.Re_a))
        # for i in range(len(self.Re_a)):
        #     if self.Re_a[i] >= 5e5:
        #         # self.Nu_a[i] = (0.3387*self.Re_a[i]**(1/2)*self.Pr_a**(1/3))/(1+(0.0468/self.Pr_a)**(2/3))**(1/4)
        #         self.Nu_a[i] = 0.664*(self.Re_a[i]**(1/2))*(self.Pr_a**(1/3))
        #     if self.Re_a[i] < 5e5:
        #         # self.Nu_a[i] = 0.0296*(self.Re_a[i]**(4/5))*(self.Pr_a**(1/3))
        #         self.Nu_a[i] = (0.037*self.Re_a[i]**0.8*self.Pr_a)/(1+2.443*self.Re_a[i]**(-0.1)*(self.Pr_a**(2/3)-1))
        
        # self.h_a = (self.Nu_a*self.k_a)/(self.D_hw)
        # print(self.h_a)

        # self.m_f = np.sqrt((2*self.h_a)/(self.k_copper*self.t)) #Fin effectiveness parameter
        # self.eff_f = np.tanh(self.m_f*(self.h+self.t))/(self.m_f*(self.h+self.t)) #Fin efficiency
        # self.h_a = self.h_a/self.eff_f
        # self.h_a = (1/((1/self.h_a)+(1/self.h_w)))
        # print(self.h_a)
        

        #Different method based on polyfit to Canazas paper
        h = [75,240]
        Re = [500,4000]
        a = np.polyfit(Re,h,1) 

        self.h = a[0]*self.Re_a + a[1]   
        print(self.h)   

        #Different method again


        
        



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
Rad.WaterNumbers()
Rad.AirNumbers()