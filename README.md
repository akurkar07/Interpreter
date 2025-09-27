# TreeInterpreter3

TreeInterpreter3 is a simple interpreter for a Pascal-like programming language. It takes in a program written in a specific grammar, tokenises it, parses it into an Abstract Syntax Tree (AST), and evaluates the result. This project demonstrates the implementation of a lexer, parser, and interpreter for educational purposes.

---

## Features

- **Lexer**: Converts the input text into tokens.
- **Parser**: Converts tokens into an Abstract Syntax Tree (AST) based on the defined grammar.
- **Interpreter**: Evaluates the AST and executes the program.
- **Error Handling**: Handles syntax and lexical errors gracefully.
- **Global Scope**: Stores variables and their values during execution.

---

## Project Structure

- **`main.py`**: The entry point of the interpreter. Reads instructions from `instructions.txt` or user input and executes the program.
- **`Lexer.py`**: Contains the `Lexer` class, which tokenises the input text.
- **`Parser.py`**: Contains the `Parser` class, which parses tokens into an AST.
- **`ASTNodes.py`**: Defines the various nodes used in the AST.
- **`tokens.py`**: Defines token types, reserved keywords, and global scope. Also includes custom error classes.
- **`instructions.txt`**: A sample program written in the supported grammar.
- **`grammar.txt`**: The formal grammar definition for the language.

---

## Grammar

The interpreter supports the following grammar:

```
program : PROGRAM variable SEMI block DOT

block : declarations compound_statement

declarations : VAR (variable_declaration SEMI)+
             | empty

variable_declaration : ID (COMMA ID)* COLON type_spec

type_spec : INTEGER | REAL

compound_statement : BEGIN statement_list END

statement_list : statement
               | statement SEMI statement_list

statement : compound_statement
          | assignment_statement
          | empty

assignment_statement : variable ASSIGN expr

empty :

expr : term ((PLUS | MINUS) term)*

term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*

factor : PLUS factor
       | MINUS factor
       | INTEGER_CONST
       | REAL_CONST
       | LPAREN expr RPAREN
       | variable

variable: ID
```

---

## How to Run

1. Clone the repository or download the project files.
2. Ensure you have Python 3 installed.
3. Run the interpreter:
   ```bash
   python main.py
   ```
4. The interpreter will execute the program in `instructions.txt` by default. Alternatively, you can enter instructions interactively.

---

## Example Program

The following program is included in `instructions.txt`:

```pascal
PROGRAM Test;
VAR
  a, b, c : INTEGER;
  x, y    : REAL;

BEGIN
  a := 2;
  b := 10;
  c := a + b * 3;

  x := 3.14;
  y := x + 2 * (b - a) / 4.0;

  a := b DIV 3;

  x := +5.0;
  y := -x;

  c := c - 1
END.
```

This program demonstrates variable declarations, arithmetic operations, and assignments.

---

## Error Handling

The interpreter raises the following errors:

- **`LexerError`**: Raised for invalid characters during tokenisation.
- **`ParserError`**: Raised for syntax errors during parsing.
- **`InterpreterError`**: Raised for runtime errors during interpretation.

---

## License

This project is for educational purposes and is not licensed for commercial use. Feel free to explore and modify the code for learning.

---
