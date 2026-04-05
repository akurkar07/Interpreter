PROGRAM recursion;
FUNCTION Factorial(n : INTEGER) : INTEGER;
    BEGIN
        IF n = 1 THEN Factorial := 1
        ELSE Factorial := n * Factorial(n - 1);
    END;

BEGIN 
    WRITELN(Factorial(5));
END.
    
