import numpy as np
import matplotlib.pyplot as plt

class SquareBeamShearFlow:

    def __init__(self, b, t, Vx, Vy):
        """
        Initialize the square beam properties.
        :param b: Side length of the square cross-section (outer dimension).
        :param t: Thickness of the square wall (thin-walled assumption).
        :param Vx: Horizontal shear force.
        :param Vy: Vertical shear force.
        """
        self.b = b
        self.t = t
        self.Vx = Vx
        self.Vy = Vy

    def calculate_Ixx(self):
        """
        Calculate the second moment of area (Ixx).
        """
        I_xx_outer = (1 / 12) * self.b**4
        I_xx_inner = (1 / 12) * (self.b - 2 * self.t)**4
        return I_xx_outer - I_xx_inner

    def calculate_Iyy(self):
        """
        Calculate the second moment of area (Iyy).
        """
        return self.calculate_Ixx()

    def calculate_shear_flow_Vx(self):
        """
        Calculate the shear flow for Vx (horizontal shear force) along the edges of the square.
        :return: Dictionary of shear flow arrays for each segment.
        """
        b, t, Vx = self.b, self.t, self.Vx
        Iyy = self.calculate_Iyy()

        # Edge c4 (midpoint of 4-1) to 1
        s_c4_1 = np.linspace(0, b / 2, 100)
        q_c4_1 = (-Vx * t / Iyy) * (b / 2) * s_c4_1

        # Edge 1 to 2
        s_1_2 = np.linspace(0, b, 100)
        q_1_2 = (-Vx * t / Iyy) * ((b / 2) * s_1_2 - s_1_2**2 / 2)

        # Edge 2 to c3 (midpoint of 2-3)
        s_2_c3 = np.linspace(0, b / 2, 100)
        q_2_c3 = (Vx * t / Iyy) * (b / 2) * s_2_c3

        # Edge 3 to c2 (mirror of edge 2 to c3)
        q_3_c2 = -q_2_c3

        return {
            "c4_1": (s_c4_1, q_c4_1),
            "1_2": (s_1_2, q_1_2),
            "2_c3": (s_2_c3, q_2_c3),
            "3_c2": (s_2_c3, q_3_c2),
        }

    def plot_shear_flow_Vx(self):
        """
        Plot the cross-section and shear flow lines for Vx (horizontal shear force).
        """
        b = self.b
        shear_flows = self.calculate_shear_flow_Vx()

        # Plot the square cross-section
        square_vertices = np.array([[0, b], [b, b], [b, 0], [0, 0], [0, b]])
        plt.figure(figsize=(8, 8))
        plt.plot(square_vertices[:, 0], square_vertices[:, 1], 'k-', label='Cross-Section')

        # Plot shear flow on each segment
        offset = 0.1  # Scaling factor for visualization

        # Edge c4 to 1
        s_c4_1, q_c4_1 = shear_flows["c4_1"]
        plt.plot(-offset * q_c4_1 / max(abs(q_c4_1)), b - s_c4_1, 'r-', label='q_c4_1')

        # Edge 1 to 2
        s_1_2, q_1_2 = shear_flows["1_2"]
        plt.plot(s_1_2, b + offset * q_1_2 / max(abs(q_1_2)), 'g-', label='q_1_2')

        # Edge 2 to c3
        s_2_c3, q_2_c3 = shear_flows["2_c3"]
        plt.plot(b + offset * q_2_c3 / max(abs(q_2_c3)), b - s_2_c3, 'b-', label='q_2_c3')

        # Edge 3 to c2
        s_3_c2, q_3_c2 = shear_flows["3_c2"]
        plt.plot(b - offset * q_3_c2 / max(abs(q_3_c2)), s_3_c2, 'm-', label='q_3_c2')

        # Formatting the plot
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
        plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.title('Shear Flow Visualization for Vx (Horizontal Shear Force)')
        plt.grid(True)
        plt.show()

# Example usage
beam = SquareBeamShearFlow(b=1.0, t=0.1, Vx=1000, Vy=0)
beam.plot_shear_flow_Vx()
