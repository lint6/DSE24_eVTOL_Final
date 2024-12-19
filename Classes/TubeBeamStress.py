import numpy as np 
import matplotlib.pyplot as plt 

class TubeBeamStress: 
    def __init__(self, radius, thickness, Mx, My):
        self.radius = radius 
        self.thickness = thickness 
        self.Mx = Mx 
        self.My = My 
        self.Ixx = (np.pi / 4) * (self.radius**4 - (self.radius - self.thickness)**4)
        self.Iyy = self.Ixx
    
    def calculate_stress(self, x, y):
        sigma = (self.Mx * y) / self.Ixx - (self.My * x) / self.Iyy 
        return sigma 
    
    def generate_coordinates(self):
        coords = []

        theta = np.linspace(0, 2*np.pi, 500)
        x_outer = self.radius * np.cos(theta)
        y_outer = self.radius * np.sin(theta)

        inner_radius = self.radius - self.thickness 
        x_inner = inner_radius * np.cos(theta)
        y_inner = inner_radius * np.sin(theta)

        return x_outer, y_outer, x_inner, y_inner
    
    def plot_stress_distribution(self):
        x_outer, y_outer, x_inner, y_inner = self.generate_coordinates()

        stresses = [self.calculate_stress(x, y) / (10**6) for x, y in zip(x_outer, y_outer)]

        x_NA = np.linspace(-self.radius, self.radius, 500)
        y_NA = np.zeros_like(x_NA)

        plt.figure(figsize=(10, 6))
        plt.scatter(x_outer, y_outer, c=stresses, cmap='viridis', marker='o', label='Stress Points')

        plt.plot(x_outer, y_outer, color='black', linestyle='-', linewidth=1.5, label='Outer Circle Beam Shape')
        plt.plot(x_inner, y_inner, color='black', linestyle='-', linewidth=1.5, label='Inner Circle Beam Shape')

        plt.plot(x_NA, y_NA, color='red', linestyle='-', linewidth=0.5, label='Neutral Axis')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

        plt.colorbar(label='Stress (MPa)')
        plt.title('Bending Stress Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.grid(False)
        plt.axis('equal')
        plt.show()


if __name__ == '__main__':
    radius = 0.1 
    thickness = 0.01 
    Mx = 5000
    My = 2000
    beam = TubeBeamStress(radius, thickness, Mx, My)
    beam.plot_stress_distribution()
    

        
