import sys

from tokens import LexerError, ParserError, InterpreterError
from Lexer import Lexer
from Parser import Parser
from SemanticAnalyser import SemanticAnalyser
from interpreter import Interpreter


def run_script(path):
    with open(path, "r", encoding="utf-8") as instruction_file:
        text = instruction_file.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()
    print(f"Running {ast.name.name}...")

    sem_analyser = SemanticAnalyser()
    sem_analyser.visit(ast)

    interpreter = Interpreter()
    interpreter.visit(ast)

    print("GLOBAL_SCOPE:", interpreter.GLOBAL_SCOPE)
    print("SYMBOL_TABLE:", sem_analyser.symtab)


def parse_command(raw):
    command = raw.strip()
    if not command:
        return None, None
    if command == ":q":
        return "quit", None
    if command.startswith(":run "):
        path = command[5:].strip()
        return ("run", path) if path else (None, None)
    return "run", command


def main():
    print("Alex's PascalInterpreter")

    pending_path = sys.argv[1] if len(sys.argv) > 1 else None

    while True:
        if pending_path is None:
            raw = input("script> ")
            action, path = parse_command(raw)

            if action is None:
                continue
            if action == "quit":
                print("Quitting")
                return
            pending_path = path

        try:
            run_script(pending_path)
        except (LexerError, ParserError, InterpreterError) as e:
            print(f"Error: {e}")
        except OSError as e:
            print(f"Error reading '{pending_path}': {e}")
        finally:
            pending_path = None


if __name__ == "__main__":
    main()
