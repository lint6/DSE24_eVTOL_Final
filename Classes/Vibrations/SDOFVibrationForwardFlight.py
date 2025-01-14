import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.fft import fft

class SDOFVibrationForwardFlight:

    def __init__(self, L=1.2, E=220, I=135000, T_min=900, T_max=1100, C_damp=0.03, m=1, RPM=1000, gust_velocity=19, gust_time=0, impulse_duration=0.1):
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
        self.gust_velocity = gust_velocity # [m/s]
        self.gust_time = gust_time # [s]
        self.impulse_duration = impulse_duration # [s]

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

    def gust_force(self, t):
        m_eq = self.calculate_equivalent_mass()
        impulse = m_eq * self.gust_velocity 
        F = impulse / self.impulse_duration  
        if self.gust_time <= t <= self.gust_time + self.impulse_duration:
            return F 
        else:
            return 0.0

    def calculate_force_at_point_t(self, t):
        '''Calculate the Thrust at a Point in Time t'''
        thrust = self.thrust_function()
        gust = self.gust_force(t)
        return thrust(t) + gust
    
    def equation_of_motion(self, t, y):
        ''' Define the System's Differential Equation '''
        m_eq = self.calculate_equivalent_mass()
        C = 2 * self.C_damp * m_eq * np.sqrt(3 * self.E * self.I / (m_eq * self.L**3))
        K = 3 * self.E * self.I / self.L**3 

        T_t = self.calculate_force_at_point_t(t)
        dxdt = [y[1], (T_t - C * y[1] - K * y[0]) / m_eq]
        return dxdt
    
    def solve_motion(self, t_span, y0):
        ''' Solve the Sysem's Differential Equation '''
        sol = solve_ivp(self.equation_of_motion, t_span, y0, t_eval=np.linspace(t_span[0], t_span[1], 5000))
        return sol 
    
    def plot_response(self, t_span=[0, 10], y0=[0.0, 0.0]):
        ''' Plot the System's Response '''
        # t_span = [0, t_final], y0 = [initial_displacement, initial_velocity]
        sol = self.solve_motion(t_span, y0)
        plt.figure(figsize=(10, 6))
        plt.plot(sol.t, sol.y[0], label='Displacement x(t)', color='blue')
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [m]')
        plt.title('SDOF Vibration Response Forward Flight')
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_force(self, t_span=[0, 0.5]):
        ''' Plot the Applied Force with Gust Represented as an Upward Arrow '''
        t_eval = np.linspace(t_span[0], t_span[1], 5000)  # Time points for evaluation
        forces = [self.thrust_function()(t) for t in t_eval]  # Compute only the thrust force

        # Plot the constant thrust force
        plt.figure(figsize=(10, 6))
        plt.plot(t_eval, forces, label='Thrust Force', color='red')

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

    def plot_frequency_response(self, t_span=[0, 10], y0=[0.0, 0.0]):
        ''' Plot the Frequency Domain Response (Amplitude Spectrum) '''
        # Solve the motion to get displacement over time
        sol = self.solve_motion(t_span, y0)
        
        # Perform Fourier Transform on displacement (y[0]) over time (sol.t)
        displacement = sol.y[0]
        dt = sol.t[1] - sol.t[0]  # Time step
        N = len(displacement)  # Number of data points
        freqs = np.fft.fftfreq(N, dt)  # Frequency bins

        # Perform FFT
        fft_result = fft(displacement)
        fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT

        # Plot frequency response (Amplitude Spectrum)
        plt.figure(figsize=(10, 6))
        plt.plot(freqs[:N // 2], fft_magnitude[:N // 2])  # Plot positive frequencies
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.title('Frequency Domain Response')
        plt.grid(True)
        plt.show()


    def analyze_resonance(self, t_span=[0, 10], y0=[0.0, 0.0]):
        ''' Analyze the System for Resonance and Plot It '''
        # Natural frequency
        m_eq = self.calculate_equivalent_mass()
        K = 3 * self.E * self.I / self.L**3  # Stiffness constant
        omega_n = np.sqrt(K / m_eq)  # Natural frequency in radians per second
        f_n = omega_n / (2 * np.pi)  # Natural frequency in Hz

        # Excitation frequency (based on RPM)
        f_excitation = self.RPM / 60  # RPM to Hz conversion

        # Solve the motion to get displacement over time
        sol = self.solve_motion(t_span, y0)

        # Perform Fourier Transform on displacement (y[0]) over time (sol.t)
        displacement = sol.y[0]
        dt = sol.t[1] - sol.t[0]  # Time step
        N = len(displacement)  # Number of data points
        freqs = np.fft.fftfreq(N, dt)  # Frequency bins

        # Perform FFT
        fft_result = fft(displacement)
        fft_magnitude = np.abs(fft_result)  # Magnitude of the FFT

        # Plot frequency response (Amplitude Spectrum)
        plt.figure(figsize=(10, 6))
        plt.plot(freqs[:N // 2], fft_magnitude[:N // 2], label="Frequency Response")
        
        # Highlight the natural frequency as a red vertical line
        plt.axvline(f_n, color='red', linestyle='--', linewidth=2, label=f"Natural Frequency: {f_n:.2f} Hz")
        
        # Highlight the excitation frequency as a dashed green line
        plt.axvline(f_excitation, color='green', linestyle='--', linewidth=2, label=f"Excitation Frequency: {f_excitation:.2f} Hz")
        
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Amplitude')
        plt.title('Frequency Domain Response with Resonance Analysis')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Display results
        print(f"Natural Frequency: {f_n:.2f} Hz")
        print(f"Excitation Frequency: {f_excitation:.2f} Hz")

        # Check for resonance
        if np.isclose(f_n, f_excitation, atol=0.1):  # Consider resonance if the difference is small
            print("Resonance detected!")
        else:
            print("No resonance detected.")


if __name__ == '__main__':
    sys = SDOFVibrationForwardFlight()
    sys.plot_response()
    sys.plot_force()
    sys.plot_frequency_response()
    sys.analyze_resonance()

