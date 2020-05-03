"""
The utils module provide some functions for syntactic sugar.
"""


class RegexSwitch:

    """
    A class used to mimic the switch statement in other languages.  This one operates
    on regular expressions.
    """

    def __init__(self, operand_type):
        self.operand_type = operand_type


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False


    def __call__(self, pattern):
        return pattern.match(self.operand_type)
