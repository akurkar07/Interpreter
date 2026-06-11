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

void execute(VM *vm)
{
    while (vm->pc < vm->instruction_count)
    {
        char *opcode = vm->instructions[vm->pc].opcode;
        char *operand = vm->instructions[vm->pc].operand;

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
            // TODO: parse operand and push Value onto vm->stack.
            (void)operand;
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "LOAD") == 0)
        {
            // TODO: self.stack.append(self.load_name(operand))
            (void)operand;
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
            // TODO: pop right, pop left, apply arithmetic op, push result.
            vm->pc++;
            continue;
        }

        if (strinlist(opcode, COMPARATOR_OPS, COMPARATOR_OPS_COUNT))
        {
            // TODO: pop right, pop left, compare, push boolean result.
            vm->pc++;
            continue;
        }

        if (strcmp(opcode, "NEG") == 0)
        {
            // TODO: self.stack.append(-self.pop_value())
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
            // TODO: condition = self.pop_value()
            // TODO: if condition is false, self.jump_to_label(operand)
            (void)operand;
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
