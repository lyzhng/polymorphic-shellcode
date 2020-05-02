"""
The transpiler module is responsible for converting shellcode into x86 asm and
vice versa.
"""

#pylint: disable=wrong-import-position

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


from pwn import asm, context, disasm, unhex


context.arch = 'i686'
context.os = 'linux'


def shellcode_to_asm(shellcode, byte=True, offset=True):
    'Convert shellcode into x86 asm code.'
    return disasm(shellcode, byte=byte, offset=offset).split('\n')


def asm_to_shellcode(asm_code):
    'Convert x86 asm code into shellcode.'
    return asm(asm_code)
