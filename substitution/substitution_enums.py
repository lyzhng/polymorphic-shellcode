"""
The enums module provides constants to be used when mentioning x86 asm
commands or argument types.
"""

# pylint: disable=wrong-import-position

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


import enum


class Operator(enum.Enum):

    'Represents the various x86 asm commands'

    LEA = 'load effective address'
    MOV = 'move'
    POP = 'pop'
    PUSH = 'push'

    ADD = 'addition'
    DEC = 'decrement'
    IDIV = 'integer division'
    IMUL = 'integer multiplication'
    INC = 'increment'
    NEG = 'negate'
    SHL = 'shift left'
    SHR = 'shift right'
    SUB = 'subtraction'

    AND = 'and'
    NOT = 'not'
    OR = 'or'
    XOR = 'xor'

    CMP = 'compare'
    JE = 'jump when equal'
    JG = 'jump when greater than'
    JGE = 'jump when greater than or equal'
    JL = 'jump when less than'
    JLE = 'jump when less than or equal'
    JMP = 'jump'
    JNE = 'jump when not equal'
    JNZ = 'jump when not zero'
    JZ = 'jump when zero'
    TEST = 'test'

    CALL = 'call'
    INT = 'int'
    RET = 'return'

    NOP = 'nop'

    XCHG = 'xchg'
    DAS = 'das'
    BOUND = 'bound'
    JAE = 'jae'
    JO = 'jo'
    ARPL = 'arpl'
    OUTS = 'outs'
    INS = 'ins'


    def __eq__(self, other):
        # pylint: disable=comparison-with-callable
        return self.value == other.value


class Operand(enum.Enum):

    'Represents the various x86 asm argument types'

    LABEL = 'label'
    MEM = 'memory address'
    REG = 'any register'
    REG8 = '8-bit register'
    REG16 = '16-bit register'
    REG32 = '32-bit register'
    CONST = 'any constant'
    CONST8 = '8-bit constant'
    CONST16 = '16-bit constant'
    CONST32 = '32-bit constant'


    def __eq__(self, other):
        # pylint: disable=comparison-with-callable
        return self.value == other.value
