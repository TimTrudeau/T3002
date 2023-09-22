
import src.gcode as gcode
from src.gcode import _gcodes
# from robot_serial_port import serial_port_manager
import src.robot_serial_port as robot_serial_port

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

    def __init__(self, port: str = None, path: str = None, run: bool = True):
        """ The serial port and/or the output file name can be passed
        in from the command line with the call to the Interpreter module.
        """
        self.run = run
        if GCodeMaker.serialport is None:
            GCodeMaker.serialport = robot_serial_port.serial_port_manager(port)
            GCodeMaker.serialport.timeout = 1
            print(f'GCodeMaker serial port {GCodeMaker.serialport} type {type(GCodeMaker.serialport)}\n')
        self.linear_limit = gcode.linlimit
        self.rotation_limit = gcode.rotatlimit
        if path is None:
            path = 'tmp.gcode'
        self.gcode_path = path
        self.outfile = open(self.gcode_path, 'w')
        self.send(f'M92 X{gcode.linsteps_per_mm} Y{gcode.rotsteps_per_degree}')
        self.send('M503')



    def run_gcode(self, path: str):
        """Read in GCODE file and send to serial port.
        --Called from either main or from GUI--.
        """
        try:
            if path is None:
                return
            with open(path, 'r') as fp:
                self.gcode = fp.readlines()
            for line in self.gcode:
                GCodeMaker.serialport.write(bytes(line, 'utf-8'))
                while GCodeMaker.serialport.readline().decode().strip() != 'ok':
                    pass # Serial port will time_out if nothing returned.
                pass
        except FileExistsError as ex:
            raise Exception(f'Run GCODE {ex}')

    def close_outfile(self):
        print(f'close_outfile {self.gcode_path} type {type(self.gcode_path)}\n')
        self.outfile.close()

    def send(self, command: str):
        """ Send Interpreted commands to Output GCODE file.
        """
        print(f'Command={command}')
        cmd = command + '\n'
        try:
            if self.run:
                GCodeMaker.serialport.write(bytes(cmd, 'utf-8'))
                reply = ''
                while reply != 'ok':
                    reply = GCodeMaker.serialport.readline().decode().strip()
                    print(f'{reply}')
        except Exception as ex:
            print(f'exception from serialport write {ex}')

        try:
            self.outfile.write(cmd)
        except (FileExistsError, AttributeError,) as ex:
            raise Exception(f'send to outfile {ex}')

    def motorspeed(self, value: float, axis: str):
        if axis == 'X':
            flow = gcode.flow.get('linMaxFlow')
            speed = min(flow, flow * (value / 100))
        else:
            flow = gcode.flow.get('rotMaxFlow')
            speed = min(flow, flow * (value / 100))
        return float(speed)

    def go_home(self):
        self.send(_gcodes.get(gcode.HOME))

    def stop(self):
        self.send(_gcodes.get(gcode.STOP))

    def set_absolute(self):
        self.relative_mode = False
        self.send(_gcodes.get(gcode.ABSOLUTE))

    def set_relative(self):
        self.relative_mode = True
        self.send(_gcodes.get(gcode.RELATIVE))

    def move_lin(self, value: float, speed: int = 10, relative: bool = False):
        sendstr = "{0}F{1:5.3f} X{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'X'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def move_rot(self, value: float, speed: int = 10, relative: bool = False):
        sendstr = "{0}F{1:5.3f} Y{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'Y'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def wait(self, value: float):
        sendstr = "{0}S{1:5.3f}".format(_gcodes.get(gcode.WAIT), value)
        self.send(sendstr)

    def set_zero(self):
        sendstr = "{0}".format(_gcodes.get(gcode.SETZERO))
        self.send(sendstr)

    def get_position(self):
        sendstr = "{0}".format(_gcodes.get(gcode.GET_POS))
        pos_ = self.send(sendstr)
        index_ = pos_.index('Z')
        print(f"MY INDEX {index_}")
        return pos_[:index_]
