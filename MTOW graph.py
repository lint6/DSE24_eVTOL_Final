import numpy as np
import matplotlib.pyplot as plt

iterations = [1,2,3,4,5,6,7]
weights = [718.89,709.63,953.15,765.13,822.17,832.03,839.24]

plt.figure(figsize=(10, 6))
plt.scatter(iterations, weights, color='blue')

plt.title(f"Iteration Weight Progression")
# plt.legend(loc='upper left', fontsize='large')
plt.grid(color='gray', linestyle=':', linewidth=0.5)
plt.xlabel("Iteration Number")
plt.ylabel("MTOW [kg]")

plt.tight_layout()
plt.show()
