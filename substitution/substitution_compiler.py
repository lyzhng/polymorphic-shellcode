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
from typing import Dict, List


from substitution_parser import Annotation, OperandNode
from substitution_enums import Operator


_CALL_JUMP_INSTRUCTIONS: List[Operator] = [
    Operator.CALL,
    Operator.JA,
    Operator.JAE,
    Operator.JB,
    Operator.JBE,
    Operator.JC,
    Operator.JCXZ,
    Operator.JE,
    Operator.JECXZ,
    Operator.JG,
    Operator.JGE,
    Operator.JL,
    Operator.JLE,
    Operator.JMP,
    Operator.JNA,
    Operator.JNAE,
    Operator.JNB,
    Operator.JNBE,
    Operator.JNC,
    Operator.JNE,
    Operator.JNG,
    Operator.JNGE,
    Operator.JNL,
    Operator.JNLE,
    Operator.JNO,
    Operator.JNP,
    Operator.JNS,
    Operator.JNZ,
    Operator.JO,
    Operator.JP,
    Operator.JPE,
    Operator.JPO,
    Operator.JS,
    Operator.JZ,
]
_LABEL_PREFIX: str = 'sub_asm_engine'


class CodeTemplate():

    'CodeTemplate represents the template for the replacement code.'

    def __init__(self, targets: List[str], template: str, is_original: bool = False):
        self.targets: List[str] = targets
        self.template: str = template
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
                 mem_addr: int):
        # pylint: disable= too-many-arguments
        self.operator: Operator = operator
        self.operands: List[OperandNode] = operands
        self.template: CodeTemplate = template
        self.mem_addr: int = mem_addr


    def apply_template(self) -> None:
        'Apply the operands to the template.'
        return self.template.apply(self.operands)


    def __repr__(self) -> str:
        operator: str = self.operator.name.lower()
        operands: str = ', '.join([operand.value for operand in self.operands])

        str_form: str = f'The instruction, {operator} {operands}, would be replaced with...\n'
        str_form += f'{self.template.template}\n'
        str_form += f'Originally located at {self.mem_addr}\n'
        return str_form


class Compiler():

    """
    The compiler is responsible for rewriting the given program with
    different instructions.
    """

    def __init__(self):
        self.signatures: Dict[str, str] = {}
        self.substitutions: Dict[str, List[List[int, str, str]]] = {}


    def add_signature(self, operator: str, operands: List[OperandNode], filename: str) -> None:
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
            operator: str = annotation.operator.name
            operands_key: str = ', '.join([operand.kind.name for operand in annotation.operands])

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
        template: CodeTemplate = random.choice(self.substitutions[filename])
        self.substitutions[filename].pop()
        return template


    def get_default_template(self, annotation: Annotation) -> CodeTemplate:
        # pylint: disable=no-self-use
        'Create a template for the given annotation using the original instruction as template.'
        targets: List[str] = []
        operator: str = annotation.operator.name.lower()
        operands: str = ', '.join([operand.value for operand in annotation.operands])
        template: str = f'{operator} {operands}'
        return CodeTemplate(targets, template, is_original=True)


    def apply_substitution(self, asm_annotations: List[Annotation]) -> str:
        """
        Rewrite the given program by substituting each instruction with valid substitutions.
        """
        program: List[SubstitutedCode] = self.substitute_first_pass(asm_annotations)
        rewritten_program: List[SubstitutedCode] = self.substitute_second_pass(program)
        return self.substitute_third_pass(rewritten_program)


    def substitute_first_pass(self, asm_annotations: List[Annotation]) -> List[SubstitutedCode]:
        """
        Use the annotations provided by the parser and the library of valid substitutions to
        produce a list of SubstitutedCode which represent the rewritten program.
        """
        rewritten_program: List[SubstitutedCode] = []

        template: CodeTemplate
        for annotation in asm_annotations:
            if self.check_coverage([annotation]):
                template = self.get_template(annotation)
            else:
                template = self.get_default_template(annotation)

            sub_code: SubstitutedCode = SubstitutedCode(annotation.operator, annotation.operands,
                                                        template, annotation.memory_address)
            rewritten_program.append(sub_code)

        return rewritten_program

    def substitute_second_pass(self, program: List[SubstitutedCode]) -> List[SubstitutedCode]:
        # pylint: disable=no-self-use
        """
        Correct the memory offsets for call and jump instructions after substituting in
        instructions.
        """
        mem_label_mapping: Dict[int, str] = {}
        last_mem_addr: int = program[-1].mem_addr
        label_index: int = 0
        for line in program:
            if line.operator in _CALL_JUMP_INSTRUCTIONS:
                mem_addr: int = int(line.operands[0].value, 0)

                if mem_addr <= last_mem_addr:
                    address_label = f'{_LABEL_PREFIX}_{label_index}'
                    mem_label_mapping[mem_addr] = address_label
                    label_index += 1

                    line.operands[0] = line.operands[0]._replace(value=address_label)
                    if line.template.is_original:
                        line.template.template = f'{line.operator.name.lower()} {address_label}'

        final_program: List[SubstitutedCode] = []
        for line in program:
            if line.mem_addr in mem_label_mapping:
                address_label: str = mem_label_mapping[line.mem_addr]
                sub_code: SubstitutedCode = _create_label_sub_code(address_label)
                final_program.append(sub_code)
            final_program.append(line)

        return final_program


    def substitute_third_pass(self, rewritten_program: List[SubstitutedCode]) -> str:
        # pylint: disable=no-self-use
        """
        Apply the operands to the template within the rewritten program to get the final
        program.
        """
        program: List[str] = [line.apply_template() for line in rewritten_program]
        return '\n'.join(program)


def parse_substitution_file(filename: str) -> List[CodeTemplate]:
    """
    Parse the valid substitutions in the file given so that it can be used by
    get_substitution() method of Compiler.
    """
    with open(filename) as file_handler:
        valid_substitutions: List[str] = file_handler.read().split('----------')
        for index, substitution in enumerate(valid_substitutions):
            substitution_lines: List[str] = substitution.strip().split('\n')

            targets: List[str] = substitution_lines[0].split()
            template: str = '\n'.join(substitution_lines[1:]).strip()

            valid_substitutions[index] = CodeTemplate(targets, template)

        return valid_substitutions


def _create_label_sub_code(address_label: str) -> SubstitutedCode:
    """
    Create a SubstitutedCode object that represents the label specifed.
    """
    template: CodeTemplate = CodeTemplate([], f'{address_label}:', is_original=True)
    sub_code: SubstitutedCode = SubstitutedCode(Operator.LABEL, [], template, address_label)
    return sub_code
