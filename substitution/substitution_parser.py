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
from typing import List, NamedTuple, Union


from substitution_enums import Operator, Operand
from substitution_utils import RegexSwitch


_CONST = re.compile(r'0x[0-9a-zA-Z]+')
_MEM = re.compile(r'((BYTE PTR )|(WORD PTR )|(DWORD PTR ))?(\[.+\])', re.IGNORECASE)
_REG = re.compile(r'eax|ebx|ecx|edx|esi|edi|esp|ebp|ax|bx|cx|dx|ah|al|bh|bl|ch|cl|dh|dl')


class Annotation():

    'Annotation stores data needed for the compiler to do its work'

    def __init__(self):
        self.operands: List[OperandNode] = []


    def set_operator(self, operator: Operator):
        self.operator: Operator = operator


    def set_operands(self, operands: List[OperandNode]):
        self.operands = operands


    def add_operand(self, operand: OperandNode):
        self.operands.append(operand)


    def set_memory_address(self, memory_address: str):
        self.memory_address: str = memory_address


    def set_size(self, size: int):
        self.size: int = size


    def __repr__(self):
        operands = ', '.join([operand.value for operand in self.operands])
        return f'{self.operator} {operands} with {self.size} bytes at {self.memory_address}'


class OperandNode(NamedTuple):

    'OperandNode stores the kind and value of the operand.'

    kind: str
    value: str

    def __repr__(self):
        return f'Operand of type {self.kind} and of value {self.value}'


def parse(asm_code: List[str]) -> List[List[Union[Operator, Operand]]]:
    'Annotate the asm code to be used by the compiler.'
    parse_data = []
    for line in asm_code:
        parse_annotation = []

        components = line.strip().split(' ', 1)
        for operator in Operator:
            if components[0] == operator.name.lower():
                parse_annotation.append(operator)
                break

        operands = [operand.strip('\t, ') for operand in components[1].split(',')]
        for operand in operands:
            with RegexSwitch(operand) as case:
                if case(_CONST):
                    operand_node = OperandNode(Operand.CONST, operand)
                    parse_annotation.append(operand_node)
                elif case(_MEM):
                    operand_node = OperandNode(Operand.MEM, operand)
                    parse_annotation.append(operand_node)
                elif case(_REG):
                    operand_node = OperandNode(Operand.REG, operand)
                    parse_annotation.append(operand_node)
                else:
                    raise TypeError(f'{operand} is not of a type supported by the parser')

        parse_data.append(parse_annotation)

    return parse_data


class AsmNode(NamedTuple):

    'AsmNode stores the offset, size, and code of a line in the raw disassembly.'

    offset: int
    size: int
    code: str

    def __repr__(self):
        return f'{code} is {size} bytes at {offset}.'


def parse_first_pass(raw_disassembly: List[str]) -> List[AsmNode]:
    """
    The first pass is responsible for parsing the memory address and instruction from the
    raw disassembly.  The raw disassembly should be in the format of memory_offset: asm_code.
    """
    asm_code = []
    
    regex = re.compile(r' +(\d+): +(.+)')
    for line in raw_disassembly:
        match = regex.fullmatch(line)
        if match is None:
            raise ValueError('Invalid format!')
        asm_node = AsmNode(int(match.group(0)), match.group(1))
        asm_code.append(asm_node)

    return asm_code