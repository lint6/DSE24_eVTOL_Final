import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant
from CellWeights import CellWeights

#Currently, this finds the required design power for a user specified net power. It iterates over a range of pressures, and finds what pressure and design power combination gives lowest PEMFC weight

#If you want to run a specific file, just uncomment the stuff at the bottom of that file.
#The general order of files is IVCurves -> CellParameters -> BalanceOfPlant -> CellWeights


#Required design power check for a user specified net power. Note to self: this is critical for comparing performance at different stack pressures.
#Because highest stack pressures give lower weights for a set design power, but they also give lower net power (due to higher P_BOP)

safety_factor = 1 
P_motor = 71817.87 #Input from performance
P_battery = 7134.52 #Input from performance
P_avionics = 2110.50 #Get this from the Avionics class [W]

converter_efficiency = 0.98 #Based on NASA SoA DC/DC converter 
inverter_efficiency = 0.98 #Based on Yamaguchi IEEE paper for SiC inverter efficiency
motor_efficiency = 0.93 #From motor graph, check if accurate

P_net = safety_factor * (((P_motor)/(converter_efficiency*motor_efficiency*inverter_efficiency))+P_avionics/(converter_efficiency**2)+P_battery/converter_efficiency)  #Power that fuel cell needs to deliver during cruise. Note that BoP power and converter is already included in BalanceOfPlant.
P_range = 0.5*P_net #Range to iterate over
P_iterate = np.linspace(P_net,P_net+P_range,1000)
tolerance = 100

mission_time = 81.61*60 #Mission time [s]

input_pressures = np.linspace(1.00,2.50,100) #Input stack pressures
P_D_list = []
Weight_list = []
counter = 0

V_design = 840 #Design voltage [V]

for j in input_pressures:
    inputIV = IVCurves(p_s=j)
    for i in P_iterate:
        inputCell = CellParameters(IVCurves=inputIV,P_D=i,V_D=V_design)
        BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
        BOP.AirPower()
        BOP.HTCPower()
        BOP.LTCPower()
        BOP.WaterPower()
        BOP.ElecPower()
        BOP.BOPPower()
        Weights = CellWeights(IVCurves=inputIV,CellParameters=inputCell,BalanceOfPlant=BOP,missiontime=mission_time)
        Weights.StackWeight()
        Weights.HydrogenWeight()
        Weights.TankWeight()
        Weights.AirWeight()
        Weights.HTCWeight()
        Weights.LTCWeight()
        Weights.WaterWeight()
        Weights.ElectricalWeight()
        Weights.TotalWeight()
        
        index = 0
        for n in range(len(Weights.W_PEMFC)):
            if Weights.W_PEMFC[n] == min(Weights.W_PEMFC):
                index = n

        if P_net - tolerance <= (inputCell.P_D-BOP.P_BOP_gross[index]) <= P_net + tolerance:
            P_D_list.append(i)
            Weight_list.append(Weights.W_PEMFC[index])
            break
            # print(f"The required design power for a net power of {P_net} is {P_iterate[i]:.2f}")
    counter += 1
    print(counter) #Just to show progress as it can take a while to run
            
# print(P_D_list)
# print(Weight_list)

#Find the best combination:
bindex = 0
for i in range(len(Weight_list)):
    if Weight_list[i] == min(Weight_list):
        bindex = i

print(f"The best combination for a PEMFC with a net power of {P_net:.2f} [W] is a pressure of {input_pressures[bindex]:.2f} [atm] and a design power of {P_D_list[bindex]:.2f} [W], which gives a weight of {Weight_list[bindex]:.2f} [kg]")

#Get the best stack characteristics
inputIV = IVCurves(p_s=input_pressures[bindex])
inputCell = CellParameters(IVCurves=inputIV,P_D=P_D_list[bindex],V_D=V_design)
BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
BOP.AirPower()
BOP.HTCPower()
BOP.LTCPower()
BOP.WaterPower()
BOP.ElecPower()
BOP.BOPPower()
Weights = CellWeights(IVCurves=inputIV,CellParameters=inputCell,BalanceOfPlant=BOP,missiontime=mission_time)
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



#Create plot showing pressure vs weight
plt.figure(figsize=(10, 6))
plt.plot(input_pressures, Weight_list, color='blue')

plt.scatter(input_pressures[bindex], Weight_list[bindex], color='orange', zorder=5)

plt.title(f"PEMFC system weight vs Stack Pressure")
plt.grid(color='gray', linestyle=':', linewidth=0.5)
plt.xlabel("Stack pressure [atm]")
plt.ylabel("PEMFC system weight [kg]")

plt.tight_layout()
plt.show()




#Optimal stack pressure check (valid inputs are pressures on range [1, 2.5])
#Note that as of now this basically just tells you that higher stack pressures give you lower weights, but as explained above this is not a valid comparison. 
#Need to update tool

# input_pressures = np.linspace(1.00,2.50,1000) #Input stack pressures
# print(max(input_pressures))
# output_weights = []

# for i in input_pressures:
#     inputIV = IVCurves(p_s=i)
#     inputCell = CellParameters(IVCurves=inputIV,P_D=105000,V_D=840)
#     BOP = BalanceOfPlant(IVCurves=inputIV,CellParameters=inputCell)
#     BOP.AirPower()
#     BOP.HTCPower()
#     BOP.LTCPower()
#     BOP.WaterPower()
#     BOP.ElecPower()
#     BOP.BOPPower()
#     Weights = CellWeights(IVCurves=inputIV,CellParameters=inputCell,BalanceOfPlant=BOP)
#     Weights.StackWeight()
#     Weights.HydrogenWeight()
#     Weights.TankWeight()
#     Weights.AirWeight()
#     Weights.HTCWeight()
#     Weights.LTCWeight()
#     Weights.WaterWeight()
#     Weights.ElectricalWeight()
#     Weights.TotalWeight()
#     output_weights.append(min(Weights.W_PEMFC))

# pin = 0
# for i in range(len(output_weights)):
#     if output_weights[i] == min(output_weights):
#         pin = i

# print(f"The lowest weight is {min(output_weights):.2f} kg at a pressure of {input_pressures[pin]} atm")
