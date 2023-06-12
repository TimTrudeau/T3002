

import pytest
from interpreter.parser import Parser
from interpreter.lexer import Lexer
from interpreter.lexer import Token as Token
from interpreter.token_types import *

from test_lexer import makeLexer

If_expressions = [
    ('IF 3 >= 3:  \n tt := 22; \n ELSE: \n tt := -66; \n ENDIF;', 22, -66),
    ('IF 3 <= 3:  \n tt := 22; \n ENDIF;', 22, None),
    ('IF 3 != 3:  \n tt := 0; \n ELSE: \n tt := 22; \n ENDIF;', 0, 22),
    ('IF 3 == 3:  \n tt := 22; \n ENDIF;', 22, None),
]


@pytest.mark.parametrize("expr, truestat, falsestat", If_expressions)
def test_parse_if(expr, falsestat, truestat):
    # TODO IF should handle compound boolean statements
    parser = Parser(expr)
    node = parser.statement()
    assert node.token.type == IF
    result = node.true.children[0].right.value
    assert result == truestat
    if falsestat is None:
        assert 'NoOp' in str(type(node.false))
    else:
        result = get_Op_value(node.false.children[0].right)
        assert result == falsestat


def test_nested_if():
    # TODO IF should handle compound boolean statements (and, or)
    expr = ';IF 3 == 3:  \n aa := -22; \n IF 4 > 3: \n bb := 2; \n ENDIF;\n ELSE: \n cc := 66; \n ENDIF;'
    parser = Parser(expr)
    nodes = parser.statement_list()
    assert nodes is not None
    assert len(nodes) == 3
    assert 'NoOp' in str(type(nodes[0]))
    assert 'IfNode' in str(type(nodes[1]))
    assert 'BinOp' in str(type(nodes[1].logicNode))
    assert 'Assign' in str(type(nodes[1].true.children[0]))
    assert nodes[1].true.children[0].right.op.type == MINUS
    assert nodes[1].true.children[0].right.expr.value == 22
    assert 'IfNode' in str(type(nodes[1].true.children[1]))
    assert nodes[1].true.children[1].logicNode.op.type == 'GT'
    assert nodes[1].false.children[0].right.value == 66


def test_parse_loop():
    # TODO UNTIL should handle compound boolean statements
    statement = 'LOOP:  \n count := count + 1; \n UNTIL (count > 100);\n'
    parser = Parser(statement)
    node = parser.statement()
    assert node.token.type == LOOP
    assert node.logicNode.left.value == 'count'
    assert node.logicNode.right.value == 100
    assert node.logicNode.op.value == '>'
    assert node.statements.children[0].left.value == 'count'
    assert node.statements.children[0].right.op.type == PLUS
    assert node.statements.children[0].right.right.token.type == INTEGER_CONST


def varDecl_compare(node, value, type_):
    if node.type_node.value == type_ and node.var_node.value == value:
        return True
    else:
        return False


def test_variable_declaration():
    statement = ' aa, bb, cc: INTEGER\n   x, y, z: REAL\n flag,tester: BOOL'
    parser = Parser(statement)
    nodes = parser.variable_declaration()
    assert len(nodes) == 3
    assert varDecl_compare(nodes[0], 'aa', INTEGER)
    assert varDecl_compare(nodes[2], 'cc', INTEGER)
    nodes = parser.variable_declaration()
    assert len(nodes) == 3
    assert varDecl_compare(nodes[0], 'x', REAL)
    assert varDecl_compare(nodes[2], 'z', REAL)
    nodes = parser.variable_declaration()
    assert len(nodes) == 2
    assert varDecl_compare(nodes[0], 'flag', BOOL)
    assert varDecl_compare(nodes[1], 'tester', BOOL)


def test_term():
    statement = '(33 + 45)*(4 >= 3)'
    parser = Parser(statement)
    nodes = parser.term()
    assert 'BinOp' in str(type(nodes))
    assert nodes.left.left.value == 33
    assert nodes.left.right.value == 45
    assert nodes.right.left.value == 4
    assert nodes.right.right.value == 3
    assert nodes.left.token.type == PLUS
    assert nodes.right.token.type == GTE
    assert nodes.token.type == MUL


