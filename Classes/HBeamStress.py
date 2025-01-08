import numpy as np
import matplotlib.pyplot as plt

class HBeamStress:

    def __init__(self, Mx=1000, My=2000, h_t=10, w_t=170, h_w=180, w_w=10, h_b=10, w_b=170, beam_length=3, density=2710):
        ''' Initialize the HBeamStress Class'''
        self.Mx = Mx
        self.My = My
        self.h_t = h_t / 1000
        self.w_t = w_t / 1000
        self.h_w = h_w / 1000
        self.w_w = w_w / 1000
        self.h_b = h_b / 1000
        self.w_b = w_b / 1000

        self.y_t = -self.h_w/2 - self.h_t/2
        self.x_t = 0
        self.y_w = 0
        self.x_w = 0
        self.y_b = self.h_w/2 + self.h_b/2

        self.beam_length = beam_length # [m]
        self.density = density # [kg/m^3]

    def calculate_cross_sectional_area(self):
        A_t = self.w_t * self.h_t 
        A_w = self.w_w * self.h_w 
        A_b = self.w_b * self.h_b 
        return A_t + A_w + A_b
    
    def calculate_volume(self):
        return self.calculate_cross_sectional_area() * self.beam_length # [m^3]
    
    def calculate_weight(self): 
        return self.calculate_volume() * self.density # [kg]

    def calculate_Ixx(self):
        Ixx_t = (1/12)*self.w_t*(self.h_t**3) + (self.w_t * self.h_t * (self.y_t**2))
        Ixx_w = (1/12)*self.w_w*(self.h_w**3) + (self.w_w * self.h_w * (self.y_w**2))
        Ixx_b = (1/12)*self.w_b*(self.h_b**3) + (self.w_b * self.h_b * (self.y_b**2))
        Ixx = Ixx_t + Ixx_w + Ixx_b
        return Ixx
    
    def calculate_Iyy(self):
        Iyy_t = (1/12)*self.h_t*(self.w_t**3) + (self.h_t * self.w_t * (self.x_t**2))
        Iyy_w = (1/12)*self.h_w*(self.w_w**3) + (self.h_w * self.w_w * (self.x_w**2))
        Iyy_b = (1/12)*self.h_b*(self.w_b**3) + (self.h_b * self.w_b * (self.x_w**2))
        Iyy = Iyy_t + Iyy_w + Iyy_b
        return Iyy 
    
    def calculate_stress_point(self, x, y):
        sigma = (self.Mx * y) / self.calculate_Ixx() - (self.My * x) / self.calculate_Iyy()
        return sigma 
    
    def calculate_maximum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.max(stresses)
    
    def calculate_minimum_stress(self):
        _, _, stresses = self.calculate_stress_distribution()
        return np.min(stresses)

    def calculate_stress_distribution(self, resolution=200):
        y_top = np.linspace(-self.h_w/2 - self.h_t, -self.h_w/2, resolution) * 1000
        y_web = np.linspace(-self.h_w/2, self.h_w/2, resolution) * 1000
        y_bottom = np.linspace(self.h_w/2, self.h_w/2 + self.h_b, resolution) * 1000

        x_top = np.linspace(-self.w_t/2, self.w_t/2,resolution) * 1000
        x_web = np.linspace(-self.w_w/2, self.w_w/2, resolution) * 1000
        x_bottom = np.linspace(-self.w_b/2, self.w_b/2, resolution) * 1000

        x_coords = []
        y_coords = []
        stresses = []

        for x in x_top:
            for y in y_top:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)
        
        for x in x_web:
            for y in y_web:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)

        for x in x_bottom:
            for y in y_bottom:
                stress = self.calculate_stress_point(x/1000, y/1000)
                x_coords.append(x)
                y_coords.append(y)
                stresses.append(stress)

        return np.array(x_coords), np.array(y_coords), np.array(stresses)
    
    def plot_stress_distribution(self):
        ''' Plot the Stress Distribution along the H-Beam '''
        x_coords, y_coords, stresses = self.calculate_stress_distribution()

        plt.figure(figsize=(10, 5))
        
        scatter = plt.scatter(x_coords, y_coords, c=stresses/(10**6), cmap='seismic', s=1)
        plt.colorbar(scatter, label='Stress [MPa]')

        plt.xlabel('x-axis [mm]')
        plt.ylabel('y-axis [mm]')
        
        ax = plt.gca()
        
        # Invert the axes to flip the signs
        ax.invert_xaxis()  # Flip the x-axis
        ax.invert_yaxis()  # Flip the y-axis
        
        plt.title('Stress Distribution along the H-Beam')
        plt.axis('equal')
        plt.grid(False)
        plt.show()


if __name__ == '__main__':
    beam = HBeamStress()
    beam.plot_stress_distribution()
    print('-------- H Beam Stress Analysis --------')
    print(f"Moment of Inertia (Ixx): {beam.calculate_Ixx()} [m^4]")
    print(f"Moment of Inertia (Iyy): {beam.calculate_Iyy()} [m^4]")
    print(f'Stress at Point 1: {round(beam.calculate_stress_point(0.085, -0.100)/10**6, 4)} [MPa]')
    print(f'Stress at Point 2: {round(beam.calculate_stress_point(-0.085, -0.100)/10**6, 4)} [MPa]')
    print(f'Stress at Point 3: {round(beam.calculate_stress_point(-0.085, 0.100)/10**6, 4)} [MPa]')
    print(f'Stress at Point 4: {round(beam.calculate_stress_point(0.085, 0.100)/10**6, 4)} [MPa]')
    print(f'Weight of the Beam: {round(beam.calculate_weight(), 4)} [kg]')
    print(f'Maximum Positive Stress: {round(beam.calculate_maximum_stress()/10**6, 4)} [MPa]')
    print(f'Maximum Negative Stress: {round(beam.calculate_minimum_stress()/10**6, 4)} [MPa]')
