import numpy as np
import matplotlib.pyplot as plt
import math
from airfoil import AirfoilData

class BEMT():
    # coding on blade-element momentum theory

    def __init__(self):
        # constants
        self.rho = 1.225 # kg/m^3, the air density

        # airfoil specification
        self.a_r = 5.73  # /rad, the profile lift curve slope in the linear region

        # specify initial rotor sizing parameters
        self.R = 5 # m, the rotor radius in meters
        self.b = 1 # - , number of blades
        self.omega = 40 # rad/s, rotational velocity



    def discretise(self):

        num_sections = 4

        self.c_r_list = [0.2,0.2,0.2,0.2]
        self.theta_r_list = [0.0,0.0,0.0,0.0]
        self.a_r_list = [self.a_r, self.a_r, self.a_r, self.a_r]

        self.r_list = [i * (self.R / num_sections) + 0.5 * (self.R / num_sections) for i in range(num_sections)]
        self.dr = (self.R / num_sections)


    def lift_drag(self, omega=None, theta_r=None, c_r=None, r=None, dr=None, V_c=None):
        # define non-dimensionalised rotor radius position
        r_bar = r / self.R
        V_t = omega * self.R

        # compute induced velocity at point r
        induced_1 = (self.a_r * self.b * c_r)/(16 * math.pi * self.R)
        induced_2 = -1 * (induced_1 + (V_c / (2 * V_t)))
        induced_3 = math.sqrt((induced_1 + (V_c /(2 * V_t)))**2 + ((induced_1 * 2) * ((r_bar * theta_r) - (V_c / V_t))))
        v_r = V_t * (induced_2 + induced_3)

        alpha = theta_r - (V_c + v_r) / (omega * r)

        # lift for a blade element of size dr
        dL_r = 0.5 * self.a_r * self.rho * (alpha) * c_r * ((omega * r)**2) * dr

        # drag for a blade element of size dr
        airfoildata = AirfoilData()
        interpolated_c_l, interpolated_c_d = airfoildata.interpolate_cl_cd(alpha)
        print(interpolated_c_d)
        dDp_r = 0.5 * interpolated_c_d * self.rho * ((omega * r)**2) * c_r * dr

        # thrust generated by a blade element of size dr
        dT_r = dL_r - dDp_r * ((V_c + v_r)/(omega * r))

        # torque needed for a blade element of size dr
        dQ_r = (dL_r * ((V_c + v_r)/(omega * r)) + dDp_r) * r

        prop = [dL_r,dDp_r,dT_r,dQ_r]
        return prop



if __name__ == '__main__':
    BEMT = BEMT()
    BEMT.discretise()
    print(BEMT.r_list)

    dL_r_list = []
    dDp_r_list = []
    dT_r_list = []
    dQ_r_list = []

    for chord, theta, a, r in zip(BEMT.c_r_list, BEMT.theta_r_list, BEMT.a_r_list, BEMT.r_list):
        prop = BEMT.lift_drag(omega=BEMT.omega, theta_r=theta, c_r=chord, r=r, dr=BEMT.dr, V_c=0)
        dL_r_list.append(prop[0])
        dDp_r_list.append(prop[1])
        dT_r_list.append(prop[2])
        dQ_r_list.append(prop[3])

    print(dL_r_list)
    print(dDp_r_list)
    print(dT_r_list)
    print(dQ_r_list)





