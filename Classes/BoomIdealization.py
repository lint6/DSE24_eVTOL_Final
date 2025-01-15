import numpy as np 
import matplotlib.pyplot as plt 

class BoomIdealization:

    def __init__(self, r=0.75, Vy=-30000.4, A=70.5, tau_y=283, t=3):
        ''' Initialize the BoomIdealization Class '''
        ### Input radius r in [m], Vy in [N], Ixx in [mm^4], stringer area A in [mm^2], yield shear stress tau_y in [MPa], t in [mm]
        self.r = r  # [m]
        self.Vy = Vy # [N] # included the load factor 
        self.A = A * (0.001)**2  # [m^2]
        self.tau_y = tau_y * 10**6  # [Pa]
        self.t = t * 0.001  # [m]
        self.num_booms = 24  # Number of booms

    def calculate_boom_coordinates(self):
        ''' Calculate the Boom Coordinates for the Idealization '''
        boom_y_coordinates = []
        boom_x_coordinates = []
        theta = np.pi / self.num_booms  # Initial angle step
        for i in range(self.num_booms):
            # Calculate coordinates for each boom
            boom_y_coordinates.append(-self.r * np.cos(theta))
            boom_x_coordinates.append(-self.r * np.sin(theta))
            theta += 2 * np.pi / self.num_booms  # Step through angles
        return boom_x_coordinates, boom_y_coordinates

    def calculate_boom_areas(self):
        ''' Calculate the Boom Areas for the Idealization '''
        boom_areas = []
        boom_y = self.calculate_boom_coordinates()[1]
        b = (2 * np.pi * self.r) / self.num_booms  # Boom spacing
        for i in range(self.num_booms):
            # Calculate the boom areas using symmetry
            prev_idx = (i - 1) % self.num_booms
            next_idx = (i + 1) % self.num_booms
            area = self.A + (self.t * b / 6) * (4 + (boom_y[prev_idx] / boom_y[i]) + (boom_y[next_idx] / boom_y[i]))
            boom_areas.append(area)
            print(area)
        return boom_areas 

    def calculate_Ixx(self):
        ''' Calculate the Ixx for the Idealization '''
        boom_areas = self.calculate_boom_areas()
        boom_y = self.calculate_boom_coordinates()[1]
        Ixx = 0.0 
        for i in range(self.num_booms):
            Ixx += boom_areas[i] * boom_y[i]**2
        return Ixx

    def calculate_shear_flow(self):
        ''' Calculate the Shear Flow Along the Fuselage '''
        boom_areas = self.calculate_boom_areas()
        boom_y = self.calculate_boom_coordinates()[1]
        Ixx = self.calculate_Ixx()
        shear_sides = []
        q_prev = 0
        for i in range(self.num_booms):
            if i == 0:
                shear_sides.append(q_prev)
            else:
                q = q_prev + (-self.Vy * boom_areas[i - 1] * boom_y[i - 1] / Ixx)
                shear_sides.append(q)
                q_prev = q 
        return shear_sides

    def calculate_minimum_thickness(self):
        ''' Calculate the Minimum Thickness for the Idealization '''
        shear_sides = self.calculate_shear_flow() 
        q_max = np.max(shear_sides)
        print(q_max)
        return q_max / self.tau_y

    # Remaining methods unchanged
    def plot_idealization_shape(self):
        ''' Plot the Boom Idealization Shape '''
        boom_x, boom_y = self.calculate_boom_coordinates()  # Get boom coordinates

        # Create the smooth circular fuselage shape
        theta = np.linspace(0, 2 * np.pi, 120)  # Generate 100 points for a smooth circle
        circle_x = -self.r * np.sin(theta)      # Circular fuselage x-coordinates
        circle_y = -self.r * np.cos(theta)      # Circular fuselage y-coordinates

        # Plot the fuselage circle and booms
        plt.figure(figsize=(6, 6))
        plt.plot(circle_x, circle_y, label='Fuselage', linestyle='-', color='black', linewidth=1)  # Smooth circle
        plt.scatter(boom_x, boom_y, color='blue', label='Booms', s=100)  # Booms as red points
        #plt.scatter(x=-1, y=-1, color='blue', label='(-1, -1)', s= 100)

        # Add labels and grid for clarity
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Boom Idealization Shape')
        plt.axis('equal')  # Ensure the aspect ratio makes the circle look round
        plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')

        plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()

        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_shear_flow(self, k=0.0009):
        ''' Plot the Shear Flow Magnitudes as Circular Arcs along the Circular Shape '''
        shear_sides = np.abs(self.calculate_shear_flow())  # Get the magnitudes of shear flow values
        boom_x, boom_y = self.calculate_boom_coordinates()  # Get boom coordinates

        # Calculate q_max (maximum shear flow)
        q_max = np.max(shear_sides)  # Max value of shear flow

        # Number of data points to interpolate the circular arcs
        num_points = 100

        # Plot the fuselage circle (original radius)
        theta = np.linspace(0, 2 * np.pi, num_points)
        circle_x = -self.r * np.sin(theta)  # Original fuselage x-coordinates
        circle_y = -self.r * np.cos(theta)  # Original fuselage y-coordinates

        plt.figure(figsize=(6, 6))
        plt.plot(circle_x, circle_y, label='Fuselage', linestyle='-', color='black', linewidth=1)  # Smooth circle

        # Loop through each segment between consecutive booms
        for i in range(24):
            # Calculate new radius based on shear flow for the segment
            shear_radius = self.r + k * shear_sides[i]

            # Calculate the angles for the segment (between boom i and boom (i+1))
            theta_start = (i * np.pi / 12) - np.pi / 24  # Start angle offset by 7.5 degrees
            theta_end = ((i + 1) * np.pi / 12) - np.pi / 24  # End angle offset by 7.5 degrees

            # Create the angular coordinates for the arc between boom i and boom (i+1)
            arc_theta = np.linspace(theta_start, theta_end, num_points)

            # Calculate the x and y coordinates for the arc at the new shear_radius
            arc_x = -shear_radius * np.sin(arc_theta)  # X-coordinates of the shear flow arc
            arc_y = -shear_radius * np.cos(arc_theta)  # Y-coordinates of the shear flow arc

            # Plot the arc for the current segment (between boom i and boom i+1)
            plt.plot(arc_x, arc_y, linestyle='-', color='red', linewidth=1)  # Red lines for shear flow

            # Calculate start and end points of the arc at the outer radius
            start_x = -self.r * np.sin(theta_start)  # X-coordinate at original fuselage radius
            start_y = -self.r * np.cos(theta_start)  # Y-coordinate at original fuselage radius
            end_x = -self.r * np.sin(theta_end)  # X-coordinate at original fuselage radius
            end_y = -self.r * np.cos(theta_end)  # Y-coordinate at original fuselage radius

            # Plot vertical lines connecting the edge of the arc to the fuselage
            plt.plot([start_x, arc_x[0]], [start_y, arc_y[0]], linestyle='-', color='red', linewidth=1)  # Line at start
            plt.plot([end_x, arc_x[-1]], [end_y, arc_y[-1]], linestyle='-', color='red', linewidth=1)  # Line at end

        # Plot the booms
        plt.scatter(boom_x, boom_y, color='blue', label='Booms', s=100)  # Blue points for the booms

        # Add labels and grid for clarity
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Shear Flow Along Fuselage')
        plt.axis('equal')
        plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')

        # Invert the axes to match the coordinate system
        plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()
        plt.legend()
        plt.grid(False)
        plt.show()


if __name__ == '__main__':
    boom = BoomIdealization(r=4.5) 
    boom.plot_idealization_shape()
    boom.plot_shear_flow()
    print(f'Minimum Thickness: {boom.calculate_minimum_thickness()*1000} [mm]')