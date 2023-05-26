
import gcode
from gcode import _gcodes
from robot_serial_port import serial_port_manager, serialscan

usable_gpio = [0, 3, 4, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26]
linlimit_io = 5
rotatlimit_io = 6

try:
    import gpiozero as gpio
except Exception as e:
    print(f"No Pi GPIO {e}")
    print(f"GPIO UNAVAILABLE {e}")
    raise ImportError


class GCodeMaker:
    serialport = None

    def __init__(self, outfile='junk.txt'):
        serialscan()
        self.linear_limit = gcode.linlimit
        self.rotation_limit = gcode.rotatlimit
        self.outfile = outfile

    def send(self, command):
        print(command)
        try:
            cmd = command + '\n'
            GCodeMaker.serialport.write(cmd.encode())
            response = bytes('', 'utf-8')
            # time.sleep(.1)
            while 'ok' not in str(response):
                response += GCodeMaker.serialport.readline()
            response = response.decode('utf-8')
            return response

        except AttributeError as ex:
            response = '!!!'
            print(f'{command} {response}')
        if self.outfile is not None:
            self.outfile.write(f'{command} ')
            self.outfile.write(f'{response}\n')
            self.outfile.flush()

    def motorspeed(self, value, axis):
        if axis == 'X':
            flow = gcode.flow.get('linMaxFlow')
            speed = min(gcode.flow.get('linMaxFlow'), flow * (value /100))
        else:
            flow = gcode.flow.get('rotMaxFlow')
            speed = min(gcode.flow.get('rotMaxFlow'), flow * (value / 100))
        return float(speed)

    def go_home(self):
        self.send('M92 X700')
        self.send(_gcodes.get(gcode.HOME))
        self.send('M92 X1670')

    def stop(self):
        self.send(_gcodes.get(gcode.STOP))

    def set_absolute(self):
        self.relative_mode = False
        self.send(_gcodes.get(gcode.ABSOLUTE))


    def set_relative(self):
        self.relative_mode = True
        self.send(_gcodes.get(gcode.RELATIVE))

    def move_lin(self, value, relative=False, speed=10):
        sendstr = "{0}F{1:5.3f} X{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'X'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def move_rot(self, value, relative=False, speed=10):
        sendstr = "{0}F{1:5.3f} Y{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'Y'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def wait(self, value):
        sendstr = "{0}S{1:5.3f}".format(_gcodes.get(gcode.WAIT), value)
        self.send(sendstr)

    def set_zero(self):
        sendstr = "{0}".format(_gcodes.get(gcode.SETZERO))
        self.send(sendstr)

    def get_position(self):
        sendstr = "{0}".format(_gcodes.get(gcode.GET_POS))
        pos_ =  self.send(sendstr)
        index_ = pos_.index('Z')
        print(f"MY INDEX {index_}")
        return pos_[:index_]
