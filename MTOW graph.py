import numpy as np
import matplotlib.pyplot as plt

iterations = [1,2,3,4,5,6,7]
weights = [718.89,709.63,953.15,765.13,822.17,832.03,839.24]
max_powers = [97.64,96.38,88.03,68.72,79.86,83.53,85.51]
cruise_powers = [61.85,61.12,42.71,35.25,42.46,42.96,44.23]

plt.figure(figsize=(10, 6))
plt.scatter(iterations, weights, color='blue')

plt.title(f"Iteration Weight Progression")
# plt.legend(loc='upper left', fontsize='large')
plt.grid(color='gray', linestyle=':', linewidth=0.5)
plt.xlabel("Iteration Number")
plt.ylabel("MTOW [kg]")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(iterations, max_powers, label='Max Power', color='red')
plt.scatter(iterations, cruise_powers, label='Cruise Power', color='blue')

plt.title(f"Iteration Power Progression")
plt.legend(loc='upper right', fontsize='large')
plt.grid(color='gray', linestyle=':', linewidth=0.5)
plt.xlabel("Iteration Number")
plt.ylabel("Power [kW]")

plt.tight_layout()
plt.show()
