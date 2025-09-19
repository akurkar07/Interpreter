INTEGER, REAL, INTEGER_CONST, REAL_CONST, PLUS, MINUS, MUL, FLOAT_DIV, INTEGER_DIV,\
LPAREN, RPAREN, BEGIN, END, DOT, ID, ASSIGN, SEMI, COMMA, COLON, VAR, PROGRAM, EOF =\
'INTEGER', 'REAL', 'INTEGER_CONST', 'REAL_CONST', 'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'INTEGER_DIV',\
'LPAREN', 'RPAREN', 'BEGIN', 'END', 'DOT', 'ID', 'ASSIGN', 'SEMI', 'COMMA', 'COLON', 'VAR', 'PROGRAM', 'EOF'

class Token(object):
    """
    Every symbol in the expression being evaluated is a token.
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()
    
RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    ':=': Token(ASSIGN, ':='),
    ';': Token(SEMI, ';'),
    '.': Token(DOT, '.'),
    '+': Token(PLUS, '+'),
    '-': Token(MINUS, '-'),
    '*': Token(MUL, '*'),
    '/': Token(FLOAT_DIV, '/'),
    '(': Token(LPAREN, '('),
    ')': Token(RPAREN, ')'),
    ',': Token(COMMA, ','),
    ':': Token(COLON, ':')
}


GLOBAL_SCOPE = {}

# Custom error classes for robust error handling
class LexerError(Exception):
    pass

class ParserError(Exception):
    pass

class InterpreterError(Exception):
    pass