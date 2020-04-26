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
        operands_key = ','.join([operand.name for operand in operands])

        if operator.name in self.signatures:
            self.signatures[operator.name][operands_key] = filename
        else:
            self.signatures[operator.name] = {operands_key: filename}
