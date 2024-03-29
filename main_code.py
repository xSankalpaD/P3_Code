#P3 code yoyo

ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P3A' # Enter the project identifier i.e. P2A or P2B

# SERVO TABLE CONFIGURATION
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 
#check
bin1_offset = 0.15 # offset in meters
bin1_color = [1, 0, 0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.15
bin2_color = [0, 1, 0]
bin2_metallic = False

bin3_offset = 0.15
bin3_color = [0, 0, 1]
bin3_metallic = False

bin4_offset = 0.15
bin4_color = [1, 0, 1]
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)


#global value to hold contianer dispensed
container=0
#global list that hold qualities of container dispensed
mass_binlist= [["apple", 0,0],["apple", 9.25,3],["apple", 15,1],["apple", 10,2],["apple", 22.469,4],["apple", 26.649,1],["apple", 29.281,4]]
#global value that hold intial positon of the Q bot
initial_position = bot.position()
#global value that holds which it must go to
bin_value=0
#global boolean to keep track of dispensed container
no_container = True
#global list that hold which bin it must go to based the container 
bin_list= [0,3,1,2,4,1,4]

'''
dispense_container()
Purpose: The purpose of this function is to dispense container from Servo Table
Parameters: None
Randomly generates a container 
Updates global variable mass_binlist and bin_value
Return: None
'''
def dispense_container():
    global container
    global mass_binlist
    global bin_value
    global bin_list

     
    container= random.randint(1,6)
    container_info= table.dispense_container(container, True)  #random container generated and store it's qualities in container_info
    mass_binlist[container] = container_info
    bin_value= bin_list[container]
        
    return None

'''
bottle_load()
Purpose: The purpose of this function is load a bottle into the hopper
Parameters: Take a numeric value for which spot on the hopper to load on
Picks up the bottle from the table and loads it
Return: None
'''
def bottle_load(spot_num):
    time.sleep(3)
    arm.move_arm(0.64,0,0.23) #pickup position
    time.sleep(3)
    arm.control_gripper(40)
    time.sleep(3)
    arm.move_arm(0.012,-0.376, 0.621) #spot before loading
    time.sleep(3)
    if spot_num==1:
        arm.move_arm(0.012,-0.637,0.531) #1st load spot
        time.sleep(3)
    elif spot_num==2:
        arm.move_arm(0.012,-0.521,0.498) #2nd load spot
        time.sleep(3)
    elif spot_num==3:
        arm.move_arm(0.012,-0.462,0.478) #3rd load spot
        time.sleep(3)
    arm.control_gripper(-40)
    time.sleep(3)
    arm.move_arm(0,-0.376, 0.621) #back to to spot before loading
    time.sleep(3)
    arm.home()

'''
can_load()
Purpose: The purpose of this function is load a can into the hopper
Parameters: Take a numeric value for which spot on the hopper to load on
Picks up the can from the table and loads it
Return: None=
'''
def can_load(spot_num):
    time.sleep(3)
    arm.move_arm(0.64,0,0.23) #pickup position
    time.sleep(3)
    arm.control_gripper(40)
    time.sleep(3)
    arm.move_arm(0.012,-0.376, 0.621) #spot before loading
    time.sleep(3)
    if spot_num==1:
        arm.move_arm(0.012,-0.621,0.562) #1st load spot
        time.sleep(3)
    elif spot_num==2:
        arm.move_arm(0.012,-0.521,0.498) #2nd load spot
        time.sleep(3)
    elif spot_num==3:
        arm.move_arm(0.012,-0.462,0.478) #3rd load spot
        time.sleep(3)
    arm.control_gripper(-40)
    time.sleep(3)
    arm.move_arm(0,-0.376, 0.621) #back to to spot before loading
    time.sleep(3)
    arm.home()

'''
load_container()
Purpose: The purpose of this function is load a container into the hopper consideirng the conditions
Parameter: None
Utilizes other functions: can_load, bottle_load and dispense_container
Conditons: 
The hopper can have only 3 containers, all the contianer in the hopper must go the same bin and the 
total mass of the containers on the hopper cannot exceed 90 grams.
Return: previous container's bin value and boolean for whether there's a container dispensed or not
'''
def load_container():
    global container
    global mass_binlist
    global bin_value
    global no_container
    p_bin=0 #value for previous container
    total_weight=0
    num_container=0 #to keep count of how many containers get loaded
    counter=True

    #while loop for loop control
    while counter==True: 
        #if statements to dispense container and store boolean value that keeps track of it
        if no_container:
        
            dispense_container()
            no_container = False

        #stores total mass of the conatiners being loaded     
        total_weight += mass_binlist[container][1] 
        #nested if for container going to bin 1
        if bin_value==1:
            #if stament for the 1st container
            if num_container==0:
                can_load(1)
                p_bin=bin_value
                num_container+=1
                no_container = True
            #if stament for the 2nd container
            elif num_container==1:
                #if statment to check if it passes the conditons
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    can_load(2)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            #if stament for the 3rd container
            elif num_container==2:
                #if statment to check if it passes the conditons
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    can_load(3)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container == 3:
                counter = False

        #nested if for container going to bin 2        
        elif bin_value==2:
            if num_container==0:
                bottle_load(1)
                p_bin=bin_value
                num_container+=1
                no_container = True

            elif num_container==1:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(2)
                    p_bin=bin_value
                    num_container = num_container +1
                    no_container = True
        

            elif num_container==2:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(3)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container == 3:
                counter = False

        #nested if for container going to bin 3
        elif bin_value==3:
            if num_container==0:
                bottle_load(1)
                p_bin=bin_value
                num_container+=1
                no_container = True
            elif num_container==1:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(2)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container==2:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(3)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container == 3:
                counter = False

        #nested if for container going to bin 4
        elif bin_value==4:
            if num_container==0:
                bottle_load(1)
                p_bin=bin_value
                num_container+=1
                no_container = True
            elif num_container==1:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(2)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container==2:
                if total_weight>90 or p_bin!=bin_value:
                    counter=False
                else:
                    bottle_load(3)
                    p_bin=bin_value
                    num_container+=1
                    no_container = True
            elif num_container == 3:
                counter = False         
    
    return p_bin, no_container


