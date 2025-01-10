import numpy as np 
import matplotlib.pyplot as plt 

class SquareBeamStress: 

    def __init__(self, Mx=1000, My=2000, h=200, t=10, beam_length=3, density=2710):
        ''' Initialize the SquareBeamStress Class'''
        ### input Mx and My in [Nm], h in [mm], t in [mm], beam_length in [m], and density in [kg/m^3]
        self.Mx = Mx # in [Nm]
        self.My = My # in [Nm]
        self.h = h / 1000 # in [m]
        self.t = t / 1000 # in [m]
        self.beam_length = beam_length # [m]
        self.density = density # [kg/m^3]

    def calculate_cross_sectional_area(self):
        return self.h**2 - (self.h - 2*self.t)**2 # [m^2]
    
    def calculate_volume(self):
        return self.calculate_cross_sectional_area() * self.beam_length # [m^3]
    
    def calculate_weight(self): 
        return self.calculate_volume() * self.density # [kg]

    def calculate_Ixx(self):
        Ixx_outer = (1/12) * (self.h)**4
        Ixx_inner = (1/12)* (self.h - 2*self.t)**4
        Ixx = Ixx_outer - Ixx_inner 
        return Ixx # returns [m^4]
    
    def calculate_Iyy(self):
        return self.calculate_Ixx() # returns [m^4]
    
    def calculate_stress_point(self, x, y):
        sigma = (self.Mx * y) / self.calculate_Ixx() - (self.My * x) / self.calculate_Iyy()
        return sigma # returns in [Pa]
    
    def calculate_maximum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.max(stresses)
    
    def calculate_minimum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.min(stresses)
    
    def calculate_stress_distribution(self, resolution=200):
        outer_length = self.h 
        inner_length = self.h - 2*self.t

        x_outer = np.linspace(-outer_length/2, outer_length/2, resolution) * 1000
        y_outer = np.linspace(-outer_length/2, outer_length/2, resolution) * 1000 

        x_coords = []
        y_coords = []
        stresses = []

        # outer top and bottom flanges
        for x in x_outer:
            for y in np.linspace(-outer_length/2, -inner_length/2, resolution) * 1000:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)
            for y in np.linspace(inner_length/2, outer_length/2, resolution) * 1000:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)

        # webs on the left and right side 
        for y in y_outer:
            for x in np.linspace(-outer_length/2, - inner_length/2, resolution) * 1000:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)
            for x in np.linspace(inner_length/2, outer_length/2, resolution) * 1000:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)
        
        return np.array(x_coords), np.array(y_coords), np.array(stresses)
    
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

        plt.title('Stress Distribution along the Square Beam')
        plt.axis('equal')
        plt.grid(False)
        plt.show()

        
if __name__ == '__main__':
    beam = SquareBeamStress()
    beam.plot_stress_distribution()
    print('-------- Square Beam Stress Analysis --------')
    print(f'Moment of Inertia (Ixx = Iyy) = {beam.calculate_Ixx()} [m^4]')
    print(f'Stress at Point 1 = {round(beam.calculate_stress_point(0.1, -0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 2 = {round(beam.calculate_stress_point(-0.1, -0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 3 = {round(beam.calculate_stress_point(-0.1, 0.1)/10**6, 4)} [MPa]')
    print(f'Stress at Point 4 = {round(beam.calculate_stress_point(0.1, 0.1)/10**6, 4)} [MPa]')
    print(f'Weight of the Beam: {round(beam.calculate_weight(), 4)} [kg]')
    print(f'Maximum Positive Stress: {round(beam.calculate_maximum_stress()/10**6, 4)} [MPa]')
    print(f'Maximum Negative Stress: {round(beam.calculate_minimum_stress()/10**6, 4)} [MPa]')