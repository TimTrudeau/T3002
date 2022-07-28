import dearpygui.dearpygui as dpg
from gcode_maker import GCodeMaker, open_serial_port
from main import main

# Rail length = 300 mm
dpg.create_context()
# with dpg.value_registry():
#     dpg.add_string_value(default_value="Default string", tag="string_value")

def button_save(sender, app_data, user_data):
    print(f"save sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def button_load(sender, app_data, user_data):
    print(f"load sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    dpg.set_value('string_value_file_name', app_data.get('file_path_name'))
    fn = dpg.get_value('string_value_file_name')
    print(f'newfilename={fn}')

def run_program_1(sender, app_data, user_data):
    print(f"run sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    prog_file = dpg.get_value('string_value_file_name')
    print(f'my file {prog_file}')
    if prog_file is not None:
        main(f"-f{prog_file}")

def button_stop(sender, app_data, user_data):
    print(f"stop sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.stop()

def go_home(sender, app_data, user_data):
    print(f"home sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.move_lin(-45, relative=True, speed=100)
    gcm.go_home()

def sets_zero(sender, app_data, user_data):
    print(f"home sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.set_zero()

def button_move_linear(sender, app_data, user_data):
    print(f"move lin sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def button_move_forward(sender, app_data, user_data):
    print(f"move forware sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def button_move_backward(sender, app_data, user_data):
    print(f"move backward sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def button_rotate_l(sender, app_data, user_data):
    print(f"rotate left sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def button_rotate_r(sender, app_data, user_data):
    print(f"rotate right sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def linear_move_to():
    linear_value = dpg.get_value(linear_location)
    speed_value = dpg.get_value(speed)
    print(f"linear_move location is: {linear_value}")
    print(f"Speed: {speed_value}")
    gcm.move_lin(linear_value, speed=speed_value)

def rotation():
    rotation_value = dpg.get_value(rotation_location)
    speed_value = dpg.get_value(speed)
    print(f"rotation location is: {rotation_value}")
    print(f"Speed: {speed_value}")
    gcm.move_rot(rotation_value, speed=speed_value)

def gcode_send():
    cmd =  dpg.get_value(gcode_input).upper()
    print(f"GCODE cmd is: {cmd}")
    gcm.send(cmd)

def report_pos(homed):
    pos = gcm.get_position()
    print(pos)
    dpg.set_value(pos_text, pos)

def set_waypoint1(sender, app_data, user_data):
    print(f"Waypoint1 set")
    gcm.set_absolute()
    #gcm.send("G1 F")

def go_waypoint1(sender, app_data, user_data):
    print(f"Move to Waypoint1")
    speed_value = 100
    gcm.move_lin(180,speed=speed_value)
    gcm.move_rot(180,speed=speed_value)

def go_waypoint2(sender, app_data, user_data):
    print(f"Move to Waypoint2")
    speed_value = dpg.get_value(speed)
    gcm.move_lin(15, relative=True, speed=speed_value)

def go_waypoint3(sender, app_data, user_data):
    print(f"Move to Waypoint3")
    speed_value = dpg.get_value(speed)
    gcm.move_lin(30, relative=True, speed=speed_value)
    gcm.wait(.02)
    gcm.move_rot(0, relative=False, speed=speed_value)
    gcm.move_rot(180, relative=False, speed=speed_value)
    gcm.wait(.02)
    gcm.move_lin(-30, relative=True, speed=speed_value)

def go_waypoint4(sender, app_data, user_data):
    print(f"Move to Waypoint4")
    speed_value = dpg.get_value(speed)
    gcm.move_rot(0, relative=False, speed=speed_value)

def go_waypoint5(sender, app_data, user_data):
    print(f"Move to Waypoint5")
    speed_value = dpg.get_value(speed)
    gcm.move_rot(180, relative=False, speed=speed_value)
    gcm.wait(.2)
    gcm.move_lin(-30, relative=True, speed=speed_value)

#------------------END CALL BACKS ----------------------------------
homed = False
with dpg.value_registry():
    dpg.add_string_value(default_value=None, tag='string_value_file_name')

# file dialog
with dpg.file_dialog(label="File Dialog", width=600, height=400, show=False, callback=button_load, tag="file_dialog_tag"):
    dpg.add_file_extension("Program files(.nps){.nps}", color=(255, 0, 0, 255), custom_text="[robot]")
    dpg.add_file_extension("Python(.py){.py}", color=(0, 255, 0, 255))

# Main screen
with dpg.window(label="Robot", width = 900, height = 800):
    dpg.add_group(label="hori", horizontal=True)
    dpg.add_input_text(label = "Name", default_value= "NPD Robot Interface")
    # dpg.add_button(label="Load", callback=button_load, user_data="Some Data")
    # dpg.add_same_line()
    # dpg.add_button(label="Save", callback=button_save, user_data="Some Data")
    dpg.add_button(label="Load Program",
                   callback=lambda: dpg.show_item("file_dialog_tag"),
                   user_data=dpg.last_container(),
                   width = 100, height = 50)
    dpg.add_same_line()
    dpg.add_button(label="STOP", callback=button_stop, user_data="STOP", width = 100, height = 50)
    dpg.add_button(label="Home", callback=go_home, user_data="Home", width = 60, height = 50)
    dpg.add_button(label="Set Zero", callback=sets_zero, user_data="Set Zero")
    dpg.add_button(label="Run Program 1", callback=run_program_1, user_data="Run Program 1", width=150, height=75)
    dpg.add_input_int(label="cycles")

    speed = dpg.add_slider_int(label = "Speed (%)", default_value = 50, min_value= 1, max_value = 100)

    # Move the key to a specific location
    linear_location = dpg.add_slider_int(min_value = 0, max_value = 325)
    dpg.add_same_line()
    dpg.add_button(label="Move to", callback=linear_move_to)

    rotation_location = dpg.add_slider_int(default_value=0, min_value= -180, max_value=180)
    dpg.add_same_line()
    dpg.add_button(label="Rotate to", callback=rotation)

    gcode_input = dpg.add_input_text(label="GCODE", default_value= "")
    dpg.add_same_line()
    dpg.add_button(label="Send", callback=gcode_send)
    dpg.add_button(label="Position", callback=report_pos, width = 120, height = 20)
    dpg.add_same_line()
    pos_text = dpg.add_input_text(width = 140, height = 20)

    #dpg.add_button(label="Set Waypoint 1", callback=set_waypoint1, user_data="wp1", width = 120, height = 20)
    dpg.add_button(label="SetUp", callback=go_waypoint1, user_data="wp1", width = 120, height = 20)
    #dpg.add_button(label="Set Waypoint 2", callback=set_waypoint1, user_data="wp2", width = 120, height = 20)
    dpg.add_button(label="Poise", callback=go_waypoint2, user_data="wp2", width = 120, height = 20)
    #dpg.add_button(label="Set Waypoint 3", callback=set_waypoint1, user_data="wp3", width = 120, height = 20)
    dpg.add_button(label="Insert", callback=go_waypoint3, user_data="wp3", width = 120, height = 20)
    #dpg.add_button(label="Set Waypoint 4", callback=set_waypoint1, user_data="wp4", width = 120, height = 20)
    dpg.add_button(label="Rotate", callback=go_waypoint4, user_data="wp4", width = 120, height = 20)
    dpg.add_button(label="Return", callback=go_waypoint5, user_data="wp5", width = 120, height = 20)

dpg.create_viewport(title='Robot Programmer', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
with open_serial_port('COM8', outfile=None) as sport:
    gcm = GCodeMaker(sport, None)
    dpg.start_dearpygui()
    dpg.destroy_context()