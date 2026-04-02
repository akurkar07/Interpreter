PROGRAM ControlFlowOutput;
VAR
  i, sum : INTEGER;
  keep_going : BOOLEAN;

BEGIN
  i := 1;
  sum := 0;
  keep_going := i <= 5;

  IF keep_going THEN
    WRITELN(i)
  ELSE
    WRITELN(0);

  WHILE i <= 5 DO
  BEGIN
    sum := sum + i;
    WRITELN(sum);
    i := i + 1;
  END;

  IF sum = 15 THEN
    WRITELN(sum)
  ELSE
    WRITELN(999);
END.
