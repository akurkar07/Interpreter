import sys
from pathlib import Path

from .tokens import LexerError, ParserError, SemanticError, InterpreterError, BytecodeError
from .Lexer import Lexer
from .Parser import Parser
from .SemanticAnalyser import SemanticAnalyser
from .interpreter import Interpreter
from .bytecode import BytecodeVisitor
from .vm import VirtualMachine

SOURCE_SUFFIXES = {".pas", ".txt"}
BYTECODE_SUFFIXES = {".pbc"}
ACTIONS_SUFFIXES = {
    "run": SOURCE_SUFFIXES,
    "compile": SOURCE_SUFFIXES,
    "vm": BYTECODE_SUFFIXES,
}
ACTION_LABELS = {
    "run": "Running",
    "compile": "Compiling",
    "vm": "Running on VM",
}


def execute_path(path_str, action):
    path = Path(path_str)
    handler = ACTION_HANDLERS.get(action)
    allowed_suffixes = ACTIONS_SUFFIXES.get(action)

    if handler is None or allowed_suffixes is None:
        raise ValueError(f"Unknown action: {action}")

    if path.is_file():
        if path.suffix in allowed_suffixes:
            handler(path)
            return
        expected = ", ".join(sorted(allowed_suffixes))
        raise ValueError(f"Unsupported file type: {path.suffix}. Expected {expected}")

    if path.is_dir():
        files = sorted(
            p for p in path.iterdir()
            if p.is_file() and p.suffix in allowed_suffixes
        )

        if not files:
            expected = ", ".join(sorted(allowed_suffixes))
            print(f"No matching {expected} files found in '{path}'")
            return

        for file_path in files:
            print(f"\n=== {ACTION_LABELS[action]} {file_path} ===")
            try:
                handler(file_path)
            except (LexerError, ParserError, SemanticError, InterpreterError, BytecodeError, NotImplementedError) as e:
                print(f"Error in {file_path}: {e}")
        return

    raise FileNotFoundError(f"Path not found: {path}")


def load_program(path):
    with open(path, "r", encoding="utf-8") as instruction_file:
        text = instruction_file.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    sem_analyser = SemanticAnalyser()
    sem_analyser.visit(ast)
    return ast


def run_script(path):
    ast = load_program(path)
    print(f"Running {ast.name.name}...")

    interpreter = Interpreter()
    interpreter.visit(ast)

    # print("GLOBAL_SCOPE:", interpreter.GLOBAL_SCOPE)
    # print("SYMBOL_TABLE:", sem_analyser.current_scope)


def compile_script(path):
    ast = load_program(path)
    bytecode_visitor = BytecodeVisitor()
    bytecode_visitor.visit(ast)
    output_path = path.with_suffix(".pbc")

    with open(output_path, "w", encoding="utf-8") as bytecode_file:
        bytecode_file.write(bytecode_visitor.bytecode)

    print(f"Wrote bytecode to {output_path}")


def run_vm_script(path):
    with open(path, "r", encoding="utf-8") as bytecode_file:
        _bytecode = bytecode_file.read()

    vm = VirtualMachine(_bytecode)
    vm.execute()
    


ACTION_HANDLERS = {
    "run": run_script,
    "compile": compile_script,
    "vm": run_vm_script,
}


def print_help():
    print("Commands:")
    print("  :help / :h           Show this help message")
    print("  :quit / :q           Quit")
    print("  :run <path>          Run a Pascal script file or directory")
    print("  :vm <path>           Run a bytecode file or directory (.pbc) in the VM")
    print("  :compile <path>      Emit a Pascal script or directory as bytecode without running it")
    print("  <path>               Run a Pascal script file or directory")


def parse_command(raw):
    command = raw.strip()
    if not command:
        return None, None

    aliases = {
        ":help": "help",
        ":h": "help",
        ":quit": "quit",
        ":q": "quit",
    }
    if command in aliases:
        return aliases[command], None

    if not command.startswith(":"):
        return "run", command

    verb, _, rest = command.partition(" ")
    path = rest.strip()

    if verb in {":run", ":compile", ":vm"} and path:
        return verb[1:], path

    return None, None


def main():
    print("="*24 + "\nAlex's PascalInterpreter\n" + "="*24)

    pending_action = "run"
    pending_path = sys.argv[1] if len(sys.argv) > 1 else None

    while True:
        if pending_path is None:
            try:
                raw = input("\nscript> ")
            except KeyboardInterrupt:  # CTRL + C
                continue
            except EOFError:  # CTRL + Z
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

            pending_action = action
            pending_path = path

        try:
            execute_path(pending_path, pending_action)
        except (LexerError, ParserError, SemanticError, InterpreterError, BytecodeError, NotImplementedError) as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except OSError as e:
            print(f"Error reading '{pending_path}': {e}")
        except KeyboardInterrupt:
            print("\nExecution Cancelled")
        finally:
            pending_action = "run"
            pending_path = None


if __name__ == "__main__":
    main()
