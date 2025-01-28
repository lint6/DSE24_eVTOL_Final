import numpy as np 
import matplotlib.pyplot as plt 

class CripplingStres:

    def __init__(self, alpha=0.8, n=0.6, E=71.7, v=1/3,  t=1.5, sigma_y=503):
        ### E in [GPa], t in [mm], sigma_y in [MPa]
        ### t is stringer thickness
        self.alpha = alpha 
        self.n = n 
        self.E = E * 10**9 # [Pa]
        self.v = v 
        self.t = t / 1000 # [m]
        self.sigma_y = sigma_y * 10**6 # [Pa]
        self.b1 = 0.010 # [m]
        self.b2 = 0.027 # [m]
        self.b3 = 0.010 # [m]
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
    
    def calculate_average_crippling(self):
        ratio1 = self.calculate_ratio_1(self.sigma_y)
        ratio2 = self.calculate_ratio_2(self.sigma_y)
        ratio3 = self.calculate_ratio_3(self.sigma_y)
        actual1 = ratio1 * self.sigma_y
        actual2 = ratio2 * self.sigma_y
        actual3 = ratio3 * self.sigma_y
        return (actual1*self.t*self.b1 + actual2*self.t*self.b2 + actual3*self.t*self.b3) / (self.t * (self.b1 + self.b2 + self.b3))
    
    def calculate_stringer_area(self):
        area1 = self.b1 * self.t
        area2 = self.b2 * self.t
        area3 = self.b3  * self.t
        return area1 + area2 + area3

    def calculate_total_crippling(self):
        # total criplling of panel (including skin)
        t_skin = 0.0005 # [m] DERIVED FROM BOOM IDEALIZATION
        b_stiffener_spacing = 0.22253 # [m] DERIVED FROM BOOM IDEALIZATION
        sigma_buckling_skin = 0.43 * 10**6 #[Pa] DERIVED FROM BOOM IDEALIZATION
        average_cripple = self.calculate_average_crippling()
        area_stringer = self.calculate_stringer_area()
        sigma_total = ((average_cripple * area_stringer) + (t_skin * b_stiffener_spacing * sigma_buckling_skin)) / (area_stringer + b_stiffener_spacing * t_skin)
        print(sigma_total/10**6) # [MPa]
        return sigma_total
    
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
    print(f"Average Stringer Crippling Stress: {round(CS.calculate_average_crippling()/10**6, 2)} [MPa]")
    print(f"Stringer Area: {round(CS.calculate_stringer_area() * (1000)**2, 4)} [mm^2]")
    print(f"Total Crippling Stress: {round(CS.calculate_total_crippling()/10**6, 2)} [MPa]")
    #CS.plot_ratio1_vs_yield()
    #CS.plot_ratio2_vs_yield()
