

import unittest
from gcode import linlimit, rotatlimit
from gcode_maker import GCodeMaker
from robot_serial_port import serial_port_manager, serialscan, _openSerialPort

class test_gcode_maker(unittest.TestCase):
    def test_GCodeMaker(self):
        GCM = GCodeMaker(None)
        assert GCM.linear_limit == linlimit
        assert GCM.rotation_limit == rotatlimit

    def test_open_serial_port(self):
        ports = serialscan()
        with _openSerialPort(ports[0]) as port:
            assert port is not None
            assert port.is_open
            assert port.baudrate == 115200

    def test_gcode_maker_init(self):
        GCM = GCodeMaker()
        with serial_port_manager() as manager:
            GCM.serialport = manager
            assert (GCM.serialport.is_open is True)
            GCM.set_absolute()  # This is command to send gcode to robot
        pass
        assert (GCM.serialport.is_open is False)

if __name__ == '__main__':
    pytest.main()

