## From Interpreter to Compiler: Bytecode and Virtual Machine Design

### 1. Introduction

This project extends a Pascal-style interpreter into a compiler by introducing an intermediate representation in the form of **stack-based bytecode** and executing it using a **Virtual Machine (VM)**. The goal is to separate *program structure* from *execution*, enabling a more realistic compiler architecture.

---

### 2. Current Interpreter Architecture

The existing interpreter follows the standard pipeline:

```text
Source Code → Lexer → Parser → AST → Evaluator
```

The evaluator traverses the Abstract Syntax Tree (AST) and directly computes results. While simple, this tightly couples parsing and execution.

---

### 3. Transition to a Compiler

To evolve into a compiler, execution is no longer performed directly on the AST. Instead, the AST is translated into a lower-level representation:

```text
Source Code → Lexer → Parser → AST → Bytecode → Execution
```

This introduces a clear separation between **analysis** and **execution**.

---

### 4. Stack-Based Bytecode Design

The compiler targets a **stack machine model**, where operations are performed on an implicit stack rather than registers.

#### Example

Given the Pascal expression:

```pascal
x := 2 + 3 * 4;
```

The AST is translated into bytecode:

```asm
PUSH_INT 2
PUSH_INT 3
PUSH_INT 4
MUL
ADD
STORE x
```

Execution proceeds by pushing values onto a stack and applying operations in sequence.

#### Characteristics

* Instructions operate on a stack
* No explicit registers required
* Naturally aligns with recursive AST traversal
* Equivalent to structured postfix notation for expressions

---

### 5. Instruction Set

A minimal instruction set includes:

**Data operations**

```text
PUSH_INT n
PUSH_REAL n
LOAD name
STORE name
```

**Arithmetic**

```text
ADD, SUB, MUL, DIV, NEG
```

**Control**

```text
JMP, JMP_IF_FALSE, HALT
```

This set can be extended to support comparisons, procedures, and control flow.

#### Example Program

Given a Pascal-style program:

```pascal
PROGRAM Demo;
VAR
    x : INTEGER;

PROCEDURE PrintTwice(n : INTEGER);
BEGIN
    WRITELN(n);
    WRITELN(n);
END;

BEGIN
    x := 5;
    PrintTwice(x);
END.
```

One possible bytecode form is:

```asm
JMP main

LABEL proc_PrintTwice
STORE n
LOAD n
WRITELN
LOAD n
WRITELN
RET

LABEL main
PUSH_INT 5
STORE x
LOAD x
CALL proc_PrintTwice
HALT
```

This example shows a few important design choices:

* procedure bodies are emitted as labeled blocks
* the main program jumps over routine declarations at startup
* arguments are pushed by the caller before `CALL`
* parameters are bound by the callee using `STORE`
* a procedure ends with `RET`

#### Comprehensive Feature Showcase

The following program exercises the main language features currently supported by the interpreter:

* integer, real, boolean, and string literals
* arithmetic and unary operators
* comparisons
* `IF ... THEN ... ELSE`
* `WHILE`
* `FOR ... TO` and `FOR ... DOWNTO`
* `WRITE` and `WRITELN`
* procedures
* functions
* recursion

Pascal source:

```pascal
PROGRAM FeatureShowcase;
VAR
    x, y, i, result : INTEGER;
    r : REAL;
    cmp : BOOLEAN;
    s : STRING;

PROCEDURE CountDown(n : INTEGER);
BEGIN
    WRITELN(n);
    IF n > 0 THEN
        CountDown(n - 1)
    ELSE
        WRITELN(0);
END;

FUNCTION Adjust(a : INTEGER; b : INTEGER) : INTEGER;
VAR
    temp : INTEGER;
BEGIN
    temp := +(a * 2) + -(b DIV 2);
    IF temp >= 0 THEN
        Adjust := temp
    ELSE
        Adjust := 0;
END;

BEGIN
    x := 6;
    y := 3;
    r := 3.5;
    s := 'hi';
    cmp := TRUE;
    cmp := FALSE;
    cmp := x = y;
    cmp := x <> y;
    cmp := x < y;
    cmp := x <= y;
    cmp := x > y;
    cmp := x >= y;

    WRITE(s);
    WRITELN(s + '!');
    WRITELN(r);

    IF x > y THEN
        WRITELN(x)
    ELSE
        WRITELN(y);

    WHILE x > 0 DO
    BEGIN
        WRITE(x);
        x := x - 1;
    END;

    FOR i := 1 TO 3 DO
        WRITELN(i);

    FOR i := 3 DOWNTO 1 DO
        WRITELN(i);

    CountDown(2);
    result := Adjust(8, 3);
    WRITELN(result);
END.
```

One possible bytecode form is:

