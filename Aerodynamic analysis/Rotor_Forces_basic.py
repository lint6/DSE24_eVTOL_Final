import numpy as np
import matplotlib.pyplot as plt

#Inputs req: Rotor chord, Collective angle, Max cyclic angle, 
# Diameter of the rotor, T/c ratio for propeller section
# Sea level density, 
# RPM, Forward velocity, 
# Tilt, Climb speed, 
#Max flapping velocity

#Outputs: Thrust, Torque, Mx, My

#This is mainly for a helicopter rotor & inputs not so useful, so 
# will probably change this 



# Chord length of blade assumed constant with radius
chord = 0.20
# Collective angle
collective = 8.0 / 180 * np.pi
# Max cyclic angle
cyclic = 0.0 / 180 * np.pi
# Diameter of the rotor
dia = 4.0
# Tip radius
R = dia / 2.0
# Rotor speed in RPM
RPM = 400.0
# Thickness to chord ratio for propeller section (constant with radius)
tonc = 0.12 * chord
# Standard sea level atmosphere density
rho = 1.225
# RPM --> revs per second
n = RPM / 60.0
# Revs per second --> radians per second
omega = n * 2.0 * np.pi
# Use 16 blade segments (starting at 20% R (hub) to 95% R)
rstep = (0.95 - 0.2) / 16 * R
# Forward velocity
V = 0.0
# Tilt
tilt = 0.0 / 180.0 * np.pi
# Climb speed
Vc = 0.0
# Max flapping velocity
vflap = 0.0
# Initialize outputs
thrust = 0.0
torque = 0.0
Mx = 0.0
My = 0.0

# Preallocate arrays
r1 = np.zeros(16)
t1 = np.zeros(16)
val = np.zeros((16, 16))
x = np.zeros((16, 16))
y = np.zeros((16, 16))

# Loop over each blade element
for i in range(16):
    rad = ((0.95 - 0.2) / 16 * (i + 1) + 0.2) * R
    r1[i] = rad / R
    
    # Loop over each angular sector
    for j in range(16):
        psi = np.pi / 8 * (j + 1) - np.pi / 16
        t1[j] = psi
        
        # Calculate local blade element setting angle
        theta = collective + cyclic * np.cos(psi)
        sigma = 2.0 * chord / (2.0 * np.pi * rad)
        
        # Guess initial value of induced velocity
        Vi = 10.0
        finished = False
        iteration_count = 0
        
        while not finished:
            # Normal velocity components
            V0 = Vi + Vc + V * np.sin(tilt) + vflap * rad * np.sin(psi)
            # Disk plane velocity
            V2 = omega * rad + V * np.cos(tilt) * np.sin(psi)
            # Flow angle
            phi = np.arctan2(V0, V2)
            # Blade angle of attack
            alpha = theta - phi
            # Lift coefficient
            cl = 6.2 * alpha
            # Drag coefficient
            cd = 0.008 - 0.003 * cl + 0.01 * cl * cl
            # Local velocity at blade
            Vlocal = np.sqrt(V0**2 + V2**2)
            # Thrust grading
            DtDr = 0.5 * rho * Vlocal**2 * 2.0 * chord * (cl * np.cos(phi) - cd * np.sin(phi)) / 16.0
            # Torque grading
            DqDr = 0.5 * rho * Vlocal**2 * 2.0 * chord * rad * (cd * np.cos(phi) + cl * np.sin(phi)) / 16.0
            # Momentum check on induced velocity
            tem1 = DtDr / (np.pi / 4.0 * rad * rho * V0)
            
            # Stabilize iteration
            Vinew = 0.9 * Vi + 0.1 * tem1
            if Vinew < 0:
                Vinew = 0.0
            
            # Check for convergence
            if abs(Vinew - Vi) < 1.0e-5:
                finished = True
            Vi = Vinew
            
            # Increment iteration count
            iteration_count += 1
            if iteration_count > 500:
                finished = True
        
        val[i, j] = alpha
        thrust += DtDr * rstep
        torque += DqDr * rstep
        Mx += rad * np.sin(psi) * DtDr * rstep
        My += rad * np.cos(psi) * DtDr * rstep

# Generate x, y coordinates for contour plot
for i in range(16):
    for j in range(16):
        x[i, j] = r1[i] * np.cos(t1[j])
        y[i, j] = r1[i] * np.sin(t1[j])

# Plot contour
plt.contour(x, y, val, levels=50)
plt.axis('equal')
plt.title('Blade Angle of Attack Distribution')
plt.xlabel('x (normalized radius)')
plt.ylabel('y (normalized radius)')
plt.colorbar(label='Angle of Attack (rad)')
plt.show()

# Print outputs
print(f"Thrust: {thrust:.4f} N")
print(f"Torque: {torque:.4f} Nm")
print(f"Mx: {Mx:.4f} Nm")
print(f"My: {My:.4f} Nm")
