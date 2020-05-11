"""
The compiler module is responsible for rewriting the given program with
different instructions.
"""

import os
import random
from typing import Dict, List


from .enums import Operator
from .parser import Annotation, OperandNode


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

    def __init__(self, operator: Operator, operands: List[OperandNode], template: CodeTemplate):
        self.operator: Operator = operator
        self.operands: List[OperandNode] = operands
        self.template: CodeTemplate = template


    def apply_template(self) -> None:
        'Apply the operands to the template.'
        return self.template.apply(self.operands)


    def __repr__(self) -> str:
        operator: str = self.operator.name.lower()
        operands: str = ', '.join([operand.value for operand in self.operands])

        str_form: str = f'The instruction, {operator} {operands}, would be replaced with...\n'
        str_form += f'{self.template.template}\n'
        return str_form


class Compiler():

    """
    The compiler is responsible for rewriting the given program with
    different instructions.
    """

    def __init__(self):
        self.signatures: Dict[str, str] = {}
        self.substitutions: Dict[str, List[List[Union[int, str, str]]]] = {}


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


    def discover_signatures(self, directory: str) -> None:
        """
        Scan through the directory for files of the format operator_operand+.txt and
        create a signature for them.
        """
        for filename in os.listdir(directory):
            if not filename.endswith('.txt'):
                continue
            operator: str = filename[:filename.find('_')].upper()
            operands: List[str] = filename[filename.find('_')+1:-4].split('_')

            abs_filename: str = os.path.join(directory, filename)
            operands_key: str = ', '.join(operands).upper()
            if operator in self.signatures:
                self.signatures[operator][operands_key] = abs_filename
            else:
                self.signatures[operator] = {operands_key: abs_filename}


    def check_coverage(self, annotations: List[Annotation], debug=True) -> bool:
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
                if debug:
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


    def apply_substitution(self, asm_annotations: List[Annotation], debug=True) -> str:
        """
        Rewrite the given program by substituting each instruction with valid substitutions.
        """
        rewritten_program: List[SubstitutedCode] = self.substitute_first_pass(asm_annotations, debug)
        final_program: List[SubstitutedCode] = self.substitute_second_pass(rewritten_program)
        return final_program


    def substitute_first_pass(self, asm_annotations: List[Annotation], debug=True) -> List[SubstitutedCode]:
        """
        Use the annotations provided by the parser and the library of valid substitutions to
        produce a list of SubstitutedCode which represent the rewritten program.
        """
        rewritten_program: List[SubstitutedCode] = []

        template: CodeTemplate
        for annotation in asm_annotations:
            if self.check_coverage([annotation], debug):
                template = self.get_template(annotation)
            else:
                template = self.get_default_template(annotation)

            sub_code: SubstitutedCode = SubstitutedCode(annotation.operator, annotation.operands,
                                                        template)
            rewritten_program.append(sub_code)

        return rewritten_program


    def substitute_second_pass(self, rewritten_program: List[SubstitutedCode]) -> str:
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
