import serial
from serial.tools import list_ports
from pathlib import Path
import contextlib
import os
import sys


def serialscan():
    """Scan and list valid serial ports.
    """
    # print()
    # print("Valid serial ports detected:")
    ports = list_ports()
    ports.sort()
    if ports:
        # [print("\t" + p) for p in ports if p]
        return ports
    else:
        # print("\tNone")
        return None


def list_ports():
    """
        Get a list of available serial port device names.
        :returns: List of strings containing the serial port device names.
    """
    try:
        ports = serial.tools.list_ports.comports()
        portlist = [p.device for p in ports]
    except Exception as ex:
        raise ex
    return portlist

def serial_port_manager(portname: str=None):
    if os.name == 'nt':
        if portname is None or portname == '':
            portlist = serialscan()
            portname = portlist[0]
    else:
        portname = '/dev/ttyUSB0'  # This is the serial port on the raspberry pi
    try:
        _serialport = _openSerialPort(portname)
        print(f"GM Serial Port name={_serialport.name}.")
        sys.stdout.flush()
        _serialport.flush()
        return _serialport
    except ValueError as ex:
        print(f"Serial Port parameter error={ex}")
        return None
    except (serial.SerialException, AttributeError) as ex:
        print(f"Serial Port not found. {ex}")
        return None
    except Exception as ex:
        print(f'unknown {ex}')
        return None

def _openSerialPort(comport: str):
    """Opens the serial port name passed in comport. Returns the stream id"""
    # debuglog.info("Check if serial module is available in sys {}".format(sys.modules["serial"]))
    s = None
    try:
        s = serial.Serial(
            port=comport,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2,
            write_timeout=1
        )
    except Exception as ex:
    # except serial.SerialException as ex:
        print(f"Failed to capture serial port: {ex}")
        raise serial.SerialException
    finally:
        return s


if __name__ == '__main__':
    print(f'Avalable serial ports {serialscan()}')
    with serial_port_manager() as serialport:
        serialport.write(b'M114 D')
    print("whats going on")
