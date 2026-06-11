import shlex

from .tokens import BytecodeError

INSTRUCTION_SET = [
    "JMP",
    "JMP_IF_FALSE",
    "LABEL",
    "HALT",
    "CALL",
    "RET",
    "LOAD",
    "STORE",
    "PUSH_INT",
    "PUSH_REAL",
    "PUSH_BOOL",
    "PUSH_STR",
    "WRITE",
    "WRITELN",
    "NEG",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "IDIV",
    "EQ",
    "NEQ",
    "LT",
    "LTE",
    "GT",
    "GTE",
]

COMPARATOR_OPS = {
    "EQ": lambda left, right: left == right,
    "NEQ": lambda left, right: left != right,
    "LT": lambda left, right: left < right,
    "LTE": lambda left, right: left <= right,
    "GT": lambda left, right: left > right,
    "GTE": lambda left, right: left >= right,
}

ARITHMETIC_OPS = {
    "ADD": lambda left, right: left + right,
    "SUB": lambda left, right: left - right,
    "MUL": lambda left, right: left * right,
    "DIV": lambda left, right: left / right,
    "IDIV": lambda left, right: left // right,
}


class VirtualMachine:
    def __init__(self, bytecode):
        self.pc = 0
        self.stack = []
        self.instructions = []
        self.labels = {}
        self.frames = [{"locals": {}, "return_pc": None}]
        self.load_instructions(bytecode)

    def load_instructions(self, bytecode):
        for raw_line in bytecode.splitlines():
            # shlex keeps quoted operands like PUSH_STR 'hello world' together
            # so string literals with spaces are parsed as one operand.
            parts = shlex.split(raw_line)
            if not parts:
                continue

            opcode = parts[0]
            operand = parts[1] if len(parts) > 1 else None
            self.instructions.append((opcode, operand))

            if opcode == "LABEL" and operand is not None:
                self.labels[operand] = len(self.instructions) - 1

    def current_frame(self):
        return self.frames[-1]["locals"]

    def parse_operand(self, opcode, operand):
        if opcode == "PUSH_INT":
            return int(operand)
        if opcode == "PUSH_REAL":
            return float(operand)
        if opcode == "PUSH_BOOL":
            return operand == "TRUE"
        if opcode == "PUSH_STR":
            return operand
        return operand

    def pop_value(self):
        if not self.stack:
            raise BytecodeError("Stack underflow")
        return self.stack.pop()

    def jump_to_label(self, label):
        target = self.labels.get(label)
        if target is None:
            raise BytecodeError(f"Unknown label: {label}")
        self.pc = target

    def load_name(self, name):
        for frame in reversed(self.frames):
            if name in frame["locals"]:
                return frame["locals"][name]
        raise BytecodeError(f"Variable {name} is not defined")

    def store_name(self, name, value):
        self.current_frame()[name] = value

    def execute(self):
        while self.pc < len(self.instructions):
            opcode, operand = self.instructions[self.pc]

            if opcode not in INSTRUCTION_SET:
                self.pc += 1
                continue

            if opcode == "LABEL":
                self.pc += 1
                continue

            if opcode in ("PUSH_INT", "PUSH_REAL", "PUSH_BOOL", "PUSH_STR"):
                self.stack.append(self.parse_operand(opcode, operand))
                self.pc += 1
                continue

            if opcode == "LOAD":
                self.stack.append(self.load_name(operand))
                self.pc += 1
                continue

            if opcode == "STORE":
                self.store_name(operand, self.pop_value())
                self.pc += 1
                continue

            if opcode in ARITHMETIC_OPS:
                right = self.pop_value()
                left = self.pop_value()
                if opcode in ("DIV", "IDIV") and right == 0:
                    raise BytecodeError("Division by zero")
                self.stack.append(ARITHMETIC_OPS[opcode](left, right))
                self.pc += 1
                continue

            if opcode in COMPARATOR_OPS:
                right = self.pop_value()
                left = self.pop_value()
                self.stack.append(COMPARATOR_OPS[opcode](left, right))
                self.pc += 1
                continue

            if opcode == "NEG":
                self.stack.append(-self.pop_value())
                self.pc += 1
                continue

            if opcode == "WRITE":
                print(self.pop_value(), end="")
                self.pc += 1
                continue

            if opcode == "WRITELN":
                print(self.pop_value())
                self.pc += 1
                continue

            if opcode == "JMP":
                self.jump_to_label(operand)
                continue

            if opcode == "JMP_IF_FALSE":
                condition = self.pop_value()
                if not condition:
                    self.jump_to_label(operand)
                    continue
                self.pc += 1
                continue

            if opcode == "CALL":
                self.frames.append({
                    "locals": {},
                    "return_pc": self.pc + 1,
                })
                self.jump_to_label(operand)
                continue

            if opcode == "RET":
                frame = self.frames.pop()
                if frame["return_pc"] is None:
                    return
                self.pc = frame["return_pc"]
                continue

            if opcode == "HALT":
                return

            self.pc += 1
