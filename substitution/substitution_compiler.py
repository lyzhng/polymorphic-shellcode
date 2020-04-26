"""
The compiler module is responsible for rewriting the given program with
different instructions.
"""

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


class Compiler():

    """
    The compiler is responsible for rewriting the given program with
    different instructions.
    """

    def __init__(self):
        self.signatures = {}


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
