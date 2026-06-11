from .tokens import *

OPERATORS = {
    ':=': ASSIGN,
    '<=': LESS_EQUAL,
    '>=': GREATER_EQUAL,
    '<>': NOT_EQUAL,
    ';': SEMI,
    '.': DOT,
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': FLOAT_DIV,
    '=': EQUAL,
    '<': LESS_THAN,
    '>': GREATER_THAN,
    '(': LPAREN,
    ')': RPAREN,
    ',': COMMA,
    ':': COLON
}

class Lexer(object):
    """
    The lexer operates at the character level\n
    The lexer is responsible for turning sequences of characters from the original text into tokens for the parser\n
    Invalid character errors come from here
    """
    def __init__(self, text):
        self.text = text
        self.column = 0
        self.pos = 0
        self.line = 1
        self.current_char = self.text[self.pos] if self.text else None

    def __str__(self):
        return f"Lexer | Current Position: {self.pos} | Current Character: {self.current_char}"

    def __repr__(self):
        return self.__str__()

    def error(self, message=None, line=None, column=None):
        raise LexerError(
            message if message is not None else f"Invalid character: {self.current_char}",
            self.line if line is None else line,
            (self.column + 1) if column is None else column,
        )

    def advance(self):
        """Move position forward and update current_char\n
        Also increments line counter per newline"""
        if self.current_char == "\n":
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        "Skips spaces, tabs, newlines and carriage returns"
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        start_line = self.line
        start_column = self.column + 1

        while self.current_char is not None and self.current_char != '}':
            self.advance()

        if self.current_char is None:
            self.error("Unterminated comment", start_line, start_column)

        self.advance()  # Skip the closing curly brace
    
    def number(self):
        start_line = self.line
        start_column = self.column + 1
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(REAL_CONST, float(result), start_line, start_column)
        return Token(INTEGER_CONST, int(result), start_line, start_column)
    
    def string(self):
        start_line = self.line
        start_column = self.column + 1
        result = ''
        while self.current_char is not None and self.current_char != "'":
            if self.current_char == "\n":
                self.error("Unterminated string", start_line, start_column)
            result += self.current_char
            self.advance()
        if self.current_char is None:
            self.error("Unterminated string", start_line, start_column)

        self.advance()  # Skip closing quote
        return Token(STRING_CONST, result, start_line, start_column)


    def peek(self):
        "Returns the token after the current token if there is one"
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
    
    def _id(self):
        """Handle identifiers and reserved keywords"""
        start_line = self.line
        start_column = self.column + 1
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        result_upper = result.upper()
        reserved = RESERVED_KEYWORDS.get(result_upper)
        if reserved is not None:
            return Token(reserved.type, reserved.value, start_line, start_column)
        return Token(ID, result_upper, start_line, start_column)

    def match_operator(self):
        "Match the longest fixed-symbol token starting at the current position"
        start_line = self.line
        start_column = self.column + 1
        for length in (2, 1):
            text = self.text[self.pos:self.pos + length]
            token_type = OPERATORS.get(text)
            if token_type is not None:
                for _ in range(length):
                    self.advance()
                return Token(token_type, text, start_line, start_column)
        return None

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == "'":
                self.advance()
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
            
            if self.current_char.isdigit():
                return self.number()  

            token = self.match_operator()
            if token is not None:
                return token

            self.error()

        return Token(EOF, None, self.line, self.column + 1)
