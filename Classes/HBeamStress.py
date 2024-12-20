import numpy as np
import matplotlib.pyplot as plt

class HBeamStress:
    def __init__(self, Mx, My, Ixx, Iyy, top_box, web, bottom_box):
        """
        Initialize the HBeamStress class with bending moments, moments of inertia, and H-beam dimensions.

        Args:
            Mx (float): Bending moment about the x-axis (Nm).
            My (float): Bending moment about the y-axis (Nm).
            Ixx (float): Second moment of area about the x-axis (mm^4).
            Iyy (float): Second moment of area about the y-axis (mm^4).
            top_box (tuple): Dimensions of the top box (width, thickness) in mm.
            web (tuple): Dimensions of the web (height, thickness) in mm.
            bottom_box (tuple): Dimensions of the bottom box (width, thickness) in mm.
        """
        self.Mx = Mx
        self.My = My
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.top_box = top_box
        self.web = web
        self.bottom_box = bottom_box

    def sigma_z(self, x, y):
        """
        Calculate the bending stress (sigma_z) at a point (x, y) on the cross-section.

        Args:
            x (float): x-coordinate of the point (mm).
            y (float): y-coordinate of the point (mm).

        Returns:
            float: Bending stress (Pa).
        """
        sigma = (self.Mx * y) / self.Ixx - (self.My * x) / self.Iyy
        return sigma

    def generate_H_beam_coords(self):
        """
        Generate the coordinates of the edge points of an H-beam.
        Only include coordinates along the web for accurate stress plotting.
        """
        top_width, top_thickness = self.top_box
        web_height, web_thickness = self.web
        bottom_width, bottom_thickness = self.bottom_box

        coords = []

        # Top box (upper edge)
        coords.extend([(x, web_height / 2 + top_thickness) for x in np.linspace(-top_width / 2, top_width / 2, 500)])
        
        # Right edge of the web (only vertical line along the web)
        coords.extend([(top_width / 2, y) for y in np.linspace(web_height / 2, -web_height / 2, 500)])
        
        # Bottom box (lower edge)
        coords.extend([(x, -web_height / 2 - bottom_thickness) for x in np.linspace(top_width / 2, -top_width / 2, 500)])
        
        # Left edge of the web (only vertical line along the web)
        coords.extend([(-top_width / 2, y) for y in np.linspace(-web_height / 2, web_height / 2, 500)])
        return coords


    def generate_H_beam_shape(self):
        """
        Generate the vertices for plotting the H-beam shape.

        Returns:
            list: Lists of x and y coordinates for the H-beam outline.
        """
        top_width, top_thickness = self.top_box
        web_height, web_thickness = self.web
        bottom_width, bottom_thickness = self.bottom_box

        x_coords = [
            -top_width / 2, top_width / 2, top_width / 2, web_thickness / 2,
            web_thickness / 2, bottom_width / 2, bottom_width / 2, -bottom_width / 2,
            -bottom_width / 2, -web_thickness / 2, -web_thickness / 2, -top_width / 2
        ]
        y_coords = [
            web_height / 2 + top_thickness, web_height / 2 + top_thickness, web_height / 2,
            web_height / 2, -web_height / 2, -web_height / 2, -web_height / 2 - bottom_thickness,
            -web_height / 2 - bottom_thickness, -web_height / 2, -web_height / 2,
            web_height / 2, web_height / 2
        ]

        return x_coords, y_coords

    def plot_stress_distribution_with_shape(self):
        """
        Plot the bending stress distribution along the edge of an H-beam with its shape.
        """
        coords = self.generate_H_beam_coords()
        stresses = [self.sigma_z(x, y)/(10**6) for x, y in coords]

        # I-beam shape
        x_shape, y_shape = self.generate_H_beam_shape()

        # Neutral Axis 
        NA = (self.My * self.Ixx) / (self.Mx * self.Iyy) 
        NA_angle = (np.arctan(NA) * 180) / np.pi # neutral axis degrees
        x_NA = np.linspace(-self.top_box[0], self.top_box[0], 500)
        y_NA = NA * x_NA

        # Plotting
        x_coords = [x for x, y in coords]
        y_coords = [y for x, y in coords]

        plt.figure(figsize=(10, 6))
        plt.scatter(x_coords, y_coords, c=stresses, cmap='viridis', marker='o', label="Stress Points")
        plt.plot(x_shape, y_shape, color='black', linestyle='-', linewidth=1.5, label="I-Beam Shape")
        
        # Neutral Axis Line
        plt.plot(x_NA, y_NA, color='red', linestyle='--', linewidth=0.5, label='Neutral Axis')

        # Axis Lines
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

        # Corrected small vertical outline in the upper left corner of the I-beam
        plt.plot([-self.top_box[0] / 2, -self.top_box[0] / 2], 
                 [self.web[0] / 2 + self.top_box[1], self.web[0] / 2],  # Corrected y-coordinate to close the shape
                 color='black', linewidth=1.5, label="Small Vertical Outline")

        plt.colorbar(label='Bending Stress (MPa)')
        plt.title('Bending Stress Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.grid(False)
        plt.axis('equal')
        plt.show()

# Example usage
if __name__ == '__main__':
    # Bending moments
    Mx = 1000  # Nm
    My = 2000  # Nm

    # Moments of inertia
    Ixx = 3.5573 * 10**-5 # m^4
    Iyy = 8.2 * 10**-6 # m^4

    # I-beam dimensions
    top_box = (0.170, 0.010)  # width x thickness in m
    web = (0.180, 0.010)      # height x thickness in m
    bottom_box = (0.170, 0.010)  # width x thickness in m

    # Create an instance of HBeamStress
    hbeam = HBeamStress(Mx, My, Ixx, Iyy, top_box, web, bottom_box)

    # Plot stress distribution with I-beam shape
    hbeam.plot_stress_distribution_with_shape()

    # Example of calculating bending stress at a point (0.085, 0.100)
    print(hbeam.sigma_z(0.085, 0.100)/(10**6))  # Stress in MPa
