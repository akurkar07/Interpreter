#ifndef PASCAL_VALUE_OPS_H
#define PASCAL_VALUE_OPS_H

#include "vm.h"

Value make_int(int value);
Value make_real(double value);
Value make_bool(bool value);

double value_as_number(Value value);

Value add_values(Value left, Value right);
Value sub_values(Value left, Value right);
Value mul_values(Value left, Value right);
Value div_values(Value left, Value right);
Value idiv_values(Value left, Value right);

Value eq_values(Value left, Value right);
Value neq_values(Value left, Value right);
Value lt_values(Value left, Value right);
Value lte_values(Value left, Value right);
Value gt_values(Value left, Value right);
Value gte_values(Value left, Value right);

extern const BinaryOperation ARITHMETIC_OPERATIONS[];
extern const int ARITHMETIC_OPERATION_COUNT;
extern const BinaryOperation COMPARATOR_OPERATIONS[];
extern const int COMPARATOR_OPERATION_COUNT;

#endif
