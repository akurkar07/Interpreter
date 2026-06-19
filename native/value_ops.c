#include "value_ops.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void runtime_error(const char *message)
{
    fprintf(stderr, "Error: %s\n", message);
    exit(1);
}

static bool is_number(Value value)
{
    return value.type == VAL_INT || value.type == VAL_REAL;
}

static bool has_real_operand(Value left, Value right)
{
    return left.type == VAL_REAL || right.type == VAL_REAL;
}

Value make_int(int value)
{
    Value result;
    result.type = VAL_INT;
    result.as.integer = value;
    return result;
}

Value make_real(double value)
{
    Value result;
    result.type = VAL_REAL;
    result.as.real = value;
    return result;
}

Value make_bool(bool value)
{
    Value result;
    result.type = VAL_BOOL;
    result.as.boolean = value;
    return result;
}

double value_as_number(Value value)
{
    if (value.type == VAL_INT) return value.as.integer;
    if (value.type == VAL_REAL) return value.as.real;

    runtime_error("expected a number");
    return 0;
}

Value add_values(Value left, Value right)
{
    if (left.type == VAL_STRING && right.type == VAL_STRING) {
        size_t left_length = strlen(left.as.string);
        size_t right_length = strlen(right.as.string);
        char *joined = malloc(left_length + right_length + 1);

        if (joined == NULL) {
            runtime_error("out of memory while concatenating strings");
        }

        memcpy(joined, left.as.string, left_length);
        memcpy(joined + left_length, right.as.string, right_length + 1);

        Value result;
        result.type = VAL_STRING;
        result.as.string = joined;
        return result;
    }

    if (!is_number(left) || !is_number(right)) {
        runtime_error("ADD expects two numbers or two strings");
    }

    if (has_real_operand(left, right)) {
        return make_real(value_as_number(left) + value_as_number(right));
    }

    return make_int(left.as.integer + right.as.integer);
}

Value sub_values(Value left, Value right)
{
    if (!is_number(left) || !is_number(right)) {
        runtime_error("SUB expects two numbers");
    }

    if (has_real_operand(left, right)) {
        return make_real(value_as_number(left) - value_as_number(right));
    }

    return make_int(left.as.integer - right.as.integer);
}

Value mul_values(Value left, Value right)
{
    if (!is_number(left) || !is_number(right)) {
        runtime_error("MUL expects two numbers");
    }

    if (has_real_operand(left, right)) {
        return make_real(value_as_number(left) * value_as_number(right));
    }

    return make_int(left.as.integer * right.as.integer);
}

Value div_values(Value left, Value right)
{
    if (!is_number(left) || !is_number(right)) {
        runtime_error("DIV expects two numbers");
    }

    if (value_as_number(right) == 0) {
        runtime_error("division by zero");
    }

    return make_real(value_as_number(left) / value_as_number(right));
}

Value idiv_values(Value left, Value right)
{
    if (left.type != VAL_INT || right.type != VAL_INT) {
        runtime_error("IDIV expects two integers");
    }

    if (right.as.integer == 0) {
        runtime_error("division by zero");
    }

    return make_int(left.as.integer / right.as.integer);
}

Value eq_values(Value left, Value right)
{
    if (is_number(left) && is_number(right)) {
        return make_bool(value_as_number(left) == value_as_number(right));
    }

    if (left.type != right.type) {
        return make_bool(false);
    }

    if (left.type == VAL_BOOL) {
        return make_bool(left.as.boolean == right.as.boolean);
    }

    if (left.type == VAL_STRING) {
        return make_bool(strcmp(left.as.string, right.as.string) == 0);
    }

    return make_bool(false);
}

Value neq_values(Value left, Value right)
{
    Value equal = eq_values(left, right);
    return make_bool(!equal.as.boolean);
}

Value lt_values(Value left, Value right)
{
    if (is_number(left) && is_number(right)) {
        return make_bool(value_as_number(left) < value_as_number(right));
    }

    if (left.type == VAL_STRING && right.type == VAL_STRING) {
        return make_bool(strcmp(left.as.string, right.as.string) < 0);
    }

    runtime_error("LT expects two numbers or two strings");
    return make_bool(false);
}

Value lte_values(Value left, Value right)
{
    if (is_number(left) && is_number(right)) {
        return make_bool(value_as_number(left) <= value_as_number(right));
    }

    if (left.type == VAL_STRING && right.type == VAL_STRING) {
        return make_bool(strcmp(left.as.string, right.as.string) <= 0);
    }

    runtime_error("LTE expects two numbers or two strings");
    return make_bool(false);
}

Value gt_values(Value left, Value right)
{
    if (is_number(left) && is_number(right)) {
        return make_bool(value_as_number(left) > value_as_number(right));
    }

    if (left.type == VAL_STRING && right.type == VAL_STRING) {
        return make_bool(strcmp(left.as.string, right.as.string) > 0);
    }

    runtime_error("GT expects two numbers or two strings");
    return make_bool(false);
}

Value gte_values(Value left, Value right)
{
    if (is_number(left) && is_number(right)) {
        return make_bool(value_as_number(left) >= value_as_number(right));
    }

    if (left.type == VAL_STRING && right.type == VAL_STRING) {
        return make_bool(strcmp(left.as.string, right.as.string) >= 0);
    }

    runtime_error("GTE expects two numbers or two strings");
    return make_bool(false);
}

const BinaryOperation ARITHMETIC_OPERATIONS[] = {
    {"ADD", add_values},
    {"SUB", sub_values},
    {"MUL", mul_values},
    {"DIV", div_values},
    {"IDIV", idiv_values},
};

const int ARITHMETIC_OPERATION_COUNT =
    sizeof(ARITHMETIC_OPERATIONS) / sizeof(ARITHMETIC_OPERATIONS[0]);

const BinaryOperation COMPARATOR_OPERATIONS[] = {
    {"EQ", eq_values},
    {"NEQ", neq_values},
    {"LT", lt_values},
    {"LTE", lte_values},
    {"GT", gt_values},
    {"GTE", gte_values},
};

const int COMPARATOR_OPERATION_COUNT =
    sizeof(COMPARATOR_OPERATIONS) / sizeof(COMPARATOR_OPERATIONS[0]);
