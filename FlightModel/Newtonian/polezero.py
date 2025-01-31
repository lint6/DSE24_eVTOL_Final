import control as ct
import numpy as np
import matplotlib.pyplot as plt

A = np.array([[-0.016, -0.022, -0.12, 0.47],
               [-3.30, -1.85, -10.88, -9.80],
               [-1.56e-4, 2.25e-4, -0.028, 0],
               [0,0,1,0]])

B = np.array([[0],[0],[0],[0]])
C = np.array([1,0,0,0])
D = np.array([0])

sys_ss = ct.ss(A, B,C,D)
sys_tf = ct.ss2tf(sys_ss)

print(sys_tf)
ct.pzmap(sys_ss, plot = True)
plt.show()     