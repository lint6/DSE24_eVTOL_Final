import numpy as np

#Thingy for sizing the converters and the inverter

class Converter:
    def __init__(self):
        self.converter_efficiency = 0.98 #NASA SoA
        self.inverter_efficiency = 0.98 #Yamaguchi
        self.motor_efficiency = 0.93

        #Power inputs from performance
        self.P_net_motor = 38760.60e-3 #Net motor power [kW]
        self.P_net_bat = 5651.78e-3 
        self.P_net_BOP = 4081.34e-3
        self.P_net_av = 2.11

        self.P_bat = self.P_net_bat/self.converter_efficiency #Power through battery converter [kW]
        self.P_BOP = self.P_net_BOP/self.converter_efficiency #Power through BoP converter
        self.P_av = self.P_net_av/(self.converter_efficiency**2) #Power through avionics converters [kW]
        self.P_motor = self.P_net_motor/(self.motor_efficiency*self.converter_efficiency*self.inverter_efficiency) #Power through motor converter [kW]
        # self.W_single_converter = 0.507 #Weight of a single converter [kg], from Louvrier
        self.P_specific_converter = 7.5 #[kW/kg], from NASA SoA


    def ConverterWeight(self):
        self.W_BOPconv = self.P_BOP/self.P_specific_converter
        self.W_Motconv = self.P_motor/(self.P_specific_converter)
        self.W_Batconv = self.P_bat/(self.P_specific_converter)
        self.W_Avconv = 2*self.P_av/(self.P_specific_converter)
        self.W_Totconv = self.W_BOPconv+self.W_Motconv+self.W_Batconv+self.W_Avconv
        print(f"BOP converter weight is {self.W_BOPconv:.2f} [kg]")
        print(f"Motor converter weight is {self.W_Motconv:.2f} [kg]")
        print(f"Battery converter weight is {self.W_Batconv:.2f} [kg]")
        print(f"Avionics converters (total) weight is {self.W_Avconv:.2f} [kg]")
        print(f"Total converter weight is {self.W_Totconv:.2f} [kg]")
        
    
    def ConverterSize(self):
        self.l = 48 #[cm/10 kW]
        self.w = 12 #[cm/10 kW]
        self.h = 6.5 #[cm/10 kW]

        #Very simplified converter sizing, basically only motor is relevant imo
        print(f"BOP converter size is: {self.l:.2f} x {self.w:.2f} x {(self.P_BOP/10)*self.h:.2f} cm") 
        print(f"Motor converter size is: {self.l:.2f} x {self.w:.2f} x {(self.P_motor/10)*self.h:.2f} cm")
        print(f"Battery converter size is: {self.l:.2f} x {self.w:.2f} x {(self.P_bat/10)*self.h:.2f} cm")
        print(f"Avionics converters size is: {self.l:.2f} x {self.w:.2f} x {(self.P_av/10)*self.h:.2f} cm")
    
    def Inverter(self):
        self.P_specific_inverter = 50 #[kW/kg], Yamaguchi paper
        self.P_Motinv = self.P_motor*self.converter_efficiency #Power through inverter [kW]
        self.W_Motinv = self.P_Motinv/self.P_specific_inverter #Inverter weight [kg]

        self.l_i = 10.4 #[cm/33 kW] Yamaguchi values
        self.w_i = 11.0 #[cm/33 kW]
        self.h_i = 4.5 #[cm/33 kW]

        print(f"Inverter weight is {self.W_Motinv:.2f} [kg]")
        print(f"Inverter size is {self.l_i:.2f} x {self.w_i:.2f} x {(self.P_Motinv/33)*self.h_i:.2f} cm")

    def ConversionLosses(self):
        self.BOP_loss = 140.53e-3 #[kW], input from PEMFC model
        self.conversion_loss = (self.P_motor-self.P_net_motor) + (self.P_av-self.P_net_av) + (self.P_bat-self.P_net_bat) + self.BOP_loss
        print(f"Total conversion losses are {self.conversion_loss:.2f} [kW]")
    
    def TotalWeights(self):
        self.W_PDU = 16 #[kg], from EPEC product specification for passive PDUFPHN1PXXX 
        self.W_total = self.W_Totconv + self.W_Motinv + self.W_PDU
        print(f"Total infrastructure weight is {self.W_total:.2f} [kg]")




Convert = Converter()
Convert.ConverterWeight()
Convert.ConverterSize()
Convert.Inverter()
Convert.ConversionLosses()
Convert.TotalWeights()
