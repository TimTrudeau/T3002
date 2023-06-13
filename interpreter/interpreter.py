""" Interpreter for Medeco NPD key tester robot"""

###############################################################################
#
#  INTERPRETER
#  Third pass
#  Scans the Abstract Syntax Tree and performs the actions defined in nodes.
#  Generates GCODES and writes GCODE to file. If run is True passes GCODE
#  to seria port.
###############################################################################

# from __init__ import logger
import SRC.gcode_maker
from interpreter.token_types import *

class NodeVisitor(object):
    def __init__(self):
        # logger.info("STARTING LOG")
        pass

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        # try:
        #     logger.info(f'method name {method_name} attr {node.__dict__.keys()}')
        # except Exception:
        #     logger.info(f'method name {method_name}')
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser, port: str = None, outfile: str = None, run: bool = False):
        self.GLOBAL_SCOPE = {}
        self.declaredDict = {}
        self.waypointList = {}
        self.ioList = {}
        self.parser = parser
        self.port = port
        self.out_file = outfile
        self.run = run
        self.gcode = SRC.gcode_maker.GCodeMaker(port, outfile, run)

    def interpret(self):
        NodeVisitor.__init__(self)
        tree = self.parser.parse()
        if tree is None:
            return ''
        # TODO test the tree.GLOBAL_SCOPE and tree.declarations agree
        return self.visit(tree)

    def getType(self, node):
        """Recursive call to find terminal (leaf) node.
        *** This method is Not used. ***
        """
        if hasattr(node, 'right'):
            return self.getType(node.right)
        if hasattr(node, 'expr'):
            return self.getType(node.expr)
        if hasattr(node.token, 'type_'):
            return node.token.type
        else:
            return None

    def handleTypeConversion(self, lType: str, rValue:str):
        """ This code should not be used if type conversion is NOT allowed."""
        import math
        if lType == INTEGER:  # convert 'float to int
            rValue = math.trunc(rValue)
        elif lType == REAL:  # convert 'int to float
            rValue = float(rValue)
        elif lType == BOOL:  # convert int/float to bool
            rValue = False if rValue == 0 else True
        else:
            raise TypeError(f'Illegal lValue type {lType}')
        return rValue

    def visit_Program(self, node):
        self.declarations = node.block.declarations
        self.waypointList = node.block.waypoint_list
        self.ioList = node.block.io_list
        self.visit(node.block) #  recursive
        self.gcode.close_outfile()
        print("Source Interpreter finished")

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        for declaration in node.io_list:
            self.visit(declaration)
        for declaration in node.waypoint_list:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        self.declaredDict[node.var_node.value] = node.type_node.value

    def visit_IO_(self, node):
        # TODO add IO functionality
        pass

    def visit_Type(self, node):
        # TODO add type checking
        pass

    def visit_BinOp(self, node):
        try:
            rightvalue = self.visit(node.right)
            leftvalue = self.visit(node.left)

            if node.op.type == PLUS:
                return (leftvalue + rightvalue)
            elif node.op.type == MINUS:
                return (leftvalue - rightvalue)
            elif node.op.type == MUL:
                return (leftvalue * rightvalue)
            elif node.op.type == INTEGER_DIV:
                return (leftvalue // rightvalue)
            elif node.op.type == FLOAT_DIV:
                return float(leftvalue) / float(rightvalue)
            elif node.op.type == EQUAL:
                return (leftvalue == rightvalue)
            elif node.op.type == LT:
                return (leftvalue < rightvalue)
            elif node.op.type == GT:
                return (leftvalue > rightvalue)
            elif node.op.type == LTE:
                return (leftvalue <= rightvalue)
            elif node.op.type == GTE:
                return (leftvalue >= rightvalue)
            elif node.op.type == NEQUAL:
                return (leftvalue != rightvalue)
            else:
                return False
        except Exception as e:
            print(e)
            raise e

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            newExp = -self.visit(node.expr)
        return newExp

    def visit_Compound(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self.visit(child)

    def visit_Assign(self, node):
        lVarName = node.left.value
        try:
            lType = self.declaredDict[lVarName]  # test if var has been declared
        except KeyError:
            raise Exception(f"Variable {lVarName} not declared")
        rvalue = self.visit(node.right)
        rvalue = self.handleTypeConversion(lType, rvalue)
        self.GLOBAL_SCOPE[lVarName] = rvalue

    def visit_Bool(self, node):
        value = node.value
        val_type = str(type(value).__name__)
        if val_type != 'str':
            raise TypeError('visit_bool did not find TRUE/FALSE string')
        return (value == 'TRUE')

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.GLOBAL_SCOPE.get(var_name)
        if var_value is None:
            raise NameError(f'{repr(var_name)} is defined but has not been assigned a value.')
        else:
            return var_value

    def visit_Waypoint(self, node):
        """******* point is a dict. Need to process dict for point type by visiting dict entries
            evaluate distance and speed down to signed integers not nodes. store dict of ints
        """
        point = {k: self.visit(v) for (k, v) in node.point.items()}
        self.GLOBAL_SCOPE[node.value] = point

    def visit_NoOp(self, node):
        pass

    def visit_IfNode(self, node):
        if self.visit(node.logicNode) is True:
            self.visit(node.true)
        else:
            self.visit(node.false)

    def visit_Loop(self, node):
        while True:
            self.visit(node.statements)
            if self.visit(node.logicNode) is True:
                break

    def visit_Wait(self, node):
        pause = self.visit(node.token.value)
        # TODO Use GPIO delay
        self.gcode.wait(float(pause))
        return pause

    def visit_Moveto(self, node):
        if type(node.value).__name__ == 'Var':
            waypoint_name = node.value.value  # returns str
            wp = self.GLOBAL_SCOPE.get(waypoint_name)  # returns dict
            distance = wp.get('distance')
            speed = wp.get('speed')
            name = list(filter(lambda x: x.value == waypoint_name, self.waypointList))
            _type = type(name[0].point['distance']).__name__
        elif type(node.value).__name__ == 'dict':
            distance = self.visit(node.value['distance'])
            speed = self.visit(node.value['speed'])
            _type = type(node.value['distance']).__name__
        relative = False if _type == 'Num' else True
        self.gcode.move_lin(float(distance), float(speed), relative)

    def visit_Rotate(self, node):
        if type(node.value).__name__ == 'Var':
            waypoint_name = node.value.value  # returns str
            wp = self.GLOBAL_SCOPE.get(waypoint_name)  # returns dict
            distance = wp.get('distance')
            speed = wp.get('speed')
            name = list(filter(lambda x: x.value == waypoint_name, self.waypointList))
            _type = type(name[0].point['distance']).__name__
        elif type(node.value).__name__ == 'dict':
            distance = self.visit(node.value['distance'])
            speed = self.visit(node.value['speed'])
            _type = type(node.value['distance']).__name__
        relative = False if _type == 'Num' else True
        self.gcode.move_rot(float(distance), float(speed), relative)

    def visit_Home(self, node):
        self.gcode.go_home()
        # self.gcode.send(0, 0)
        # self.gcode.send('RELATIVE')
        # while self.gcode.input(self.gcode.linear_limit) is False:
        #     self.gcode.send(-1, 0)
        # self.gcode.send('ABSOLUTE')

    def visit_Stop(self, node):
        self.gcode.stop()
