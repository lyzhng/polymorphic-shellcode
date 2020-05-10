"""
The utils module provide some functions for syntactic sugar.
"""


class RegexSwitch:

    """
    A class used to mimic the switch statement in other languages.  This one operates
    on regular expressions.
    """

    def __init__(self, value):
        self.value = value


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False


    def __call__(self, pattern):
        return pattern.match(self.value)


class Switch:

    """
    A class used to mimic the switch statement in other languages.  This one operates
    on primitives.
    """

    def __init__(self, value):
        self.value = value


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return False


    def __call__(self, other):
        return self.value == other