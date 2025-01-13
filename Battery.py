import numpy as np
import matplotlib.pyplot as plt
import math 
#This calculation considers 1.27 safety factor on the powers
#as well as 20%-80% Depth of Discharge
#as well as a degree of hybridizaation of ...

#global input
P_req = 36965           #[W]
t = 315                 #[s] -> sum of longest consecutive discharge phases
Crate = 10

# Tesla 4680 
nVT = 3.7               #[V]
W_Tcell = 0.350         #[g]
E_Tspecific = 272       #[Wh/kg]
Cap_T = 25.73           #[Ah per cell]
Cap_Tkg = Cap_T / W_Tcell   #[Ah per kg]
P_Tdis = 1488           #[W/kg]


# Skeleton SuperBattery 
nVS = 2.25               #[V]
W_Scell = 0.810         #[g]
E_Sspecific = 65        #[Wh/kg]
Cap_S = 23.0            #[Ah per cell]
Cap_Skg = Cap_S / W_Scell   #[Ah per kg]
P_Sdis = 4000           #[W/kg]

def calculate_battery_configuration(P, t, V_cell, C_cell, I_max, V_pack, W):
    """
    Calculate the number of cells in series and parallel required to meet power and energy demands.

    Parameters:
        P (float): Power requirement in watts (W).
        t (float): Duration of operation in seconds (s).
        V_cell (float): Nominal voltage of a single cell in volts (V).
        C_cell (float): Capacity of a single cell in ampere-hours (Ah).
        I_max (float): Maximum discharge current of a single cell in amperes (A).
        V_pack (float): Desired pack voltage in volts (V).

    Returns:
        dict: A dictionary containing the number of cells in series, in parallel, and the total cells required.
    """
    # Step 1: Calculate energy required in watt-hours
    E_wh = (P * t) / 3600

    # Step 2: Calculate the number of cells in series
    N_series = np.ceil(V_pack / V_cell)

    # Step 3: Calculate the energy per cell in watt-hours
    E_cell = C_cell * V_cell

    # Step 4: Calculate the number of cells in parallel
    N_parallel = np.ceil(E_wh / (E_cell * N_series))

    # Step 5: Verify current limits
    I_req = P / V_pack
    I_per_cell = I_req / N_parallel

    if I_per_cell > I_max:
        raise ValueError("Current per cell exceeds the maximum allowable discharge current. Increase N_parallel.")

    # Step 6: Calculate total cells
    N_total = N_series * N_parallel

    return {
        "N_series": N_series,
        "N_parallel": N_parallel,
        "N_total": N_total,
        
    }

def find_optimal_configuration(P, t, V_cell, C_cell, V_pack_values, I_max_values, W):
    
    best_configuration = None
    lowest_weight = float('inf')
    results = []
    for V_pack in V_pack_values:
        for I_max in I_max_values:
            try:
                result = calculate_battery_configuration(P, t, V_cell, C_cell, I_max, V_pack, W)
                # Estimate weight based on the number of cells
                weight = result['N_total'] * W  # Fixed weight per cell in kilograms
                if weight < lowest_weight:
                    lowest_weight = weight
                    best_configuration = {
                        "V_pack": V_pack,
                        "I_req": P/V_pack,
                        "I_max": I_max,
                        "result": result,
                        "weight": weight
                    }
            except ValueError:
                continue
    
    return best_configuration

    



# Example Usage
if __name__ == "__main__":
    # Input Parameters
    P = P_req          # Power in watts
    t = t            # Time in seconds
    V_cell = nVT       # Voltage of a single cell in volts
    C_cell = Cap_T       # Capacity of a single cell in ampere-hours
    W = W_Tcell
    Crate = Crate       # C-rating considered to be around 10...,   11.4285 is the actual crating to discharge the cell completely.
    rara = 840            #starting range voltage

    # Iterate over different V_pack and I_max values
    V_pack_values = []  # Example pack voltages in volts
    I_max_values = [C_cell*Crate]   # Example maximum discharge currents in amperes
    for i in range(rara,841):
        V_pack_values.append(i)

    # for i in range(64,841):
    #     I_max_values.append(i)  


    optimal_solution = find_optimal_configuration(P, t, V_cell, C_cell, V_pack_values, I_max_values, W)

    if optimal_solution:
        print("\nOptimal configuration for the lowest weight using TESLA 4680 Gen 2:")
        print(f"V_pack: {optimal_solution['V_pack']} V")
        print(f"I_pack: {optimal_solution['I_req']} A")
        print(f"I_max: {optimal_solution['I_max']} A")
        print(f"Number of cells in series: {optimal_solution['result']['N_series']}")
        print(f"Number of cells in parallel: {optimal_solution['result']['N_parallel']}")
        print(f"Total number of cells: {optimal_solution['result']['N_total']}")
        print(f"Estimated weight: {optimal_solution['weight']} kg")
    else:
        print("\nNo working configuration found.")
    # Input Parameters
    P = P_req          # Power in watts
    t = t            # Time in seconds
    V_cell = nVS       # Voltage of a single cell in volts
    C_cell = Cap_S       # Capacity of a single cell in ampere-hours
    W = W_Scell
    Crate = Crate       # C-rating considered to be around 10...,   11.4285 is the actual crating to discharge the cell completely.

    # Iterate over different V_pack and I_max values
    V_pack_values = []  # Example pack voltages in volts
    I_max_values = [C_cell*Crate]   # Example maximum discharge currents in amperes
    for i in range(rara,841):
        V_pack_values.append(i)

    # for i in range(64,841):
    #     I_max_values.append(i)  


    optimal_solution = find_optimal_configuration(P, t, V_cell, C_cell, V_pack_values, I_max_values, W)

    if optimal_solution:
        print("\nOptimal configuration for the lowest weight Skeleton SuperBattery:")
        print(f"V_pack: {optimal_solution['V_pack']} V")
        print(f"I_pack: {optimal_solution['I_req']} A")
        print(f"I_max: {optimal_solution['I_max']} A")
        print(f"Number of cells in series: {optimal_solution['result']['N_series']}")
        print(f"Number of cells in parallel: {optimal_solution['result']['N_parallel']}")
        print(f"Total number of cells: {optimal_solution['result']['N_total']}")
        print(f"Estimated weight: {optimal_solution['weight']} kg")
    else:
        print("\nNo working configuration found.")



def compute_rectangle_size(circle_diameter, num_circles, row_limit=None):
    """
    Computes the size of the rectangle required to fit a given number of circles side by side or in multiple rows.

    Parameters:
    - circle_diameter (float): The diameter of a single circle.
    - num_circles (int): The total number of circles.
    - row_limit (int, optional): The maximum number of circles allowed per row. Defaults to all circles in one row.

    Returns:
    - (float, float): The width and height of the rectangle.
    """
    # Set row_limit to num_circles if not provided (all circles in one row by default)
    if row_limit is None or row_limit > num_circles:
        row_limit = num_circles

    # Calculate the number of rows and columns
    rows = math.ceil(num_circles / row_limit)
    columns = min(num_circles, row_limit)

    # Calculate rectangle dimensions
    width = columns * circle_diameter
    height = rows * circle_diameter

    return width, height

# Example usage
if __name__ == "__main__":
    circle_diameter = 46  # Diameter of each circle
    num_circles = 280      # Total number of circles
    row_limit = 17         # Maximum number of circles per row (optional)

    width, height = compute_rectangle_size(circle_diameter, num_circles, row_limit)
    print(f"To fit {num_circles} circles with diameter {circle_diameter} in rows of {row_limit}:")
    print(f"Rectangle dimensions: {width} x {height}")