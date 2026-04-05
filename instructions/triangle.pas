PROGRAM triangle;

VAR
    n : INTEGER;
    r : INTEGER;
    
FUNCTION factorial(n : INTEGER) : INTEGER;
    BEGIN
        IF n <= 1 THEN Factorial := 1
        ELSE Factorial := n * Factorial(n - 1);
    END;

FUNCTION choose(n, r : INTEGER) : INTEGER;
    BEGIN
        choose := factorial(n) DIV (factorial(n - r) * factorial(r));
    END;

BEGIN 
    n := 0;
    WHILE n < 10 DO
    BEGIN
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
    
