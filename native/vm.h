#ifndef PASCAL_VM_H
#define PASCAL_VM_H

#include <stdbool.h>

#define VM_STACK_MAX 1024
#define VM_INSTRUCTION_MAX 4096
#define VM_LABEL_MAX 1024
#define VM_FRAME_MAX 1024
#define VM_LOCALS_MAX 1024

typedef enum {
    VAL_INT,
    VAL_REAL,
    VAL_BOOL,
    VAL_STRING
} ValueType;

typedef struct {
    ValueType type;
    union {
        int integer;
        double real;
        bool boolean;
        char *string;
    } as;
} Value;

typedef struct {
    char *opcode;
    char *operand;
} Instruction;

typedef struct {
    char *name;
    int instruction_index;
} Label;

typedef struct {
    char *name;
    Value value;
} Local;

typedef struct {
    Local locals[VM_LOCALS_MAX];
    int local_count;
    int return_pc;
} Frame;

typedef struct {
    int pc;

    Value stack[VM_STACK_MAX];
    int stack_count;

    Instruction instructions[VM_INSTRUCTION_MAX];
    int instruction_count;

    Label labels[VM_LABEL_MAX];
    int label_count;

    Frame frames[VM_FRAME_MAX];
    int frame_count;
} VM;

typedef Value (*BinaryValueFn)(Value left, Value right);

typedef struct {
    const char *opcode;
    BinaryValueFn fn;
} BinaryOperation;

typedef enum {
    OP_JMP,
    OP_JMP_IF_FALSE,
    OP_LABEL,
    OP_HALT,
    OP_CALL,
    OP_RET,
    OP_LOAD,
    OP_STORE,
    OP_PUSH_INT,
    OP_PUSH_REAL,
    OP_PUSH_BOOL,
    OP_PUSH_STR,
    OP_WRITE,
    OP_WRITELN,
    OP_NEG,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_IDIV,
    OP_EQ,
    OP_NEQ,
    OP_LT,
    OP_LTE,
    OP_GT,
    OP_GTE
} Opcode;

static const char *INSTRUCTION_SET[] = {
    "JMP",
    "JMP_IF_FALSE",
    "LABEL",
    "HALT",
    "CALL",
    "RET",
    "LOAD",
    "STORE",
    "PUSH_INT",
    "PUSH_REAL",
    "PUSH_BOOL",
    "PUSH_STR",
    "WRITE",
    "WRITELN",
    "NEG",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "IDIV",
    "EQ",
    "NEQ",
    "LT",
    "LTE",
    "GT",
    "GTE"
};

static const int INSTRUCTION_SET_COUNT = sizeof(INSTRUCTION_SET) / sizeof(INSTRUCTION_SET[0]);

static const char *PUSH_OPS[] = {
    "PUSH_INT",
    "PUSH_REAL",
    "PUSH_BOOL",
    "PUSH_STR"
};

static const int PUSH_OPS_COUNT = sizeof(PUSH_OPS) / sizeof(PUSH_OPS[0]);

static const char *ARITHMETIC_OPS[] = {
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "IDIV"
};

static const int ARITHMETIC_OPS_COUNT = sizeof(ARITHMETIC_OPS) / sizeof(ARITHMETIC_OPS[0]);

static const char *COMPARATOR_OPS[] = {
    "EQ",
    "NEQ",
    "LT",
    "LTE",
    "GT",
    "GTE"
};

static const int COMPARATOR_OPS_COUNT = sizeof(COMPARATOR_OPS) / sizeof(COMPARATOR_OPS[0]);

int strinlist(const char *str, const char *strlist[], int count);
void init_vm(VM *vm);
void free_vm(VM *vm);
Value parse_instruction(Instruction instruction);
Value pop_value(VM *vm);
void push_value(VM *vm, Value value);
void execute(VM *vm);

#endif
