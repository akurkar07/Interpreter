PROGRAM triangle;

VAR
    n, r, limit, spaces : INTEGER;

FUNCTION factorial(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN
        factorial := 1
    ELSE
        factorial := n * factorial(n - 1);
END;

FUNCTION choose(n, r : INTEGER) : INTEGER;
BEGIN
    choose := factorial(n) DIV (factorial(n - r) * factorial(r));
END;

BEGIN
    limit := 10;

    FOR n := 0 TO limit - 1 DO
    BEGIN
        FOR spaces := 0 TO limit - n - 1 DO
            WRITE(' ');

        FOR r := 0 TO n DO
        BEGIN
            WRITE(choose(n, r));
            WRITE(' ');
        END;

        WRITELN('');
    END;
END.
