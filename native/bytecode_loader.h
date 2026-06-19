#ifndef PASCAL_BYTECODE_LOADER_H
#define PASCAL_BYTECODE_LOADER_H

#include "vm.h"

#include <stdio.h>

void load_instructions(VM *vm, FILE *fp);

#endif
