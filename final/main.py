import re


import parser
from compiler import Compiler

_ENCRYPTED_SC = b''
_IV = b''
_KEY = b''

_TEMPLATE_TARGET_REGEX = re.compile(r'[\t ]*{{ ([\w\d_]+) }}[\t ]*')


def main():
    final_program: str = ''
    compiler = Compiler()
    
    with open('template.s') as template:
        for line in template:
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