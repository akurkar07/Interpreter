#include "bytecode_loader.h"
#include "vm.h"

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Error: Incorrect number of arguments\n");
        return 1;
    }

    FILE *bytecode_file = fopen(argv[1], "r");
    if (!bytecode_file) {
        fprintf(stderr, "Error: Could not open bytecode file '%s'\n", argv[1]);
        return 1;
    }

    VM *vm = malloc(sizeof(VM));
    if (vm == NULL) {
        fprintf(stderr, "Error: out of memory while creating VM\n");
        fclose(bytecode_file);
        return 1;
    }

    init_vm(vm);
    load_instructions(vm, bytecode_file);
    fclose(bytecode_file);

    execute(vm);
    free_vm(vm);
    free(vm);
    return 0;
}
