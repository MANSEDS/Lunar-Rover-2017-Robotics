# System variables
wheel_diameter = 0.12 # m
pi = 3.14159
max_rpm = 26
max_ang_vel = max_rpm * pi / 30 # rad/s


def calc_dc(dc_min, dc_max, angle):
    dc_range = dc_max - dc_min
    inter = dc_range * angle / 180
    dc = dc_min + inter
    return dc


if __name__ == "__main__":

    import argparse

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="Angle (Degrees)")
    parser.add_argument("dc_min", help="Minimum Duty Cycle")
    parser.add_argument("dc_max", help="Maximum Duty Cycle")
    args = parser.parse_args()
    a = float(args.a)
    dc_min = float(args.dc_min)
    dc_max = float(args.dc_max)
    if args.od:
        overdrive = True
        print("Overdrive enabled, not recommended for extended durations")
    else:
        overdrive = False


    # Calculate interpolated duty cycle
    dc = calc_dc(dc_min, dc_max, a)
    print("Required duty cycle is: "+str(dc))

else:
    des_ang_vel = calc_des_ang_vel(v)
    dc = calc_dc
    print(dc)
