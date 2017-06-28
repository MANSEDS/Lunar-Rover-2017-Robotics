

# System variables
wheel_diameter = 0.12 # m
pi = 3.14159
max_rpm = 26
max_ang_vel = max_rpm * pi / 30 # rad/s

# Calculate angular velocity for desired velocity
def calc_des_ang_vel(v):
    des_ang_vel = 2 * v / wheel_diameter # rad/s
    if des_ang_vel > max_ang_vel:
        if overdrive:
            des_ang_vel = max_ang_vel
            print("Desired velocity exceeds maximum velocity, velocity set to maximum due to" + \
                                "overdrive, extended use of overdrive is not recommended")
        else:
            des_ang_vel = max_ang_vel * 0.9
    elif des_ang_vel >= 0.9 * max_ang_vel:
        if not overdrive:
            des_ang_vel = 0.9 * max_ang_vel
    return des_ang_vel


def calc_dc(dc_min, dc_max, des_ang_vel):
    dc_range = dc_max - dc_min
    inter = dc_range * des_ang_vel / max_ang_vel
    dc = dc_min + inter
    return dc


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("v", help="Velocity")
    parser.add_argument("dc_min", help="Minimum Duty Cycle")
    parser.add_argument("dc_max", help="Maximum Duty Cycle")
    parser.add_argument("--od", help="Overdrive Enable")
    args = parser.parse_args()
    v = float(args.v)
    dc_min = float(args.dc_min)
    dc_max = float(args.dc_max)
    if args.od:
        overdrive = True
        print("Overdrive enabled, not recommended for extended durations")
    else:
        overdrive = False

    # Calculate angular velocity for desired velocity
    des_ang_vel = calc_des_ang_vel(v)
    print("Desired angular velocity is: "+str(des_ang_vel))


    # Calculate interpolated duty cycle
    dc_range = dc_max - dc_min
    inter = dc_range * des_ang_vel / max_ang_vel
    dc = dc_min + inter
    print("Required duty cycle is: "+str(dc))

else:
    des_ang_vel = calc_des_ang_vel(v)
    dc = calc_dc
    print(dc)
