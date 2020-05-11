import re
import sys
from typing import Dict, List


import encryptor
import parser
from compiler import Compiler
from utils import RegexSwitch

_ENCRYPTED_SC_TARGET_REGEX = re.compile(r'{{ ENCRYPTED_SC }}')
_IV_TARGET_REGEX = re.compile(r'{{ IV }}')
_KEY_TARGET_REGEX = re.compile(r'{{ KEY }}')
_TEMPLATE_TARGET_REGEX = re.compile(r'[\t ]*{{ ([\w\d_]+) }}[\t ]*')


_SHELLCODE: bytes
hex_to_ascii_mapping: Dict[int, str] = {
    0x0: '0',
    0x9: '\\t',
    0xa: '\\n',
    0xc: '\\f',
    0xd: '\\r', 
    0x22: '\"',
    0x5c: '\\\\',
}


def to_hexstring(sc: str) -> str:
    return ''.join([sc[i+2:i+4] for i in range(0, len(sc), 4)])


def hex_to_asm_string(hex_values: bytes) -> str:
    result: str = ''

    for hex in hex_values:
        if hex in hex_to_ascii_mapping:
            result += hex_to_ascii_mapping[hex]
        elif 32 <= hex <= 122:
            result += chr(hex)
        else:
            result += f'\\{oct(hex)[2:]:0>3}'
    
    return result


def main():
    final_program: str = ''
    compiler = Compiler()

    _KEY, _IV, _ENCRYPTED_SC = encryptor.encrypt_sc(_SHELLCODE)
    
    with open('template.s') as template:
        for line in template:
            with RegexSwitch(line.strip()) as case:
                if case(_ENCRYPTED_SC_TARGET_REGEX):
                    final_program += f'        .string "{hex_to_asm_string(_ENCRYPTED_SC)}"\n'
                elif case(_IV_TARGET_REGEX):
                    final_program += f'        .ascii "{hex_to_asm_string(_IV)}"\n'
                elif case(_KEY_TARGET_REGEX):
                    _KEY = hex_to_asm_string(_KEY)
                    key_part_one: str = _KEY[:62]
                    key_part_two: str = _KEY[62:]
                    final_program += f'        .ascii "{key_part_one}"\n'
                    final_program += f'        .ascii "{key_part_two}"\n'
                elif case(_TEMPLATE_TARGET_REGEX):
                    match = _TEMPLATE_TARGET_REGEX.fullmatch(line.strip())
                    if match is not None:
                        template_filename: str = f'templates\{match.group(1)}.template'
                        operand_to_type_mapping, code = parser.preprocess(template_filename)
                        annotations: List[Annotation] = parser.parse(operand_to_type_mapping, code)
                        rewritten_program: str = compiler.apply_substitution(annotations)
                        rewritten_program = '\n'.join(map(lambda x: f'        {x}', rewritten_program.split('\n')))
                        final_program += rewritten_program
                        final_program += '\n'
                else:
                    final_program += line
            
    print(final_program)


if __name__ == '__main__':
    _SHELLCODE = bytes.fromhex(to_hexstring(sys.argv[1]))
    main()