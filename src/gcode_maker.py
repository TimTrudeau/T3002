import contextlib
import os
import sys
import time
import serial

import gcode
from gcode import _gcodes

usable_gpio = [0, 3, 4, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26]
linlimit_io = 5
rotatlimit_io = 6

try:
    import gpiozero as gpio
except Exception as e:
    print(f"No Pi GPIO {e}")
    print(f"GPIO UNAVAILABLE {e}")
    raise ImportError

def capture_serial_output_header(serialPort, outfile):
    time.sleep(1)
    response = serialPort.readline()
    while serialPort.inWaiting() > 0:
        response += serialPort.readline()
    outfile.write(response.decode('utf-8'))
    outfile.flush()


@contextlib.contextmanager
def open_serial_port(portnum, outfile=None):
    if os.name == 'nt':
        port = portnum
    else:
        port = '/dev/ttyUSB0'
    try:
        serialPort = _openSerialPort(port)
        print(f"GM Serial Port name={serialPort.name}.")
        sys.stdout.flush()
        if outfile is not None:
            capture_serial_output_header(serialPort, outfile)
        serialPort.flush()
        yield serialPort
    except ValueError as ex:
        print(f"Serial Port parameter error={ex}")
        return None
    except (serial.SerialException, AttributeError) as ex:
        print(f"Serial Port not found. {ex}")
        return None
    except Exception as ex:
        print(f'unknown {ex}')
        return None
    finally:
        pass


def _openSerialPort(comport):
    """Opens the serial port name passed in comport. Returns the stream id"""
    #debuglog.info("Check if serial module is available in sys {}".format(sys.modules["serial"]))
    s = None
    try:
        s = serial.Serial(
            port=comport,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=10,
            write_timeout=10
        )
    except serial.SerialException as ex:
        print(f"Failed to capture serial port: {ex}")
        raise serial.SerialException
    finally:
        return s


class GCodeMaker:
    serialport = None

    def __init__(self, sport, outfile=None):
        self.linear_limit = gcode.linlimit
        self.rotation_limit = gcode.rotatlimit
        self.outfile = outfile
        if GCodeMaker.serialport is None:
            GCodeMaker.serialport = sport


    def send(self, command):
        try:
            cmd = command + '\n'
            GCodeMaker.serialport.write(cmd.encode())
            print(command)
            response = bytes('', 'utf-8')
            #time.sleep(.1)
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
            speed = min(gcode.flow.get('linMaxFlow'), flow * (value/100))
        else:
            flow = gcode.flow.get('rotMaxFlow')
            speed = min(gcode.flow.get('rotMaxFlow'), flow * (value / 100))
        return int(speed)

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
        sendstr = "{0}F{1:1d} X{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'X'), value)
        self.set_relative() if relative is True else self.set_absolute()
        self.send(sendstr)

    def move_rot(self, value, relative=False, speed=10):
        sendstr = "{0}F{1:1d} Y{2:5.3f}".format(_gcodes.get(gcode.MOVE), self.motorspeed(speed, 'Y'), value)
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