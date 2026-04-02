# How To Read Grammars

This project uses a simple BNF/EBNF-style grammar to describe the Pascal-like language and the parser structure.

Related files:

- [Project README](README.md)
- [Grammar reference](grammar.txt)
- [Parser implementation](src/Parser.py)

## Basic Rule Shape

Each rule looks like this:

```text
rule_name : thing_to_match
```

Read that as:

`rule_name` is defined as `thing_to_match`.

For example:

```text
program : PROGRAM variable SEMI block DOT
```

means a `program` must contain:

- `PROGRAM`
- a `variable`
- a semicolon
- a `block`
- a final dot

## Common Symbols

- `:` means "is defined as"
- `|` means "or"
- `(...)` groups parts together
- `*` means "zero or more times"
- `+` means "one or more times"
- `?` means "optional" or "zero or one time"

## Worked Examples

Example:

```text
variable_declaration : ID (COMMA ID)* COLON type_spec
```

This means:

- start with an `ID`
- then allow zero or more extra `, ID` pairs
- then require a `:`
- then require a type

Valid shapes include:

```text
x : INTEGER
x, y, z : REAL
```

Example:

```text
expression : arithmetic_expr ((EQUAL | NOT_EQUAL | LESS_THAN | LESS_EQUAL | GREATER_THAN | GREATER_EQUAL) arithmetic_expr)?
```

This means:

- first parse an `arithmetic_expr`
- then optionally parse one comparison operator
- then parse another `arithmetic_expr`

So both of these fit:

```text
a + 2
a + 2 < b * 3
```

## Reading Rules Top Down

When one rule name appears inside another rule, it means the parser will parse that sub-rule next.

For example:

```text
expression -> arithmetic_expr -> term -> factor
```

That chain is also how precedence is expressed:

- `factor` is the tightest level
- `term` handles `*`, `DIV`, and `/`
- `arithmetic_expr` handles `+` and `-`
- `expression` optionally adds a comparison on top

So:

```text
2 + 3 * 4
```

is read like:

```text
2 + (3 * 4)
```

not:

```text
(2 + 3) * 4
```

## Grammar vs Implementation

The grammar describes what the language should look like.

The parser methods in [`src/Parser.py`](src/Parser.py) are the implementation of those rules. For example:

- `expression(...)` implements the `expression` rule
- `arithmetic_expr(...)` implements the `arithmetic_expr` rule
- `term(...)` implements the `term` rule
- `factor(...)` implements the `factor` rule

So the grammar is both:

- a description of the language
- a guide for how the recursive-descent parser is organized
