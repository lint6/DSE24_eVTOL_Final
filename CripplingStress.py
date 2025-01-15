import numpy as np 
import matplotlib.pyplot as plt 

class CripplingStres:

    def __init__(self, alpha=0.8, n=0.6, E=70, v=1/3,  t=1.5, sigma_y=250):
        ### E in [GPa], t in [mm], sigma_y in [MPa]
        self.alpha = alpha 
        self.n = n 
        self.E = E * 10**9 # [Pa]
        self.v = v 
        self.t = t / 1000 # [m]
        self.sigma_y = sigma_y * 10**6 # [Pa]
        self.b1 = 0.010 # [m]
        self.b2 = 0.020 # [m]
        self.C1 = 0.425
        self.C2 = 4.0

    def calculate_ratio_1(self, sigma_y):
        ratio = self.alpha * ((self.C1/sigma_y) * (self.t/self.b1)**2 * (np.pi**2 * self.E / (12 * (1 - self.v**2)))) ** (1 - self.n)
        return ratio
    
    def calculate_ratio_2(self, sigma_y):
        ratio = self.alpha * ((self.C2/sigma_y) * (self.t/self.b2)**2 * (np.pi**2 * self.E / (12 * (1 - self.v**2)))) ** (1 - self.n)
        return ratio

    def calculate_ratio_3(self, sigma_y):
        return self.calculate_ratio_1(sigma_y)
    
    def plot_ratio1_vs_yield(self):
        sigma_y_values = np.linspace(100, 1000, 100) * 10**6  # Yield stress from 100 MPa to 1000 MPa
        ratios = [self.calculate_ratio_1(sigma_y) for sigma_y in sigma_y_values]
        closest_index = np.argmin(np.abs(np.array(ratios) - 1))
        sigma_y_closest = sigma_y_values[closest_index] / 10**6
        ratio_closest = ratios[closest_index]

        plt.figure(figsize=(8, 6))
        plt.plot(sigma_y_values / 10**6, ratios, label='Ratio 1 vs Yield Stress', color='blue')
        plt.scatter([sigma_y_closest], [ratio_closest], color='red', label=f'Ratio 1 = 1 at $\sigma_y$ = {sigma_y_closest:.2f} MPa')
        plt.title('Ratio 1 vs Yield Stress', fontsize=14)
        plt.xlabel('Yield Stress, $\sigma_y$ [MPa]', fontsize=12)
        plt.ylabel('Ratio 1', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.show()

    def plot_ratio2_vs_yield(self):
        sigma_y_values = np.linspace(100, 1000, 100) * 10**6  # Yield stress from 100 MPa to 1000 MPa
        ratios = [self.calculate_ratio_2(sigma_y) for sigma_y in sigma_y_values]
        closest_index = np.argmin(np.abs(np.array(ratios) - 1))
        sigma_y_closest = sigma_y_values[closest_index] / 10**6
        ratio_closest = ratios[closest_index]

        plt.figure(figsize=(8, 6))
        plt.plot(sigma_y_values / 10**6, ratios, label='Ratio 2 vs Yield Stress', color='green')
        plt.scatter([sigma_y_closest], [ratio_closest], color='red', label=f'Ratio 2 = 1 at $\sigma_y$ = {sigma_y_closest:.2f} MPa')
        plt.title('Ratio 2 vs Yield Stress', fontsize=14)
        plt.xlabel('Yield Stress, $\sigma_y$ [MPa]', fontsize=12)
        plt.ylabel('Ratio 2', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.show()
    

if __name__ == '__main__':
    CS = CripplingStres() 
    ratio1 = round(CS.calculate_ratio_1(CS.sigma_y), 3)
    ratio2 = round(CS.calculate_ratio_2(CS.sigma_y), 3)
    ratio3 = round(CS.calculate_ratio_3(CS.sigma_y), 3)
    print(f"Ratio 1: {ratio1}, Ratio 2: {ratio2}, Ratio 3: {ratio3}")
    CS.plot_ratio1_vs_yield()
    CS.plot_ratio2_vs_yield()
