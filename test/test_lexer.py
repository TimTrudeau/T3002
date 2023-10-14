import pytest
import contextlib
from src.interpreter.lexer import Lexer
from src.interpreter.token_types import *

token_list = [
    ('TRUE', BOOL_CONST, TRUE),
    ('FALSE', BOOL_CONST, FALSE),
    ('234', INTEGER_CONST, 234),
    ('3.14', REAL_CONST, 3.14),
    ('*', MUL, '*'),
    ('DIV', INTEGER_DIV, 'DIV'),
    ('/', FLOAT_DIV, '/'),
    ('+', PLUS, '+'),
    ('-', MINUS, '-'),
    ('(', LPAREN, '('),
    (')', RPAREN, ')'),
    (':=', ASSIGN, ':='),
    ('==', EQUAL, '=='),
    ('!=', NEQUAL, '!='),
    ('<=', LTE, '<='),
    ('>=', GTE, '>='),
    ('<', LT, '<'),
    ('>', GT, '>'),
    ('.', DOT, '.'),
    (';', SEMI, ';'),
    ('IF', IF, 'IF'),
    ('ELSE', ELSE, 'ELSE'),
    ('ENDIF', ENDIF, 'ENDIF'),
    ('LOOP', LOOP, 'LOOP'),
    ('UNTIL', UNTIL, 'UNTIL'),
    ('MOVETO', MOVETO, 'MOVETO'),
    ('ROTATE', ROTATE, 'ROTATE'),
    ('STOP', STOP, 'STOP'),
    ('HOME', HOME, 'HOME'),
    ('number', ID, 'number'),
    ('BEGIN', BEGIN, 'BEGIN'),
    ('WAYPOINT', WAYPOINT, 'WAYPOINT'),
    ('WAIT', WAIT, 'WAIT'),
    ('IO', IO, 'PIN'),
    ('END', END, 'END'),
    ('AND', AND, 'AND'),
    ('OR', OR, 'OR'),
    ('NOT', NOT, 'NOT'),

]

@contextlib.contextmanager
def makeLexer(text):
    try:
        lexer = Lexer(text)
        yield lexer
    finally:
        del lexer

#  This test fails when called from Run All Test because
@pytest.mark.parametrize("text, tok_type, tok_val", token_list)
def test_tokens(text, tok_type, tok_val):
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == tok_type
        assert token.value == tok_val

def test_init():
    # create a lexer object with some text
    lex = Lexer("hello")
    # assert that the attributes are initialized correctly
    assert lex.text == "hello"
    assert lex.line_count == 0
    assert lex.line_pos == 0
    assert lex.pos == 0
    assert lex.current_char == "h"

def test_advance():
    # create a lexer object with some text
    lex = Lexer("hello")
    # call the advance method on the lexer object
    lex.advance()
    # assert that the pos and line_pos are incremented by 1
    assert lex.pos == 1
    assert lex.line_pos == 1
    # assert that the current_char is updated to the next character in the text
    assert lex.current_char == "e"
    # call the advance method again until the end of input is reached
    for _ in range(len(lex.text) - 1):
        lex.advance()
    # assert that the current_char is None when the end of input is reached
    assert lex.current_char is None

def test_comment():
    text = '{this is a comment}  \n'
    with makeLexer(text) as lexer:
        try:
            lexer.get_next_token()
        except Exception as ex:
            assert False, f"Comment test failed {ex}"

        with pytest.raises(Exception):
            lexer = makeLexer('{missing closing brace  \n')
            lexer.skip_comment()

def test_number():
    text = '12345  )))'
    with makeLexer(text) as lexer:
        token = lexer.number()
        assert token.type == 'INTEGER_CONST'
        assert token.value == 12345

    text = '123.45'
    with makeLexer(text) as lexer:
        token = lexer.number()
        assert token.type == 'REAL_CONST'
        assert token.value == 1.2345e+2

def test_get_next_token():
    text = '  !=  '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == NEQUAL
    text = '  ==  '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == EQUAL
    text = '  <= '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == LTE
    text = '  >= '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == GTE
    text = '  <= '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == LTE
    text = '  <= '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == LTE
    text = '  <= '
    with makeLexer(text) as lexer:
        token = lexer.get_next_token()
        assert token.type == LTE
    text = '  @'
    with makeLexer(text) as lexer:
        with pytest.raises(ValueError):
            _ = lexer.get_next_token()
        assert lexer.line_count == 0
        assert lexer.line_pos == 2

if __name__ == '__main__':
    pytest.main()
