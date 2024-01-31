ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()

#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

def rotate_base(colour):
    autoclave_found = False
    arm.home()
    old_reading = potentiometer.right()
    while not autoclave_found:
        if arm.check_autoclave(colour) == True:
            if colour == "red":
                arm.move_arm(0.0, 0.406, 0.483)
            elif colour == "blue":
                arm.move_arm(0.0, -0.406, 0.483)
            else:
                arm.move_arm(-0.379, 0.146, 0.483)
            autoclave_found = True
        else:
            new_reading = potentiometer.right()
            delta = new_reading - old_reading
            increment = 348*delta
            arm.rotate_base(increment)
            time.sleep(0.2)
            old_reading = new_reading
                
rotate_base("green")

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    



