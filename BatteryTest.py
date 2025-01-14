import math

def calculate_battery_pack(
    nominal_capacity_ah,
    nominal_voltage_v,
    nominal_energy_wh,
    mass_per_cell_kg,
    diameter_mm,
    height_mm,
    max_discharge_power_cell_w,
    power_required_w,
    duration_s,
    max_cell_current_a
):
    # Calculate number of cells in series 
    
    # Calculate number of cells in series
    cells_in_series = math.ceil(power_required_w / max_discharge_power_cell_w)

    # Calculate total voltage and ensure cells in series provide sufficient voltage
    battery_voltage = cells_in_series * nominal_voltage_v

    # Calculate current required from the battery pack
    current_required_a = power_required_w / battery_voltage

    # Calculate number of cells in parallel
    cells_in_parallel = math.ceil(current_required_a / max_cell_current_a)

    # Ensure the required energy is met
    energy_required_wh = power_required_w * (duration_s / 3600)
    energy_per_parallel_string_wh = cells_in_series * nominal_energy_wh
    min_parallel_cells_for_energy = math.ceil(energy_required_wh / energy_per_parallel_string_wh)

    # Adjust cells in parallel to meet energy requirements
    cells_in_parallel = max(cells_in_parallel, min_parallel_cells_for_energy)

    # Improve safety by ensuring at least two parallel strings
    cells_in_parallel = max(cells_in_parallel, 2)

    # Total number of cells
    total_cells = cells_in_series * cells_in_parallel

    # Weight of the battery pack
    battery_weight_kg = total_cells * mass_per_cell_kg

    # Overall capacity of the battery pack
    total_capacity_ah = cells_in_parallel * nominal_capacity_ah

    # Overall energy of the battery pack
    total_energy_wh = total_capacity_ah * battery_voltage

    # Arrange cells in a rectangular shape as close to a square as possible
    rows = math.ceil(math.sqrt(total_cells))
    cols = math.ceil(total_cells / rows)

    # Dimensions of the battery pack
    pack_width_mm = cols * diameter_mm
    pack_length_mm = rows * diameter_mm
    pack_height_mm = height_mm

    # Results
    results = {
        "Cells in Series": cells_in_series,
        "Cells in Parallel": cells_in_parallel,
        "Total Cells": total_cells,
        "Battery Voltage (V)": battery_voltage,
        "Battery Current (A)": current_required_a,
        "Battery Weight (kg)": battery_weight_kg,
        "Battery Capacity (Ah)": total_capacity_ah,
        "Battery Energy (Wh)": total_energy_wh,
        "Pack Dimensions (mm)": {
            "Width": pack_width_mm,
            "Length": pack_length_mm,
            "Height": pack_height_mm,
        },
    }

    return results

# Example inputs Tesla 4680 Gen 2
inputs = {
    "nominal_capacity_ah": 25.73,
    "nominal_voltage_v": 3.7,
    "nominal_energy_wh": 95.2,
    "mass_per_cell_kg": 0.35,
    "diameter_mm": 46,
    "height_mm": 80,
    "max_discharge_power_cell_w": 521,
    "power_required_w": 42961,
    "duration_s": 315,
    "max_cell_current_a": 2.73*25.73 ,
}


# 5.4734537493158182813355227148331


# #Example inputs Skeleton Superbattery 
# inputs = {
#     "nominal_capacity_ah": 23.0,
#     "nominal_voltage_v": 2.25,
#     "nominal_energy_wh": 53,
#     "mass_per_cell_kg": 0.810,
#     "diameter_mm": 60,
#     "height_mm": 138,
#     "max_discharge_power_cell_w": 1060,
#     "power_required_w": 42961,
#     "duration_s": 315,
#     "max_cell_current_a": 460 ,
# }

# Calculate battery pack design
battery_pack_design = calculate_battery_pack(**inputs)

# Display results
for key, value in battery_pack_design.items():
    print(f"{key}: {value}")
