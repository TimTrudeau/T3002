"""
#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#    May 19, 2023 04:39:12 PM EDT  platform: Windows NT
"""
import sys
import tkinter as tk
import src.Page_GUI.pdrobot as pdrobot
from src.gdfile_dialog import FileDialog
from src.interpreter.interpreter import Interpreter
from src.interpreter.parser import Parser
from pathlib import Path
from src.gcode_maker import GCodeMaker

_debug = False  # False to eliminate debug printing from callback functions.
system_packages = set(sys.modules.keys())

# GLOBALS
gm = None
top_win = None

def main(toplevel: object = None):
    """Main entry point for the application.
    toplevel is None unless this is called by test routine
    """
    global top_win, root, gm
    if toplevel is None:
        try:
            root = tk.Tk()
            root.protocol('WM_DELETE_WINDOW', root.destroy)
            top_win = pdrobot.Toplevel1(root)
            gm = GCodeMaker()
            # Creates a toplevel widget
            root.mainloop()
        finally:
            gm.serialport.close()
    else:
        # toplevel provided by test
        top_win = toplevel
        gm.serialport.close()


def cb_buttonHome(*args):
    # For now go_home homes both axis
    # if args[0] == 'LIN':
    #     top_win.absolutePos.set(0)
    # if args[0] == 'ROT':
    #     top_win.absoluteRot.set(0)
    top_win.absolutePos.set(0)
    top_win.absoluteRot.set(0)
    gm.go_home()


def cb_buttonLin(*args):
    global top_win
    position = float(args[0])
    val = top_win.absolutePos.get()
    speed = top_win.speedLin.get()
    val = 0.0 if val == "" else float(val)
    val += position
    top_win.absolutePos.set(str(f'{val:3.2f}'))
    gm.move_lin(position, speed=speed, relative=True)


def cb_buttonRot(*args):
    global top_win
    rotation = float(args[0])
    val = top_win.absoluteRot.get()
    speed = top_win.speedRot.get()
    val = 0.0 if val == "" else float(val)
    val += rotation
    top_win.absoluteRot.set(f'{val:3.2f}')
    gm.move_rot(rotation, speed=speed, relative=True)


def cb_scaleLinSpeed(*args):
    global top_win
    speed = float(args[0])
    print(f'lin speed {speed} {args}')
    top_win.speedLin.set(speed)


def cb_scaleRotSpeed(*args):
    global top_win
    speed = float(args[0])
    print(f'rot speed {speed} {args}')
    top_win.speedRot.set(speed)


def cb_stop(*args):
     gm.stop()
     top_win.halt = True


def cb_go(*args):
    global top_win
    try:
        pos = args[1].get()
        rot = args[2].get()
        top_win.absolutePos.set(pos)
        top_win.absoluteRot.set(rot)
        flow = top_win.speedRot.get()
        gm.move_both(float(pos), float(rot), flow)


    except ValueError as e:
        print(f'Error in cb_go: {e}')
        pass

def cb_toggle_wp_set(*args):
    if args[0].get() == 0:
        args[1].foreground = '#777777'
        print(f' waypoint state 777 ')
    else:
        args[1].foreground = '#000'
        print(f' waypoint state 000')

def cb_waypoint(*args):
    global top_win
    pos = top_win.absolutePos.get()
    rot = top_win.absoluteRot.get()
    if args[0] == 1 and not top_win.set1_locked.get():
        top_win.set1_pos.set(pos)
        top_win.set1_rot.set(rot)
    elif args[0] == 2 and not top_win.set2_locked.get():
        top_win.set2_pos.set(pos)
        top_win.set2_rot.set(rot)
    elif args[0] == 3 and not top_win.set3_locked.get():
        top_win.set3_pos.set(pos)
        top_win.set3_rot.set(rot)
    elif args[0] == 4 and not top_win.set4_locked.get():
        top_win.set4_pos.set(pos)
        top_win.set4_rot.set(rot)


def cb_serial_port_reset(*args):
    gm.serial_port_reset()


def cb_cancel_file(*args):
    global top_win
    gm.serialport.reset_output_buffer()
    top_win.halt = True
    top_win.dg_filename.set("")
    top_win.gcode_list_var.set("")
    top_win.ButtonRunProg.configure(state='disabled')
    top_win.ButtonStepProg.configure(state='disabled')
    top_win.ButtonEditProg.configure(state='disabled')


def cb_getSourceFile(*args):
    global top_win
    _listbox = args[0]
    _pd_file = FileDialog()  # Opens a file dialog picker
    top_win.source_file = Path(_pd_file.get_file_dialog())
    if top_win.source_file.suffix == '.gcode':
        target_file = str(top_win.source_file)
    else:
        top_win.gcode_file = str(top_win.source_file.with_suffix('.gcode'))
        top_win.dg_filename.set(str(top_win.source_file.name))  # Put file name in file widgit
        _source = top_win.source_file.read_text(encoding='utf-8')  # reads entire file
        parser = Parser(_source)
        interp = Interpreter(parser, outfile=top_win.gcode_file)
        interp.interpret()
        if not interp.gcode.outfile.closed:
            interp.gcode.outfile.close()
        target_file = interp.gcode.gcode_path
    with open(target_file, 'r') as fp:
        text = fp.readlines()
        results = list(enumerate(text))
    for index, item in results:
        _listbox.insert(index, item)
    _listbox.selection_set(0)
    top_win.ButtonRunProg.configure(state='active')
    top_win.ButtonStepProg.configure(state='active')
    top_win.ButtonEditProg.configure(state='active')


def cb_run_program(*args):
    top_win.halt = False
    #  gm.run_gcode(top_win.gcode_file)
    listbox = args[0]
    gcode = listbox.get(0)
#    root.after(500, lambda: runnext(listbox))  // 500ms skews delays
    root.after(50, lambda: runnext(listbox))

def cb_step_program(*args):
    try:
        _listbox = args[0]
        index = _listbox.curselection()[0]
        _listbox.selection_clear(index)
        gcode = _listbox.get(index).strip('\n')
        gm.send(gcode)
        index += 1
        _listbox.selection_set(index)
        _listbox.see(index)
        return 1
    except IndexError:
        _listbox.selection_set(0)
        return 0

def cb_edit_program(*arg):
    import subprocess
    import platform
    global top_win
    if platform.system() == "Windows":
        app_name = "notepad.exe "
    else:
        app_name = "geany "
    try:
        app_name += str(top_win.source_file)
        subprocess.Popen(app_name.split())
    except Exception as e:
        print(f'File editor failed to open: {e}')

def runnext(_listbox: object):
    if top_win.halt is True:
        return
    if cb_step_program(_listbox):
        root.after(50, lambda: runnext(_listbox))


def cb_exit_program(*args):
    print(f'Exiting cyclebot')
    root.destroy()



if __name__ == '__main__':
    pdrobot.start_up()
