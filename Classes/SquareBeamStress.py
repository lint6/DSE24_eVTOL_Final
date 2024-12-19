import numpy as np
import matplotlib.pyplot as plt

class SquareBeamStress:
    def __init__(self, height, thickness, Mx, My):
        self.height = height
        self.thickness = thickness
        self.Mx = Mx
        self.My = My
        self.Ixx = self.Iyy = (height**3) * thickness / 12  # Moments of inertia

    def calculate_stress(self, x, y):
        """Calculate bending stress at a point (x, y)."""
        return (self.Mx * y) / self.Ixx - (self.My * x) / self.Iyy

    def generate_coordinates(self):
        """Generate the edge coordinates of the square beam."""
        coords = []

        # Outer boundary
        coords.extend([(x, self.height / 2) for x in np.linspace(-self.height / 2, self.height / 2, 500)])  # Top edge
        coords.extend([(self.height / 2, y) for y in np.linspace(self.height / 2, -self.height / 2, 500)])  # Right edge
        coords.extend([(x, -self.height / 2) for x in np.linspace(self.height / 2, -self.height / 2, 500)])  # Bottom edge
        coords.extend([(-self.height / 2, y) for y in np.linspace(-self.height / 2, self.height / 2, 500)])  # Left edge

        return coords

    def generate_shapes(self):
        """Generate the outer and inner boundaries of the square beam."""
        # Outer square
        x_outer = [-self.height / 2, self.height / 2, self.height / 2, -self.height / 2, -self.height / 2]
        y_outer = [self.height / 2, self.height / 2, -self.height / 2, -self.height / 2, self.height / 2]

        # Inner square
        inner_height = self.height - self.thickness
        x_inner = [-inner_height / 2, inner_height / 2, inner_height / 2, -inner_height / 2, -inner_height / 2]
        y_inner = [inner_height / 2, inner_height / 2, -inner_height / 2, -inner_height / 2, inner_height / 2]

        return x_outer, y_outer, x_inner, y_inner

    def plot_stress_distribution(self):
        """Plot the stress distribution and the beam shape."""
        coords = self.generate_coordinates()
        stresses = [self.calculate_stress(x, y) / (10**6) for x, y in coords]

        # Generate beam shapes
        x_outer, y_outer, x_inner, y_inner = self.generate_shapes()

        # Neutral Axis
        x_NA = np.linspace(-self.height / 2, self.height / 2, 500)
        if self.Mx != 0 and self.My != 0:
            NA = (self.My * self.Ixx) / (self.Mx * self.Iyy)
            y_NA = NA * x_NA
        else:
            y_NA = np.zeros_like(x_NA)

        # Plotting
        x_coords = [x for x, y in coords]
        y_coords = [y for x, y in coords]

        plt.figure(figsize=(10, 6))
        plt.scatter(x_coords, y_coords, c=stresses, cmap='viridis', marker='o', label="Stress Points")

        # Plot outer and inner squares
        plt.plot(x_outer, y_outer, color='black', linestyle='-', linewidth=1.5, label="Outer Square Beam Shape")
        plt.plot(x_inner, y_inner, color='black', linestyle='-', linewidth=1.5, label="Inner Square Beam Shape")

        # Neutral Axis Line
        plt.plot(x_NA, y_NA, color='red', linestyle='--', linewidth=0.5, label='Neutral Axis')

        # Axis Lines
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

        plt.colorbar(label='Bending Stress (MPa)')
        plt.title('Bending Stress Distribution')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.grid(False)
        plt.axis('equal')
        plt.show()

# Example usage
if __name__ == '__main__':
    # Parameters
    height = 0.2  # m
    thickness = 0.01  # m
    Mx = 5000  # Nm
    My = 2000  # Nm

    # Create an instance of the SquareBeamStress class
    beam = SquareBeamStress(height, thickness, Mx, My)

    # Plot stress distribution
    beam.plot_stress_distribution()
