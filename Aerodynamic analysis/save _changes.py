
   def interpolation(self):
    print("Hello")

        # interpolate with numpy the values of lift and drag as a function of the radius position
        self.dL_r_interp = np.interp(self.r_list, self.r_list, [
            self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, V_c=0.0, a_r=a)[0] if self.cutout < r < self.r_e else 0.0
            for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list)
        ])
        self.dD_r_interp = np.interp(self.r_list, self.r_list, [
            self.vertical(omega=self.omega, theta_r=theta, c_r=chord, r=r, dr=self.dr, V_c=0.0, a_r=a)[1] if self.cutout < r < self.r_e else 0.0
            for chord, theta, a, r in zip(self.c_r_list, self.theta_r_list, self.a_r_list, self.r_list)
        ])
        # return the values
        return self.dL_r_interp, self.dD_r_interp


