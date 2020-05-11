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
    JA = 'jump if above'
    JAE = 'jump if above or equal'
    JB = 'jump if below'
    JBE = 'jump if below or equal'
    JC = 'jump if carry'
    JCXZ = 'jump if cx register is 0'
    JE = 'jump if equal'
    JECXZ = 'jump if ecx register is 0'
    JG = 'jump if greater than'
    JGE = 'jump if greater than or equal'
    JL = 'jump if less than'
    JLE = 'jump if less than or equal'
    JMP = 'jump'
    JNA = 'jump if not above'
    JNAE = 'jump if not above or equal'
    JNB = 'jump if not below'
    JNBE = 'jump if not below or equal'
    JNC = 'jump if not carry'
    JNE = 'jump if not equal'
    JNG = 'jump if not greater'
    JNGE = 'jump if not greater than or equal'
    JNL = 'jump if not less than'
    JNLE = 'jump if not less than or equal'
    JNO = 'jump if not overflow (OF=0)'
    JNP = 'jump if not parity (PF=0)'
    JNS = 'jump if not sign (SF=0)'
    JNZ = 'jump if not zero'
    JO = 'jump if overflow (OF=1)'
    JP = 'jump if parity (PF=1)'
    JPE = 'jump if even parity (PF=1)'
    JPO = 'jump if odd parity (PF=0)'
    JS = 'jump if sign (SF=1)'
    JZ = 'jump if zero'
    TEST = 'test'

    CALL = 'call'
    INT = 'int'
    RET = 'return'

    NOP = 'nop'

    XCHG = 'xchg'
    DAS = 'das'
    BOUND = 'bound'
    ARPL = 'arpl'
    OUTS = 'outs'
    INS = 'ins'
    REP = 'rep'
    MOVZX = 'movzx'

    LABEL = 'a label'


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
