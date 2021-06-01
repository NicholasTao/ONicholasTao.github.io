import ast
from textwrap import dedent


def to_procedure(code):
    module = ast.parse(dedent("""\
    def _bf():
        from sys import stdout as output, stdin as input
        from collections import defaultdict
        data_ptr, memory = 0, defaultdict(int)
    """))
    instructions, instruction_stack = [], []
    _parse_node = lambda exp: ast.parse(exp).body[0]
    for char in code:
        if char == ">":
            instructions.append(_parse_node("data_ptr += 1"))
        elif char == "<":
            instructions.append(_parse_node("data_ptr -= 1"))
        elif char == "+":
            instructions.append(_parse_node("memory[data_ptr] += 1"))
        elif char == "-":
            instructions.append(_parse_node("memory[data_ptr] -= 1"))
        elif char == ".":
            instructions.append(_parse_node("output.write(chr(memory[data_ptr]))"))
        elif char == ",":
            instructions.append(_parse_node("_tmp = input.read(1)"))
            instructions.append(_parse_node("memory[data_ptr] = ord(_tmp) if _tmp else -1"))
        elif char == "[":
            node = _parse_node("while memory[data_ptr]: pass")
            instructions.append(node)
            instruction_stack.insert(0, instructions)
            instructions = node.body
        elif char == "]":
            instructions = instruction_stack.pop(0)
    module.body[0].body.extend(instructions)
    exec(compile(ast.fix_missing_locations(module), "<bf>", "exec"), globals(), locals())
    return locals()["_bf"]


code = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>+++.<++.>>++++++++.+++.+++++++.-----------------.<<.>>++++++++++++++++++++.----------.++++++."
to_procedure(code)()
