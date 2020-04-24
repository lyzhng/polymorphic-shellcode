import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


import enum


class Operator(enum.Enum):

    ADD = 'add'


    def __eq__(self, other):
        return self.value == other


class Operand(enum.Enum):

    ADDR  = 'address'
    REG   = 'register'
    VALUE = 'value'


    def __eq__(self, other):
        return self.value == other
