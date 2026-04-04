import sys
from pathlib import Path

from tokens import LexerError, ParserError, SemanticError, InterpreterError
from Lexer import Lexer
from Parser import Parser
from SemanticAnalyser import SemanticAnalyser
from interpreter import Interpreter

def run_path(path_str):
    path = Path(path_str)

    if path.is_file():
        if path.suffix in {".pas", ".txt"}:
            run_script(path)
            return
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}. Expected .pas or .txt")
 

    if path.is_dir():
        files = sorted(
            p for p in path.iterdir()
            if p.is_file() and p.suffix in {".pas", ".txt"}
        )

        if not files:
            print(f"No runnable scripts found in '{path}'")
            return

        for file_path in files:
            print(f"\n=== Running {file_path} ===")
            try:
                run_script(file_path)
            except (LexerError, ParserError, SemanticError, InterpreterError) as e:
                print(f"Error in {file_path}: {e}")
        return

    raise FileNotFoundError(f"Path not found: {path}")

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

def print_help():
    print("Commands:")
    print("  :help / :h           Show this help message")
    print("  :quit / :q           Quit")
    print("  :run <path>          Run a Pascal script file or directory")
    print("  <path>               Run a Pascal script file or directory")


def parse_command(raw):
    command = raw.strip()
    if not command:
        return None, None
    if command in (":help",":h"):
        return "help", None
    if command in (":quit",":q"):
        return "quit", None
    if command.startswith(":run "):
        path = command[5:].strip()
        return ("run", path) if path else (None, None)
    return "run", command


def main():
    print("="*24 + "\nAlex's PascalInterpreter\n" + "="*24)

    pending_path = sys.argv[1] if len(sys.argv) > 1 else None

    while True:
        if pending_path is None:
            try: 
                raw = input("\nscript> ")
            except KeyboardInterrupt: # CTRL + C
                continue
            except EOFError: # CTRL + Z
                print("Quitting due to EOFError")
                quit()

            action, path = parse_command(raw)

            if action is None:
                continue
            if action == "help":
                print_help()
                continue
            if action == "quit":
                print("Quitting")
                return
            pending_path = path

        try:
            run_path(pending_path)
        except (LexerError, ParserError, SemanticError, InterpreterError) as e: # MY ERRORS
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except OSError as e:                                                    # Can't find the file
            print(f"Error reading '{pending_path}': {e}")
        except KeyboardInterrupt:                                               # CTRL + C during execution
            print("\nExecution Cancelled")
        finally:
            pending_path = None


if __name__ == "__main__":
    main()
