"""
An example of how to use the substitution compiler module.
"""

# pylint: disable=wrong-import-position,import-error

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)
PARENT_DIR_NAME = os.path.join(MODULE_DIR_NAME, '..')
if PARENT_DIR_NAME not in sys.path:
    sys.path.insert(0, PARENT_DIR_NAME)


import substitution_parser as parser
from substitution_compiler import Compiler
from substitution_enums import Operand, Operator
from substitution_transpiler import asm_to_shellcode, shellcode_to_asm


_ASM_CODE = (
    'add eax, ebx\n'
    'sub eax, 0x5d\n'
)


def main():
    'Sample usage of the compiler module.'
    print('Outputting given asm code...')
    print(_ASM_CODE)
    print('')

    print('Outputting shellcode...')
    shellcode = asm_to_shellcode(_ASM_CODE)
    print(shellcode)
    print('')

    raw_disassembly = shellcode_to_asm(shellcode)
    annotations = parser.parse(raw_disassembly)

    compiler = Compiler()
    compiler.add_signature(Operator.ADD, [Operand.REG, Operand.REG], '../library/add_reg_reg.txt')
    compiler.add_signature(Operator.SUB, [Operand.REG, Operand.CONST], '../library/sub_reg_const.txt')

    print('Outputting rewritten program...')
    rewritten_program = compiler.apply_substitution(annotations)
    print(rewritten_program)
    print('')

    print('Outputting rewritten shellcode...')
    rewritten_shellcode = asm_to_shellcode(rewritten_program)
    print(rewritten_shellcode)
    print('')


if __name__ == '__main__':
    main()
