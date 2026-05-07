# Bytecode Language Specification

## Purpose

This document defines the stack-based bytecode language emitted from the Pascal AST and executed by the VM.

The pipeline is:

```text
source -> lexer -> parser -> AST -> bytecode -> VM
```

The bytecode is intentionally higher-level than raw machine code. It is designed to be:

- easy to emit from the AST
- easy to read while debugging
- simple for the VM to execute


## Execution Model

The VM is a stack machine.

- literal values are pushed onto the stack
- most operations pop their operands from the stack
- most operations push a result back onto the stack
- variables live in VM-managed scopes / frames
- control flow uses labels and jumps


## Program Shape

A compiled program is a sequence of instructions, one per line.

Example:

```asm
PUSH_INT 2
PUSH_INT 3
PUSH_INT 4
MUL
ADD
STORE x
HALT
```


## Operand Conventions

- integers use decimal form: `PUSH_INT 42`
- reals use decimal form: `PUSH_REAL 3.14`
- booleans use uppercase literals: `PUSH_BOOL TRUE`, `PUSH_BOOL FALSE`
- strings are emitted quoted using Python-style `repr(...)`: `PUSH_STR 'hello'`
- variable references use names for now: `LOAD x`, `STORE x`
- labels end with `:`


## Instruction Set

### Data

```text
PUSH_INT <int>
PUSH_REAL <real>
PUSH_BOOL TRUE|FALSE
PUSH_STR <quoted-string>
LOAD <name>
STORE <name>
POP
```

Meaning:

- `PUSH_*` pushes a literal onto the stack
- `LOAD name` pushes the current value of `name`
- `STORE name` pops the top of the stack into `name`
- `POP` discards the top of the stack


### Arithmetic

```text
ADD
SUB
MUL
DIV
IDIV
NEG
```

Meaning:

- `ADD`: pop `b`, pop `a`, push `a + b`
- `SUB`: pop `b`, pop `a`, push `a - b`
- `MUL`: pop `b`, pop `a`, push `a * b`
- `DIV`: pop `b`, pop `a`, push `a / b`
- `IDIV`: pop `b`, pop `a`, push `a // b`
- `NEG`: pop `a`, push `-a`

Notes:

- division-by-zero is a VM runtime error
- `DIV` is real division
- `IDIV` is integer division


### Comparison

```text
EQ
NEQ
LT
LTE
GT
GTE
```

Meaning:

- `EQ`: pop `b`, pop `a`, push `a == b`
- `NEQ`: pop `b`, pop `a`, push `a != b`
- `LT`: pop `b`, pop `a`, push `a < b`
- `LTE`: pop `b`, pop `a`, push `a <= b`
- `GT`: pop `b`, pop `a`, push `a > b`
- `GTE`: pop `b`, pop `a`, push `a >= b`


### Control Flow

```text
LABEL <name>
JMP <label>
JMP_IF_FALSE <label>
HALT
```

Meaning:

- `LABEL name` marks a jump target
- `JMP label` unconditionally jumps to `label`
- `JMP_IF_FALSE label` pops a condition and jumps if it is false
- `HALT` stops execution

Label syntax may also be rendered as:

```text
loop_start:
```

If that form is used, the VM/parser should treat it the same as a label declaration.


### Procedures and Functions

```text
CALL <name>
RET
```

Meaning:

- `CALL name` invokes a procedure or function
- `RET` returns to the caller

Expected VM behavior:

- create a new frame for the call
- bind arguments to parameters
- preserve a return address
- on function return, leave the return value on the stack

This instruction set is intentionally higher-level than raw `JMP` because calls need frame setup and return handling.


### IO

```text
WRITE
WRITELN
```

Meaning:

- `WRITE` pops one value and prints it without a newline
- `WRITELN` pops one value and prints it with a newline


## AST Lowering Rules

### Literals

```pascal
42
```

becomes:

```asm
PUSH_INT 42
```

```pascal
3.5
```

becomes:

```asm
PUSH_REAL 3.5
```

### Variables

```pascal
x
```

becomes:

```asm
LOAD x
```

### Assignment

```pascal
x := 2 + 3;
```

becomes:

```asm
PUSH_INT 2
PUSH_INT 3
ADD
STORE x
```

### Unary Operators

```pascal
-x
```

becomes:

```asm
LOAD x
NEG
```

### Comparisons

```pascal
x < 10
```

becomes:

```asm
LOAD x
PUSH_INT 10
LT
```

### If Statement

```pascal
IF x < 10 THEN
    WRITELN(x);
```

can become:

```asm
LOAD x
PUSH_INT 10
LT
JMP_IF_FALSE if_end_1
LOAD x
WRITELN
LABEL if_end_1
```

### While Loop

```pascal
WHILE x < 10 DO
    x := x + 1;
```

can become:

```asm
LABEL while_start_1
LOAD x
PUSH_INT 10
LT
JMP_IF_FALSE while_end_1
LOAD x
PUSH_INT 1
ADD
STORE x
JMP while_start_1
LABEL while_end_1
```


## Scope Model

The emitter does not resolve runtime values directly.

- the semantic analyser checks whether a variable is valid in the current lexical scope
- the bytecode emitter emits symbolic instructions such as `LOAD x` and `STORE x`
- the VM resolves those names against its current frame / scope stack at runtime

This keeps the compiler simple while the VM is still name-based.

A later optimization could replace named variables with slots such as:

```text
LOAD_LOCAL 0
STORE_LOCAL 0
LOAD_GLOBAL 2
```


## Errors

Bytecode/VM execution errors should raise `BytecodeError`.

Examples:

- loading an undefined variable
- storing to an invalid target
- division by zero
- jumping to an unknown label
- stack underflow
- invalid operand types for an instruction


## Current Direction

The current design target is a mid-level VM instruction set:

- expressions are stack-based
- control flow is explicit with jumps
- procedures/functions use `CALL` and `RET`
- variables are name-based for now

This is a good balance between simplicity and realism for the interpreter-to-VM transition.
