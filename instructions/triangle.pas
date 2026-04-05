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
    n := 0;
    WHILE n < limit DO
    BEGIN
        spaces := 0;
        WHILE spaces < limit - n DO
        BEGIN
            WRITE(' ');
            spaces := spaces + 1;
        END;

        r := 0;
        WHILE r <= n DO
        BEGIN
            WRITE(choose(n, r));
            WRITE(' ');
            r := r + 1;
        END;

        WRITELN('');
        n := n + 1;
    END;
END.
