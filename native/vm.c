#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
        int boolean;
        char *string;
    } as;
} Value;

typedef struct {
    int pc;

    Value stack[1024];
    int stack_count;

    Instruction instructions[4096];
    int instruction_count;

    // later:
    // labels
    // frames
} VM;

char *copy_string(const char *text) {
    size_t length = strlen(text) + 1;
    char *copy = malloc(length);
    if (copy == NULL) {
        return NULL;
    }
    memcpy(copy, text, length);
    return copy;
}

void load_instructions(VM *vm, FILE *fp) {
    // Placeholder for loading instructions into the VM
    
    char line[256];
    while (fgets(line, 256, fp))
    {
        Instruction instruction;
        char *opcode = strtok(line, " \t\n");
        char *operand = strtok(NULL, " \t\n");

        if (opcode == NULL) {
            continue;
        }

        if (vm->instruction_count >= 4096) {
            fprintf(stderr, "Error: too many instructions\n");
            exit(1);
        }

        instruction.opcode = copy_string(opcode); // malloc and string copy

        if (operand != NULL) instruction.operand = copy_string(operand); 
        else instruction.operand = NULL;

        if (instruction.opcode == NULL || (operand != NULL && instruction.operand == NULL)) {
            fprintf(stderr, "Error: out of memory while loading instructions\n");
            free(instruction.opcode);
            free(instruction.operand);
            exit(1);
        }
        
        vm->instructions[vm->instruction_count] = instruction;
        vm->instruction_count++;
    }
}

int main(int argc, char **argv) {

    if (argc != 2)
    {
        fprintf(stderr, "Error: Incorrect number of arguments");
        return 1;
    }

    FILE *bytecode_file = fopen(argv[1],"r");
    if (!bytecode_file)
    {
        fprintf(stderr, "Error: Could not open bytecode file '%s'\n", argv[1]);
        return 1;
    }

    VM *vm = malloc(sizeof(VM));
    vm->pc = 0;
    vm->stack_count = 0;
    vm->instruction_count = 0;
    load_instructions(vm, bytecode_file); // loads the instructions from the file into the vm struct
    fclose(bytecode_file); // since the bytecode is in the vm, we don't need the file anymore

    // VM CODE HERE

    for (int i = 0; i < vm->instruction_count; i++) printf("%s\n", vm->instructions[i].opcode);




    // CLEANUP

    for (int i = 0; i < vm->instruction_count; i++) // free all the instructions because they are strings allocated on the heap
    {
        free(vm->instructions[i].opcode);
        free(vm->instructions[i].operand);
    }
    free(vm); // free the vm itself
    return 0;
}
