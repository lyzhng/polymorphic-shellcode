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


context.arch = 'i386'
context.os = 'linux'


def shellcode_to_asm(shellcode, raw_hex=True):
    'Convert shellcode into x86 asm code.  If raw_hex is False, need to unhex it first.'
    if raw_hex:
        return disasm(shellcode, byte=False, offset=False).split('\n')
    return disasm(unhex(shellcode), byte=False, offset=False).split('\n')


def asm_to_shellcode(asm_code):
    'Convert x86 asm code into shellcode.'
    return asm(asm_code)