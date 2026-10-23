PROGRAM globals;
VAR
    counter : INTEGER;
    greeting : STRING;

PROCEDURE ShowGlobals(depth : INTEGER);
    BEGIN
        WRITELN(greeting);
        WRITELN(counter + depth);
        IF depth > 0 THEN
            ShowGlobals(depth - 1);
    END;

FUNCTION AddToCounter(n : INTEGER) : INTEGER;
    BEGIN
        AddToCounter := counter + n;
    END;

BEGIN
    counter := 10;
    greeting := 'reading a global from inside a procedure';
    ShowGlobals(2);
    WRITELN(AddToCounter(5));
END.
