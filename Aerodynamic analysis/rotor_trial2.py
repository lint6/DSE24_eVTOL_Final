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
        self.intercept_cl = 0.2379 # NACA 2412


    def discretise(self, num_elements=1000):
        # divide blade into elements
        self.cutout = 0.15 * self.R
        #self.r_bar_e = 0.95 #effective blade radius due to tip losses, approximate input for now
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
        c_l_linear = a_r * alpha + self.intercept_cl

        U_r = np.hypot(omega * r, (V_c + v_r))

        # drag for a blade element of size dr
        airfoildata = AirfoilData()
        interpolated_c_l, interpolated_c_d = airfoildata.interpolate_cl_cd(alpha * (180 / np.pi))

        # Lift for a blade element of size dr
        dDp_r = interpolated_c_d * 0.5 * self.rho * ((U_r) ** 2) * c_r * dr

        dL_r = c_l_linear * 0.5 * self.rho * ((U_r) ** 2) * c_r * dr

        dT_r = dL_r * np.cos(phi) - dDp_r * np.sin(phi)
        
        # torque needed for a blade element of size dr
        dFx = dL_r * np.sin(phi) + dDp_r * np.cos(phi)
        dQ_r = (dL_r * np.sin(phi) + dDp_r * np.cos(phi)) * r
        dP_r = dQ_r * omega

        dP_ind = 4 * math.pi * (self.R ** 2) * self.rho * (v_r ** 3) * r_bar * dr_bar

        prop = [dL_r, dDp_r, dT_r, dQ_r, dP_r, dP_ind]
        return prop, v_r, c_l_linear

    def calculate_radius_and_rotors(self, num_elements=1000):
        # initial guess for radius
        self.R = 0.98

        self.cutout = 0.15 * self.R
       # self.r_bar_e = 0.95 #effective blade radius due to tip losses, approximate input for now
        self.r_e = 0.95 * self.R
        
        self.discretise(num_elements)

        dT_r_list = []
        dL_r_list = []
        dDp_r_list = []
        dQ_r_list = []
        dP_r_list = []
        dP_ind_list = []
        for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list):
            prop = self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, a_r=a, V_c=0)
            if self.cutout < r < self.r_e:
                dT_r_list.append(prop[0][2])
                dL_r_list.append(prop[0][0])
                dDp_r_list.append(prop[0][1])
                dQ_r_list.append(prop[0][3])
                dP_r_list.append(prop[0][4])
                dP_ind_list.append(prop[0][5])
            else:
                dT_r_list.append(0.0)
                dL_r_list.append(0.0)
                dDp_r_list.append(0.0)
                dQ_r_list.append(0.0)
                dP_r_list.append(0.0)
                dP_ind_list.append(0.0)


        total_thrust = sum(dT_r_list) * self.n_rot * self.b
        total_lift = sum(dL_r_list) * self.n_rot * self.b
        total_drag = sum(dDp_r_list) * self.n_rot * self.b

        max_iterations = 1000  # Set a maximum number of iterations to prevent infinite loop
        iteration = 0

        while total_thrust < self.thrust and iteration < max_iterations:
            if self.omega < 140:
                self.omega += 5
            elif self.n_rot < 6:
                self.n_rot += 2
                self.omega = 100  # Reset omega to 200 when the number of rotors increases
            else:
                #self.n_rot = 8  # Reset the number of rotors to 4 when omega reaches 200
                self.R += 0.01  # If all conditions are met, increase the radius
                    
            self.discretise(num_elements)
            dT_r_list = []
            dL_r_list = []
            dDp_r_list = []
            dQ_r_list = []
            dP_r_list = []
            dP_ind_list = []
            for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list):
                prop = self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, a_r=a, V_c=0)
                if self.cutout < r < self.r_e:
                    dT_r_list.append(prop[0][2])
                    dL_r_list.append(prop[0][0])
                    dDp_r_list.append(prop[0][1])
                    dQ_r_list.append(prop[0][3])
                    dP_r_list.append(prop[0][4])
                    dP_ind_list.append(prop[0][5])
                else:
                    dT_r_list.append(0.0)
                    dL_r_list.append(0.0)
                    dDp_r_list.append(0.0)
                    dQ_r_list.append(0.0)
                    dP_r_list.append(0.0)
                    dP_ind_list.append(0.0)
            total_thrust = sum(dT_r_list) * self.n_rot * self.b
            total_lift = sum(dL_r_list) * self.n_rot * self.b
            total_drag = sum(dDp_r_list) * self.n_rot * self.b
            total_torque = sum(dQ_r_list) * self.n_rot * self.b
            total_power = sum(dP_r_list) * self.n_rot * self.b
            total_induced_power = sum(dP_ind_list) * self.n_rot * self.b
            iteration += 1
            #print(f"Iteration: {iteration}, Total Thrust: {total_thrust}, Radius: {self.R}, Number of Rotors: {self.n_rot}, Omega: {self.omega}")
            print(f"Iteration: {iteration}, Total Thrust: {total_thrust}, Radius: {self.R}, Number of Rotors: {self.n_rot}, Omega: {self.omega}, Total Power: {total_power}")

        # Calculate total thrust and power for one blade
        total_thrust_one_blade = total_thrust / (self.n_rot * self.b)
        total_power_one_blade = total_power / (self.n_rot * self.b)
        print(f"Total Thrust for One Blade: {total_thrust_one_blade}")
        print(f"Total Power for One Blade: {total_power_one_blade}")

        if iteration == max_iterations:
            print("Reached maximum iterations without achieving desired thrust.")

        return self.R, self.n_rot

if __name__ == '__main__':
    a_r = 0.1225 * 180 / np.pi#0.1 * 180 / np.pi
    b = 6
    n_rot = 6
    omega = 100
    thrust = 7758.73 #7900/np.cos(np.deg2rad(5))  # desired thrust in Newtons
    R = 0.75
    bemt = BEMT(a_r, b, n_rot, omega, thrust)
    radius, num_rotors = bemt.calculate_radius_and_rotors()

    print(f"Required Radius: {radius} meters")
    print(f"Number of Rotors: {num_rotors}")
    print(f"Final Omega: {bemt.omega}")
    
    # Calculate the thrust coefficient
    total_thrust = sum([bemt.vertical(omega=bemt.omega, theta_r=theta, c_r=chord, r=r, dr=bemt.dr, a_r=a, V_c=0)[0][2] for chord, theta, a, r in zip(bemt.c_r_list, bemt.theta_r_list, bemt.a_r_list, bemt.r_list)]) * bemt.n_rot * bemt.b
    thrust_coefficient = total_thrust / (bemt.rho * (bemt.omega ** 2) * (bemt.R ** 4) * bemt.n_rot * bemt.b)
    print(f"Thrust Coefficient: {thrust_coefficient}")
    # print total power required
    
    

   
