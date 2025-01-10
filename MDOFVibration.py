import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class MDOFVibrationForwardFlight:

    def __init__(self, M=1.0, I=0.5, Cs=0.1, Calpha=0.05, Ks=10.0, Kalpha=5.0,
                 F_amplitude=1.0, e_1=0.2, omega=2.0):
        """Initialize the MDOF Vibration System"""
        self.M = M  # Mass
        self.I = I  # Rotational inertia
        self.Cs = Cs  # Damping coefficient (translation)
        self.Calpha = Calpha  # Damping coefficient (rotation)
        self.Ks = Ks  # Stiffness (translation)
        self.Kalpha = Kalpha  # Stiffness (rotation)
        self.F_amplitude = F_amplitude  # Force amplitude
        self.e_1 = e_1  # Offset for moment
        self.omega = omega  # Frequency of force

    def external_force(self, t):
        """Define the external force as a function of time"""
        return self.F_amplitude * np.sin(self.omega * t)

    def equation_of_motion(self, t, z):
        """Define the coupled system of first-order equations"""
        y, alpha, y_dot, alpha_dot = z  # State variables

        # Mass and stiffness matrices
        M_mat = np.array([[self.M, 0], [0, self.I]])
        C_mat = np.array([[self.Cs, 0], [0, self.Calpha]])
        K_mat = np.array([[self.Ks, 0], [0, self.Kalpha]])

        # Force vector
        F = np.array([-self.external_force(t), self.e_1 * self.external_force(t)])

        # State derivative calculation
        vel = np.array([y_dot, alpha_dot])
        accel = np.linalg.inv(M_mat) @ (F - C_mat @ vel - K_mat @ np.array([y, alpha]))

        return [y_dot, alpha_dot, accel[0], accel[1]]

    def solve_motion(self, t_span, z0):
        """Solve the system's differential equation"""
        sol = solve_ivp(self.equation_of_motion, t_span, z0, t_eval=np.linspace(t_span[0], t_span[1], 5000))
        return sol

    def plot_response(self, t_span=[0, 20], z0=[0.0, 0.0, 0.0, 0.0]):
        """Plot the system's response"""
        sol = self.solve_motion(t_span, z0)
        
        plt.figure(figsize=(12, 6))
        plt.plot(sol.t, sol.y[0], label='Displacement y(t)', color='blue')
        plt.plot(sol.t, sol.y[1], label='Rotation alpha(t)', color='red')
        plt.xlabel('Time [s]')
        plt.ylabel('Response')
        plt.title('MDOF Vibration Response')
        plt.grid(True)
        plt.legend()
        plt.show()

if __name__ == '__main__':
    system = MDOFVibrationForwardFlight()
    system.plot_response()
