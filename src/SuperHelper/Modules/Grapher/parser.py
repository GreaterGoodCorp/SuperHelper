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


class UnaryMinus:
    def __init__(self, value):
        self.value = value


class UserInputParser:
    tokens = UserInputLexer.tokens

    @staticmethod
    def p_simple_expression(p):
        """expression : term"""
        p[0] = p[1]

    @staticmethod
    def p_expression_ops(p):
        """expression : expression PLUS term
                      | expression MINUS term
                      | expression TIMES term
                      | expression DIVIDE term"""
        p[0] = BinaryOps(p[1], p[2], p[3])

    @staticmethod
    def p_simple_term(p):
        """term : NUMBER
                | VARIABLE
                | power"""
        p[0] = p[1]

    @staticmethod
    def p_term_is_paren_exp(p):
        """term : LPAREN expression RPAREN"""
        p[0] = p[2]

    @staticmethod
    def p_unary_term(p):
        """term : MINUS term"""
        p[0] = UnaryMinus(p[2])

    @staticmethod
    def p_term_recursive(p):
        """term : term term"""
        p[0] = BinaryOps(p[1], "*", p[2])

    @staticmethod
    def p_power(p):
        """power : term CARAT term"""
        p[0] = BinaryOps(p[1], "^", p[3])

    @staticmethod
    def p_error(p):
        print(f"Syntax error: {p}")

    def __init__(self, **kwargs):
        self.lexer = UserInputLexer().lexer
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data, self.lexer)


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
