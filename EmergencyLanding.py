import numpy as np
from performance import PerformanceAnalysis, EnergyAnalysis

#Short thing to calculate the emergency landing energy requirements

class EmergencyLanding:
    def __init__(self,PerformanceAnalysis,distance=5000):
        #Get performance class
        self.PerformanceAnalysis = PerformanceAnalysis if PerformanceAnalysis else PerformanceAnalysis()

        self.h_start = 300 #Max altitude [m]
        self.h_end = 30 #Min altitude [m]
        self.V_steep = 7.6 #Steep descent vertical speed [m/s]

        self.distance = distance #Distance to fly before landing during emergency

    def DistanceTime(self):
        self.t_steep = (self.h_end-self.h_start)/self.V_steep #Steep descent time [s]
        self.d_steep = self.PerformanceAnalysis.power_velocity_steep_descent*self.t_steep #Steep descent distance [m]

        self.d_cruise = self.distance - self.d_steep #Cruise distance to fly [m]
        self.t_cruise = self.d_cruise/self.PerformanceAnalysis.min_power_velocity #Time to cruise [s]

        self.t_Vdescent = 60 #Time to descent vertically [s]
        self.t_HOGE = 10 #Time to HOGE [s]

    def Energy(self):
        self.E_steep = self.t_steep*self.PerformanceAnalysis.power_steep_descent_watts 
        self.E_cruise = self.t_cruise*self.PerformanceAnalysis.min_power_watts
        self.E_Vdescent = self.t_Vdescent*self.PerformanceAnalysis.P_vertical_descent
        self.E_HOGE = self.t_HOGE*self.PerformanceAnalysis.P_hoge

        self.E_emergency = self.E_steep+self.E_cruise+self.E_Vdescent+self.E_HOGE

        print(f"The battery energy required for emergency landing is {self.E_emergency/3600:.2f} [Wh]")
        

#Stuff for testing if it works
performance = PerformanceAnalysis()
performance.hover_powers()
performance.vertical_climb_descent_powers()
performance.forward_flight_powers()
performance.climb_descent_powers()
performance.iterate_design()
performance.plot_forward_flight()
performance.plot_CD_power()
emergency = EmergencyLanding(performance)
emergency.DistanceTime()
emergency.Energy()

        

