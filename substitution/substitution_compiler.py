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


class CodeTemplate():

    'CodeTemplate represents the template for the replacement code.'

    def __init__(self, targets: List[str], template: str, size: int):
        self.targets: List[str] = targets
        self.template: str = template
        self.size: int = size


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


    def get_substitution(self, annotation: Annotation) -> List[Union[int, str]]:
        """
        Retrieve a valid substitution for the instruction as described by the given operator
        and operands.
        """
        operands_key: str = ', '.join([operand.kind.name for operand in annotation.operands])
        filename: str = self.signatures[annotation.operator.name][operands_key]
        if filename not in self.substitutions:
            self.substitutions[filename] = parse_substitution_file(filename)

        size, header, chosen_substitution = random.choice(self.substitutions[filename])

        for template, operand in zip(header.split(), annotation.operands):
            chosen_substitution = chosen_substitution.replace(template, operand.value)

        return [size, chosen_substitution]


    def apply_substitution(self, asm_annotations: List[Annotation]) -> List[SubstitutedCode]:
        """
        Rewrite the given program by substituting each instruction with valid substitutions.
        """
        return substitute_first_pass(asm_annotations)


    def substitute_first_pass(self, asm_annotations: List[Annotation]) -> List[SubstitutedCode]:
        """
        Use the annotations provided by the parser and the library of valid substitutions to
        produce a list of SubstitutedCode which represent the rewritten program.  This still has
        to go through some post-processing to fix memory offsets for call and jump instructions.
        """
        rewritten_program = []
        current_address = 0

        for annotation in asm_annotations:
            old_mem_addr: int = annotation.memory_address
            substituted_code: SubstitutedCode

            if self.check_coverage([annotation]):
                size, new_code = self.get_substitution(annotation)
                substituted_code = SubstitutedCode(new_code, size, old_mem_addr, current_address)
            else:
                operator: str = annotation.operator.name.lower()
                operands: str = ', '.join([operand.value for operand in annotation.operands])
                new_code: str = f'{operator} {operands}'
                size: int = annotation.size
                substituted_code = SubstitutedCode(new_code, size, old_mem_addr, current_address)

            current_address += substituted_code.size
            rewritten_program.append(substituted_code)

        return rewritten_program


    def substitute_second_pass(self, rewritten_program: List[SubstitutedCode]) -> List[str]:
        """
        Adjust memory offsets for call and jump instructions after adding more instructions
        during the substitution process.
        """
        pass


def parse_substitution_file(filename: str) -> List[List[Union[int, str, str]]]:
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
            header: str = substitution_lines[1]
            substitution: str = '\n'.join(substitution_lines[2:]).strip()

            valid_substitutions[index] = [size, header, substitution]

        return valid_substitutions
