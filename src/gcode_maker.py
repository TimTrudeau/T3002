import os
import src.gcode as gcode
from src.gcode import _gcodes
import src.robot_serial_port as robot_serial_port
from serial.serialutil import SerialTimeoutException, SerialException
import src.Page_GUI.pdrobot_support as pdrobot_support

usable_gpio = [0, 3, 4, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26]
linlimit_io = 5
rotatlimit_io = 6

try:
    import gpiozero as gpio
except Exception as e:
    print(f"No Pi GPIO {e}")
    print(f"GPIO UNAVAILABLE {e}")
    if os.name == 'posix':
        raise ImportError


class GCodeMaker:
    serialport = None

    def __init__(self, port: str = None, path: str = None, run: bool = True):
        """ The serial port and/or the output file name can be passed
        in from the command line with the call to the Interpreter module.
        """
        self.run = run
        self.serial_port_reset(port)
        print(f'GCODEMAKER SERIAL PORT: {GCodeMaker.serialport} \n type {type(GCodeMaker.serialport)}\n')
        self.linear_limit = gcode.linlimit
        self.rotation_limit = gcode.rotatlimit
        if path is None:
            path = 'tmp.gcode'
        self.gcode_path = path
        self.outfile = open(self.gcode_path, 'w')
        self.send(f'M92 X{gcode.linsteps_per_mm} Y{gcode.rotsteps_per_degree}')
        self.send('M503')



    def run_gcode(self, path: str) -> None:
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
                reply = GCodeMaker.serialport.readline().decode().strip()
                if not reply:
                    raise SerialTimeoutException("Serial Port Timed out during ")

        except (FileExistsError, SerialTimeoutException) as ex:
            raise Exception(f'Run GCODE {ex}')

    def close_outfile(self) -> None:
        print(f'close_outfile {self.gcode_path} type {type(self.gcode_path)}\n')
        self.outfile.close()

    def send(self, command: str) -> str:
        """ Send Interpreted commands to Output GCODE file.
        """
        print(f'Command===={command}')
        cmd = command + '\n'
        try:
            if self.run:
                GCodeMaker.serialport.write(bytes(cmd, 'utf-8'))
                reply = GCodeMaker.serialport.readline().decode().strip()
                print(f'SERIAL PORT REPLY >>{reply}<<')
                if not reply:
                    raise SerialException
        except (SerialException, PermissionError) as ex:
            print(f'WRITE EXCEPTION FROM SERIALPORT: {ex}')
            self.serial_port_reset()
        try:
            self.outfile.write(cmd)
        except (FileExistsError, AttributeError,) as ex:
            raise Exception(f'SEND TO OUTFILE {ex}')
        finally:
            return ""

    def motorspeed(self, value: float, axis: str) -> float:
        if axis == 'X':
            flow = gcode.flow.get('linMaxFlow')
            speed = min(flow, flow * (value / 100.0))
        else:
            flow = gcode.flow.get('rotMaxFlow')
            speed = min(flow, flow * (value / 100.0))
        return float(speed)

    def go_home(self) -> None:
        self.send(_gcodes.get(gcode.HOME))

    def stop(self) -> None:
        self.send(_gcodes.get(gcode.STOP))

    def set_absolute(self) -> None:
        self.relative_mode = False
        self.send(_gcodes.get(gcode.ABSOLUTE))

    def set_relative(self) -> None:
        self.relative_mode = True
        self.send(_gcodes.get(gcode.RELATIVE))

    def move_lin(self, value: float, speed: int = 10, relative: bool = False) -> None:
        sendstr = "{0}F{1:5.3f} X{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'X'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def move_rot(self, value: float, speed: int = 10, relative: bool = False) -> None:
        sendstr = "{0}F{1:5.3f} Y{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'Y'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def move_both(self, pos: float, rot: float, speed: int = 10, relative: bool = False) -> None:
        sendstr = "{0}F{1:5.3f} X{2:5.3f} Y{3:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'X'), pos, rot)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def wait(self, value: float) -> None:
        sendstr = "{0}S{1:5.3f}".format(_gcodes.get(gcode.WAIT), value)
        self.send(sendstr)

    def set_zero(self) -> None:
        sendstr = "{0}".format(_gcodes.get(gcode.SETZERO))
        self.send(sendstr)

    def get_position(self) -> None:
        sendstr = "{0}".format(_gcodes.get(gcode.GET_POS))
        pos_ = self.send(sendstr)
        index_ = pos_.index('Z')
        print(f"MY INDEX {index_}")
        return pos_[:index_]

    def serial_port_reset(self, name: str=None):
        try:
            if GCodeMaker.serialport is None:
                GCodeMaker.serialport = robot_serial_port.serial_port_manager()
                GCodeMaker.serialport.timeout = 1
            else:
                if GCodeMaker.serialport.is_open:
                    GCodeMaker.serialport.reset_output_buffer()
                    GCodeMaker.serialport.close()
                GCodeMaker.serialport = robot_serial_port.serial_port_manager(name)
                pdrobot_support.top_win.EntrySp.configure(foreground="#000000")
                pdrobot_support.top_win.EntrySp.configure(background="green")
                pdrobot_support.top_win.serial_prt.set(GCodeMaker.serialport.name)

        except Exception as e:
            print(f'Exception during serial port reset" {e}')
            pdrobot_support.top_win.serial_prt.set('XXXXX')
            pdrobot_support.top_win.EntrySp.configure(foreground="#ff0000")
            pdrobot_support.top_win.EntrySp.configure(background="white")
