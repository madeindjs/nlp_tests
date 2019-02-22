import sys
from termcolor import colored, cprint


class Entity():
    """Represent a word, an expression, or something else"""

    def __init__(self, entity):
        self.content = entity.text
        self.type = entity.label_

    def __str__(self):
        return "{} [{}]".format(self.content, self.type)
