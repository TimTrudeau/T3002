"""
Interpreter for the NPD cycle tester robot
Command line aruments:
--file
--com
--out
--step
--version
--debug
--help
"""
from parser import Parser
from lexer import Lexer
from interpreter import Interpreter
import argparse

def main(*args):
    import sys
    _version = '0.1.0'
    arguments = argparse.ArgumentParser(description="Interpreter for the NPD cycle tester robot.", prog='T3001')
    arguments.add_argument('-f', '--file', help='Program source file', type=str, default='../cliq_test.nps')
    arguments.add_argument('-c', '--com', help='Specify serial port', type=str, default='COM5')
    arguments.add_argument('-o', '--out', help='File name for GCODE output', type=str, default='out.gcode')
    arguments.add_argument('-r', '--run', help='Enable for execution of generated GCODE', type=str, default=False)
    arguments.add_argument('-s', '--step', help='Enable stepping of source', dest='stepping', action='store_true')
    arguments.add_argument('-v', '--version', help='Display version', dest='version', action='store_true')
    arguments.add_argument('-d', '--debug', help='Display contents of identifier dictionary', dest='db',
                        action='store_true')

#    options = arguments.parse_args(sys.argv[1:])
    options = arguments.parse_args()
    if options.version:
        print(f'Version: {_version}')
    try:
        text = open(options.file, 'r').read()
    except (IndexError, NameError):
        text = open('cliq_test.txt', 'r').read()

    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        with open(options.out, 'w') as outfile:
            interpreter = Interpreter(parser, port, outfile)
            interpreter.interpret()
    except Exception as ex:
        print(f'{ex}')
        if "yield" in ex.args[0] :
            with open(options.out, 'w') as outfile:
                interpreter = Interpreter(parser, None, outfile)
                interpreter.interpret()

    if options.db:
        print('\n Debug on: Displaying the contents of the declared GLOBAL identifiers \n')
        for k, v in sorted(interpreter.GLOBAL_SCOPE.items()):
            try:
                if type(v).__name__ == 'dict':
                    d = v.get('distance')
                    if hasattr(d, 'expr'):
                        value = d.expr.value
                    else:
                        value = d.value
                    print(f"{k} = Distance: {value}, Speed: {v.get('speed').value}")
                else:
                    print(f'{k} = {v}')
            except Exception as ex:
                print(f'{ex}')
    return

if __name__ == "__main__":
    main()
