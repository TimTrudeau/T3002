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
import tkinter.ttk as ttk
from tkinter.constants import *
from SRC.robot_serial_port import serial_port_manager
from SRC.gdfile_dialog import FileDialog
import Page_GUI.pdrobot as pdrobot
import SRC.gcode_maker as gm
from interpreter import Interpreter, Lexer
_debug = False  # False to eliminate debug printing from callback functions.

global win, robbie, robotPort
win = robbie = None


def main(top_win=None):
    """Main entry point for the application."""
    global robbie
    robbie = gm.GCodeMaker()
    if top_win is None:
        global root
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)
        # Creates a toplevel widget.
        global _top1, win
        _top1 = root
        win = pdrobot.Toplevel1(_top1)
        with serial_port_manager() as manager:
            gm.GCodeMaker.serialport = manager
            root.mainloop()
    else:
        win = top_win


def cb_buttonHome(*args):
    global robbie
    if _debug:
        print('pdrobot_support.cb_buttonHome')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    # For now go_home homes both axis
    # if args[0] == 'LIN':
    #     win.absolutePos.set(0)
    # if args[0] == 'ROT':
    #     win.absoluteRot.set(0)
    win.absolutePos.set(0)
    win.absoluteRot.set(0)
    robbie.go_home()


def cb_buttonLin(*args):
    global robbie
    if _debug:
        print('pdrobot_support.cb_buttonLin')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    val = win.absolutePos.get()
    speed = win.speedLin.get()
    val = 0 if val == "" else int(val)
    val += args[0]
    win.absolutePos.set(str(val))
    robbie.move_lin(val, speed=speed)

def cb_buttonRot(*args):
    global robbie
    if _debug:
        print('pdrobot_support.cb_buttonRot')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    val = win.absoluteRot.get()
    speed = win.speedRot.get()
    val = 0 if val == "" else int(val)
    val += args[0]
    win.absoluteRot.set(str(val))
    robbie.move_rot(val, speed=speed)


def cb_cancel_file(*args):
    if _debug:
        print('pdrobot_support.cb_cancel_file')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()


def cb_getFile(*args):
    if _debug:
        print('pdrobot_support.cb_openFile')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    pd_file = FileDialog()  #  Opens a file dialog picker
    win.filepath = pd_file.get_file_dialog()

def cb_open_program(*args):
    if _debug:
        print('pdrobot_support.cb_open_program')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    try:
        with open(win.filepath, 'r') as _filepath:
            win.pd_source = _filepath.readlines()
    except (FileExistsError, FileNotFoundError,):
        pd_file = FileDialog()
        win.filepath = pd_file.get_file_dialog()
        with open(win.filepath, 'r') as _filepath:
            win.pd_source = _filepath.readlines()


def cb_run_program(*args):
    if _debug:
        print('pdrobot_support.cb_run_program')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    try:
        lexer = Lexer(win.pd_source)
        parser = Parser(lexer)
        with open(options.out, 'w') as outfile:
            interpreter = Interpreter(parser, port, outfile)
            interpreter.interpret()
    except Exception as ex:
        print(f'{ex}')
        if "yield" in ex.args[0]:
            with open(options.out, 'w') as outfile:
                interpreter = Interpreter(parser, None, outfile)
                interpreter.interpret()

def cb_scaleLinSpeed(*args):
    if _debug:
        print('pdrobot_support.cb_scaleLinSpeed')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    speed = float(args[0])
    win.speedLin.set(speed)

def cb_scaleRotSpeed(*args):
    if _debug:
        print('pdrobot_support.cb_scaleRotSpeed')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    speed = float(args[0])
    win.speedRot.set(speed)


def cb_step_program(*args):
    if _debug:
        print('pdrobot_support.cb_step_program')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    try:
        pass
    except ValueError:
        pass



def cb_stop(*args):
    if _debug:
        print('pdrobot_support.cb_stop')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    robbie.stop()


def cb_go(*args):
    if _debug:
        print('pdrobot_support.cb_go')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    try:
        val = args[1].get()
        win.absolutePos.set(val)
        robbie.move_lin(int(val), )
        val = args[2].get()
        win.absoluteRot.set(val)
        robbie.move_rot(int(val))
    except ValueError:
        pass

def cb_waypoint(*args):
    if _debug:
        print('pdrobot_support.cb_waypoint')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    pos = win.absolutePos.get()
    rot = win.absoluteRot.get()
    if args[0] == 1 and not win.set1_locked.get():
        win.set1_pos.set(pos)
        win.set1_rot.set(rot)
    elif args[0] == 2:
        win.set2_pos.set(pos)
        win.set2_rot.set(rot)
    elif args[0] == 3:
        win.set3_pos.set(pos)
        win.set3_rot.set(rot)
    elif args[0] == 4:
        win.set4_pos.set(pos)
        win.set4_rot.set(rot)


if __name__ == '__main__':
    pdrobot.start_up()
