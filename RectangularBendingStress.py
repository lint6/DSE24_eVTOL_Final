import numpy as np 
import matplotlib.pyplot as plt 

class BeamStress: 

    def __init__(self, Mx=619, My=5.62644, h=7.68, w=None, beam_length=1.22, density=1274):
        ''' Initialize the BeamStress Class'''
        ### input Mx and My in [Nm], h and w in [mm], beam_length in [m], and density in [kg/m^3]
        self.Mx = Mx # in [Nm]
        self.My = My # in [Nm]
        self.h = h / 1000 # in [m]
        self.w = w / 1000 if w else self.h # in [m], default to h if not provided
        self.beam_length = beam_length # [m]
        self.density = density # [kg/m^3]

    def calculate_cross_sectional_area(self):
        return self.h * self.w # [m^2]
    
    def calculate_volume(self):
        return self.calculate_cross_sectional_area() * self.beam_length # [m^3]
    
    def calculate_weight(self): 
        return self.calculate_volume() * self.density # [kg]

    def calculate_Ixx(self):
        Ixx = (1/12) * self.w * self.h**3
        return Ixx # returns [m^4]
    
    def calculate_Iyy(self):
        Iyy = (1/12) * self.h * self.w**3
        return Iyy # returns [m^4]
    
    def calculate_stress_point(self, x, y):
        sigma = (self.Mx * y) / self.calculate_Ixx() - (self.My * x) / self.calculate_Iyy()
        return sigma # returns in [Pa]
    
    def calculate_maximum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.max(stresses)
    
    def calculate_minimum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.min(stresses)
    
    def calculate_stress_distribution(self, resolution=500):
        x_coords = np.linspace(-self.w/2, self.w/2, resolution) * 1000
        y_coords = np.linspace(-self.h/2, self.h/2, resolution) * 1000

        x_grid, y_grid = np.meshgrid(x_coords, y_coords)
        stresses = self.calculate_stress_point(x_grid/1000, y_grid/1000)
        
        return x_grid.flatten(), y_grid.flatten(), stresses.flatten()
    
    def plot_stress_distribution(self):
        x_coords, y_coords, stresses = self.calculate_stress_distribution()
        
        plt.figure(figsize=(12, 6))

        scatter = plt.scatter(x_coords, y_coords, c=stresses/(10**6), cmap='seismic', s=1)
        plt.colorbar(scatter, label='Stress [MPa]')
        plt.xlabel('x-axis [mm]')
        plt.ylabel('y-axis [mm]')

        ax = plt.gca()
        ax.invert_xaxis()
        ax.invert_yaxis()

        plt.title('Stress Distribution Throughout the Cross-Section')
        plt.axis('equal')
        plt.grid(False)
        plt.show()

        
if __name__ == '__main__':
    # Example for a square beam
    # square_beam = BeamStress()
    # square_beam.plot_stress_distribution()
    # print('-------- Square Beam Stress Analysis --------')
    # print(f'Moment of Inertia (Ixx) = {square_beam.calculate_Ixx()} [m^4]')
    # print(f'Moment of Inertia (Iyy) = {square_beam.calculate_Iyy()} [m^4]')
    # print(f'Stress at Point 1 = {round(square_beam.calculate_stress_point(0.1, -0.1)/10**6, 4)} [MPa]')
    # print(f'Stress at Point 2 = {round(square_beam.calculate_stress_point(-0.1, -0.1)/10**6, 4)} [MPa]')
    # print(f'Stress at Point 3 = {round(square_beam.calculate_stress_point(-0.1, 0.1)/10**6, 4)} [MPa]')
    # print(f'Stress at Point 4 = {round(square_beam.calculate_stress_point(0.1, 0.1)/10**6, 4)} [MPa]')
    # print(f'Weight of the Beam: {round(square_beam.calculate_weight(), 4)} [kg]')
    # print(f'Maximum Positive Stress: {round(square_beam.calculate_maximum_stress()/10**6, 4)} [MPa]')
    # print(f'Maximum Negative Stress: {round(square_beam.calculate_minimum_stress()/10**6, 4)} [MPa]')

    # Example for a rectangular beam
    rectangular_beam = BeamStress(w=64)
    rectangular_beam.plot_stress_distribution()
    print('-------- Rectangular Beam Stress Analysis --------')
    print(f'Moment of Inertia (Ixx) = {rectangular_beam.calculate_Ixx()} [m^4]')
    print(f'Moment of Inertia (Iyy) = {rectangular_beam.calculate_Iyy()} [m^4]')
    print(f'Stress at Point 1 = {round(rectangular_beam.calculate_stress_point(0.1, -0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 2 = {round(rectangular_beam.calculate_stress_point(-0.1, -0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 3 = {round(rectangular_beam.calculate_stress_point(-0.1, 0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 4 = {round(rectangular_beam.calculate_stress_point(0.1, 0.1)/10**6, 4)} [MPa]')
    print(f'Weight of the Beam: {round(rectangular_beam.calculate_weight(), 4)} [kg]')
    print(f'Maximum Positive Stress: {round(rectangular_beam.calculate_maximum_stress()/10**6, 4)} [MPa]')
    print(f'Maximum Negative Stress: {round(rectangular_beam.calculate_minimum_stress()/10**6, 4)} [MPa]')