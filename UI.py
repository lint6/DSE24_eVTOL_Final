import numpy as np
import matplotlib.pyplot as plt
from IVCurves import IVCurves
from CellParameters import CellParameters
from ThermodynamicProperties import ThermoDynamicProperties
from BalanceOfPlant import BalanceOfPlant
from CellWeights import CellWeights

#Just some tools atm, if you want to run the entire thing look at the bottom of CellWeights
#This has some general checks (optimal pressure, net power). If you want to run a specific file, just uncomment the stuff at the bottom of that file.
#The general order of files is IVCurves -> CellParameters -> BalanceOfPlant -> CellWeights


#Required design power check for a user specified net power. Note to self: this is critical for comparing performance at different stack pressures.
#Because highest stack pressures give lower weights for a set design power, but they also give lower net power (due to higher P_BOP)

P_net = 100e3 #Net power (P_D-P_BOP), user specified 
P_range = 0.5*P_net #Range to iterate over
P_iterate = np.linspace(P_net,P_net+P_range,1000)
tolerance = 100

for i in P_iterate:
    inputIV = IVCurves(p_s=2.50)
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
    for i in range(len(Weights.W_PEMFC)):
        if Weights.W_PEMFC[i] == min(Weights.W_PEMFC):
            index = i

    if P_net - tolerance <= (inputCell.P_D-BOP.P_BOP[index]) <= P_net + tolerance:
        print(f"The required design power for a net power of {P_net} is {P_iterate[i]:.2f}")
        break
    

#Optimal stack pressure check (valid inputs are pressures on range [1, 2.5])
#Note that as of now this basically just tells you that higher stack pressures give you lower weights, but as explained above this is not a valid comparison. 
#Need to update tool

input_pressures = np.linspace(1.00,2.50,1000) #Input stack pressures
print(max(input_pressures))
output_weights = []

for i in input_pressures:
    inputIV = IVCurves(p_s=i)
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
    output_weights.append(min(Weights.W_PEMFC))

pin = 0
for i in range(len(output_weights)):
    if output_weights[i] == min(output_weights):
        pin = i

print(f"The lowest weight is {min(output_weights):.2f} kg at a pressure of {input_pressures[pin]} atm")
