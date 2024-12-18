import numpy as np
import matplotlib.pyplot as plt

# Function to calculate bending stress (sigma_z)
def sigma_z(Mx, My, x, y, Ixx, Iyy):
    """
    Calculate the bending stress (sigma_z) at a point (x, y) on the cross-section.

    Args:
        Mx (float): Bending moment about the x-axis (Nm).
        My (float): Bending moment about the y-axis (Nm).
        x (float): x-coordinate of the point (mm).
        y (float): y-coordinate of the point (mm).
        Ixx (float): Second moment of area about the x-axis (mm^4).
        Iyy (float): Second moment of area about the y-axis (mm^4).

    Returns:
        float: Bending stress (Pa).
    """
    sigma = (Mx * y) / Ixx - (My * x) / Iyy
    return sigma


# Function to generate the edge coordinates of an I-beam
def generate_I_beam_coords(top_box, web, bottom_box):
    """
    Generate the coordinates of the edge points of an I-beam.

    Args:
        top_box (tuple): Dimensions of the top box (width, thickness) in mm.
        web (tuple): Dimensions of the web (height, thickness) in mm.
        bottom_box (tuple): Dimensions of the bottom box (width, thickness) in mm.

    Returns:
        list: List of (x, y) coordinates along the edge of the I-beam.
    """
    top_width, top_thickness = top_box
    web_height, web_thickness = web
    bottom_width, bottom_thickness = bottom_box

    coords = []

    # Top box (upper edge)
    coords.extend([(x, web_height / 2 + top_thickness) for x in np.linspace(-top_width / 2, top_width / 2, 500)])
    # Right edge of the web
    coords.extend([(top_width / 2, y) for y in np.linspace(web_height / 2, -web_height / 2, 500)])
    # Bottom box (lower edge)
    coords.extend([(x, -web_height / 2 - bottom_thickness) for x in np.linspace(top_width / 2, -top_width / 2, 500)])
    # Left edge of the web
    coords.extend([(-top_width / 2, y) for y in np.linspace(-web_height / 2, web_height / 2, 500)])

    return coords


# Function to generate the shape of the I-beam for visualization
def generate_I_beam_shape(top_box, web, bottom_box):
    """
    Generate the vertices for plotting the I-beam shape.

    Args:
        top_box (tuple): Dimensions of the top box (width, thickness) in mm.
        web (tuple): Dimensions of the web (height, thickness) in mm.
        bottom_box (tuple): Dimensions of the bottom box (width, thickness) in mm.

    Returns:
        list: Lists of x and y coordinates for the I-beam outline.
    """
    top_width, top_thickness = top_box
    web_height, web_thickness = web
    bottom_width, bottom_thickness = bottom_box

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


# Plot bending stress along the edge of an I-beam with its shape
def plot_stress_distribution_with_shape(Mx, My, Ixx, Iyy, top_box, web, bottom_box):
    """
    Plot the bending stress distribution along the edge of an I-beam with its shape.

    Args:
        Mx (float): Bending moment about the x-axis (Nm).
        My (float): Bending moment about the y-axis (Nm).
        Ixx (float): Second moment of area about the x-axis (mm^4).
        Iyy (float): Second moment of area about the y-axis (mm^4).
        top_box (tuple): Dimensions of the top box (width, thickness) in mm.
        web (tuple): Dimensions of the web (height, thickness) in mm.
        bottom_box (tuple): Dimensions of the bottom box (width, thickness) in mm.
    """
    coords = generate_I_beam_coords(top_box, web, bottom_box)
    stresses = [sigma_z(Mx, My, x, y, Ixx, Iyy) for x, y in coords]

    # I-beam shape
    x_shape, y_shape = generate_I_beam_shape(top_box, web, bottom_box)

    # Plotting
    x_coords = [x for x, y in coords]
    y_coords = [y for x, y in coords]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, c=stresses, cmap='viridis', marker='o', label="Stress Points")
    plt.plot(x_shape, y_shape, color='black', linestyle='-', linewidth=1.5, label="I-Beam Shape")
    
    # Corrected small vertical outline in the upper left corner of the I-beam
    plt.plot([-top_box[0] / 2, -top_box[0] / 2], 
             [web[0] / 2 + top_box[1], web[0] / 2],  # Corrected y-coordinate to close the shape
             color='black', linewidth=1.5, label="Small Vertical Outline")


    plt.colorbar(label='Bending Stress (Pa)')
    plt.title('Bending Stress Distribution and I-Beam Shape')
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    plt.grid(False)
    plt.axis('equal')
    plt.show()


# Example usage
if __name__ == '__main__':
    # Bending moments
    Mx = 5000  # Nm
    My = 2000  # Nm

    # Moments of inertia
    Ixx = 8.2 * 10**6  # mm^4
    Iyy = 6.5 * 10**6  # mm^4

    # I-beam dimensions
    top_box = (170, 10)  # width x thickness in mm
    web = (180, 10)      # height x thickness in mm
    bottom_box = (170, 10)  # width x thickness in mm

    # Plot stress distribution with I-beam shape
    plot_stress_distribution_with_shape(Mx, My, Ixx, Iyy, top_box, web, bottom_box)