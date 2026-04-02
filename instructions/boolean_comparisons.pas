PROGRAM BooleanComparisons;
VAR
  a, b : INTEGER;
  passed_checks : INTEGER;
  x, y : REAL;
  eq_result, neq_result, lt_result, lte_result, gt_result, gte_result : BOOLEAN;

BEGIN
  a := 5;
  b := 10;
  x := 5.0;
  y := 10.5;
  passed_checks := 0;

  eq_result := a = 5;
  neq_result := a <> b;
  lt_result := a < b;
  lte_result := x <= y;
  gt_result := y > x;
  gte_result := b >= 10;

  IF eq_result THEN
    passed_checks := passed_checks + 1;

  IF neq_result THEN
    passed_checks := passed_checks + 1
  ELSE
    passed_checks := 999;

  IF lt_result THEN
    passed_checks := passed_checks + 1;

  IF lte_result THEN
    passed_checks := passed_checks + 1;

  IF gt_result THEN
    passed_checks := passed_checks + 1;

  IF gte_result THEN
    passed_checks := passed_checks + 1;

  IF a > b THEN
    passed_checks := 999
  ELSE
    passed_checks := passed_checks + 1;
END.
