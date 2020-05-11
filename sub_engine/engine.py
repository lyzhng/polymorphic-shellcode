"""
The engine module utilize the parser and compiler modules to rewrite the given template.
"""


import os


from . import parser
from .compiler import Compiler
from .parser import Annotation


_CURRENT_SCRIPT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SIGNATURE_DIRECTORY: str = f'{_CURRENT_SCRIPT_DIRECTORY}/library'


class SubEngine():

    """
    The SubEngine class uses the parser and compiler module to rewrite the given
    template.
    """

    def __init__(self, signature_directory: str = _DEFAULT_SIGNATURE_DIRECTORY):
        self.compiler = Compiler()
        self.compiler.discover_signatures(signature_directory)


    def rewrite_template(self, template_name: str):
        """
        Read in the template specified by the given template_name parameter and rewrite
        the code using different instructions.
        """
        operand_to_type_mapping, code = parser.preprocess(template_name)
        annotations: List[Annotations] = parser.parse(operand_to_type_mapping, code)
        rewritten_program: str = self.compiler.apply_substitution(annotations, debug=False)
        return '\n'.join([f'        {line}' for line in rewritten_program.split('\n')])
