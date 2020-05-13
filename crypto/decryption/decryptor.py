"""
decryptor.py generates a C program by reading in template.c and filling in the shellcode to replace _TARGET.
After generating, the program gets compiled and is executed.
"""


import sys
import os


MODULE_DIR_NAME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)


from typing import List, Union
import argparse


from encryption import encryptor


_EXECUTOR_TARGET: str = 'unsigned char code[];'
_EXECUTOR_TEMPLATE_PATH = 'templates/executor_template.c'
_DECRYPTOR_TARGET: str = 'unsigned char encrypted_sc[];' 
_DECRYPTOR_TEMPLATE_PATH: str = 'templates/decryptor_template.c' 
_KEY_TARGET: str = 'const static unsigned char key[];'
_IV_TARGET: str = 'unsigned char iv[AES_BLOCK_SIZE];'
_OUTPUT_PATH: str = 'output.c'
_OUTPUT_EXE_PATH: str = _OUTPUT_PATH[:_OUTPUT_PATH.index('.')]
_NL: str = '\n'


""" Converts from a hexstring/bytestring to a char array """
def to_char_array(sc: Union[str, bytes]) -> str:
    hexstring: str = sc.hex() if type(sc) == bytes else sc
    hexes: List[str] = [hexstring[i:i+2] for i in range(0, len(hexstring), 2)]
    with_hex_prefix = map(lambda v: '0x' + v, hexes)
    hex_arr: List[str] = list(with_hex_prefix)
    return '{' + ','.join(hex_arr) + '}'


def fill_template(sc: Union[bytes, str]) -> str:
    builder: List[str] = []
    file_to_read: str = _DECRYPTOR_TEMPLATE_PATH if args.plaintext else _EXECUTOR_TEMPLATE_PATH
    with open(file_to_read, 'r') as f:
        for line in f:
            line = line.lstrip()
            if args.plaintext and line.rstrip() == _DECRYPTOR_TARGET:
                char_arr = to_char_array(sc)
                print(char_arr)
                builder.append(f'unsigned char encrypted_sc[] = {char_arr};{_NL}')
            elif args.plaintext and line.rstrip() == _KEY_TARGET:
                char_arr = to_char_array(key)
                builder.append(f'const static unsigned char key[] = {char_arr};{_NL}')
            elif args.plaintext and line.rstrip() == _IV_TARGET:
                char_arr = to_char_array(iv)
                builder.append(f'unsigned char iv[] = {char_arr};{_NL}')
            elif args.execute and line.rstrip() == _EXECUTOR_TARGET:
                char_arr = to_char_array(sc)
                print(char_arr)
                builder.append(f'unsigned char code[] = {char_arr};{_NL}')
            else:
                builder.append(line)
    return ''.join(builder)


def read_file(filename: str) -> str:
    builder: str = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            builder.append(line)
    return ''.join(builder)


def write_file(builder: str) -> None:
    with open(_OUTPUT_PATH, 'w') as f:
        f.write(builder)


def execute_program() -> None:
    os.system(f'gcc {_OUTPUT_PATH} -g -o {_OUTPUT_EXE_PATH} -fno-stack-protector -z execstack -m32 -lssl3 -lcrypto ')
    os.system(f'./{_OUTPUT_EXE_PATH}')


def args_exist() -> bool:
    return any(v for _, v in vars(args).items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a C program by reading in a template and filling in the shellcode. After generating, the program gets compiled and is executed.')
    parser.add_argument('-x', '--execute', help='Generate a C program that executes shellcode')
    parser.add_argument('-p', '--plaintext', help='Encrypt plaintext shellcode, encrypt within this file, and then decrypt with a generated C program')
    parser.add_argument('-f', '--file', help='Read from a file, encrypt within this file, and then decrypt within template', required=False, action='store_true')
    args = parser.parse_args()
    if args_exist():
        if args.plaintext:
            key, iv, encrypted_sc = encryptor.encrypt_sc(bytes.fromhex(args.plaintext))
            builder: str = fill_template(encrypted_sc)
        if args.execute and not args.file:
            builder: str = fill_template(args.execute)
        if args.execute and args.file:
            builder: str = read_file(args.execute)
            builder: str = fill_template(builder)
        write_file(builder)
        execute_program()
    else:
        parser.print_help()
