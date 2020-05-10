"""
The parser module is responsible for annotating raw assembly instructions
which would be used by the compiler ot rewrite the program using different
instructions.
"""


import re
from typing import Dict, List, NamedTuple, Tuple


from enums import Operator, Operand
from utils import RegexSwitch, Switch


_CONST = re.compile(r'0x[0-9a-zA-Z]+')
_MEM = re.compile(r'((BYTE|WORD|DWORD|QWORD) PTR )?(([CDEFGS]S:((\[.+\])|(0x[a-fA-F0-9]+)))|(\[.+\]))', re.IGNORECASE) #pylint: disable=line-too-long
_REG = re.compile(r'eax|ebx|ecx|edx|esi|edi|esp|ebp|eip|ax|bx|cx|dx|ah|al|bh|bl|ch|cl|dh|dl|si|di|sp|bp|ip') #pylint: disable=line-too-long

_PREPROCESS_DEFINE = re.compile(r'#define_operand_type (.+)')


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


def preprocess(template_filename: str) -> Tuple[Dict[str, Operand], List[str]]:
    """
    Preprocess reads in a template to parse any operand type definition in the file while
    extracting the code snippet.
    """
    operand_to_type_mapping: Dict[str, Operand] = {}
    code: List[str] = []
    
    with open(template_filename) as template:
        for line in template:
            match = _PREPROCESS_DEFINE.fullmatch(line.strip())
            if match is not None:
                operand, operand_type = map(str.strip, match.group(1).split('='))
                with Switch(operand_type) as case:
                    if case('CONST'):
                        operand_to_type_mapping[operand] = Operand.CONST
                    elif case('MEM'):
                        operand_to_type_mapping[operand] = Operand.MEM
                    elif case('REG'):
                        operand_to_type_mapping[operand] = Operand.REG
                    else:
                        raise TypeError(f'{operand_type} is not supported by the parser.')
            elif line.strip() != '':
                code.append(line)

    return (operand_to_type_mapping, code)


def parse(operand_to_type_mapping: Dict[str, Operand], code: List[str]) -> List[Annotation]:
    """
    Annotate the asm code to be used by the compiler.  Takes raw disassembly as input
    and outputs a list of Annotation.
    """
    annotations: List[Annotation] = []

    for line in code:
        annotation: Annotation = Annotation()
        components: List[str] = line.strip().split(' ', 1)

        for operator in Operator:
            if components[0] == operator.name.lower():
                annotation.set_operator(operator)
                break

        if len(components) > 1:
            operands = [operand.strip('\t, ') for operand in components[1].split(',')]
            for operand in operands:
                if operand_to_type_mapping.get(operand) is not None:
                    operand_node = OperandNode(operand_to_type_mapping.get(operand), operand) 
                    annotation.add_operand(operand_node)
                    continue
                
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

        annotations.append(annotation)

    return annotations