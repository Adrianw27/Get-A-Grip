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
#FRI-30
import random

#Rotate_base
#Author - Adrian
#Inputs - The color of the autoclave being rotated to
#Outputs - None
#What it does - Rotates toward the potentiometer ussing the right potentiometer.
#Checks to see that the arm is in the range of the correct potentiometer, and then snaps to that autoclaves center point.
def rotate_base(colour):
    autoclave_found = False #this boolean checks if we found the correct autoclave
    old_reading = potentiometer.right() #the very first potentiometer reading
    while not autoclave_found:
        if arm.check_autoclave(colour) == True: #arm is in autoclave range
            if colour == "red":
                arm.move_arm(0.0, 0.406, 0.483) #coordinates for each autoclave
            elif colour == "blue":
                arm.move_arm(0.0, -0.406, 0.483)
            else: #green
                arm.move_arm(-0.379, 0.146, 0.483)
            autoclave_found = True
        else:
            new_reading = potentiometer.right() #if the autoclave hasnt been found yet
            delta = new_reading - old_reading
            increment = 348*delta
            arm.rotate_base(increment) #keep moving using absolute angles
            time.sleep(0.2)
            old_reading = new_reading
    time.sleep(2)


#continue_or_terminate
#Author - Adrian
#Inputs - the current list of containers that have not been processed
#Outputs - a boolean saying if more containers need to be processed or not
#What it does - checks to see if the input list is greater than 0. Also doubles as our goHome() function and brings the arm home.
def continue_or_terminate(container_list): #decide when to end the program
    potReset = False #before looping the program wait for the potentiometer values to be reset
    while not potReset:
        if potentiometer.left() == 0.5 and potentiometer .right() == 0.5:
            potReset = True
        
    if len(container_list) > 0: #there is atleast one container left to handle
        arm.home() #bring the arm home
        return True
    else:
        return False
#pickUpContainer
#Author - Mustafa
#Inputs - the current list of containers that have not been processed
#Outputs - returns a list that holds the updated container list, the color of the chosen container, and the chosen container's ID
#What it does - picks a random container from current container list and removes it from the list. Finds that container's color and ID.
#Also spawns the container and then makes the arm pick it up and return with the container to the home position.
def pickUpContainer(containerList): 
    container = random.choice(containerList)
    containerList.remove(container) #choose a random container and remove it from the list of containers left to handle
    arm.spawn_cage(container) #spawn the container
    time.sleep(2)
    arm.move_arm(containerSpawnLocation[0],containerSpawnLocation[1],containerSpawnLocation[2]) #this is where the container will spawn, it is pre determined
    time.sleep(2)
    arm.control_gripper(45)
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483) #coordinates of home (using the home function will open the gripper arm)

    if container == 1 or container == 4: #find the color of the container to return
        color = "red"

    elif container == 2 or container == 5:
        color = "green"

    elif container == 3 or container == 6:
        color = "blue"
    
    return [color, containerList, container] #return the updated container list and other container information

#dropContainer
#Author - Mustafa/Arther
#Inputs - color of the container being handled along with its ID.
#Output - No output
#What it does - Decides if the container is small or large. Double checks the container color is the same as the autoclave color.
#Drops the container into the correct position depending on size.
def dropContainer(color, container):
    dropped = False
    arm.activate_autoclaves() #activate the autoclaves
    while not dropped:
        time.sleep(1)
        potRead = potentiometer.left() #read the left potentiometer to determine where to drop the container
        if potRead > 0.5 and potRead < 1 and container <= 3: #position is 1 AND container is small
            time.sleep(2)
            if color == "red":
                #arm.move_arm(0.0, 0.652, 0.308)  #predetermined coordinates
                arm.move_arm(0.0, 0.696, 0.296)

            elif color == "blue":
                #arm.move_arm(0.0, -0.652, 0.308)
                arm.move_arm(0.0, -0.696, 0.295)

            elif color == "green":
                #arm.move_arm(-0.608, 0.234, 0.308)
                arm.move_arm(-0.679, 0.261, 0.313)
            time.sleep(2)

            arm.control_gripper(-45) #actually drop the container
            time.sleep(2)
            dropped = True
    
        elif potRead == 1 and container >= 4: #position is 2 AND container is large
            arm.open_autoclave(color, True) #open the drawer
            time.sleep(2)
            if color == "red":
                arm.move_arm(0.0, 0.484, 0.177) #predetermined coordinates

            elif color == "blue":
                arm.move_arm(0.0, -0.465, 0.148)

            elif color == "green":
                #arm.move_arm(-0.476, 0.182, 0.161)
                arm.move_arm(-0.496, 0.19, 0.189)

            time.sleep(2)
            arm.control_gripper(-45) #do the drop
            time.sleep(2)
            dropped = True
            arm.home()
            time.sleep(3)
            arm.open_autoclave(color,False) #close the drawer
            time.sleep(2)

            
    arm.deactivate_autoclaves()
    arm.home()
    return None



containerSpawnLocation = [0.653, 0.057, 0.044]
oldContainerList = [1,2,3,4,5,6] #all the containers


con_or_term = True
while con_or_term:
    

    containerInfo = pickUpContainer(oldContainerList) #recall this function returns container info after picking it up
    newContainerList = containerInfo[1]
    oldContainerList = newContainerList

    color = containerInfo[0]
    container = containerInfo[2] #unpacking the container information

    rotate_base(color)

    dropContainer(color, container)

    con_or_term = continue_or_terminate(oldContainerList)  #check to see if we should continue or not and then update the flag accordingly
    
print("End of Program!!")




#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

