PROGRAM SyntaxTour;

CONST
  MaxCount = 5;
  Greeting = 'Hello';

TYPE
  Day = (Mon, Tue, Wed, Thu, Fri, Sat, Sun);

  IntArray = ARRAY[1..MaxCount] OF INTEGER;

  Person = RECORD
    Name : STRING;
    Age  : INTEGER;
  END;

VAR
  I, J, Sum : INTEGER;
  X, Y      : REAL;
  Done      : BOOLEAN;
  Today     : Day;
  Numbers   : IntArray;
  User      : Person;

PROCEDURE PrintNumber(N : INTEGER);
BEGIN
  WRITELN('Number = ', N);
END;

FUNCTION Square(N : INTEGER) : INTEGER;
BEGIN
  Square := N * N;
END;

BEGIN
  { Assignment }
  I := 1;
  J := 2;
  X := 3.5;
  Y := 4.0;
  Done := FALSE;
  Today := Wed;

  { Arithmetic }
  Sum := I + J * 3;
  X := X / Y;
  J := 17 DIV 3;

  { Comparison + boolean logic }
  IF (I < J) AND (X <= Y) THEN
    WRITELN('Condition was true')
  ELSE
    WRITELN('Condition was false');

  { While loop }
  WHILE I < MaxCount DO
  BEGIN
    WRITELN('I = ', I);
    I := I + 1;
  END;

  { Repeat until loop }
  REPEAT
    J := J - 1;
  UNTIL J = 0;

  { For loop }
  FOR I := 1 TO MaxCount DO
    Numbers[I] := Square(I);

  { Case statement }
  CASE Today OF
    Mon: WRITELN('Monday');
    Tue: WRITELN('Tuesday');
    Wed: WRITELN('Wednesday');
    Thu: WRITELN('Thursday');
    Fri: WRITELN('Friday');
    Sat: WRITELN('Saturday');
    Sun: WRITELN('Sunday');
  END;

  { Record usage }
  User.Name := 'Alex';
  User.Age := 30;
  WRITELN(User.Name, ' is ', User.Age);

  { Array access }
  FOR I := 1 TO MaxCount DO
    WRITELN('Numbers[', I, '] = ', Numbers[I]);

  { Procedure call }
  PrintNumber(Sum);
END.
