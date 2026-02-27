from interpreter import Interpreter
from SemanticAnalyser import SemanticAnalyser
from tokens import GLOBAL_SCOPE, LexerError, ParserError, InterpreterError
from Lexer import Lexer
from Parser import Parser

def main():
    readExternalInstructions = True
    while True:
        try:
            if readExternalInstructions: # Runs the instructions file first then forms a CLI
                with open("instructions.txt", "r", encoding="utf-8") as instructionFile:
                    lines = instructionFile.readlines()
                    text = "".join(lines)
                readExternalInstructions = False
            else:
                text = input("> ")
                if text == ":q":
                    print("Quitting")
                    quit()
            lexer = Lexer(text)                         # Creates a lexer object with the input text
            parser = Parser(lexer)                      # Creates a parser with the lexer
            AST = parser.parse()                        # Parses the input and returns the root of the AST
            print(f"Running {AST.name.name}...")        # Prints the name of the procedure being run (TEMPORARY)
            
            semAnalyser = SemanticAnalyser()
            semAnalyser.visit(AST)

            interpreter = Interpreter()                     # Creates a visitor object
            result = interpreter.visit(AST)                 # Visits the AST and returns the result of the program              
            
            print("GLOBAL_SCOPE:", GLOBAL_SCOPE)
            print("SYMBOL_TABLE:", semAnalyser.symtab)
        except (LexerError, ParserError, InterpreterError) as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()