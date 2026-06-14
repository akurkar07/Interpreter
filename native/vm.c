#include "vm.h"

#include <stdlib.h>
#include <string.h>

char *copy_string(const char *text) {
    size_t length = strlen(text) + 1;
    char *copy = malloc(length);
    if (copy == NULL) {
        return NULL;
    }
    memcpy(copy, text, length);
    return copy;
}

bool strinlist(const char *str, const char *strlist[], int count)
{
    for (int i = 0; i < count; i++) {
        if (strcmp(str, strlist[i]) == 0) return true;
    }
    return false;
}

void load_instructions(VM *vm, FILE *fp) {
    char line[256];
    while (fgets(line, 256, fp))
    {
        Instruction instruction;
        char *opcode = strtok(line, " \t\n");
        char *operand = strtok(NULL, " \t\n");

        if (opcode == NULL) continue;

        if (vm->instruction_count >= VM_INSTRUCTION_MAX) {
            fprintf(stderr, "Error: too many instructions\n");
            exit(1);
        }

        instruction.opcode = copy_string(opcode);

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

Value parse_instruction(Instruction instruction)
{
    char *opcode = instruction.opcode;
    char *operand = instruction.operand;
    Value value;
    if (strcmp(opcode, "PUSH_INT") == 0)
    {
        value.type = VAL_INT;
        value.as.integer = strtol(operand, NULL, 10);
    }
    if (strcmp(opcode, "PUSH_REAL") == 0)
    {
        value.type = VAL_REAL;
        value.as.real = strtod(operand, NULL);
    }
    if (strcmp(opcode, "PUSH_BOOL") == 0)
    {
        value.type = VAL_BOOL;
        value.as.boolean = strcmp(operand, "TRUE") == 0;
    }
    if (strcmp(opcode, "PUSH_STR") == 0)
    {
        value.type = VAL_STRING;
        value.as.string = operand;
    }
    return value;
}

Value pop_value(VM *vm)
{
    if (vm->stack_count <= 0) 
    {
        fprintf(stderr, "Error: Stack Underflow");
        exit(1);
    }
    vm->stack_count--;
    return vm->stack[vm->stack_count];
}

void push_value(VM *vm, Value value)
{
    if (vm->stack_count >= VM_STACK_MAX)
    {
        fprintf(stderr, "Error: Stack Overflow");
        exit(1);
    }
    vm->stack[vm->stack_count] = value;
    vm->stack_count++;
}

void execute(VM *vm)
{
    while (vm->pc < vm->instruction_count)
    {
        Instruction instruction = vm->instructions[vm->pc];
        char *opcode = instruction.opcode;
        char *operand = instruction.operand;

        if (!strinlist(opcode, INSTRUCTION_SET, INSTRUCTION_SET_COUNT))
        {
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "LABEL") == 0)
        {
            vm->pc++;
            continue;
        }

        if (strinlist(opcode, PUSH_OPS, PUSH_OPS_COUNT))
        {
            Value value = parse_instruction(instruction);
            push_value(vm, value);
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "LOAD") == 0)
        {
            // TODO: self.stack.append(self.load_name(operand))
            push_value(vm, );
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "STORE") == 0)
        {
            // TODO: self.store_name(operand, self.pop_value())
            (void)operand;
            vm->pc++;
            continue;
        }

        if (strinlist(opcode, ARITHMETIC_OPS, ARITHMETIC_OPS_COUNT))
        {
            Value right = pop_value(vm);
            Value left = pop_value(vm);
            push_value(vm, result);
            vm->pc++;
            continue;
        }

        if (strinlist(opcode, COMPARATOR_OPS, COMPARATOR_OPS_COUNT))
        {
            Value right = pop_value(vm);
            Value left = pop_value(vm);
            push_value(vm, result);
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "NEG") == 0)
        {
            // TODO: self.stack.append(-self.pop_value())
            Value value = pop_value(vm);
            if (value.type == VAL_INT) {}
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "WRITE") == 0)
        {
            // TODO: print(self.pop_value(), end="")
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "WRITELN") == 0)
        {
            // TODO: print(self.pop_value())
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "JMP") == 0)
        {
            // TODO: self.jump_to_label(operand)
            (void)operand;
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "JMP_IF_FALSE") == 0)
        {
            Value condition = pop_value(vm);
            if (condition.as.boolean == false)
            {
                // self.jump_to_label(operand)
            }
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "CALL") == 0)
        {
            // TODO: push a frame with return_pc = vm->pc + 1, then jump to label.
            (void)operand;
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "RET") == 0)
        {
            // TODO: pop frame and restore return_pc, or return if no caller.
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "HALT") == 0) return;

        vm->pc++;
    }
}

int main(int argc, char **argv) {

    if (argc != 2)
    {
        fprintf(stderr, "Error: Incorrect number of arguments\n");
        return 1;
    }

    FILE *bytecode_file = fopen(argv[1],"r");
    if (!bytecode_file)
    {
        fprintf(stderr, "Error: Could not open bytecode file '%s'\n", argv[1]);
        return 1;
    }

    VM *vm = malloc(sizeof(VM));
    if (vm == NULL)
    {
        fprintf(stderr, "Error: out of memory while creating VM\n");
        fclose(bytecode_file);
        return 1;
    }

    vm->pc = 0;
    vm->stack_count = 0;
    vm->instruction_count = 0;
    load_instructions(vm, bytecode_file);
    fclose(bytecode_file);

    execute(vm);

    for (int i = 0; i < vm->instruction_count; i++)
    {
        free(vm->instructions[i].opcode);
        free(vm->instructions[i].operand);
    }
    free(vm);
    return 0;
}
