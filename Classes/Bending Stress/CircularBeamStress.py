import numpy as np
import matplotlib.pyplot as plt

class CircularBeamStress:

    def __init__(self, Mx=3650, My=667.7, D_outer=100, t=2, beam_length=2.93, density=2810):
        ''' Initialize the CircularBeamStress Class'''
        ### input Mx and My in [Nm], D_outer and t in [mm], beam_length in [m], and density in [kg/m^3]
        self.Mx = Mx  # in [Nm]
        self.My = My  # in [Nm]
        self.D_outer = D_outer / 1000  # in [m]
        self.t = t / 1000  # in [m]
        self.beam_length = beam_length # [m]
        self.density = density # [kg/m^3]

    def calculate_cross_sectional_area(self):
        return (np.pi / 4) * (self.D_outer**2 - (self.D_outer - 2 * self.t)**2) # [m^2]

    def calculate_volume(self):
        return self.calculate_cross_sectional_area() * self.beam_length # [m^3]
    
    def calculate_weight(self): 
        return self.calculate_volume() * self.density # [kg]

    def calculate_Ixx_Iyy(self):
        I_outer = (np.pi / 64) * (self.D_outer**4)
        I_inner = (np.pi / 64) * ((self.D_outer - 2 * self.t)**4)
        I = I_outer - I_inner
        return I  # returns [m^4]

    def calculate_stress_point(self, x, y):
        I = self.calculate_Ixx_Iyy()
        sigma = (self.Mx * y) / I - (self.My * x) / I
        return sigma  # returns in [Pa]
    
    def calculate_maximum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.max(stresses)
    
    def calculate_minimum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.min(stresses)

    def calculate_stress_distribution(self, resolution=500):
        R_outer = self.D_outer / 2
        R_inner = R_outer - self.t

        theta = np.linspace(0, 2 * np.pi, resolution)
        r = np.linspace(R_inner, R_outer, resolution)

        x_coords = []
        y_coords = []
        stresses = []

        for r_i in r:
            for theta_i in theta:
                x = r_i * np.cos(theta_i)
                y = r_i * np.sin(theta_i)
                stress = self.calculate_stress_point(x, y)
                x_coords.append(x * 1000)
                y_coords.append(y * 1000)
                stresses.append(stress)

        return np.array(x_coords), np.array(y_coords), np.array(stresses)

    def plot_stress_distribution(self):
        x_coords, y_coords, stresses = self.calculate_stress_distribution()

        plt.figure(figsize=(12, 6))

        scatter = plt.scatter(x_coords, y_coords, c=stresses / (10**6), cmap='seismic', s=1)
        plt.colorbar(scatter, label='Stress [MPa]')
        plt.xlabel('x-axis [mm]')
        plt.ylabel('y-axis [mm]')

        ax = plt.gca()
        ax.invert_xaxis()
        ax.invert_yaxis()

        plt.title('Stress Distribution along the Circular Beam')
        plt.axis('equal')
        plt.grid(False)
        plt.show()

if __name__ == '__main__':
    beam = CircularBeamStress()
    beam.plot_stress_distribution()
    print('-------- Circular Beam Stress Analysis --------')
    print(f"Moment of Inertia's (Ixx = Iyy): {beam.calculate_Ixx_Iyy()} [m^4]")
    print(f'Stress at Point 1: {round(beam.calculate_stress_point(0, -0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 2: {round(beam.calculate_stress_point(-0.1, 0)/10**6, 4)} [MPa]')
    print(f'Stress at Point 3: {round(beam.calculate_stress_point(0, 0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 4: {round(beam.calculate_stress_point(0.1, 0)/10**6, 4)} [MPa]')
    print(f'Weight of the Beam: {round(beam.calculate_weight(), 4)} [kg]')
    print(f'Maximum Positive Stress: {round(beam.calculate_maximum_stress()/10**6, 4)} [MPa]')
    print(f'Maximum Negative Stress: {round(beam.calculate_minimum_stress()/10**6, 4)} [MPa]')