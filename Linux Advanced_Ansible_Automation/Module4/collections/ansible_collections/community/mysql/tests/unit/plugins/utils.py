from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class dummy_cursor_class():
    """Dummy class for returning an answer for SELECT VERSION()."""
    def __init__(self, output, ret_val_type='dict'):
        self.output = output
        self.ret_val_type = ret_val_type

    def execute(self, query):
        pass

    def fetchone(self):
        if self.ret_val_type == 'dict':
            return {'version': self.output}

        elif self.ret_val_type == 'list':
            return [self.output]
