import numpy as np 
import matplotlib.pyplot as plt 

class CriticalBucklingStress:

    def __init__(self, C=4, E=71.7, v=1/3, t=0.5, r=0.85):
        ### E in [GPa], t in [mm], r in [m]
        self.C = C
        self.E = E * 10**9 # [Pa]
        self.v = v 
        self.t = t / 1000 # [m]
        self.r = r

    def calculate_critical_at_b(self, b):
        sigma = self.C * (np.pi * self.E) / (12 * (1 - self.v**2)) * (self.t / b)**2 
        return sigma / 10**6 # [MPa]

    def plot_critical_buckling_stress(self):
        b = np.linspace(0.1, 0.5, 1000)  # Plate width from 0.01m to 2m
        sigmas = [self.calculate_critical_at_b(i) for i in b]
        n_stiffeners = 24
        b_actual = 2 * np.pi * self.r / n_stiffeners
        sigma_actual = self.calculate_critical_at_b(b_actual)
        plt.figure(figsize=(8, 6))
        plt.plot(b, sigmas, label=r'$\sigma_{cr}$ vs b', color='blue')
        plt.scatter(b_actual, sigma_actual, color='red', label=f"Design Point: {round(sigma_actual, 2)} [MPa]", s=100)
        plt.title('Skin Critical Buckling Stress ($\sigma_{cr}$) vs Stringer Spacing (b) for 24 stringers', fontsize=14)
        plt.xlabel('Stiffener Spacing, b [m]', fontsize=12)
        plt.ylabel('Critical Buckling Stress [MPa]', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.show()

if __name__ == '__main__':
    CBS = CriticalBucklingStress()
    CBS.plot_critical_buckling_stress()