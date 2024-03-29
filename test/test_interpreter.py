import pytest


def makeProgramSyntax(intAssign='345', realAssign='2.22', boolAssign='TRUE', syntax=None, breakcode=None):
    testcode = \
        f"""PROGRAM Test;
            VAR
                turned: BOOL;
                aa : INTEGER;
                BB, x : REAL;
                cc : INTEGER;
            BEGIN
                aa := {intAssign};
                BB := {realAssign};
                turned := {boolAssign};
                MOVETO -10, 200;
                cc := 1;
                IF turned == TRUE:
                    cc := 100;
                ENDIF;
            END.
         """
    if breakcode is not None:
        brokecode = testcode.replace(syntax, breakcode, 1)
        return brokecode
    else:
        return testcode


def makeInterpreter(aprogram):
    from interpreter import Parser
    from interpreter.interpreter import Interpreter

    parser = Parser(aprogram)
    interpreter = Interpreter(parser, None)
    return interpreter


Wait_expressions = [
    ('WAIT  6 + 3;\n', 6 + 3),
    ('WAIT  5;\n', 5),
    ('WAIT  1.5;\n', 1.5),
    ('WAIT  1 - 1;\n', 1 - 1),
    ('WAIT  1.5 * 2;\n', 1.5 * 2),
    ('WAIT  4 / 2;\n', 4 / 2),
]


@pytest.mark.parametrize("expr, answer", Wait_expressions)
def test_parse_wait(expr, answer):
    interpreter = makeInterpreter(expr)
    node1 = interpreter.parser.wait_statement()
    result1 = interpreter.visit(node1)
    interpreter.parser('WAIT 1;')
    node2 = interpreter.parser.wait_statement()
    result2 = interpreter.visit(node2)
    assert node1.token.type == WAIT
    assert result1 == answer
    assert node1.token.type == WAIT
    assert result2 == 1
    pass


arithmetic_expressions = [
    ('5.5 - - - + - (3 + 4) - +2', 10),
    ('- 3', -3),
    ('14 + 2 * 3 - 6 DIV 2', 17),
    ('2 + 7 * 5', 37),
    ('3+1', 4),
    ('7 - 8 DIV 4', 5),
    ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1))', 22),
    ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1)) DIV (2 + 3) - 5 - 3 + (8)', 10),
    ('7 + (((3 + 2)))', 12),
    ('+ 3', 3),
    ('5 - - - + - 3', 8),
    ('-5 + 5', 0),
    ('5/2', 2),
    ('5 DIV 2', 2),
]


@pytest.mark.parametrize("expr, result", arithmetic_expressions)
def test_integer_arithmetic_expressions(expr, result):
    progText = makeProgramSyntax(intAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert id_table['aa'] == result


float_expressions = [
    ('100', 100.00),
    ('3.14', 3.14),
    ('2.14 + 7 * 5', 37.14),
    ('(2.14 + 7) * 5', 45.7),
    ('7.14 - 8 / 4', 5.14),
    ('(7.14 - 8) / 4', -0.215),
    ('-3.14', -3.14),
    ('5/2', 2.5),
    ('5 DIV 2', 2),
]


@pytest.mark.parametrize("expr, result", float_expressions)
def test_float_arithmetic_expressions(expr, result):
    progText = makeProgramSyntax(realAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert (id_table['BB']) == pytest.approx(result)


bool_expressions = [
    ('3 > 2', True),
    ('2 > 3', False),
    ('2 < 3', True),
    ('3 < 2', False),
    ('3 >= 2', True),
    ('3 >= 3', True),
    ('2 <= 3', True),
    ('3 <= 2', False),
    ('3 == 3', True),
    ('3 == 2', False),
    ('3 != 2', True),
    ('3 != 3', False),
]


@pytest.mark.parametrize("expr, result", bool_expressions)
def test_bool_expressions(expr, result):
    progText = makeProgramSyntax(boolAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert id_table['turned'] == result


bad_syntax = [
    ('VAR', 'var'),  # lower case keyword
    ('VAR', 'VAR:'),  # invalid colon
    (':=', '='),  # invalid assignment operator
    ('cc : INTEGER;', 'cc  INTEGER;'),  # missing colon
    ('cc : INTEGER;', 'cc : INTEGER'),  # missing semicolon
    ('INTEGER', 'INTIGER'),  # misspelled keyword
    ('END.', 'END')  # missing dot
]


@pytest.mark.parametrize("expr, repl", bad_syntax)
def test_expression_invalid_syntax_01(expr, repl):
    progText = makeProgramSyntax(syntax=expr, breakcode=repl)
    interpreter = makeInterpreter(progText)
    with pytest.raises(Exception):
        interpreter.interpret()


# "TODO These should be caught by the interpreter"
bad_expr = [
    #('aa := 345;', 'aa := 3.14;'),  #assign float to int. This is legal!
    ('aa := 345;', 'aa := "string";'),  # Does not support strings
    ('cc := 1;', 'cc := 1 (2+3);'),  # missing operator
    ('345;', '345'),  # missing semicolon
    ('aa', 'xx'),  # assign to an undeclared var
]


@pytest.mark.parametrize("expr, repl", bad_expr)
def test_expression_invalid_syntax_02(expr, repl):
    progText = makeProgramSyntax(syntax=expr, breakcode=repl)
    interpreter = makeInterpreter(progText)
    with pytest.raises(Exception):
        interpreter.interpret()


program = """\
PROGRAM Full;
VAR
   number     : INTEGER;
   iftest     : INTEGER;
   a, b, c    : INTEGER;
   y, x       : REAL;
   
IO
    limit   : PININ 6;

WAYPOINT
    approach := 250, 55;
    pullout := -10, (20*5);
    unlock  := 90, 30;
    relock  := 110, 40;
    
BEGIN {Part10}
{ Test of comment }
    HOME;
    ROTATE  +90, 360;
    MOVETO pullout;
    MOVETO  +3.6, 240;   
    MOVETO  2, 20;   
    WAIT 2;
    ROTATE  -110, 360;
    number := 5;
    a := (number + 11) / 2;
    b := (10 * a) + (11 * number) DIV 4;
    IF FALSE:
        iftest := 10;
    ELSE:
        iftest := 20;
    ENDIF;
    IF 3 == 3:
        c := a;
    ELSE:
        c := 1;
    ENDIF;
    WAIT 3;
    ROTATE -90,300;
    LOOP:
        number := number + 1;
        WAIT 0.27;
        MOVETO approach;
    UNTIL number > 3;  
    STOP;
    x := 11 / 2;
    y := 20 / 7 + 3.14;
END.  {Part10}
"""


def test_program():
    interpreter = makeInterpreter(program)
    interpreter.interpret()

    globals = interpreter.GLOBAL_SCOPE
    assert len(globals.keys()) == 11
    assert 'approach' in globals.keys()
    assert 'pullout' in globals.keys()
    assert globals['iftest'] == 20
    assert globals['number'] == 6
    assert globals['a'] == 8
    assert globals['b'] == 93
    assert globals['c'] == globals['a']
    assert globals['x'] == 5.5
    pytest.approx(globals['y'], pytest.approx(20.0 / 7 + 3.14))  # 5.9971...


if __name__ == '__main__':
    pytest.main()

