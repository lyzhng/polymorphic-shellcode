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


class Annotation(NamedTuple):

    'Annotation stores data needed for the compiler to do its work'

    operator: Operator
    operands: List[OperandNode]
    memory_address: str
    size: int

    def __repr__(self):
        operands = ', '.join([operand.value for operand in self.operands])
        return f'{self.operator} {operands} with {self.size} bytes at {self.memory_size}'


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
