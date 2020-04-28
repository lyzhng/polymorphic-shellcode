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


class Compiler():

    """
    The compiler is responsible for rewriting the given program with
    different instructions.
    """

    def __init__(self):
        self.signatures = {}
        self.substitutions = {}


    def add_signature(self, operator, operands, filename):
        """
        Associate a filename with the given operator and operands from which
        valid substitutions would be parsed.
        """
        operands_key = ', '.join([operand.name for operand in operands])

        if operator.name in self.signatures:
            self.signatures[operator.name][operands_key] = filename
        else:
            self.signatures[operator.name] = {operands_key: filename}


    def check_coverage(self, parse_data):
        """
        Check to see if there is a signature for every command in the parse data and
        print any commands that are not covered.
        """
        incomplete_coverage = True

        for parse_annotation in parse_data:
            operator, operands = parse_annotation[0].name, parse_annotation[1:]
            operands_key = ', '.join([operand.kind.name for operand in operands])

            if operator not in self.signatures or operands_key not in self.signatures[operator]:
                incomplete_coverage = False
                print(f'Missing signature for {operator} {operands_key}')

        return incomplete_coverage


    def get_substitution(self, operator, operands):
        """
        Retrieve a valid substitution for the instruction as described by the given operator
        and operands.
        """
        operands_key = ', '.join([operand.kind.name for operand in operands])
        filename = self.signatures[operator.name][operands_key]
        if filename not in self.substitutions:
            self.substitutions[filename] = parse_substitution_file(filename)

        header, chosen_substitution = random.choice(self.substitutions[filename])

        for template, operand in zip(header.split(), operands):
            chosen_substitution = chosen_substitution.replace(template, operand.value)

        return chosen_substitution


def parse_substitution_file(filename):
    """
    Parse the valid substitutions in the file given so that it can be used by
    self.get_substitution().
    """
    with open(filename) as file_handler:
        valid_substitutions = file_handler.read().split('----------')
        for index, substitution in enumerate(valid_substitutions):
            substitution_lines = substitution.split('\n')
            header = substitution_lines[0]
            substitution = '\n'.join(substitution_lines[1:])

            valid_substitutions[index] = [header, substitution]

        return valid_substitutions
