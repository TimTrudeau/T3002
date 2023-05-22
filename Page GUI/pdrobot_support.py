#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#    May 19, 2023 04:39:12 PM EDT  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import pdrobot

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = pdrobot.Toplevel1(_top1)
    root.mainloop()

def cb_buttonHome(*args):
    if _debug:
        print('pdrobot_support.cb_buttonHome')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    if args[0] == 'LIN':
        _w1.absolutePos.set(0)
    if args[0] == 'ROT':
        _w1.absoluteRot.set(0)

def cb_buttonLin(*args):
    if _debug:
        print('pdrobot_support.cb_buttonLin')
        for arg in args:
            print('    another arg:', arg)
        sys.stdout.flush()
    val = _w1.absolutePos.get()
    val = 0 if val == "" else int(val)
    _w1.absolutePos.set(str(val + args[0]))


def cb_buttonRot(*args):
    if _debug:
        print('pdrobot_support.cb_buttonRot')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    val = _w1.absoluteRot.get()
    val = 0 if val == "" else int(val)
    _w1.absoluteRot.set(val + args[0])


def cb_cancel_file(*args):
    if _debug:
        print('pdrobot_support.cb_cancel_file')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_openFile(*args):
    if _debug:
        print('pdrobot_support.cb_openFile')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_run_program(*args):
    if _debug:
        print('pdrobot_support.cb_run_program')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_scaleLinSpeed(*args):
    if _debug:
        print('pdrobot_support.cb_scaleLinSpeed')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_scaleRotSpeed(*args):
    if _debug:
        print('pdrobot_support.cb_scaleRotSpeed')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_step_program(*args):
    if _debug:
        print('pdrobot_support.cb_step_program')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_stop(*args):
    if _debug:
        print('pdrobot_support.cb_stop')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

def cb_go(*args):
    if _debug:
        print('pdrobot_support.cb_go')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    val = args[1].get()
    _w1.absolutePos.set(val)
    val = args[2].get()
    _w1.absoluteRot.set(val)

def cb_waypoint(*args):
    if _debug:
        print('pdrobot_support.cb_waypoint')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    if args[0] == 1:
        _w1.set1_pos.set(_w1.absolutePos.get())
        _w1.set1_rot.set(_w1.absoluteRot.get())
    elif args[0] == 2:
        _w1.set2_pos.set(_w1.absolutePos.get())
        _w1.set2_rot.set(_w1.absoluteRot.get())
    elif args[0] == 3:
        _w1.set3_pos.set(_w1.absolutePos.get())
        _w1.set3_rot.set(_w1.absoluteRot.get())
    elif args[0] == 4:
        _w1.set4_pos.set(_w1.absolutePos.get())
        _w1.set4_rot.set(_w1.absoluteRot.get())

if __name__ == '__main__':
    pdrobot.start_up()