PROGRAM BooleanComparisons;
VAR
  a, b : INTEGER;
  x, y : REAL;
  eq_result, neq_result, lt_result, lte_result, gt_result, gte_result : BOOLEAN;

BEGIN
  a := 5;
  b := 10;
  x := 5.0;
  y := 10.5;

  eq_result := a = 5;
  neq_result := a <> b;
  lt_result := a < b;
  lte_result := x <= y;
  gt_result := y > x;
  gte_result := b >= 10;
END.
