from tokens import *

# single character tokens map characters to token types rather than token objects
SINGLE_CHARS = {
    ';': SEMI,
    '.': DOT,
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': FLOAT_DIV,
    '(': LPAREN,
    ')': RPAREN,
    ',': COMMA,
    ':': COLON
}

class Lexer(object):
    """
    The lexer operates at the character level
    The lexer holds all the methods that handle the tokens and takes in the instructions when defined\n
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

    def error(self):
        raise LexerError(f'Invalid character at line {self.line}, position {self.column}: {self.current_char}')

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
        while self.current_char != '}':
            self.advance()
        self.advance()  # Skip the closing curly brace
    
    def number(self):
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
            return Token(REAL_CONST, float(result))
        return Token(INTEGER_CONST, int(result))

    def peek(self):
        "Returns the token after the current token if there is one"
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
    
    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        result_upper = result.upper()
        token = RESERVED_KEYWORDS.get(result_upper, Token(ID, result_upper))
        return token

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
            
            if self.current_char.isdigit():
                return self.number()  
                      
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            
            #Gets the token type of the current char
            token_type = SINGLE_CHARS.get(self.current_char)
            if token_type is not None:
                char = self.current_char
                self.advance()
                return Token(token_type, char)   # Returns a fresh token each time

            self.error()

        return Token(EOF, None)
