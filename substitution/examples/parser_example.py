"""
An example of how to use the substitution parser module.
"""

# pylint: disable=wrong-import-position,eval-used,import-error

import os
import sys


MODULE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))
if MODULE_DIR_NAME not in sys.path:
    sys.path.insert(0, MODULE_DIR_NAME)
PARENT_DIR_NAME = os.path.join(MODULE_DIR_NAME, '..')
if PARENT_DIR_NAME not in sys.path:
    sys.path.insert(0, PARENT_DIR_NAME)


import substitution_parser as parser


def main():
    'Sample usage of the subsitution parser module.'
    print('Here are some sample valid inputs...')
    print('> ["mov eax, ebx"]')
    print('> ["mov eax, 0x5d", "add eax, ebx", "sub eax, ecx"]')
    print('')
    print('Enter exit to quit at any time')
    print('')

    prompt = 'Enter asm commands in list format (Note: enter for previous, default for default):'
    default_asm_code = ['mov eax, 0x5d', 'add eax, ebx', 'sub eax, ecx']
    asm_code = []
    while True:
        print(prompt)
        user_input = input('> ')
        if user_input == 'exit':
            sys.exit(0)
        elif user_input == 'default':
            asm_code = default_asm_code
        elif user_input == '' and asm_code == []:
            asm_code = default_asm_code
        elif user_input != '':
            asm_code = eval(user_input)

        print('\nRunning the parser on:')
        for line in asm_code:
            print(line)

        parse_data = parser.parse(asm_code)

        print('')
        print('The output is...')
        for parse_annotation in parse_data:
            print(parse_annotation)
        print('')


if __name__ == '__main__':
    main()
