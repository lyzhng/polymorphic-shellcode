import re


import parser
from compiler import Compiler
from utils import RegexSwitch

_ENCRYPTED_SC = b''
_IV = b''
_KEY = b''

_ENCRYPTED_SC_TARGET_REGEX = re.compile(r'{{ ENCRYPTED_SC }}')
_IV_TARGET_REGEX = re.compile(r'{{ IV }}')
_KEY_TARGET_REGEX = re.compile(r'{{ KEY }}')
_TEMPLATE_TARGET_REGEX = re.compile(r'[\t ]*{{ ([\w\d_]+) }}[\t ]*')


def main():
    final_program: str = ''
    compiler = Compiler()
    
    with open('template.s') as template:
        for line in template:
            with RegexSwitch(line.strip()) as case:
                if case(_ENCRYPTED_SC_TARGET_REGEX):
                    final_program += f'        .string "{_ENCRYPTED_SC}"\n'
                elif case(_IV_TARGET_REGEX):
                    final_program += f'        .ascii "{_IV}"\n'
                elif case(_KEY_TARGET_REGEX):
                    key_part_one: str = _KEY[:21]
                    key_part_two: str = _KEY[21:]
                    final_program += f'        .ascii "{key_part_one}"\n'
                    final_program += f'        .ascii "{key_part_two}"\n'
                elif case(_TEMPLATE_TARGET_REGEX):
                    match = _TEMPLATE_TARGET_REGEX.fullmatch(line.strip())
                    if match is not None:
                        template_filename: str = f'{match.group(1)}.template'
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
    main()