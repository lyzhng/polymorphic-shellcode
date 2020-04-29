"""
decryptor.py generates a C program by reading in template.c and filling in the shellcode to replace _TARGET.
After generating, the program gets compiled and is executed.
"""


import sys
import os
from typing import List
import argparse


_EXECUTOR_TARGET: str = 'const unsigned char code[];'
_DECRYPTOR_TARGET: str = 'const unsigned char encrypted_execve_sc[];'  
_NL: str = '\n'  


def fill_template(sc: str) -> str:
	builder: List[str] = []
	file_to_read: str = 'templates/decryptor_template.c' if args.decrypt else 'templates/executor_template.c'
	with open(file_to_read, 'r') as f:
		for line in f:
			line = line.lstrip()
			if args.decrypt and line.rstrip() == _DECRYPTOR_TARGET:
				builder.append(f'const unsigned char encrypted_execve_sc[] = "{sc}";{_NL}')
			elif args.execute and line.rstrip() == _EXECUTOR_TARGET:
				builder.append(f'const unsigned char code[] = "{sc}";{_NL}')
			else:
				builder.append(line)
	return ''.join(builder)


def write_file(builder: str) -> None:
	with open('output.c', 'w') as f:
		f.write(builder)


def execute_program() -> None:
    os.system('gcc output.c -g -o output -lssl3 -lcrypto -fno-stack-protector -z execstack -m32')
    os.system('./output')


def args_exist() -> bool:
	return any(v for _, v in vars(args).items())


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate a C program by reading in a template and filling in the shellcode. After generating, the program gets compiled and is executed.')
	parser.add_argument('-d', '--decrypt', help='Generate a C program that decrypts the shellcode and then executes it')
	parser.add_argument('-x', '--execute', help='Generate a C program that executes shellcode')
	args = parser.parse_args()
	if args_exist():
		if args.decrypt:
			builder = fill_template(args.decrypt)
		if args.execute:
			builder = fill_template(args.execute)
		write_file(builder)
		execute_program()
	else:
		parser.print_help()
