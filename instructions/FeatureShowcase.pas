PROGRAM FeatureShowcase;
VAR
    x, y, i, result : INTEGER;
    r : REAL;
    cmp : BOOLEAN;
    s : STRING;

PROCEDURE CountDown(n : INTEGER);
BEGIN
    WRITELN(n);
    IF n > 0 THEN
        CountDown(n - 1)
    ELSE
        WRITELN(0);
END;

FUNCTION Adjust(a : INTEGER; b : INTEGER) : INTEGER;
VAR
    temp : INTEGER;
BEGIN
    temp := +(a * 2) + -(b DIV 2);
    IF temp >= 0 THEN
        Adjust := temp
    ELSE
        Adjust := 0;
END;

BEGIN
    x := 6;
    y := 3;
    r := 3.5;
    s := 'hi';
    cmp := TRUE;
    cmp := FALSE;
    cmp := x = y;
    cmp := x <> y;
    cmp := x < y;
    cmp := x <= y;
    cmp := x > y;
    cmp := x >= y;

    WRITE(s);
    WRITELN(s + '!');
    WRITELN(r);

    IF x > y THEN
        WRITELN(x)
    ELSE
        WRITELN(y);

    WHILE x > 0 DO
    BEGIN
        WRITE(x);
        x := x - 1;
    END;

    FOR i := 1 TO 3 DO
        WRITELN(i);

    FOR i := 3 DOWNTO 1 DO
        WRITELN(i);

    CountDown(2);
    result := Adjust(8, 3);
    WRITELN(result);
END.