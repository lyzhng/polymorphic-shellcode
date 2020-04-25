"""
The parser module is responsible for annotating raw assembly instructions
which would be used by the compiler to rewrite the program using different
instructions.
"""

#pylint: disable=wrong-import-position

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


import re
import string
from typing import NamedTuple


from substitution_enums import Operator, Operand


CONST_PATTERN = re.compile('0x[0-9a-f]+')
LABEL_PATTERN = re.compile(f'[{string.ascii_letters + string.digits}_]+')
MEM_PATTERN = re.compile(r'\[.+\]')
REGISTER_PATTERN = re.compile('eax|ebx|ecx|edx|esi|edi|esp|ebp|ax|bx|cx|dx|ah|al|bh|bl|ch|cl|dh|dl')


class OperandNode(NamedTuple):

    'OperandNode stores the kind and value of an operand.'

    kind: str
    value: str

    def __repr__(self):
        return f'Operand of type {self.kind} and of value {self.value}'


def parse(asm_code):
    'Annotate the asm code to be used by the compiler.'
    result = []

    for line in asm_code:
        print(line)
        components = list(map(lambda x: x.strip(' \t,'), line.split()))

        parsed_components = []
        for operator in Operator:
            if components[0] == operator.name.lower():
                parsed_components.append(operator)

                for operand in components[1:]:
                    if CONST_PATTERN.match(operand):
                        operand_node = OperandNode(Operand.CONST, operand)
                        parsed_components.append(operand_node)
                    elif MEM_PATTERN.match(operand):
                        operand_node = OperandNode(Operand.MEM, operand)
                        parsed_components.append(operand_node)
                    elif REGISTER_PATTERN.match(operand):
                        operand_node = OperandNode(Operand.REG, operand)
                        parsed_components.append(operand_node)
                    elif LABEL_PATTERN.match(operand):
                        operand_node = OperandNode(Operand.LABEL, operand)
                        parsed_components.append(operand_node)

                result.append(parsed_components)
    return result
