from sympy import Symbol, sympify

from SuperHelper.Modules.Grapher import UserInputLexer, yacc


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

    def pythonize(self):
        x = Symbol("x")
        while type(self.left) == BinaryOps:
            self.left = self.left.pythonize()
        while type(self.right) == BinaryOps:
            self.right = self.right.pythonize()
        # Cast variable
        self.left = x if self.left == "x" else self.left
        self.right = x if self.right == "x" else self.right
        # Turn caret to double stars
        self.op = "**" if self.op == "^" else self.op
        return sympify(f"({self.left}{self.op}{self.right})")


class UserInputParser:
    tokens = UserInputLexer.tokens

    @staticmethod
    def p_simple_expression(p):
        """expression : term"""
        p[0] = p[1]

    @staticmethod
    def p_expression_ops(p):
        """expression : expression PLUS term
                      | expression MINUS term"""
        p[0] = BinaryOps(p[1], p[2], p[3])

    @staticmethod
    def p_simple_term(p):
        """term : factor"""
        p[0] = p[1]

    @staticmethod
    def p_implicit_term(p):
        """term : term factor"""
        p[0] = BinaryOps(p[1], UserInputLexer.t_TIMES[-1], p[2])

    @staticmethod
    def p_complex_term(p):
        """term : term TIMES factor
                | term DIVIDE factor"""
        p[0] = BinaryOps(p[1], p[2], p[3])

    @staticmethod
    def p_simple_factor(p):
        """factor : constant
                  | VARIABLE"""
        p[0] = p[1]

    @staticmethod
    def p_complex_factor(p):
        """factor : LPAREN expression RPAREN"""
        p[0] = p[2]

    @staticmethod
    def p_factor_power(p):
        """factor : factor CARAT factor"""
        p[0] = BinaryOps(p[1], p[2], p[3])

    @staticmethod
    def p_constant(p):
        """constant : NUMBER
                    | uminus"""
        p[0] = p[1]

    @staticmethod
    def p_uminus(p):
        """uminus : MINUS NUMBER"""
        p[0] = p[2]

    @staticmethod
    def p_error(p):
        print(f"Syntax error: {p}")

    def __init__(self, **kwargs):
        self.lexer = UserInputLexer().lexer
        self.parser = yacc.yacc(module=self, **kwargs)
        self.ast = None

    def make_ast(self, data):
        self.ast = self.parser.parse(data, self.lexer)

    def generate_function(self):
        if self.ast is None:
            raise ValueError("Missing AST!")
        return self.ast.pythonize()


class ExpressionParser(UserInputParser):
    def __init__(self, **kwargs):
        if "EQUAL" in ExpressionParser.tokens:
            ExpressionParser.tokens = ExpressionParser.tokens[:-1]
        super().__init__(**kwargs)


class EquationParser(UserInputParser):
    @staticmethod
    def p_equation(p):
        """equation : expression EQUAL expression"""
        p[0] = Equation(p[1], p[3])

    def __init__(self, **kwargs):
        super().__init__(start="equation", **kwargs)
