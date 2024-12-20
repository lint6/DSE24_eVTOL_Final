import numpy as np
import matplotlib.pyplot as plt

#Code written by Jorrit
#This class focuses on drawing the i-v, i-p, and i-q curves for a user-specified stack pressure (1.0,1.25,1.5,2.0,2.5 atm) 
#It assumes a stack operating temperature of 80 degrees Celsius. 
#The values for modeling the losses are taken from Table 9 of the Datta PEMFC paper

class IVCurves:
    def __init__(self, p_s=1.25):
        #General constants
        self.R = 8.3144621 #Universal gas constant [J/mol-K]
        self.T = 273.15 + 80 #Stack temperature in Kelvin
        self.F = 96485 #Faraday constant [Coulomb/mol]

        #Voltage loss calculation fitting constants
        self.E_r = [1.1713, 1.1729, 1.1743, 1.1765, 1.1782] #Reversible cell voltage [V]
        self.i0_c = 0.0001                   #Cathode current adjustment, does not vary with pressure
        self.alpha_c = [0.18, 0.19, 0.20, 0.21, 0.22] #Cathode activation constant 
        self.i0_a = 0.1                     #Anode current adjustment, does not vary with pressure
        self.alpha_a = 0.5                     #Anode activation constant, does not vary with pressure
        self.ASR = 0.04                     #Area specific resistance, [Ohm cm^2], does not vary with pressure
        self.i_l = [1.75, 1.85, 1.95, 2.25, 2.45] #Limiting current [Ampere / cm^2]
        self.i_leak = [0.15, 0.15, 0.20, 0.25, 0.30] #Leak current [Ampere / cm^2]
        self.C = [0.03, 0.035, 0.035, 0.035, 0.035] #Concentration loss fitting constant [V]
        self.p = [1.00,1.25,1.50,2.00,2.50] #Corresponding pressures [atm]
        
        if 1.00 <= p_s <= 2.50:
            self.E_r = np.interp(p_s,self.p,self.E_r)
            self.alpha_c = np.interp(p_s,self.p,self.alpha_c)
            self.i_l = np.interp(p_s,self.p,self.i_l)
            self.i_leak = np.interp(p_s,self.p,self.i_leak)
            self.C = np.interp(p_s,self.p,self.C)
            
        if p_s == 4.0: #Just as a test, data from different PEMFC
            self.E_r = 1.1819
            self.alpha_c = 0.16
            self.ASR = 0.06
            self.i_l = 1.23
            self.i_leak = 0.01
            self.C = 0.12
        
        #Define max valid current density for model [A/cm^2]
        self.i_maxvalid = self.i_l - self.i_leak

        self.p_s = p_s * 101325     #Stack pressure [Pascal]

        self.CalculateIV()

    def CalculateIV(self):
        self.i = np.arange(0.01, self.i_maxvalid,0.01) #Set range for current density [A/cm^2]

        #Anode fitting coefficents (2 is from number of moles of electrons at anode)
        self.a_a = -((self.R * self.T)/(self.alpha_a*2*self.F))*np.log(self.i0_a)
        self.b_a = (self.R*self.T)/(self.alpha_a*2*self.F)

        #Cathode fitting coefficents (4 is from number of moles of electrons at cathode)
        self.a_c = -((self.R * self.T)/(self.alpha_c*4*self.F))*np.log(self.i0_c)
        self.b_c = (self.R*self.T)/(self.alpha_c*4*self.F)

        #Calculate activation loss [V]
        self.eta_act = self.a_a + self.b_a * np.log(self.i+self.i_leak) + self.a_c + self.b_c * np.log(self.i+self.i_leak)

        #Calculate ohmic loss [V]
        self.eta_ohmic = self.i * self.ASR
        
        #Calculate concentration loss [V]
        self.eta_conc = self.C * np.log(self.i_l/(self.i_l-(self.i-self.i_leak)))

        #Calculate cell voltage [V]
        self.v = self.E_r - self.eta_act - self.eta_ohmic - self.eta_conc

        #Calculate power density [W/cm^2]
        self.p = self.i*self.v

        #Ideal reversible cell voltage (Placeholder)
        self.E_h = self.E_r/0.8

        #Calculate heat [W/cm^2]
        self.q = self.i * (self.E_h - self.v)

        # #For testing, just use one point for now:
        # self.p_max = max(self.p)
        # index = 0
        # for i in range(len(self.p)):
        #     if self.p[i] == self.p_max:
        #         index = i
        
        # self.v = self.v[index]
        # self.p = self.p[index]
        # self.q = self.q[index]
        # print(f"The current design point is {self.v} V, {self.p} W/cm^2 power, and {self.q} W/cm^2 heat")


    def PlotCurves(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.i, self.v, label='Cell voltage', color='blue')
        plt.plot(self.i, self.p, label='Power Density', color='green')
        plt.plot(self.i, self.q, label='Heat', color='red')

        plt.title(f"IV Curves for {self.p_s/101325} atm")
        plt.legend(loc='upper left', fontsize='large')
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.xlabel("Current density [A/cm^2]")
        plt.ylabel("Cell voltage [V], Power density [A/cm^2], Heat [A/cm^2]")

        plt.tight_layout()
        plt.show()

#This is just to get the curves for now, move to UI later
# object = IVCurves(p_s=2.50)
# object.PlotCurves()