PROGRAM recursion;
PROCEDURE Recurse(depth : INTEGER);
    BEGIN
        WRITELN(depth);
        IF depth > 0 THEN
            Recurse(depth - 1);
    END;

BEGIN 
    Recurse(5);
END.
    
