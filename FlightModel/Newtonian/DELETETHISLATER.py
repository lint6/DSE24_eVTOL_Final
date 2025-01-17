from physics import *

def SCcraft_Airligator():

    radius_rotor = 1.17 #radius of rotor
    radius_rotor_ring = 5 # radius of rotor position ring
    rotor_mass = 23.32
    rotor_inertia =[[SCphy_Inertia_Disc[0],0,0],
                    [0,SCphy_Inertia_Disc[1],0],
                    [0,0,SCphy_Inertia_Disc[2]]]
    
    motor_mass = 22.3
    motor_inertia =[[SCphy_Inertia_Cylinder[0],0,0],
                    [0,SCphy_Inertia_Cylinder[1],0],
                    [0,0,SCphy_Inertia_Cylinder[2]]]
    

    arm_mass = 3.95
    arm_inertia = [[SCphy_Inertia_Cylinder[0],0,0],
                   [0,SCphy_Inertia_Cylinder[1],0],
                   [0,0,SCphy_Inertia_Cylinder[2]]]
    
    pax_mass = 185/2
    pax_inertia = [[SCphy_Intertia_Sphere[0],0,0],
                   [0,SCphy_Intertia_Sphere[1],0],
                   [0,0,SCphy_Intertia_Sphere[2]]]
    
    rotor_1 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3), 
                                            radius_rotor_ring * np.cos(np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    rotor_2 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3), 
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    rotor_3 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    rotor_4 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    rotor_5 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
        
    rotor_6 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = rotor_mass,       #[kg] 
                                inertia  = rotor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    motor_1 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi/3), 
                                            radius_rotor_ring * np.cos(np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
    
    motor_2 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(2*np.pi/3), 
                                            radius_rotor_ring * np.cos(2*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_3 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(np.pi), 
                                            radius_rotor_ring * np.cos(np.pi),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    motor_4 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(4*np.pi/3), 
                                            radius_rotor_ring * np.cos(4*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [-10,0,0],)  # euler angle degrees 
    
    motor_5 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(5*np.pi/3), 
                                            radius_rotor_ring * np.cos(5*np.pi/3),
                                            0],   # [m from the body axis origin ]
                                rotation = [10,0,0],)  # euler angle degrees 
        
    motor_6 = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = motor_mass,       #[kg] 
                                inertia  = motor_inertia,
                                position = [radius_rotor_ring * np.sin(0), 
                                            radius_rotor_ring * np.cos(0),
                                            0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    arm_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_3   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_4   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_5   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    arm_6   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = arm_mass,       #[kg] 
                                inertia  = arm_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    pax_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    pax_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = pax_mass,       #[kg] 
                                inertia  = pax_inertia,
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_1   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    bat_2   = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    body_1  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    tank_1  = SCobj_ForcePoint( forces   = [0, 0, 0], #[N, WITHOUT gravitational froce]
                                moments  = [0, 0, 0],   #[N*m]
                                mass     = 0,       #[kg] 
                                inertia  = [[0,0,0],
                                            [0,0,0],
                                            [0,0,0]],
                                position = [0,0,0],   # [m from the body axis origin ]
                                rotation = [0,0,0],)  # euler angle degrees 
    
    
