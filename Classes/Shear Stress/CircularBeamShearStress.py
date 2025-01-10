import numpy as np  
import matplotlib.pyplot as plt 

class CircularBeamShearStress:

    def __init__(self, T):
        ''' Initialize the CircularBeamShearStress Class '''
        ### Input T in [N]
        ### Note that this is the Shear Stress caused by a Torque T
        self.T = T # [N]


class HollowTubeShearFlow:

    def __init__(self, r=1.5, t=0.05, Vy=-1300000, Vx=0, tau_y=190):
        ''' Initialize the HollowTubeShearFlow Class '''
        ### Inputs: radius r in [m], thickness t in [m], Vy and Vx in [N], yield shear stress tau_y in [MPa]
        self.r = r # Outer radius [m]
        self.t = t # Thickness of the tube [m]
        self.Vy = Vy # Shear force in y-direction [N]
        self.Vx = Vx # Shear force in x-direction [N]
        self.tau_y = tau_y * 1e6 # Yield shear stress [Pa]
        
        # Geometry-related parameters
        self.r_inner = self.r - self.t  # Inner radius [m]

    def calculate_Ixx(self):
        ''' Calculate the second moment of area about the x-axis (Ixx) '''
        return np.pi * (self.r**4 - self.r_inner**4) / 4

    def calculate_Iyy(self):
        ''' Calculate the second moment of area about the y-axis (Iyy) '''
        return np.pi * (self.r**4 - self.r_inner**4) / 4

    def shear_flow(self, s, Vx=None, Vy=None):
        ''' Calculate the shear flow at a point along the tube circumference '''
        if Vx is None: Vx = self.Vx
        if Vy is None: Vy = self.Vy
        
        # Angle along the tube (theta in radians)
        theta = s / self.r  # Convert arc length to angle (s = r * theta)

        # Coordinates at angle theta (x, y)
        x = self.r * np.cos(theta)
        y = self.r * np.sin(theta)

        # Shear flow due to vertical and horizontal shear forces
        q_b = - (Vy / self.calculate_Ixx()) * self.t * y
        q_s = - (Vx / self.calculate_Iyy()) * self.t * x

        # Total shear flow (combining both effects)
        return q_b + q_s

    def plot_shear_flow(self):
        ''' Plot the shear flow along the circumference of the tube '''
        # Total angle around the tube
        total_angle = 2 * np.pi

        # Arc length distribution (s = r * theta)
        num_points = 100
        arc_lengths = np.linspace(0, total_angle * self.r, num_points)

        # Calculate shear flow for each point along the tube circumference
        shear_flows = [self.shear_flow(s) for s in arc_lengths]

        # Get the coordinates for plotting (circle)
        theta = np.linspace(0, total_angle, num_points)
        circle_x = self.r * np.cos(theta)
        circle_y = self.r * np.sin(theta)

        # Plot the shear flow distribution
        plt.figure(figsize=(6, 6))

        # Plot the tube (circle)
        plt.plot(circle_x, circle_y, label='Outer Tube Boundary', color='black')

        # Plot the shear flow as color-coded along the tube
        plt.scatter(circle_x, circle_y, c=shear_flows, cmap='viridis', label='Shear Flow', s=20)

        # Add labels and title
        plt.xlabel('X-axis [m]')
        plt.ylabel('Y-axis [m]')
        plt.title('Shear Flow Distribution along Hollow Circular Tube')
        plt.axis('equal')  # Keep aspect ratio equal for a perfect circle
        plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')

        # Add colorbar for shear flow values
        cbar = plt.colorbar()
        cbar.set_label('Shear Flow [N/m]')

        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    # Initialize the HollowTubeShearFlow with given parameters
    tube = HollowTubeShearFlow(r=4.5, t=0.1, Vy=-1300000, Vx=0, tau_y=190)
    
    # Plot the shear flow distribution
    tube.plot_shear_flow()
