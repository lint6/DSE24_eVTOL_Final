import math
import numpy as np 
import matplotlib.pyplot as plt

class NVM:

    def __init__(self, length=3, rho=2710, area=0.1, E=70, I=4 * 10**-5, thrust_load=1000):
        ''' Thrust acts upwards at the end of the beam , distributed load acts downwards along the entire length of the beam
        Note that the beam itself is fixed at one end, and free on the other end '''
        self.length = length # m
        self.rho = rho # kg / m^3
        self.area = area # m^2
        self.E = E * 10**9 # GPa
        self.I = I # m^4
        self.thrust_load = thrust_load # N
        self.g = 9.80665 # m/s^2
    


        # calculations based on inputs
        self.distributed_load = (self.rho * self.area * self.length * self.g) / self.length # N / m
        self.reaction_force = (self.distributed_load * self.length) - self.thrust_load # N
        self.reaction_moment = (0.5 * self.distributed_load * self.length**2) - (self.thrust_load * self.length) # Nm

    def shear_force(self, x: float):
        ''' Shear Force Calculation at a Distance 'x' from the fixed end '''
        V = (-self.distributed_load * x) + self.reaction_force # N
        return V 
    
    def bending_moment(self, x: float):
        ''' Bending Moment Calculation at a Distance 'x'  from the fixed end'''
        M = self.reaction_moment - (self.reaction_force*x) + (0.5*self.distributed_load*x**2)
        return M
    
    def deflection(self, x: float):
        ''' Deflection Calculation at a Distance 'x' from the fixed end '''
        v = (-1/(self.E * self.I)) * (-(self.distributed_load * x**4)/24 - (self.reaction_force * x**3)/6 + (self.reaction_moment * x**2)/2)
        return v
    
    def deflection_angle(self, x: float):
        ''' Deflection Angle Calculation at a Distance 'x' from the fixed end '''
        theta = (-1/(self.E * self.I)) * (-(self.distributed_load * x**3)/6 - (self.reaction_force * x**2)/2 + (self.reaction_moment * x))
        return theta

    
    def plot_NVM(self):
        ''' Plotting the Shear Force and Bending Moment Diagrams '''
        x = np.linspace(0, self.length, 1000)
        shear_forces = [self.shear_force(i) for i in x]
        bending_moments = [-self.bending_moment(i) for i in x]

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(x, shear_forces, color='blue')
        plt.plot([0, 0], [0, self.shear_force(0)], color='blue')
        plt.plot([self.length, self.length], [0, self.shear_force(self.length)], color='blue')
        plt.axhline(y=0, color='black')
        plt.fill_between(x, shear_forces, color='blue', alpha=0.15)
        plt.title('Shear Force Diagram')
        plt.xlabel('Distance from Fixed End [m]')
        plt.ylabel('Shear Force [N]')
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.plot(x, bending_moments, color='red')
        plt.plot([0, 0], [0, -self.bending_moment(0)], color='red')
        plt.plot([self.length, self.length], [0, self.bending_moment(self.length)], color='red')
        plt.axhline(y=0, color='black')
        plt.fill_between(x, bending_moments, color='red', alpha=0.15)
        plt.title('Bending Moment Diagram')
        plt.xlabel('Distance from Fixed End [m]')
        plt.ylabel('Bending Moment [Nm]')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def plot_deflection(self):
        ''' Plotting the Shear Force and Bending Moment Diagrams '''
        x = np.linspace(0, self.length, 1000)
        deflections = [self.deflection(i) for i in x]
        deflection_angles = [self.deflection_angle(i) for i in x]

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(x, deflections, color='blue')
        plt.axhline(y=0, color='black')
        plt.title('Deflection Along the Beam')
        plt.xlabel('Distance from Fixed End [m]')
        plt.ylabel('Deflection Along the Beam [m]')
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.plot(x, deflection_angles, color='red')
        plt.axhline(y=0, color='black')
        plt.title('Deflection Angle Along the Beam')
        plt.xlabel('Distance from Fixed End [m]')
        plt.ylabel('Deflection Angle [rad]')
        plt.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    beam = NVM()
    beam.plot_deflection()








