# MANSEDS Lunar Rover - Command Executor
# Author: Ethan Ramsay

# Import dependencies
import os
import subprocess
import datetime


# Execute function
def execute(command):
    static_arg = None
    dynamic_args = None
    system_controllers = [None, 'python Drive_controller.py ', 'python Arm_controller.py ', + \
                                        'python Camera_controller.py ', 'python Camera_controller.py ']
    system_id, args = command.splt(' ', 1)[0, 1]
    system_controller = system_controllers[system_id]
    static_args = [['-f ', '-b ', '-l ', '-r '], ['-s ', '-e ', '-i ', '-g ', '-d ', '-p ', '-o '], ['-p ', '-m '], ['-p ', '-m ']]
    if args.split(' ', 1)[1]:
        static_arg_id, dynamic args  = args.split(' ', 1)[0, 1]
        static_arg = static_args[system_id][static_arg_id]
    else:
        static_arg_id = args

    # Rebuild command for command line
    if dynamic_args is not None:
        command = system_controller + static_arg + dynamic_args
    else:
        command = system_controller +static_arg
    subprocess.call([command], shell=True, stderr=PIPE)


# Main
if __name__ = "__main__":
    # Read command log
    command = None
    while True:
        while os.stat("/var/www/html/command-queue.dat").st_size is not 0:
            if os.path.isfile("/var/www/html/command-queue.dat"):
                with open("/var/www/html/drive.dat", "r") as handle:
                    command = handle.readline()

            execute(command)


            with open("/var/www/html/command-history.dat", "a+") as handle:
                handle.write("{} {}".format(command, datetime.now()))

            subprocess.call(["sed -i -e '1d' '/var/www/html/command-queue.dat' "], shell=True, stderr=PIPE)
