import numpy as np 
import matplotlib.pyplot as plt 

class SDOFVibration:

    def __init__(self, L=0.8, E=70, I=1000, T_min=400, T_max=540, C_damp=0.03, m=1, RPM=10000):
        '''Initialize the SDOFVibration Class'''
        ### Input length in [m], E in [GPA], I in [mm^4], T_min and T_max in [N], C_damp in [-]
        self.L = L # [m]
        self.E = E * 10**9 # [Pa]
        self.I = I * (0.001)**4 # [m^4]
        self.T_min = T_min # [N]
        self.T_max = T_max # [N]
        self.C_damp = C_damp # [-] dimensionless
        self.m = m # [kg]
        self.RPM = RPM # [rev/min]

    def calculate_equivalent_mass(self):
        '''Calculate the Equivalent Mass of the SDOF System Massless-Rod Simplification'''
        return self.m * 1/3 ### check if this makes sense, find sources 
    
    def thrust_function(self):
        ''' Define the Thrust Function Based on the Tmin and Tmax'''
        # assume T_max at t = 0
        amplitude = (self.T_max - self.T_min) / 2 
        offset = (self.T_max + self.T_min) / 2
        period = 60 / self.RPM
        return lambda t: amplitude * np.sin(2*np.pi*t/period + np.pi/2) + offset

    def calculate_thrust_at_point_t(self, t):
        '''Calculate the Thrust at a Point in Time t'''
        thrust = self.thrust_function()
        return thrust(t)
    
    def calculate_stiffness(self):
        k = (3 * self.E * self.I) / self.L**3
        return k

    def calculate_response_at_t(self, t):
        ''' Calculate the Response at a Point in Time t '''
        k = self.calculate_stiffness()
        meq = self.calculate_equivalent_mass()
        omega_n = np.sqrt(k / meq)
        omega_d = omega_n * np.sqrt(1 - self.C_damp**2)

        f0 = self.calculate_thrust_at_point_t(t) / meq 
        omega_f = 2 * np.pi * self.RPM / 60 # forced frequency
        xp_amplitude = abs(f0 / np.sqrt((omega_n**2 - omega_f**2)**2 + (2 * self.C_damp * omega_n * omega_f)**2))
        theta = np.arctan((2 * self.C_damp * omega_n * omega_f) / (omega_n**2 - omega_f**2))

        A0 = 0 # assumed to be 0 (no displacement/velocity at t=0)
        phi = 0 # assumed to be 0 (no displacement/velocity at t=0)

        x_h = A0 * np.exp(-self.C_damp * omega_n * t) * np.sin(omega_d * t + phi)
        x_p = xp_amplitude * np.cos(omega_f * t - theta)

        x_t = x_h + x_p 
        return x_t
    
    def plot_response(self, t_span=[0, 10], y0=[0.0, 0.0]):
        ''' Plot the System's Response '''
        # t_span = [0, t_final], y0 = [initial_displacement, initial_velocity]
        t = np.linspace(t_span[0], t_span[1], 1000)
        response = np.array([self.calculate_response_at_t(ti) for ti in t])
        plt.plot(t, response, label='Response x(t)', color='blue')
        plt.title('SDOF Vibration Response (by Hand)')
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [m]')
        plt.grid(True)
        plt.show() 
    

if __name__ == '__main__':
    sys = SDOFVibration()
    sys.plot_response()


    

