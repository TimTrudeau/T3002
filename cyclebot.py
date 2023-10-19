"""

"""

import os
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

import src.Page_GUI.pdrobot_support

if __name__ == '__main__':
    src.Page_GUI.pdrobot_support.main()
