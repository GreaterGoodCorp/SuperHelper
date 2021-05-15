from SuperHelper.Modules.Grapher import UserInputLexer

tokens = UserInputLexer.tokens


class Equation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def solve(self):
        raise NotImplementedError()


class BinaryOps:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryMinus:
    def __init__(self, value):
        self.value = value


def p_equation(p):
    """equation : expression EQUAL expression"""
    p[0] = Equation(p[1], p[3])


def p_simple_expression(p):
    """expression : term"""
    p[0] = p[1]


def p_expression_ops(p):
    """expression : expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term"""
    p[0] = BinaryOps(p[1], p[2], p[3])


def p_simple_term(p):
    """term : NUMBER
            | VARIABLE
            | power"""
    p[0] = p[1]


def p_term_is_paren_exp(p):
    """term : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_unary_term(p):
    """term : MINUS term"""
    p[0] = UnaryMinus(p[2])


def p_term_recursive(p):
    """term : term term"""
    p[0] = BinaryOps(p[1], "*", p[2])


def p_power(p):
    """power : term CARAT term"""
    p[0] = BinaryOps(p[1], "^", p[3])


def p_error(p):
    print(f"Syntax error: {p}")
