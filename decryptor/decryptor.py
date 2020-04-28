"""
decryptor.py generates a c program by reading in template.c and filling in the shellcode for _TARGET.
After generating, the program gets compiled and is executed.
"""


import sys
import os
from typing import List


_TARGET: str = 'const unsigned char encrypted_execve_sc[];'  
_NL: str = '\n'  


def fill_template(sc: str) -> str:
	builder: List[str] = []
	with open('template.c', 'r') as f:
		for line in f:
			line = line.lstrip()
			if line.rstrip() == _TARGET:
				builder.append(f'const unsigned char encrypted_execve_sc[] = "{sc}";{_NL}')
			else:
				builder.append(line)
	return ''.join(builder)


def write_file(builder: str) -> None:
	with open('output.c', 'w') as f:
		f.write(builder)


def execute_program() -> None:
    os.system('gcc output.c -g -o output -lssl3 -lcrypto -fno-stack-protector -z execstack -m32')
    os.system('./output')


if __name__ == '__main__':
	builder = fill_template(sys.argv[1])
	write_file(builder)
	execute_program()
