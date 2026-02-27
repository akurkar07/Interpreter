# Interpreter

A small Pascal-like interpreter built as a learning project.

Current pipeline:

`source text -> Lexer -> Parser -> AST -> SemanticAnalyser -> Interpreter`

## Current Features

- Lexer for Pascal-like tokens (`PROGRAM`, `VAR`, `BEGIN/END`, arithmetic ops, assignment, literals, identifiers)
- Recursive-descent parser that builds an AST
- AST node model in `nodes.py`
- Visitor-based execution (`NodeVisitor` + `Interpreter`)
- Semantic pass (`SemanticAnalyser`) with symbol table population, duplicate declaration checks, undeclared variable checks, assignment compatibility checks, and numeric operator checks

## Project Structure

- `main.py`: entry point and REPL loop
- `Lexer.py`: lexical analysis
- `Parser.py`: AST construction from tokens
- `nodes.py`: AST node classes
- `interpreter.py`: base visitor and runtime interpreter
- `SemanticAnalyser.py`: semantic checks + symbol table population
- `tokens.py`: token constants, token class, symbol classes/table, and custom exceptions
- `grammar.txt`: grammar notes
- `instructions.txt`: sample input program loaded on first run

## Grammar (Implemented)

```text
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

variable : ID
```

Note: standalone expression statements like `1+1` are not valid in this grammar.

## Running

1. Use Python 3.
2. From the project folder:

```bash
python main.py
```

Behavior:

- First run executes `instructions.txt`
- Then it switches to interactive input
- Type `:q` to quit

## Semantic Rules Currently Enforced

- Variables must be declared before use
- Duplicate variable declarations are rejected
- `DIV` requires `INTEGER` operands
- `/` (`FLOAT_DIV`) yields `REAL`
- `+`, `-`, `*` yield `INTEGER` only when both operands are `INTEGER`, otherwise `REAL`
- Assignments allow exact type match and widening `INTEGER -> REAL`

## Errors

The project currently uses:

- `LexerError`
- `ParserError`
- `InterpreterError` (also used by semantic analysis at the moment)

## Current Limitations

- No procedures/functions yet
- No nested scopes yet
- No booleans/relational operators yetV
- Semantic errors are not split into a dedicated `SemanticError` type yet
