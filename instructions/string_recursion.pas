PROGRAM string_recursion;
PROCEDURE Recurse(str : STRING; depth : INTEGER);
    BEGIN
        WRITELN(str + 'a');
        IF depth > 0 THEN
            Recurse(str+'a', depth - 1);
    END;

BEGIN 
    Recurse('',5);
END.
    
