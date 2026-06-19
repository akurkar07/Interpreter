#include "bytecode_loader.h"

#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static char *copy_string(const char *text)
{
    size_t length = strlen(text) + 1;
    char *copy = malloc(length);
    if (copy == NULL) return NULL;
    memcpy(copy, text, length);
    return copy;
}

static char *trim_whitespace(char *text)
{
    char *end;

    while (isspace((unsigned char)*text)) text++;
    if (*text == '\0') return text;

    end = text + strlen(text) - 1;
    while (end > text && isspace((unsigned char)*end)) end--;
    end[1] = '\0';

    return text;
}

static char *copy_unquoted_string(const char *text)
{
    size_t length = strlen(text);
    char quote = text[0];
    bool quoted = length >= 2
        && (quote == '\'' || quote == '"')
        && text[length - 1] == quote;

    if (!quoted) return copy_string(text);

    char *copy = malloc(length - 1);
    if (copy == NULL) return NULL;

    size_t out = 0;
    for (size_t i = 1; i < length - 1; i++) {
        if (text[i] == '\\' && i + 1 < length - 1) {
            i++;
            switch (text[i]) {
            case '\\':
            case '\'':
            case '"':
                copy[out++] = text[i];
                break;
            default:
                copy[out++] = '\\';
                copy[out++] = text[i];
                break;
            }
        } else {
            copy[out++] = text[i];
        }
    }

    copy[out] = '\0';
    return copy;
}

void load_instructions(VM *vm, FILE *fp)
{
    char line[256];
    while (fgets(line, 256, fp)) {
        Instruction instruction;
        char *opcode = trim_whitespace(line);
        char *operand = NULL;
        char *cursor = opcode;

        while (*cursor != '\0' && !isspace((unsigned char)*cursor)) cursor++;
        if (*cursor != '\0') {
            *cursor = '\0';
            operand = trim_whitespace(cursor + 1);
            if (*operand == '\0') operand = NULL;
        }

        if (*opcode == '\0') continue;

        if (vm->instruction_count >= VM_INSTRUCTION_MAX) {
            fprintf(stderr, "Error: too many instructions\n");
            exit(1);
        }

        instruction.opcode = copy_string(opcode);

        if (operand != NULL && strcmp(opcode, "PUSH_STR") == 0) {
            instruction.operand = copy_unquoted_string(operand);
        } else if (operand != NULL) {
            instruction.operand = copy_string(operand);
        } else {
            instruction.operand = NULL;
        }

        if (instruction.opcode == NULL || (operand != NULL && instruction.operand == NULL)) {
            fprintf(stderr, "Error: out of memory while loading instructions\n");
            free(instruction.opcode);
            free(instruction.operand);
            exit(1);
        }

        vm->instructions[vm->instruction_count] = instruction;

        if (strcmp(instruction.opcode, "LABEL") == 0 && instruction.operand != NULL) {
            if (vm->label_count >= VM_LABEL_MAX) {
                fprintf(stderr, "Error: too many labels\n");
                exit(1);
            }

            vm->labels[vm->label_count].name = instruction.operand;
            vm->labels[vm->label_count].instruction_index = vm->instruction_count;
            vm->label_count++;
        }

        vm->instruction_count++;
    }
}
