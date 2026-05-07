from tokens import *
from visitor import NodeVisitor


class BytecodeVisitor(NodeVisitor):
    """Turns the AST returned from the parser into stack-based bytecode that the VM can execute"""
    def __init__(self):
        self.bytecode = ""
        self.label_count = 0

    def runtime_error(self, message, node):
        raise BytecodeError(message, node.line, node.column)

    def emit(self, line):
        self.bytecode += f"{line}\n"
        
    def visit_Program(self, node):
        self.emit("JMP __main\n")
        # expand self.visit(node.block) to avoid encoding main jump into every block
        for declaration in node.block.declarations: 
            self.visit(declaration)
        self.emit("LABEL __main")
        self.visit(node.block.compound_statement)
        self.emit("HALT")

    def visit_Assign(self, node):
        self.visit(node.right)
        self.emit(f"STORE {node.left.name}")

    def visit_ProcedureCall(self, node):
        for arg in node.params:
            self.visit(arg)

        self.emit(f"CALL {node.name}")

    def visit_FunctionCall(self, node):
        for arg in node.params:
            self.visit(arg)

        self.emit(f"CALL {node.name}")

    def visit_If(self, node):
        self.visit(node.condition) # push the boolean value of the condition
        else_label = f"else_{self.label_count}" # create the labels with the label number so they are distinct
        end_label = f"end_{self.label_count}"
        self.label_count += 1

        self.emit(f"JMP_IF_FALSE {else_label}")
        self.visit(node.true_statement)
        if node.false_statement is not None:
            self.emit(f"JMP {end_label}")
            self.emit(f"LABEL {else_label}")
            self.visit(node.false_statement)
            self.emit(f"LABEL {end_label}")
            return

        self.emit(f"LABEL {else_label}")
        
    def visit_While(self, node):
        start_label = f"start_{self.label_count}" # create the labels with the label number so they are distinct
        end_label = f"end_{self.label_count}"
        self.label_count += 1

        self.emit(f"LABEL {start_label}")
        self.visit(node.condition)
        self.emit(f"JMP_IF_FALSE {end_label}")
        self.visit(node.statement)
        self.emit(f"JMP {start_label}")
        self.emit(f"LABEL {end_label}")


    def visit_For(self, node):
        start_label = f"start_{self.label_count}" # create the labels with the label number so they are distinct
        end_label = f"end_{self.label_count}"
        self.label_count += 1

        self.visit(node.start_expr)
        self.emit(f"STORE {node.var.name}") # load the start expression into the iterator
        self.emit(f"LABEL {start_label}")
        self.emit(f"LOAD {node.var.name}")
        self.visit(node.end_expr)
        
        self.emit("LTE" if node.direction == TO else "GTE")
        self.emit(f"JMP_IF_FALSE {end_label}") # ends the loop
        self.visit(node.statement)

        self.emit(f"LOAD {node.var.name}") # load the iterator
        self.emit("PUSH_INT 1")
        self.emit("ADD" if node.direction == TO else "SUB") # TO increases iterator, DOWNTO decreases it
        self.emit(f"STORE {node.var.name}") # stores the iterator again

        self.emit(f"JMP {start_label}")
        self.emit(f"LABEL {end_label}")

    def visit_WriteLn(self, node):
        self.visit(node.expression)
        self.emit("WRITELN")

    def visit_Write(self, node):
        self.visit(node.expression)
        self.emit("WRITE")

    def visit_ProcDecl(self, node):
        self.emit(f"LABEL {node.name}")

        for param in reversed(node.params): # Params are reversed because they are pushed to the stack in the correct order so they need to popped in reverse
            self.emit(f"STORE {param.var_node.name}")

        self.visit(node.block) # emits the body of the procedure
        self.emit("RET\n") # returns nothing
    
    def visit_FuncDecl(self, node):
        self.emit(f"LABEL {node.name}")

        for param in reversed(node.params): # Params are reversed because they are pushed to the stack in the correct order so they need to popped in reverse
            self.emit(f"STORE {param.var_node.name}")

        self.visit(node.block) # emits the body of the function
        self.emit(f"LOAD {node.name}")
        self.emit("RET\n")
    
    BINARY_OPCODE_MAP = {
        PLUS: "ADD",
        MINUS: "SUB",
        MUL: "MUL",
        FLOAT_DIV: "DIV",
        INTEGER_DIV: "IDIV",
        EQUAL: "EQ",
        NOT_EQUAL: "NEQ",
        LESS_THAN: "LT",
        LESS_EQUAL: "LTE",
        GREATER_THAN: "GT",
        GREATER_EQUAL: "GTE",
    }

    def visit_BinaryOperation(self, node):
        self.visit(node.left)
        self.visit(node.right)

        opcode = self.BINARY_OPCODE_MAP.get(node.value)
        if opcode is not None:
            self.emit(opcode)
            return

        self.runtime_error(f"Unsupported binary operator: {node.value}", node)

    def visit_UnaryOperation(self, node):
        if node.child is not None:
            self.visit(node.child)

        if node.value == PLUS:
            self.emit("NOP") # No-Op since nothing changes, VM ignores
            # return childvalue
            return
        elif node.value == MINUS:
            self.emit("NEG")
            # return -childvalue
            return

        self.runtime_error(f"Unsupported unary operator: {node.value}", node)

    def visit_Var(self, node):
        self.emit(f"LOAD {node.name}")

    def visit_IntegerNode(self, node):
        self.emit(f"PUSH_INT {node.value}")

    def visit_RealNode(self, node):
        self.emit(f"PUSH_REAL {node.value}")

    def visit_BooleanNode(self, node):
        self.emit(f"PUSH_BOOL {'TRUE' if node.value else 'FALSE'}")

    def visit_StringNode(self, node):
        # uses repr() instead of str() to return the value of node.value
        self.emit(f"PUSH_STR {node.value!r}") 

