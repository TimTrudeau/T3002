import serial
from serial.tools import list_ports
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
            portname = portlist[-1]
    else:
        portname = '/dev/ttyACM0'  # This is the serial port on the raspberry pi
    try:
        _serialport = _openSerialPort(portname)
        print(f"GM SERIAL PORT NAME={_serialport.name}.")
        sys.stdout.flush()
        _serialport.flush()
        if _serialport.isatty(): print('This is a TTY')
        if _serialport.isOpen(): print(f'SERIAL PORT IS OPEN {_serialport}')
        return _serialport
    except ValueError as ex:
        print(f"SERIAL PORT PARAMETER ERROR={ex}")
        raise Exception
    except (serial.SerialException, AttributeError) as ex:
        print(f"SERIAL PORT NOT FOUND. {ex}")
        raise Exception
    except Exception as ex:
        print(f'UNKNOWN {ex}')
        if _serialport is not None:
            _serialport.close()

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
            timeout=5,
            write_timeout=5
        )
    except Exception as ex:
    # except serial.SerialException as ex:
        raise serial.SerialException(f"FAILED TO CAPTURE SERIAL PORT: {ex}")
    finally:
        return s


if __name__ == '__main__':
    print(f'AVALABLE SERIAL PORTS {serialscan()}')
    with serial_port_manager() as serialport:
        serialport.write(b'M114 D')
    print("WHATS GOING ON")
