#ifndef PASCAL_VM_H
#define PASCAL_VM_H

#include <stdbool.h>
#include <stdio.h>

#define VM_STACK_MAX 1024
#define VM_INSTRUCTION_MAX 4096

typedef struct {
    char *opcode;
    char *operand;
} Instruction;

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
    int pc;

    Value stack[VM_STACK_MAX];
    int stack_count;

    Instruction instructions[VM_INSTRUCTION_MAX];
    int instruction_count;

    // later:
    // labels
    // frames
} VM;

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

char *copy_string(const char *text);
bool strinlist(const char *str, const char *strlist[], int count);
void load_instructions(VM *vm, FILE *fp);
void execute(VM *vm);

#endif
