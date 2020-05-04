"""
The compiler module is responsible for rewriting the given program with
different instructions.
"""

#pylint: disable=wrong-import-position

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


import random
import re
from typing import Dict, List


from substitution_parser import Annotation, OperandNode
from substitution_enums import Operator


_CALL_JUMP_INSTRUCTIONS = [
    Operator.CALL,
    Operator.JE,
    Operator.JG,
    Operator.JGE,
    Operator.JL,
    Operator.JLE,
    Operator.JMP,
    Operator.JNE,
    Operator.JNZ,
    Operator.JZ,
]


class CodeTemplate():

    'CodeTemplate represents the template for the replacement code.'

    def __init__(self, targets: List[str], template: str, size: int, is_original: bool = False):
        self.targets: List[str] = targets
        self.template: str = template
        self.size: int = size
        self.is_original: bool = is_original


    def apply(self, operands: List[OperandNode]) -> str:
        'Apply the given operands to the template.'
        template: str = self.template

        for target, operand in zip(self.targets, operands):
            template = template.replace(target, operand.value)

        return template


    def __repr__(self) -> str:
        return f'Targets: {", ".join(self.targets)}\n{self.template}'


class SubstitutedCode():

    'SubstitutedCode represents the code that would be substituted in.'

    def __init__(self, operator: Operator, operands: List[OperandNode], template: CodeTemplate,
                 old_addr: int, new_addr: int):
        # pylint: disable= too-many-arguments
        self.operator: Operator = operator
        self.operands: List[OperandNode] = operands
        self.template: CodeTemplate = template
        self.old_addr: int = old_addr
        self.new_addr: int = new_addr


    def apply_template(self):
        'Apply the operands to the template.'
        return self.template.apply(self.operands)


    def __repr__(self) -> str:
        operator = self.operator.name.lower()
        operands = ', '.join([operand.value for operand in self.operands])

        str_form = f'The instruction, {operator} {operands}, would be replaced with...\n'
        str_form += f'{self.template.template}\n'
        str_form += f'Total size: {self.template.size}\n'
        str_form += f'Originally at {self.old_addr} and now at {self.new_addr}\n'
        return str_form


class Compiler():

    """
    The compiler is responsible for rewriting the given program with
    different instructions.
    """

    def __init__(self):
        self.signatures: Dict[str, str] = {}
        self.substitutions: Dict[str, List[List[int, str, str]]] = {}


    def add_signature(self, operator: str, operands: List[OperandNode], filename: str):
        """
        Associate a filename with the given operator and operands from which
        valid substitutions would be parsed.
        """
        operands_key: str = ', '.join([operand.name for operand in operands])

        if operator.name in self.signatures:
            self.signatures[operator.name][operands_key] = filename
        else:
            self.signatures[operator.name] = {operands_key: filename}


    def check_coverage(self, annotations: List[Annotation]) -> bool:
        """
        Check to see if there is a signature for every command in the parse data and
        print any commands that are not covered.
        """
        complete_coverage: bool = True

        for annotation in annotations:
            operator = annotation.operator.name
            operands_key = ', '.join([operand.kind.name for operand in annotation.operands])

            if operator not in self.signatures or operands_key not in self.signatures[operator]:
                complete_coverage = False
                print(f'WARNING: Missing signature for {operator} {operands_key}!')

        return complete_coverage


    def get_template(self, annotation: Annotation) -> CodeTemplate:
        """
        Retrieve a valid substitution for the instruction as described by the given operator
        and operands.
        """
        operands_key: str = ', '.join([operand.kind.name for operand in annotation.operands])
        filename: str = self.signatures[annotation.operator.name][operands_key]
        if filename not in self.substitutions:
            self.substitutions[filename] = parse_substitution_file(filename)

        self.substitutions[filename].append(self.get_default_template(annotation))
        template = random.choice(self.substitutions[filename])
        self.substitutions[filename].pop()
        return template


    def get_default_template(self, annotation: Annotation) -> CodeTemplate:
        # pylint: disable=no-self-use
        'Create a template for the given annotation using the original instruction as template.'
        targets: List[str] = []
        operator: str = annotation.operator.name.lower()
        operands: str = ', '.join([operand.value for operand in annotation.operands])
        template: str = f'{operator} {operands}'
        size: int = annotation.size
        return CodeTemplate(targets, template, size, is_original=True)


    def apply_substitution(self, asm_annotations: List[Annotation]) -> str:
        """
        Rewrite the given program by substituting each instruction with valid substitutions.
        """
        rewritten_program = self.substitute_first_pass(asm_annotations)
        return self.substitute_second_pass(rewritten_program)


    def substitute_first_pass(self, asm_annotations: List[Annotation]) -> List[SubstitutedCode]:
        """
        Use the annotations provided by the parser and the library of valid substitutions to
        produce a list of SubstitutedCode which represent the rewritten program.
        """
        rewritten_program: List[SubstitutedCode] = []
        old_new_mem_mapping: Dict[int, int] = {}
        current_address: int = 0

        for annotation in asm_annotations:
            template: CodeTemplate
            if self.check_coverage([annotation]):
                template = self.get_template(annotation)
            else:
                template = self.get_default_template(annotation)

            old_mem_addr: int = annotation.memory_address
            old_new_mem_mapping[old_mem_addr] = current_address
            sub_code: SubstitutedCode = SubstitutedCode(annotation.operator, annotation.operands,
                                                        template, old_mem_addr, current_address)
            current_address += template.size
            rewritten_program.append(sub_code)

        for line in rewritten_program:
            if line.operator in _CALL_JUMP_INSTRUCTIONS:
                mem_addr = int(line.operands[0].value, 0)
                line.operands[0] = line.operands[0]._replace(value=old_new_mem_mapping[mem_addr])
                if line.template.is_original:
                    operator = line.operator.name.lower()
                    operand = hex(old_new_mem_mapping[mem_addr])
                    line.template.template = f'{operator} {operand}'

        return rewritten_program


    def substitute_second_pass(self, rewritten_program: List[SubstitutedCode]) -> str:
        #pylint: disable=no-self-use
        """
        Apply the operands to the template within the rewritten program to get the final
        program.
        """
        program = [line.apply_template() for line in rewritten_program]
        return '\n'.join(program)


def parse_substitution_file(filename: str) -> List[CodeTemplate]:
    """
    Parse the valid substitutions in the file given so that it can be used by
    get_substitution() method of Compiler.
    """
    regex = re.compile(r'\d+')

    with open(filename) as file_handler:
        valid_substitutions: List[str] = file_handler.read().split('----------')
        for index, substitution in enumerate(valid_substitutions):
            substitution_lines: List[str] = substitution.strip().split('\n')

            size: int = int(regex.search(substitution_lines[0]).group())
            targets: List[str] = substitution_lines[1].split()
            template: str = '\n'.join(substitution_lines[2:]).strip()

            valid_substitutions[index] = CodeTemplate(targets, template, size)

        return valid_substitutions
