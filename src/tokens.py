INTEGER, REAL, BOOLEAN, STRING, INTEGER_CONST, REAL_CONST, BOOLEAN_CONST, STRING_CONST, PLUS, MINUS, MUL, FLOAT_DIV, INTEGER_DIV, \
LPAREN, RPAREN, BEGIN, END, DOT, ID, ASSIGN, SEMI, COMMA, COLON, VAR, PROGRAM, IF, THEN, ELSE, WHILE, DO, \
WRITELN, PROCEDURE, EQUAL, NOT_EQUAL, LESS_THAN, LESS_EQUAL, GREATER_THAN, GREATER_EQUAL, TRUE, FALSE, EOF = \
'INTEGER', 'REAL', 'BOOLEAN', 'STRING', 'INTEGER_CONST', 'REAL_CONST', 'BOOLEAN_CONST', 'STRING_CONST', 'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'INTEGER_DIV', \
'LPAREN', 'RPAREN', 'BEGIN', 'END', 'DOT', 'ID', 'ASSIGN', 'SEMI', 'COMMA', 'COLON', 'VAR', 'PROGRAM', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', \
'WRITELN', 'PROCEDURE', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_EQUAL', 'GREATER_THAN', 'GREATER_EQUAL', 'TRUE', 'FALSE', 'EOF'

class Token(object):
    """
    Every symbol in the expression being evaluated is a token.
    """
    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        location = ""
        if self.line is not None and self.column is not None:
            location = f", line={self.line}, column={self.column}"
        return f'Token({self.type}, {repr(self.value)}{location})'

    def __repr__(self):
        return self.__str__()


class PascalError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"line {self.line}, column {self.column}: {self.message}"
        return self.message
    
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

class ProcSymbol(Symbol):
    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else []

    def __str__(self):
        return f'<ProcedureSymbol(name={self.name}, params={self.params})>'

    __repr__ = __str__

class SymbolTable(object):
    def __init__(self, scope_name=None, parent_scope=None):
        "Parent scope being None means it is global scope"
        self.name = scope_name if scope_name is not None else "global"
        self.parent_scope = parent_scope
        self._symbols = {}
        if self.parent_scope is None:
            self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))
        self.define(BuiltinTypeSymbol('BOOLEAN'))
        self.define(BuiltinTypeSymbol('STRING'))

    def __str__(self):
        if self.name == "global": return "global"
        s = f'{self.name} | Parent Scope: {self.parent_scope} | Symbols: {[value for value in self._symbols.values()]}'
        return s

    __repr__ = __str__

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        if symbol is not None:
            return symbol
        
        if self.parent_scope is not None and not current_scope_only: # Recursively searches upwards through parent scopes until global
            symbol = self.parent_scope.lookup(name)
            return symbol
        
        return None


RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'IF': Token(IF, 'IF'),
    'THEN': Token(THEN, 'THEN'),
    'ELSE': Token(ELSE, 'ELSE'),
    'WHILE': Token(WHILE, 'WHILE'),
    'DO': Token(DO, 'DO'),
    'WRITELN': Token(WRITELN, 'WRITELN'),
    'PROCEDURE': Token(PROCEDURE, 'PROCEDURE'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BOOLEAN': Token(BOOLEAN, 'BOOLEAN'),
    'STRING': Token(STRING, 'STRING'),
    'TRUE': Token(BOOLEAN_CONST, True),
    'FALSE': Token(BOOLEAN_CONST, False),
    'DIV': Token(INTEGER_DIV, 'DIV')
}

# Custom error classes for robust error handling
class LexerError(PascalError):
    pass

class ParserError(PascalError):
    pass

class SemanticError(PascalError):
    pass

class InterpreterError(PascalError):
    pass