def test_IO_declarations():
    statement = 'IO \nlimitx: PININ 6;\nlimity: PINOUT 7;\nlimitz: PININ 8;'
    parser = Parser(statement)
    node = parser.declarations()
    mylist = []
    for i in range(3):
        results = []
        for property_, value in vars(node[i]).items():
            results.append(value)
        mylist.append(results)
    assert mylist[0] == [Token(IO, 'limitx'), 'limitx', PININ, 6]
    assert mylist[1] == [Token(IO, 'limity'), 'limity', PINOUT, 7]
    assert mylist[2] == [Token(IO, 'limitz'), 'limitz', PININ, 8]


def get_Op_value(node):
    pass
    if type(node).__name__ == 'UnaryOp':
        value = node.expr.value
        sign = node.op.type
        d = -value if sign == MINUS else value
    elif type(node).__name__ == 'BinOp':
        a = str(node.left.value)
        op = node.op.value
        b = str(node.right.value)
        d = a + op + b
        return eval(d)
    else:
        d = node.value
    return d


def waypoint_compare(waypoint, datastr):
    point = waypoint[2]
    goodd = get_Op_value(point['distance'])
    goods = get_Op_value(point['speed'])

    if waypoint[0].__eq__(datastr[0]) and \
            goodd == datastr[1] and \
            goods == datastr[2]:
        return True
    else:
        return False


def test_waypoint_declarations():
    statement = 'WAYPOINT \napproach := 250,90;\nopen := +0, (90*5);\ninsert:=-33.7,+0;'
    parser = Parser(statement)
    node = parser.declarations()
    mylist = []
    for i in range(3):
        results = []
        for property_, value in vars(node[i]).items():
            results.append(value)
        mylist.append(results)
    truth = waypoint_compare(mylist[0], (Token(WAYPOINT, 'approach'), 250, 90))
    assert truth
    truth = waypoint_compare(mylist[1], (Token(WAYPOINT, 'open'), 0, (90 * 5)))
    assert truth
    truth = waypoint_compare(mylist[2], (Token(WAYPOINT, 'insert'), -33.7, +0))
    assert truth


points = ['100,(90*5)', 'newDistance,newSpeed', 'waypoint', '300,5', 'position,0', '-250,speed', '+10, 6']
@pytest.mark.parametrize("moves", points)
def test_moveto(moves):
    statement = f'MOVETO {moves};\n'
    parser = Parser(statement)
    node = parser.moveto_statement()
    ds = moves.split(',')
    if type(node.value).__name__ == 'dict':
        distance = get_Op_value(node.value.get('distance'))
        speed = get_Op_value(node.value.get('speed'))
        assert eval(ds[0]) == distance
        assert eval(ds[1]) == speed
    elif node.value.token.type == 'ID':
        value = node.value.token.value
        assert ds[0] == value

@pytest.mark.parametrize("moves", points)
def test_rotate(moves):
    statement = f'ROTATE {moves};\n'
    parser = Parser(statement)
    node = parser.rotate_statement()
    ds = moves.split(',')
    if type(node.value).__name__ == 'dict':
        distance = get_Op_value(node.value.get('distance'))
        speed = get_Op_value(node.value.get('speed'))
        assert eval(ds[0]) == distance
        assert eval(ds[1]) == speed
    elif node.value.token.type == 'ID':
        value = node.value.token.value
        assert ds[0] == value



def test_home():
    statement = 'HOME;'
    parser = Parser(statement)
    nodelist = parser.statement_list()
    assert type(nodelist[0]).__name__ == 'Home'


def test_stop():
    statement = 'STOP;'
    parser = Parser(statement)
    nodelist = parser.statement_list()
    assert type(nodelist[0]).__name__ == 'Stop'


if __name__ == '__main__':
    pytest.main()
