"""

"""

import os
"""
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 'src')
)
sys.path.insert(1, PROJECT_ROOT)
"""
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=22, stdoutToServer=True, stderrToServer=True)
print("SCOOBY DOOBY DOO")
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

import src.Page_GUI.pdrobot_support

if __name__ == '__main__':
    src.Page_GUI.pdrobot_support.main()