```asm
JMP main

LABEL proc_CountDown
STORE n
LOAD n
WRITELN
LOAD n
PUSH_INT 0
GT
JMP_IF_FALSE countdown_else_1
LOAD n
PUSH_INT 1
SUB
CALL proc_CountDown
JMP countdown_end_1
LABEL countdown_else_1
PUSH_INT 0
WRITELN
LABEL countdown_end_1
RET

LABEL func_Adjust
STORE b
STORE a
LOAD a
PUSH_INT 2
MUL
NOP
LOAD b
PUSH_INT 2
IDIV
NEG
ADD
STORE temp
LOAD temp
PUSH_INT 0
GTE
JMP_IF_FALSE adjust_else_1
LOAD temp
STORE Adjust
JMP adjust_end_1
LABEL adjust_else_1
PUSH_INT 0
STORE Adjust
LABEL adjust_end_1
LOAD Adjust
RET

LABEL main
PUSH_INT 6
STORE x
PUSH_INT 3
STORE y
PUSH_REAL 3.5
STORE r
PUSH_STR 'hi'
STORE s
PUSH_BOOL TRUE
STORE cmp
PUSH_BOOL FALSE
STORE cmp
LOAD x
LOAD y
EQ
STORE cmp
LOAD x
LOAD y
NEQ
STORE cmp
LOAD x
LOAD y
LT
STORE cmp
LOAD x
LOAD y
LTE
STORE cmp
LOAD x
LOAD y
GT
STORE cmp
LOAD x
LOAD y
GTE
STORE cmp

LOAD s
WRITE
LOAD s
PUSH_STR '!'
ADD
WRITELN
LOAD r
WRITELN

LOAD x
LOAD y
GT
JMP_IF_FALSE if_else_1
LOAD x
WRITELN
JMP if_end_1
LABEL if_else_1
LOAD y
WRITELN
LABEL if_end_1

LABEL while_start_1
LOAD x
PUSH_INT 0
GT
JMP_IF_FALSE while_end_1
LOAD x
WRITE
LOAD x
PUSH_INT 1
SUB
STORE x
JMP while_start_1
LABEL while_end_1

PUSH_INT 1
STORE i
LABEL for_to_start_1
LOAD i
PUSH_INT 3
LTE
JMP_IF_FALSE for_to_end_1
LOAD i
WRITELN
LOAD i
PUSH_INT 1
ADD
STORE i
JMP for_to_start_1
LABEL for_to_end_1

PUSH_INT 3
STORE i
LABEL for_down_start_1
LOAD i
PUSH_INT 1
GTE
JMP_IF_FALSE for_down_end_1
LOAD i
WRITELN
LOAD i
PUSH_INT 1
SUB
STORE i
JMP for_down_start_1
LABEL for_down_end_1

PUSH_INT 2
CALL proc_CountDown
PUSH_INT 8
PUSH_INT 3
CALL func_Adjust
STORE result
LOAD result
WRITELN
HALT
```

Notes:

* `CALL proc_CountDown` demonstrates recursive procedure calls
* `STORE b` then `STORE a` shows parameter binding for a two-argument call when arguments are pushed left-to-right
* `STORE Adjust` followed by `LOAD Adjust` models Pascal function return-by-assignment to the function's own name
* `NOP` appears here because the current unary-plus emitter treats unary `+` as a no-op
* label names such as `if_else_1` and `while_start_1` are illustrative rather than fixed

---

### 6. Virtual Machine Design

The bytecode is not directly executable by hardware. Instead, it is executed by a **Virtual Machine (VM)**.

#### Role of the VM

The VM acts as a **software-defined CPU**, responsible for:

* Maintaining a stack
* Managing program state (memory, variables)
* Executing bytecode instructions sequentially

#### Execution Model

The VM operates as a loop:

```text
Fetch → Decode → Execute → Repeat
```

Conceptually:

* **Fetch**: read instruction at program counter
* **Decode**: determine operation
* **Execute**: manipulate stack or memory
* **Advance**: move to next instruction

---

### 7. Compiler vs Interpreter

| Approach    | Execution Model               |
| ----------- | ----------------------------- |
| Interpreter | AST executed directly         |
| VM Compiler | AST → Bytecode → VM executes  |
| Native      | AST → Assembly → CPU executes |

The VM approach provides a middle ground between simplicity and realism.

---

### 8. Advantages of Using a VM

* Simplifies code generation
* Easier debugging (stack inspection)
* Decouples frontend (parsing) from backend (execution)
* Enables multiple backends (e.g. VM, ARM assembly)
* Closely mirrors real-world language runtimes (e.g. JVM, Python)

---

### 9. Future Work

Once the VM-based system is complete, the compiler can be extended to:

* Generate **AArch64 (ARM64) assembly**
* Support control flow (`IF`, `WHILE`)
* Implement procedures and function calls
* Introduce optimisation passes
* Replace the VM with native execution

---

### 10. Conclusion

By introducing bytecode and a virtual machine, the interpreter evolves into a true compiler pipeline. The VM acts as an abstraction layer, allowing programs to be executed independently of the original AST while laying the foundation for future native code generation.
