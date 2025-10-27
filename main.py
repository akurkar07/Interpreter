from tokens import GLOBAL_SCOPE, LexerError, ParserError, InterpreterError
from Lexer import Lexer
from Parser import Parser
from tokens import GLOBAL_SCOPE, SYMBOL_TABLE

def main():
    readExternalInstructions = True
    while True:
        try:
            if readExternalInstructions: # Runs the instructions file first then forms a CLI
                with open("instructions.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    text = "".join(lines)
                readExternalInstructions = False
            else:
                text = input("> ")
                if text == "q":
                    print("Quitting")
                    quit()
            lexer = Lexer(text)
            parser = Parser(lexer)
            AST = parser.parse()
            result = AST.visit()
            print(result)
            print("GLOBAL_SCOPE:", GLOBAL_SCOPE)
            print("SYMBOL_TABLE:", SYMBOL_TABLE)
        except (LexerError, ParserError, InterpreterError) as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()