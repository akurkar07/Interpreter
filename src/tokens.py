INTEGER, REAL, BOOLEAN, INTEGER_CONST, REAL_CONST, BOOLEAN_CONST, PLUS, MINUS, MUL, FLOAT_DIV, INTEGER_DIV, \
LPAREN, RPAREN, BEGIN, END, DOT, ID, ASSIGN, SEMI, COMMA, COLON, VAR, PROGRAM, IF, THEN, ELSE, \
EQUAL, NOT_EQUAL, LESS_THAN, LESS_EQUAL, GREATER_THAN, GREATER_EQUAL, TRUE, FALSE, EOF = \
'INTEGER', 'REAL', 'BOOLEAN', 'INTEGER_CONST', 'REAL_CONST', 'BOOLEAN_CONST', 'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'INTEGER_DIV', \
'LPAREN', 'RPAREN', 'BEGIN', 'END', 'DOT', 'ID', 'ASSIGN', 'SEMI', 'COMMA', 'COLON', 'VAR', 'PROGRAM', 'IF', 'THEN', 'ELSE', \
'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_EQUAL', 'GREATER_THAN', 'GREATER_EQUAL', 'TRUE', 'FALSE', 'EOF'

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
    
class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__
    
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f'<{self.name}:{self.type}>'
    
    __repr__ = __str__

class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))
        self.define(BuiltinTypeSymbol('BOOLEAN'))

    def __str__(self):
        s = f'Symbols: {[value for value in self._symbols.values()]}'
        return s

    __repr__ = __str__

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol

RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'IF': Token(IF, 'IF'),
    'THEN': Token(THEN, 'THEN'),
    'ELSE': Token(ELSE, 'ELSE'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BOOLEAN': Token(BOOLEAN, 'BOOLEAN'),
    'TRUE': Token(BOOLEAN_CONST, True),
    'FALSE': Token(BOOLEAN_CONST, False),
    'DIV': Token(INTEGER_DIV, 'DIV')
}

# Custom error classes for robust error handling
class LexerError(Exception):
    pass

class ParserError(Exception):
    pass

class InterpreterError(Exception):
    pass
