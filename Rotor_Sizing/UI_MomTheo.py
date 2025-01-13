import Momentum_Theory
import matplotlib.pyplot as plt 
import numpy as np

def func_min_locator(list1, list2): #find the minimum and its index in list2 and locate the item at the same index in list1
    min_list2 = np.min(list2)
    min_list2_index = list(list2).index(min_list2)
    return list1[min_list2_index], min_list2

VertFli = Momentum_Theory.Vertical_Flight(mass=float(718.89/6),radius=1.2, P_a=160000)

# Calculate hover induced velocity
print(f"Hover Induced Velocity: {VertFli.calc_v_h():.2f}")

# Calculate thrust for hover
print(f"Thrust for Hover: {VertFli.calc_thrust_hover():.2f}")

# Calculate power for steady climb
if VertFli.P_a == None: #give climb rate, not power
    print(f"Given axial Rate of Climb: {VertFli.V_c:.2f}m/s")
    print(f"Power needed for climb: {VertFli.calc_P_kappa():.2f}W")
else: #give power, not climb rate
    print(f"Given power available for climb: {VertFli.P_a:.2f}W")
    print(f"Axial Rate of Climb achieved: {VertFli.calc_V_c_kappa()[0]:.2f}m/s")
if VertFli.V_c < 0 and abs(VertFli.V_c)/VertFli.v_h >= 2:
    raise Exception(f'V_c v_h ratio too negative, theory does not apply (current ratio {VertFli.V_c/VertFli.v_h}, needs to be greater than -2)')

print(f"calc_power_ideal_hover: {VertFli.calc_power_ideal_hover():.2f}")

print(f"Disc_loading: {VertFli.calc_disc_loading()[0]:.2f}")
print(f"Power_loading: {(VertFli.calc_mass()[0]/(VertFli.calc_power_ideal_hover()/1000)):.2f}")

vel = np.arange(0,100,0.01)
power = []
for i in vel :
    ForwFli = Momentum_Theory.Forward_Flight(mass=float(718.89/6), Cd0=0.96, V=i, related_vertical=VertFli, radius = 1.2, P_a=160000)    
    # VertFli.calc_v_h()
    # ForwFli.calc_V_horizontal()
    # ForwFli.calc_D()
    # ForwFli.calc_weight()
    # ForwFli.calc_T()
    # ForwFli.calc_rotor_alpha()
    # ForwFli.calc_V_nd()
    # ForwFli.calc_v_f_nd()
    # ForwFli.calc_v_f()
    # ForwFli.calc_V_dash()
    # #ForwFli.calc_T_axial()
    # ForwFli.calc_V_c_f()
    # ForwFli.calc_power_ideal_forwardflight()
    power.append(ForwFli.calc_power_ideal_forwardflight())
power = np.array(power)/int(1000)
print(power)


'''Horizontal Flight'''
# Power lines
plt.plot(vel, power.T[0], "-", label="Total")  # You can use other types like plt.scatter, plt.bar, etc.
plt.plot(vel, power.T[1], "--",label="Induced")
plt.plot(vel, power.T[2], "--",label="Parasitic")
#Critical Points
vel_power_min, power_min = func_min_locator(vel, power.T[0])
plt.plot(vel_power_min, power_min, '.', label=f'Min. Power \nV = {vel_power_min:.1f}m/s \nP = {power_min:.2f}kW')
plt.plot(vel[0], power[0][0], '.', label=f'Hover Power P = {power[0][0]:.2f}kW')

plt.title('Forward Flight Power (Single rotor)')              # Title of the graph
plt.xlabel('Velocity [m/s]')         # Label for the x-axis
plt.ylabel('Power Required [kW]')         # Label for the y-axis
plt.legend()                       # Add a legend (if needed)
plt.grid(True)                     # Add a grid (optional)
plt.show()
plt.clf

'''Vertical Flight'''
max_rate = 3
vertical_rate = np.arange(-max_rate,max_rate, max_rate/250)
vertical_rate = np.sort(np.append(vertical_rate, 0))
vertical_power = []
for i in vertical_rate :
    VertFli = Momentum_Theory.Vertical_Flight(mass=float(718.89/6),radius=0.96, V_c=i)
    vertical_power.append(VertFli.calc_P_kappa())
vertical_power = np.array(vertical_power)/int(1000)

plt.plot(vertical_rate, vertical_power, "-", label="Power Required")
plt.plot(0, vertical_power[list(vertical_rate).index(0)], '.', label=f'Hover Power P = {vertical_power[list(vertical_rate).index(0)]:.2f}kW')
# plt.plot((fan_1.v_h*-2, fan_1.v_h*-2), (min(vertical_power),max(vertical_power)), "--", label=f"V_c/v_h < -2\nV_c = {fan_1.v_h*-2:.2f}m/s")
plt.title('Power Required for vertical rate')
plt.xlabel('Vertical Rate [m/s]')
plt.ylabel('Power Required [kW]')
plt.legend() 
plt.grid(True)   
plt.show()


# fan_3 = ducted_fan_calc.Ducted_Fan_3(mtow=float(1069.137/4), gamma=2, related_fan1=fan_1, related_fan2 = fan_2 )
# print(f"V_c_slow: {fan_3.calc_V_c_slow()}")
# print(f"V_c_fast: {fan_3.calc_V_c_fast()}")
