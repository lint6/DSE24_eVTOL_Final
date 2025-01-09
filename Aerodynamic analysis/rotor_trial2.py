import numpy as np
import math
from airfoil import AirfoilData

class BEMT():
    # coding on blade-element momentum theory

    def __init__(self, a_r, b, n_rot, omega, thrust):
        # constants
        self.rho = 1.225 # kg/m^3, the air density

        # airfoil specification
        self.a_r = a_r  # [-/deg], the profile lift curve slope in the linear region NACA2414

        # specify initial rotor sizing parameters
        self.b = b # - , number of blades
        self.n_rot = n_rot # - , number of rotors
        self.omega = omega # rad/s, rotational velocity
        self.thrust = thrust # desired thrust


    def discretise(self, num_elements=4):
        # divide blade into elements
        self.cutout = 0.15 * self.R
        self.r_bar_e = 0.95 #effective blade radius due to tip losses, approximate input for now
        self.r_e = 0.95 * self.R
        self.r_list = np.linspace(0.5 * (self.R / num_elements), self.R - 0.5 * (self.R / num_elements), num_elements)
        self.dr = self.R / num_elements

        # setup chord
        c_root = 0.1 # meters
        taper = 1 # -
        c_tip = c_root * taper
        c_avg = 0.5 * (c_root + c_tip)
        self.AR = (self.R - self.cutout) / c_avg
        
        # slope of the chord distribution
        slope_c = (c_tip - c_root) / (self.R - self.cutout)

        self.c_r_list = []
        for r in self.r_list:
            c_r = (c_root - (slope_c * self.cutout)) + (slope_c * r)
            self.c_r_list.append(c_r)

        # setup theta
        theta_root = np.deg2rad(20)
        theta_tip = np.deg2rad(5)

        slope_t = (theta_tip - theta_root) / (self.R - self.cutout)

        self.theta_r_list = []
        for r in self.r_list:
            theta_r = (theta_root - (slope_t * self.cutout)) + (slope_t * r)
            self.theta_r_list.append(theta_r)

        # setup airfoil progression
        self.a_r_list = np.full(num_elements, self.a_r)

    def vertical(self, omega=None, theta_r=None, c_r=None, r=None, dr=None, V_c=None, a_r=None):
        # define non-dimensionalised rotor radius position
        r_bar = r / self.R
        V_t = omega * self.R
        dr_bar = dr / self.R

        # compute induced velocity at point r
        induced_1 = (a_r * self.b * c_r) / (16 * math.pi * self.R)
        induced_2 = -1 * (induced_1 + (V_c / (2 * V_t)))
        induced_3 = math.sqrt((induced_1 + (V_c / (2 * V_t)))**2 + ((induced_1 * 2) * ((r_bar * theta_r) - (V_c / V_t))))
        v_r = V_t * (induced_2 + induced_3)

        phi = np.arctan((V_c + v_r) / (omega * r))
        alpha = theta_r - phi
        self.alpha = alpha
        c_l_linear = a_r * alpha

        U_r = np.hypot(omega * r, (V_c + v_r))

        # drag for a blade element of size dr
        airfoildata = AirfoilData()
        interpolated_c_l, interpolated_c_d = airfoildata.interpolate_cl_cd(alpha)

        # Lift for a blade element of size dr
        dDp_r = interpolated_c_d * 0.5 * self.rho * ((U_r) ** 2) * c_r * dr

        dL_r = c_l_linear * 0.5 * self.rho * ((U_r) ** 2) * c_r * dr

        dT_r = dL_r * np.cos(phi) - dDp_r * np.sin(phi)
        
        dQ_r = (dL_r * np.sin(phi) + dDp_r * np.cos(phi)) * r

        dP_r = dQ_r * omega

        dP_ind = 4 * math.pi * (self.R ** 2) * self.rho * (v_r ** 3) * r_bar * dr_bar

        prop = [dL_r * self.b, dDp_r * self.b, dT_r * self.b, dQ_r * self.b, dP_r * self.b, dP_ind * self.b]
        return prop, v_r, c_l_linear

    def calculate_radius_and_rotors(self, num_elements=20):
        # initial guess for radius
        self.R = 0.5

        self.cutout = 0.15 * self.R
        self.r_bar_e = 0.95 #effective blade radius due to tip losses, approximate input for now
        self.r_e = 0.95 * self.R
        
        self.discretise(num_elements)

        dT_r_list = []
        dL_r_list = []
        dDp_r_list = []
        for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list):
            prop = self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, a_r=a, V_c=0)
            if self.cutout<r<self.r_e:
                dT_r_list.append(prop[0][2])
                dL_r_list.append(prop[0][0])
                dDp_r_list.append(prop[0][1])
            else:
                dT_r_list.append(0.0)
                dL_r_list.append(0.0)
                dDp_r_list.append(0.0)

        total_thrust = sum(dT_r_list) * self.n_rot
        total_lift = sum(dL_r_list) * self.n_rot
        total_drag = sum(dDp_r_list) * self.n_rot

        max_iterations = 1000  # Set a maximum number of iterations to prevent infinite loop
        iteration = 0

        while total_thrust < self.thrust and iteration < max_iterations:
            if self.omega < 120:
                self.omega += 5
            elif self.n_rot < 6:
                self.n_rot += 2
                self.omega = 100  # Reset omega to 200 when the number of rotors increases
            else:
                self.R += 0.01  # If all conditions are met, increase the radius
                    
            self.discretise(num_elements)
            dT_r_list = []
            dL_r_list = []
            dDp_r_list = []
            for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list):
                prop = self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, a_r=a, V_c=0)
                dT_r_list.append(prop[0][2])
                dL_r_list.append(prop[0][0])
                dDp_r_list.append(prop[0][1])
            total_thrust = sum(dT_r_list) * self.n_rot
            total_lift = sum(dL_r_list) * self.n_rot
            total_drag = sum(dDp_r_list) * self.n_rot
            iteration += 1
            print(f"Iteration: {iteration}, Total Thrust: {total_thrust}, Radius: {self.R}, Number of Rotors: {self.n_rot}, Omega: {self.omega}")

        if iteration == max_iterations:
            print("Reached maximum iterations without achieving desired thrust.")

        return self.R, self.n_rot

if __name__ == '__main__':
    a_r = 0.1 * 180 / np.pi
    b = 6
    n_rot = 2
    omega = 100
    thrust = 7758.73 #7900/np.cos(np.deg2rad(5))  # desired thrust in Newtons

    bemt = BEMT(a_r, b, n_rot, omega, thrust)
    radius, num_rotors = bemt.calculate_radius_and_rotors()

    print(f"Required Radius: {radius} meters")
    print(f"Number of Rotors: {num_rotors}")
    print(f"Final Omega: {bemt.omega}")
    
    # print total power required
    
    total_power = sum([bemt.vertical(omega=bemt.omega, theta_r=theta, c_r=chord, r=r, dr=bemt.dr, a_r=a, V_c=0)[0][4] for chord, theta, a, r in zip(bemt.c_r_list, bemt.theta_r_list, bemt.a_r_list, bemt.r_list)]) * bemt.n_rot
    print(f"Total Power Required: {total_power} Watts")


