from SuperHelper.Modules.Grapher import lex


class UserInputLexer:
    tokens = (
        "VARIABLE",
        "NUMBER",
        "LPAREN",
        "RPAREN",
        "CARAT",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EQUAL",
    )

    literals = "+-*/^"

    # Ignore the following tokens: SPACE and TAB
    t_ignore = " \t"

    # Define simple tokens

    # 1. Operators (+, -, *, /, ^, =)
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_CARAT = r"\^"
    t_EQUAL = r"="

    # 2. Parentheses
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # 3. Number (INT, FLOAT)
    @staticmethod
    def t_NUMBER(t):
        r"""\d+(?:\.\d+)?"""
        if t.value.isdigit():
            t.value = int(t.value)
        else:
            t.value = float(t.value)
        return t

    # 4. Variable
    t_VARIABLE = "x"

    # Additional rules

    # 1. Error handler
    @staticmethod
    def t_error(t):
        print(f"Invalid character: '{t.value[0]}'")
        t.lexer.skip(1)

    # Builder and tester implementation
    def __init__(self, **kwargs):
        self.lexer = lex(module=self, **kwargs)

    def test(self, data: str):
        self.lexer.input(data)
        return [t for t in self.lexer]
