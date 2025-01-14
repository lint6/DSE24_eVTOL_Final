import numpy as np 
import matplotlib.pyplot as plt 

class SquareBeamShearFlow:

    def __init__(self, h=0.10, t=0.01, Vy=2000, Vx=1000):
        self.h = h 
        self.t = t 
        self.Vy = Vy 
        self.Vx = Vx 
    
    def calculate_Ixx(self):
        Ixx_outer = 1/12 * self.h**4
        Ixx_inner = 1/12 * (self.h - 2*self.t)**4
        return Ixx_outer - Ixx_inner 

    def calculate_Iyy(self):
        return self.calculate_Ixx()
    
    def define_vertical_walls(self):
        # wall 1
        x_coords_1 = np.linspace(0, -self.h/2, 1000)
        y_coords_1 = np.full_like(x_coords_1, -self.h/2)

        # wall 2
        y_coords_2 = np.linspace(-self.h, 0, 2000)
        x_coords_2 = np.full_like(y_coords_2, -self.h/2)
        
        coordinates_wall1 = list(zip(x_coords_1, y_coords_1))
        coordinates_wall2 = list(zip(x_coords_2, y_coords_2))
        return coordinates_wall1, coordinates_wall2

    def calculate_q_at_point_vertical_wall1(self, point):
        ### point = (x, y)
        A = - self.Vy * self.t / self.calculate_Ixx()
        q = A * (-self.h/2) * point[0]
        return q 

    def calculate_q_at_point_vertical_wall2(self, point):
        qs0 = self.calculate_q_at_point_vertical_wall1((-self.h/2, -self.h/2))
        A = (-self.Vy * self.t) / self.calculate_Ixx()
        q = qs0 + (A * (-self.h*point[1]/2 + point[1]**2/2))
        return q

    def plot_vertical_wall1(self):
        coordinates = self.define_vertical_walls()[0]
        q_values = [self.calculate_q_at_point_vertical_wall1(coordinate) for coordinate in coordinates]
        x_coords, y_coords = zip(*coordinates)
        plot_x = np.linspace(0, self.h/2, 1000)

        plt.figure(figsize=(8, 6))
        plt.plot(plot_x, q_values)
        plt.xlabel('x coordinate [m]')
        plt.ylabel('Shear Flow [N/m]')
        plt.title('Shear Flow Distribution on Vertical Wall 1')

        plt.grid(True)
        plt.show()

    def plot_vertical_wall2(self):
        coordinates = self.define_vertical_walls()[1]
        q_values = [self.calculate_q_at_point_vertical_wall2(coordinate) for coordinate in coordinates]
        x_coords, y_coords = zip(*coordinates)

        plt.figure(figsize=(8, 6))
        plt.plot(y_coords, q_values)
        plt.xlabel('y coordinate [m]')
        plt.ylabel('Shear Flow [N/m]')
        plt.title('Shear Flow Distribution on Vertical Wall 2')

        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    SB = SquareBeamShearFlow()
    SB.plot_vertical_wall1()
    SB.plot_vertical_wall2()
    print(SB.calculate_q_at_point_vertical_wall2((-SB.h/2, -SB.h/2)))
    print(SB.calculate_Ixx())