'''
drive_Qbot()
Purpose: The purpose of this function is to make the q-bot drive and stay on the track
Parameters: None
Utilizes line following sensor to make the q bot drive on track
Return: None
'''
def drive_Qbot():

    line_reading = bot.line_following_sensors()

    if line_reading == [1, 1]:
        bot.set_wheel_speed([0.1,0.1])

    #if it is no longer on the track, it will turn back onto it
    if line_reading == [1, 0]:
        while line_reading == [1, 0]:
            bot.set_wheel_speed([0,0.1])
            line_reading = bot.line_following_sensors()

        bot.set_wheel_speed([0.1,0.1])

    if line_reading == [0, 1]:
        while line_reading == [0, 1]:
            bot.set_wheel_speed([0.1,0])
            line_reading = bot.line_following_sensors()

        bot.set_wheel_speed([0.1,0.1])

    return None

'''
transfer_container()
Purpose: The purpose of this function is to drive and stop at the correct bin to deposit the containers
Parameters: Takes a numeric value for which bin to go to
Utilizes color, ultrasonic sensor and drive_Qbot function to go to respective bin for drop off
Return: None
'''   
def transfer_container(bin_num):
    global mass_binlist
    global container
    global bin1_color
    global bin2_color
    global bin3_color
    global bin4_color

    bin = bin_num
    #creates a variable that containes the colour values of the bin
    if bin == 1:
        colour_of_bin = bin1_color
    elif bin == 2:
        colour_of_bin = bin2_color
    elif bin == 3:
        colour_of_bin = bin3_color
    else:
        colour_of_bin = bin4_color

    #stores whether the bot has unloaded or not
    colour_sensing = True

    bot.activate_color_sensor()
    bot.activate_line_following_sensor()

    #this will run until the correct bin has been sensed
    while colour_sensing:

        drive_Qbot()

        current_colour_reading = bot.read_color_sensor()

        #when the colour sensor determines it has become in range of the bin
        if current_colour_reading[0] == colour_of_bin:
            bot.deactivate_color_sensor()
            bot.activate_ultrasonic_sensor()
            colour_sensing = False
            ultrasonic_sensing = True

    #this will run until recyclables are ready to be dumped
    while ultrasonic_sensing:

        drive_Qbot()

        current_distance = bot.read_ultrasonic_sensor()

        #when the bot has reached the dropoff point
        if 0 < current_distance < 0.09:
            time.sleep(1)
            bot.stop()
            ultrasonic_sensing = False

    bot.deactivate_line_following_sensor()
    bot.deactivate_ultrasonic_sensor()
    return None

'''
deposit_container()
Purpose: The purpose of this function is to deposit the container into the bin 
Parameters: None
Utilizes rotatory motor to deposit the contianers into the bin
Return: None
'''   
def deposit_container():
    time.sleep(1)
    bot.activate_stepper_motor()
    time.sleep(2)

    i = 0
    angle = 10
    #while loop to slow down the process of deposit
    while i < 8:
        bot.rotate_hopper(angle)
        angle += 10
        i += 1

    time.sleep(2)
    bot.rotate_hopper(0)
    time.sleep(1)
    bot.deactivate_stepper_motor()

    return None

'''
return_home()
Purpose: The purpose of this function is to return the Qbot back to its home positon after depositing the contianers
Parameters: None
Utilizes line following sensors and global variable intial_positon to get it back to original spot within a margin of error
Return: None
''' 
def return_home():
    #this is separating the x and y values of the original position
    global initial_position
    initial_position_x = initial_position[0]
    initial_position_y = initial_position[1]

    bot.activate_line_following_sensor()
    current_position = bot.position()

    #this loop will run as long as the position is not within a margin of error of 0.05 of original position
    while not (((initial_position_x - 0.05) < current_position[0] < (initial_position_x + 0.05)) and ((initial_position_y - 0.05) < current_position[1] < (initial_position_y + 0.05))):

        drive_Qbot()
        current_position = bot.position()

    bot.deactivate_line_following_sensor()
    bot.stop()

    return None

'''
main()
Purpose: The purpose of this function is put all the fucntions togther and run it
Parameters: None
Utilizes functions: load_container, transfer_container, deposit_container and return_home
Return: None
''' 
def main():
    global no_container
    #while loop to run all the functions while updating values for each trial
    while True:
        p_bin_value, no_container= load_container()
        transfer_container(p_bin_value)
        deposit_container()
        return_home()
    return None

#calling the main function
main()



    

    

