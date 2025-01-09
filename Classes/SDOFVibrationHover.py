import numpy as np
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
### EIH CORRECT Ixx
class SDOFVibrationHover:

    def __init__(self, L=0.8, E=70, I=106168.32, T=7900/np.cos(np.deg2rad(5)), C_damp=0.01, m=1, RPM=1000, gust_velocity=19, gust_time=0.0, impulse_duration=0.1):
        ''' Initialize the SDOFVibrationHover Class '''
        ### Input length in [m], E in [GPa], I in [mm^4], T in [N], C_damp in [-], RPM in [rev/min]
        self.L = L # [m]
        self.E = E * 10**9 # [Pa]
        self.I = I * (0.001)**4 # [m^4]
        self.T = T # [N]
        self.C_damp = C_damp # [-] dimensionless
        self.m = m # [kg]
        self.RPM = RPM # [rev/min]
        self.gust_velocity = gust_velocity # [m/s]
        self.gust_time = gust_time # [s]
        self.impulse_duration = impulse_duration # [s]


    def calculate_equivalent_mass(self):
        return 1 / 3 * self.m ### check if this makes sense, find sources 
    
    def thrust_function(self):
        ''' Define the Thrust Function Based on the T'''
        return lambda t: self.T # constant thrust 
    

    def gust_force(self, t):
        m_eq = self.calculate_equivalent_mass()
        impulse = m_eq * self.gust_velocity 
        F = impulse / self.impulse_duration 
        if self.gust_time <= t <= self.gust_time + self.impulse_duration:
            return F 
        else:
            return 0.0
    
    def calculate_force_at_point_t(self, t):
        ''' Calculate the Thrust at a Point in Time t '''
        thrust = self.thrust_function()
        gust = self.gust_force(t)
        return thrust(t) + gust
    
    def equation_of_motion(self, t, y):
        m_eq = self.calculate_equivalent_mass()
        C = 2 * self.C_damp * m_eq * np.sqrt(3 * self.E * self.I / (m_eq * self.L**3))
        K = 3 * self.E * self.I / self.L**3 

        T_t = self.calculate_force_at_point_t(t) 
        dxdt = [y[1], (T_t - C * y[1] - K * y[0]) / m_eq]
        return dxdt 
    
    def solve_motion(self, t_span, y0):
        ''' Solve the System's Differential Equation '''
        sol = solve_ivp(self.equation_of_motion, t_span, y0, t_eval=np.linspace(t_span[0], t_span[1], 5000))
        return sol 
    
    def plot_response(self, t_span=[0, 10], y0=[0.0, 0.0]):
        ''' Plot the System's Response '''
        sol = self.solve_motion(t_span, y0)
        plt.figure(figsize=(10, 6))
        plt.plot(sol.t, sol.y[0], label='Displacement x(t)', color='blue')
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [m]')
        plt.title('SDOF Vibration Response for Hover')
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_force(self, t_span=[0, 10]):
        ''' Plot the Applied Force with Gust Represented as an Upward Arrow '''
        t_eval = np.linspace(t_span[0], t_span[1], 5000)  # Time points for evaluation
        forces = [self.thrust_function()(t) for t in t_eval]  # Compute only the thrust force

        # Plot the constant thrust force
        plt.figure(figsize=(10, 6))
        plt.plot(t_eval, forces, label='Thrust Force F(t)', color='red')

        # Add the gust impulse as an upward arrow
        gust_x = self.gust_time
        thrust_at_t0 = self.thrust_function()(0)
        arrow_height = thrust_at_t0 / 2  # Arrow height as per the requirement
        plt.annotate('', xy=(gust_x, arrow_height), xytext=(gust_x, 0),
                    arrowprops=dict(facecolor='blue', edgecolor='blue', width=1.5, headwidth=8), label='Gust Impulse')
        plt.plot(gust_x, 0, 'o', color='blue', label='Gust Impulse')
        plt.axhline(0, color='black', linewidth=1)       
        plt.xlabel('Time [s]')
        plt.ylabel('Force [N]')
        plt.title('Applied Force with Gust Impulse')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == '__main__':
    sys = SDOFVibrationHover()
    sys.plot_response()
    sys.plot_force()