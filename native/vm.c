#include "vm.h"
#include "value_ops.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int strinlist(const char *str, const char *strlist[], int count)
{
    for (int i = 0; i < count; i++) {
        if (strcmp(str, strlist[i]) == 0) return i;
    }
    return -1;
}

static void runtime_error(const char *message)
{
    fprintf(stderr, "Error: %s\n", message);
    exit(1);
}

void init_vm(VM *vm)
{
    vm->pc = 0;
    vm->stack_count = 0;
    vm->instruction_count = 0;
    vm->label_count = 0;

    vm->frame_count = 1;
    vm->frames[0].return_pc = -1;
    vm->frames[0].local_count = 0;
}

void free_vm(VM *vm)
{
    for (int i = 0; i < vm->instruction_count; i++) {
        free(vm->instructions[i].opcode);
        free(vm->instructions[i].operand);
    }
}

static void print_value(Value value)
{
    switch (value.type) {
    case VAL_INT:
        printf("%d", value.as.integer);
        break;
    case VAL_REAL:
        printf("%g", value.as.real);
        break;
    case VAL_BOOL:
        printf("%s", value.as.boolean ? "TRUE" : "FALSE");
        break;
    case VAL_STRING:
        printf("%s", value.as.string);
        break;
    default:
        runtime_error("unknown value type");
        break;
    }
}

static bool is_push_opcode(int opcode_index)
{
    return opcode_index >= OP_PUSH_INT && opcode_index <= OP_PUSH_STR;
}

static bool is_arithmetic_opcode(int opcode_index)
{
    return opcode_index >= OP_ADD && opcode_index <= OP_IDIV;
}

static bool is_comparator_opcode(int opcode_index)
{
    return opcode_index >= OP_EQ && opcode_index <= OP_GTE;
}

Frame *current_frame(VM *vm) // peeks the last frame added
{
    return &vm->frames[vm->frame_count - 1];
}

void jump_to_label(VM *vm, char *target)
{
    for (int i = 0; i < vm->label_count; i++)
    {
        Label label = vm->labels[i];
        if (strcmp(label.name, target) == 0) {
            vm->pc = label.instruction_index;
            return;
        }
    }

    runtime_error("unknown label");
}

Value load_name(VM *vm, char *name) // searches through the frames to find the value attached to a local's name
{
    for (int i = vm->frame_count - 1; i >= 0; i++) // searches through each frame
    {
        Frame frame = vm->frames[i];
        for (int j = 0; j < frame.local_count; j++) // for each local in frame
        {
            Local local = frame.locals[j];
            if (strcmp(name, local.name) == 0) return local.value;
        }
    }
    runtime_error("variable is not defined");
    return make_int(0); // here just so it "returns" something even though it never runs
}

void store_name(VM *vm, char *name, Value value)
{
    Frame *frame = current_frame(vm);
    if (frame->local_count >= VM_LOCALS_MAX)
    {
        fprintf(stderr, "Error: Local Frame Stack Overflow");
        exit(1);
    }
    for (int i = 0; i < frame->local_count; i++) // for each local in frame
        {
            Local *local = &frame->locals[i];
            if (strcmp(name, local->name) == 0)
            {
                local->name = name;
                local->value = value;
                return;
            }
        }
    frame->locals[frame->local_count].name = name;
    frame->locals[frame->local_count].value = value;
    frame->local_count++;
}

