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

P_net = 100e3 #Net power (P_D-P_BOP), user specified 
P_range = 0.5*P_net #Range to iterate over
P_iterate = np.linspace(P_net,P_net+P_range,1000)
tolerance = 100

input_pressures = np.linspace(1.00,2.50,100) #Input stack pressures
P_D_list = []
Weight_list = []
counter = 0

for j in input_pressures:
    inputIV = IVCurves(p_s=j)
    for i in P_iterate:
        inputCell = CellParameters(IVCurves=inputIV,P_D=i,V_D=840)
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
        
        index = 0
        for n in range(len(Weights.W_PEMFC)):
            if Weights.W_PEMFC[n] == min(Weights.W_PEMFC):
                index = n

        if P_net - tolerance <= (inputCell.P_D-BOP.P_BOP[index]) <= P_net + tolerance:
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
inputCell = CellParameters(IVCurves=inputIV,P_D=P_D_list[bindex],V_D=840)
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



#Create plot showing pressure vs weight
# plt.figure(figsize=(10, 6))
# plt.plot(input_pressures, Weight_list, color='blue')

# plt.scatter(input_pressures[bindex], Weight_list[bindex], color='orange', zorder=5)

# plt.title(f"PEMFC system weight vs Stack Pressure")
# plt.grid(color='gray', linestyle=':', linewidth=0.5)
# plt.xlabel("Stack pressure [atm]")
# plt.ylabel("PEMFC system weight [kg]")

# plt.tight_layout()
# plt.show()




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
