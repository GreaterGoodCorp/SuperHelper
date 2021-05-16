from sympy import Eq, Expr, Symbol, sympify

from SuperHelper.Modules.Grapher import UserInputLexer, yacc


class Equation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def pythonize(self) -> Eq:
        if type(self.left) == BinaryOps:
            self.left = self.left.pythonize()
        if type(self.right) == BinaryOps:
            self.right = self.right.pythonize()
        return Eq(self.left, self.right)


class BinaryOps:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def pythonize(self) -> Expr:
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
        temp = f"({self.left}){self.op}({self.right})"
        return sympify(temp)


class UserInputParser:
    tokens = UserInputLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UMINUS"),
        ("left", "CARAT"),
    )

    @staticmethod
    def p_expression_single(p):
        """expression : NUMBER
                      | VARIABLE"""
        p[0] = p[1]

    @staticmethod
    def p_expression_ops(p):
        """expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression CARAT expression"""
        p[0] = BinaryOps(p[1], p[2], p[3])

    @staticmethod
    def p_uminus_expression(p):
        """expression : MINUS expression %prec UMINUS"""
        p[0] = BinaryOps(0, p[1], p[2])

    @staticmethod
    def p_parens_expression(p):
        """expression : LPAREN expression RPAREN"""
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
        return self.ast


class ExpressionParser(UserInputParser):
    def __init__(self, **kwargs):
        if "EQUAL" in ExpressionParser.tokens:
            ExpressionParser.tokens = ExpressionParser.tokens[:-1]
        super().__init__(**kwargs)

    def generate_function(self):
        if self.ast is None:
            raise ValueError("Missing AST!")
        return self.ast.pythonize()


class EquationParser(UserInputParser):
    @staticmethod
    def p_equation(p):
        """equation : expression EQUAL expression"""
        p[0] = Equation(p[1], p[3])

    def __init__(self, **kwargs):
        super().__init__(start="equation", **kwargs)

    def generate_equation(self) -> Eq:
        return self.ast.pythonize()
