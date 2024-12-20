import numpy as np 
import matplotlib.pyplot as plt 

class SquareBeamStress: 

    def __init__(self, Mx, My, h, t):
        ''' Initialize the SquareBeamStress Class'''
        ### input Mx and My in [Nm], h in [mm], t in [mm]
        self.Mx = Mx # in [Nm]
        self.My = My # in [Nm]
        self.h = h / 1000 # in [m]
        self.t = t / 1000 # in [m]

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
    beam = SquareBeamStress(1000, 2000, 200, 10)
    beam.plot_stress_distribution()
    
