""" Opens a file directory tree and returns a file path.
Supports file types.

# filename == 'path/to/myfilename.txt' if you type 'myfilename'
# filename == 'path/to/myfilename.abc' if you type 'myfilename.abc'
"""

import tkinter as tk
from tkinter import filedialog

class FileDialog:
    def __init__(self):
        self.filetypes = \
            (('PDRobot Source files', '*.pdp'),
             ('Text files', '*.TXT'),
             ('Gcode files', '*.gcode'),
             ('All files', '*.*'),
             )
        self.root = tk.Tk()


    def get_file_dialog(self):
        # open-file dialog
        filename = tk.filedialog.askopenfilename(
            title='Select a file...',
            filetypes=self.filetypes,
        )
        self.root.destroy()
        return filename

    def save_as_file_dialog(self):
        # save-as dialog
        filename = tk.filedialog.asksaveasfilename(
            title='Save as...',
            filetypes=self.filetypes,
            defaultextension='.txt'
        )
        self.root.destroy()
        return filename
