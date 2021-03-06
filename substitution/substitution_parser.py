"""
The parser module is responsible for annotating raw assembly instructions
which would be used by the compiler to rewrite the program using different
instructions.
"""

# pylint: disable=wrong-import-position

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


import re
from typing import List, NamedTuple


from pwnlib.shellcraft.i386 import nop # pylint: disable=import-error, no-name-in-module
from substitution_enums import Operator, Operand
from substitution_utils import RegexSwitch


_CONST = re.compile(r'0x[0-9a-zA-Z]+')
_MEM = re.compile(r'((BYTE|WORD|DWORD|QWORD) PTR )?(([CDEFGS]S:((\[.+\])|(0x[a-fA-F0-9]+)))|(\[.+\]))', re.IGNORECASE) #pylint: disable=line-too-long
_REG = re.compile(r'eax|ebx|ecx|edx|esi|edi|esp|ebp|eip|ax|bx|cx|dx|ah|al|bh|bl|ch|cl|dh|dl|si|di|sp|bp|ip') #pylint: disable=line-too-long


class OperandNode(NamedTuple):

    'OperandNode stores the kind and value of the operand.'

    kind: str
    value: str

    def __repr__(self):
        return f'Operand of type {self.kind} and of value {self.value}'


class Annotation():

    'Annotation stores data needed for the compiler to do its work'

    def __init__(self):
        self.operator: Operator = None
        self.operands: List[OperandNode] = []
        self.memory_address: int = -1
        self.size: int = 0


    def set_operator(self, operator: Operator):
        'Set the operator attribute.'
        self.operator: Operator = operator


    def set_operands(self, operands: List[OperandNode]):
        'Set the operands attribute.'
        self.operands = operands


    def add_operand(self, operand: OperandNode):
        'Append given operand to list of stored operands.'
        self.operands.append(operand)


    def set_memory_address(self, memory_address: int):
        'Set the memory address size attribute.'
        self.memory_address: int = memory_address


    def __repr__(self):
        operands = ', '.join([operand.value for operand in self.operands])
        return f'{self.operator} {operands} at {self.memory_address}'


class AsmNode(NamedTuple):

    'AsmNode stores the offset, size, and code of a line in the raw disassembly.'

    offset: int
    code: str

    def __repr__(self):
        return f'{self.code} at {self.offset}.'


def parse_first_pass(raw_disassembly: List[str]) -> List[AsmNode]:
    """
    The first pass is responsible for parsing the memory address and instruction from the
    raw disassembly.  The raw disassembly should be in the format of
    memory_offset: opcode asm_code.
    """
    asm_code = []

    regex = re.compile(r' +([a-zA-Z0-9]+): +((?:[a-fA-F0-9]{2} )*[0-9a-fA-F]{2}) +(.+)')
    for line in raw_disassembly:
        match = regex.fullmatch(line)

        offset = int(match.group(1), 16)
        size = len(match.group(2).strip().split())
        code = match.group(3)

        asm_node = AsmNode(offset, code)
        asm_code.append(asm_node)

    asm_node = AsmNode(offset+size, nop().strip())
    asm_code.append(asm_node)

    return asm_code


def parse_second_pass(asm_nodes: List[AsmNode]) -> List[Annotation]:
    """
    The second pass is responsible for annotating each line of asm code to be used by the
    compiler for rewriting the program.
    """
    asm_annotations = []

    for asm_node in asm_nodes:
        annotation = Annotation()
        components = asm_node.code.strip().split(' ', 1)

        for operator in Operator:
            if components[0] == operator.name.lower():
                annotation.set_operator(operator)
                break

        if len(components) > 1:
            operands = [operand.strip('\t, ') for operand in components[1].split(',')]
            for operand in operands:
                with RegexSwitch(operand) as case:
                    if case(_CONST):
                        operand_node = OperandNode(Operand.CONST, operand)
                        annotation.add_operand(operand_node)
                    elif case(_MEM):
                        operand_node = OperandNode(Operand.MEM, operand)
                        annotation.add_operand(operand_node)
                    elif case(_REG):
                        operand_node = OperandNode(Operand.REG, operand)
                        annotation.add_operand(operand_node)
                    else:
                        raise TypeError(f'{operand} is not of a type supported by the parser')

        annotation.set_memory_address(asm_node.offset)
        asm_annotations.append(annotation)

    return asm_annotations


def parse(raw_disassembly: List[str]) -> List[Annotation]:
    """
    Annotate the asm code to be used by the compiler.  Takes raw disassembly as input
    and outputs a list of Annotation.
    """
    asm_nodes = parse_first_pass(raw_disassembly)
    annotations = parse_second_pass(asm_nodes)
    return annotations
