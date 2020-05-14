"""
The main module is responsible for taking in shellcode as input and changing the
shellcode so that it looks different, but exhibit the same behavior.
"""


import re
import sys
from typing import Dict, List
import argparse


from encrypt import encrypt
from sub_engine.engine import SubEngine
from substitution.substitution_transpiler import asm_to_shellcode
from utils import RegexSwitch


_ENCRYPTED_SC_TARGET_REGEX = re.compile(r'{{ ENCRYPTED_SC }}')
_NUM_CHUNKS_TARGET_REGEX = re.compile(r'{{ NUM_CHUNKS }}')
_KEY_TARGET_REGEX = re.compile(r'{{ KEY }}')
_TEMPLATE_TARGET_REGEX = re.compile(r'[\t ]*{{ ([\w\d_]+) }}[\t ]*')

_COMMENT_REGEX = re.compile(r'; .+')


def shellcodify(bytestring: bytes) -> str:
    hexstring = bytestring.hex()
    hexes = [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]
    return ''.join(hexes)


def morph(shellcode: str, debug: bool = False):
    """
    Change the given shellcode so that it looks different, but still
    exhibit the same behavior.
    """
    sub_engine = SubEngine(debug=debug)
    key, encrypted_sc = encrypt(shellcode)
    

    final_program: str = ''
    with open('template.s') as template:
        for line in template:
            with RegexSwitch(line.strip()) as case:
                if case(_COMMENT_REGEX):
                    continue
                elif case(_ENCRYPTED_SC_TARGET_REGEX):
                    for chunk in encrypted_sc:
                        final_program += f'    .string "{chunk}"\n'
                elif case(_NUM_CHUNKS_TARGET_REGEX):
                    final_program += f'    .long   {len(encrypted_sc)}\n'
                elif case(_KEY_TARGET_REGEX):
                    final_program += f'    .string "{key}"\n'
                elif case(_TEMPLATE_TARGET_REGEX):
                    match = _TEMPLATE_TARGET_REGEX.fullmatch(line.strip())
                    template_filename: str = f'templates/{match.group(1)}.template'
                    rewritten_program: str = sub_engine.rewrite_template(template_filename)
                    final_program += f'{rewritten_program}\n'
                else:
                    final_program += line
    return final_program


def read_file(filename):
    builder: List[str] = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            builder.append(line)
    builder: str = ''.join(builder)
    return builder


def args_exist() -> bool:
    return any(v for _, v in vars(args).items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='?')
    parser.add_argument('-f', '--filename', help="Reads in a filename with a hexstring inside, encrypts it, and writes the .asm template with the original's substitutions")
    parser.add_argument('-s', '--stdin', help="Reads in a hexstring from stdin, encrypts it, and writes the .asm template with the original's substitutions")
    parser.add_argument('-d', '--debug', help='Print debug statements to stdout', required=False, action='store_true')
    args = parser.parse_args()
    if args.filename:
        shellcode: str = read_file(args.filename)
        print(shellcodify(asm_to_shellcode(morph(shellcode, debug=args.debug))))
    elif args.stdin:
        shellcode: str = args.stdin        
        print(shellcodify(asm_to_shellcode(morph(shellcode, debug=args.debug))))
    else:
        parser.print_help()
