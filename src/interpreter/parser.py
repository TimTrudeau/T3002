
""" Parser module for CLIQ test robot interpreter
"""


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
from .lexer import Lexer
from .lexer import Token as Token
from .token_types import *

class AST(object):
    """ Base class for all node entities
    """
    pass

class BinOp(AST):
    """ Binary operation node
    """
    def __init__(self, left: str, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right


#TODO 'Not' operation should be handled as unaryop
class UnaryOp(AST):
    """ Negation or inversion op node
    """
    def __init__(self, op: Token, expr: Token):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    """Represents a 'BEGIN ... END' block node
    The children are the statements found in the block.
    """
    def __init__(self):
        self.children = []


class Assign(AST):
    """ Var assignment node
    The left side is the variable name (str)
    The right side is the expression to be assigned to the variable
    The op is assign operator
    """
    def __init__(self, left: str, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right


class Bool(AST):
    """The Bool node is type_ BOOL with value TRUE/FALSE."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Num(AST):
    """The Num node is type_ INTEGER/REAL with value numeric."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Var(AST):
    """The Var node has type_ ID with value of varname (str).
    """
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class VarDecl(AST):
    """Declared variable node found under the VAR heading.
    Declared variables contain a type var node and a type Num node.
    """
    def __init__(self, var_node: Var, type_node):
        self.var_node = var_node
        self.type_node = type_node

class IO_(Var):
    """The IO node is subclass of Var. Type becomes type_ IO with pin direction and pin number added.
    """
    def __init__(self, token: Token, in_out: str, pin: int):
        token.type = IO
        super(IO_, self).__init__(token)
        self.direction = in_out
        self.pin = pin

class Point(AST):
    """The Point node has type_ PNT with value distance and speed.
    Points can be either absolute of relative. Relative points are declared
    with a prepended sign.
    """
    def __init__(self, token: Token, distance, speed):
        token.type = PNT
        super(Point, self).__init__(token)
        self.distance = distance
        self.speed = speed

class Waypoint(Var):
    """The Waypoint node is subclass of Var. Type becomes WAYPOINT.
    each waypoint consists to two point objects. lpoint is the linear point
    and rpoint is the rotational.
    """
    def __init__(self, token: Token, point: Point):
        token.type = WAYPOINT
        super(Waypoint, self).__init__(token)
        self.point = point
#        self.lpoint = point
 #       self.rpoint = point

class IfNode(AST):
    """The If node is constructed from a logic test
    followed by a 'true' statement list and a 'false' statement list.
    If no ELSE present the 'false' statement will be no op.
    """
    def __init__(self, token, logicNode, truestatements, falsestatements):
        self.token = token
        self.logicNode = logicNode
        self.true = truestatements
        self.false = falsestatements

class Loop(AST):
    """The Loop node contains a statement list followed by a logic test.
    """
    def __init__(self, token: Token, logicNode, statements):
        self.token = token
        self.logicNode = logicNode
        self.statements = statements

class Wait(AST):
    """The Wait node type_ WAIT with value wait time."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Home(AST):
    """The Home node type_ HOME with value None."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Stop(AST):
    """The Stop node type_ STOP with value None."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Moveto(AST):
    """The Moveto node type_ MOVETO with value waypoint name."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Rotate(AST):
    """The Rotate node type_ ROTATE with value waypoint name."""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    """Dead end node to stop recursion"""
    pass

class Block(AST):
    """Block node holds in-scope variable declarations and is the top of the tree
     for all statements in the block"""
    def __init__(self, declarations: list, io_list: list, waypoint_list: list, compound_statement: Compound):
        self.declarations = declarations
        self.io_list = io_list
        self.waypoint_list = waypoint_list
        self.compound_statement = compound_statement


class Program(AST):
    """Program (top of tree) node, with value program name"""
    def __init__(self, name: str, block: Block):
        self.name = name
        self.block = block


class Type(AST):
    """ creates a type aware node"""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Parser(object):
    """The parser creates a lexicon scanner object which scans the input
      and returns tokens. The parser inserts the tokens into an Abstract Syntax Tree
      of nodes. Higher precedent nodes are placed lower in the tree.
    """
    def __init__(self, program_text: str):
        self.lexer = Lexer(program_text)
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        """Lexemes
        program : PROGRAM variable SEMI block DOT
        block : declarations compound_statement
        declarations : VAR (variable_declaration SEMI)+
                     | IO (io_declaration SEMI)+
                     | empty
        variable_declaration : ID (COMMA ID)* COLON type_spec
        io_declaration : ID COLON pin_spec
        pin_spec: PININ INTEGER
                | PINOUT INTEGER
        type_spec : INTEGER | REAL | BOOL
        compound_statement : BEGIN statement_list END
        statement_list : statement
                       | statement SEMI statement_list
        loop_statement: LOOP statement_list UNTIL bool_op
        if_statement: IF bool_op statement_list ELSE statement_list
        moveto command: MOVETO expr
        rotate command: ROTATE expr
        stop command: STOP nop
        wait command: WAIT expr
        home command: HOME empty
        statement : compound_statement
                  | assignment_statement
                  | empty
        assignment_statement : variable ASSIGN expr
        empty :
        expr : term ((PLUS | MINUS) term)*
        term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        point : (variable | factor) COMA (variable | factor)
        factor : PLUS factor
               | MINUS factor
               | INTEGER_CONST
               | REAL_CONST
               | LPAREN (expr) RPAREN
               | variable
        variable: ID
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error(EOF, self.current_token.type)
        return node

    def error(self, expected, found):
        raise Exception(
            f'Parse error at line {self.lexer.line_count}, '
            f'column {self.lexer.line_pos}. Expected {expected}, found {found}')

    def eat(self, token_type):
        """Compare the current token type_ with the passed token
        type_ and if they match then "eat" the current token
        and assign the next token to the self.current_token,
        otherwise raise an exception."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type, self.current_token.type)

    def program(self):
        """Lexeme
        program : PROGRAM variable SEMI block DOT
        """
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self):
        """Lexeme
        block : declarations compound_statement
        """
        declaration_list = self.declarations()
        io_list = self.declarations()
        waypoint_list = self.declarations()
        compound_list = self.compound_statement()
        node = Block(declaration_list, io_list, waypoint_list, compound_list)
        return node

    def compound_statement(self, beginBlock=True):
        """Lexeme
        compound_statement: (BEGIN statement_list END) | statement_list
        'if' and 'loop' have compound statements without BEGIN/END.
        """
        if beginBlock:
            self.eat(BEGIN)
            nodes = self.statement_list()
            self.eat(END)
        else:
            nodes = self.statement_list()
        compound_node = Compound()
        for node in nodes:
            compound_node.children.append(node)
        return compound_node

    def assignment_statement(self):
        """Lexeme
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def if_statement(self):
        """Lexeme
        if : LOGIC_TEST (statement_list) | ELSE : (statement_list) | ENDIF
        LOGIC_TEST becomes a BinOp with a logical operator (not arithmetic or assignment)
        The statement list is extracted and both are passed to IF evaluator.
        """
        tokenIf = self.current_token
        self.eat(IF)
        logic_exr = self.expr()
        self.eat(COLON)
        statement_true = self.compound_statement(False)
        tokenElse = self.current_token
        if tokenElse.type == ELSE:
            self.eat(ELSE)
            self.eat(COLON)
            statement_false = self.compound_statement(False)
        else:
            statement_false = NoOp()
        node = IfNode(tokenIf, logic_exr, statement_true, statement_false)
        self.eat(ENDIF)
        return node

    def loop_statement(self):
        """Lexeme
        loop : (statement_list) | UNTIL (LOGIC_TEST)
        """
        looptoken = self.current_token
        self.eat(LOOP)
        self.eat(COLON)
        statements = self.compound_statement(False)
        self.eat(UNTIL)
        logic_exr = self.expr()
        node = Loop(looptoken, logic_exr, statements)
        return node

    def wait_statement(self):
        """Lexeme
        wait : expr
        """
        waittoken = self.current_token
        self.eat(WAIT)
        waittoken.value = self.expr()
        node = Wait(waittoken)
        return node

    def stop_statement(self):
        """Lexeme
        stop : none
        """
        stoptoken = self.current_token
        self.eat(STOP)
        stoptoken.value = None
        node = Stop(stoptoken)
        return node

    def moveto_statement(self):
        """Lexeme
        moveto : waypoint | distance(factor)<, speed(factor)>
        """
        movetoken = self.current_token
        self.eat(MOVETO)
        token = self.current_token
        if token.type == ID:
            self.eat(ID)
            movetoken.value = Var(token)
        else:
            movetoken.value = self.point()
        node = Moveto(movetoken)
        return node

    def rotate_statement(self):
        """Lexeme
        rotate : waypoint | distance(factor)<, speed(factor)>
        """
        movetoken = self.current_token
        self.eat(ROTATE)
        token = self.current_token
        if token.type == ID:
            self.eat(ID)
            movetoken.value = Var(token)
        else:
            movetoken.value = self.point()
        node = Rotate(movetoken)
        return node

    def home_statement(self):
        """ Lexeme
        HOME : none
        """
        hometoken = self.current_token
        self.eat(HOME)
        hometoken.value = None
        node = Home(hometoken)
        return node

    def declarations(self):
        """Lexeme
        declarations : VAR (variable_declaration SEMI)+
                        | IO (io_declaration SEMI)+
                        | WAYPOINT list(distance, angle)
                        | empty
        """
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        elif self.current_token.type == IO:
            self.eat(IO)
            while self.current_token.type == ID:
                io_decl = self.io_declaration()
                declarations.append(io_decl)
                self.eat(SEMI)
        elif self.current_token.type == WAYPOINT:
            self.eat(WAYPOINT)
            while self.current_token.type == ID:
                wp_decl = self.waypoint_declaration()
                declarations.append(wp_decl)
                self.eat(SEMI)
        return declarations

    def io_declaration(self):
        """Lexeme
        io_declaration : ID COLON (PININ | PINOUT) Number
        """
        io_name = self.current_token
        self.eat(ID)
        self.eat(COLON)
        io_type = self.current_token.value
        self.eat(ID)
        pin = self.current_token.value
        self.eat(INTEGER_CONST)
        io_node = IO_(io_name, io_type, pin)  # first ID
        return io_node

    def waypoint_declaration(self):
        """Lexeme
        WAYPOINT_declaration : variable COLON factor COMMA factor)
        """
        waypoint_token = self.current_token
        self.eat(ID)
        self.eat(ASSIGN)
        point = self.point()
        wp_node = Waypoint(waypoint_token, point)
        return wp_node

    def variable_declaration(self):
        """Lexeme
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """
        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        """Lexeme
        type_spec : INTEGER
                     | BOOL
                     | REAL
                     | PININ
                     | PINOUT
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        elif self.current_token.type == BOOL:
            self.eat(BOOL)
        elif self.current_token.type == REAL:
            self.eat(REAL)
        else:
            self.error('type_spec', 'unknown type')
        node = Type(token)
        return node

    def statement_list(self):
        """Lexeme
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]
        while True:
            self.eat(SEMI)
            results.append(self.statement())
            if self.current_token.type != SEMI:
                break
        return results

    def statement(self):
        """Lexeme
        statement : compound_statement
                  | assignment_statement
                  | if_statement
                  | loop_statement
                  | wait_statement
                  | moveto_statement
                  | rotate_statement
                  | stop_statement
                  | home_statement
                  | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == LOOP:
            node = self.loop_statement()
        elif self.current_token.type == WAIT:
            node = self.wait_statement()
        elif self.current_token.type == MOVETO:
            node = self.moveto_statement()
        elif self.current_token.type == ROTATE:
            node = self.rotate_statement()
        elif self.current_token.type == STOP:
            node = self.stop_statement()
        elif self.current_token.type == HOME:
            node = self.home_statement()
        else:
            node = self.empty()
        return node

    def variable(self):
        """Lexeme
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    @staticmethod
    def empty():
        """Lexeme
        An empty expression
        """
        return NoOp()

    def expr(self):
        """Lexeme
        expr : term ((PLUS | MINUS | logical op) term)*
        Evaluates current token as a logical or arithmetic operator.
        Eats the op token and returns Binary Op node.
        """
        ops = [LT, LTE, GT, GTE, EQUAL, NEQUAL]
        node = self.term()
        token = self.current_token
        if token.type in ops:
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
            return node

        while token.type in (PLUS, MINUS):
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
            token = self.current_token
        return node

    def term(self):
        """Lexeme
        term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def point(self):
        """Lexeme
        point : (variable | factor) COMA (variable | factor)
        """
        distance_node = self.factor()
        self.eat(COMMA)
        speed_node = self.factor()
        return {'distance': distance_node, 'speed': speed_node}

    def factor(self):
        """Lexeme
        factor : PLUS factor
                  | MINUS factor
                  | INTEGER_CONST
                  | REAL_CONST
                  | BOOL_CONST
                  | BOOL_OP
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == BOOL_CONST:
            self.eat(BOOL_CONST)
            return Bool(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