Value parse_instruction(Instruction instruction)
{
    char *opcode = instruction.opcode;
    char *operand = instruction.operand;
    int opcode_index = strinlist(opcode, INSTRUCTION_SET, INSTRUCTION_SET_COUNT);

    switch ((Opcode)opcode_index) {
    case OP_PUSH_INT:
        return make_int(strtol(operand, NULL, 10));
    case OP_PUSH_REAL:
        return make_real(strtod(operand, NULL));
    case OP_PUSH_BOOL:
        return make_bool(strcmp(operand, "TRUE") == 0);
    case OP_PUSH_STR: {
        Value value;
        value.type = VAL_STRING;
        value.as.string = operand;
        return value;
    }
    default:
        runtime_error("expected PUSH instruction");
        return make_int(0);
    }
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
        int opcode_index = strinlist(opcode, INSTRUCTION_SET, INSTRUCTION_SET_COUNT);

        if (opcode_index == -1) {
            vm->pc++;
            continue;
        }

        if (is_push_opcode(opcode_index)) {
            // PUSH_* pushes a literal value.
            Value value = parse_instruction(instruction);
            push_value(vm, value);
            vm->pc++;
            continue;
        }

        if (is_arithmetic_opcode(opcode_index)) {
            // Arithmetic ops pop two values and push the numeric result.
            int arithmetic_index = opcode_index - OP_ADD;
            BinaryValueFn operation = ARITHMETIC_OPERATIONS[arithmetic_index].fn;
            Value right = pop_value(vm);
            Value left = pop_value(vm);
            push_value(vm, operation(left, right));
            vm->pc++;
            continue;
        }

        if (is_comparator_opcode(opcode_index)) {
            // Comparison ops pop two values and push a boolean result.
            int comparator_index = opcode_index - OP_EQ;
            BinaryValueFn operation = COMPARATOR_OPERATIONS[comparator_index].fn;
            Value right = pop_value(vm);
            Value left = pop_value(vm);
            push_value(vm, operation(left, right));
            vm->pc++;
            continue;
        }

        // we can cast to Opcode because it's an enum that matches the index returned from opcode index to the opcodes
        switch ((Opcode)opcode_index) {
        case OP_LABEL:
            // LABEL marks a jump target and does nothing at runtime.
            vm->pc++;
            continue;

        case OP_LOAD:
            // LOAD pushes the current value of a variable.
            push_value(vm, load_name(vm, operand));
            vm->pc++;
            continue;

        case OP_STORE:
            // STORE pops a value into a variable.
            store_name(vm, operand, pop_value(vm));
            vm->pc++;
            continue;

        case OP_NEG: {
            // NEG pushes the numeric negation of the top stack value.
            Value value = pop_value(vm);
            switch (value.type) {
            case VAL_INT:
                push_value(vm, make_int(-value.as.integer));
                break;
            case VAL_REAL:
                push_value(vm, make_real(-value.as.real));
                break;
            default:
                runtime_error("NEG expects a number");
                break;
            }
            vm->pc++;
            continue;
        }

        case OP_WRITE:
            // WRITE pops and prints a value without a newline.
            print_value(pop_value(vm));
            vm->pc++;
            continue;

        case OP_WRITELN:
            // WRITELN pops and prints a value with a newline.
            print_value(pop_value(vm));
            printf("\n");
            vm->pc++;
            continue;

        case OP_JMP:
            // JMP moves execution to a label.
            jump_to_label(vm, operand);
            continue;

        case OP_JMP_IF_FALSE: {
            // JMP_IF_FALSE pops a condition and jumps if it is false.
            Value condition = pop_value(vm);
            if (condition.as.boolean == false) jump_to_label(vm, operand);
            else vm->pc++;
            continue;
        }

        case OP_CALL: {
            // CALL creates a call frame and jumps to a procedure/function.
            if (vm->frame_count >= VM_FRAME_MAX) {
                fprintf(stderr, "Error: Frame Stack Overflow");
                exit(1);
            }

            Frame frame;
            frame.local_count = 0;
            frame.return_pc = vm->pc + 1;
            vm->frames[vm->frame_count] = frame;
            vm->frame_count++;
            jump_to_label(vm, operand);
            continue;
        }

        case OP_RET: {
            // RET returns to the caller or stops if there is no caller.
            Frame *frame = current_frame(vm);
            int return_pc = frame->return_pc;
            vm->frame_count--;

            if (return_pc == -1) return; // ret from global finishes execute
            vm->pc = return_pc;
            continue;
        }

        case OP_HALT:
            // HALT stops execution.
            return;

        default:
            // Unknown opcodes are ignored for now.
            vm->pc++;
            continue;
        }
    }
}
