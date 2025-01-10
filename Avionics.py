import numpy as np

class Avionics:
    def __init__(self,MTOW=714):
        self.MTOW = MTOW

        #Flight controls
        self.P_controls = 28*(2.2+1.5) #Bypass solenoid & SCAS

        #Flight instruments
        self.P_finstruments = 28*(0.1+4+0.8+0.8+0.2) 

        #Heating
        self.P_heating = 28*(2.8+0.14+0.2+16.7)

        #Lighting
        self.P_lighting = 28*(1.02+3.8+3.72+18.2+0.5+0.17+1.5)

        #Warning & Emergency
        self.P_emergency = 28*(0.1+0.1+0.04+0.36+0.04+0.4+4)

        #NAVCOM
        self.P_navcom = 28*(1.02+3.1+0.1+1+0.2+1.33+1.3)

        #Systems & monitoring
        self.P_sys = 28*(2.7+1+0.235)

        #Total
        self.P_av = self.P_controls+self.P_finstruments+self.P_heating+self.P_lighting+self.P_emergency+self.P_navcom+self.P_sys

        print(f"====AVIONICS POWER====")
        print(f"Flight Controls [W]: {self.P_controls:.2f}")
        print(f"Flight Instruments [W]: {self.P_finstruments:.2f}")
        print(f"Heating [W]: {self.P_heating:.2f}")
        print(f"Lighting [W]: {self.P_lighting:.2f}")
        print(f"Emergency [W]: {self.P_emergency:.2f}")
        print(f"NAV & COM [W]: {self.P_navcom:.2f}")
        print(f"Systems [W]: {self.P_sys:.2f}")
        print(f"Total [W]: {self.P_av:.2f}")

Av = Avionics()