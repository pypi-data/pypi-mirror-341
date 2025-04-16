#--------------------------------------------------
# Compiler
#--------------------------------------------------

from relationalai.early_access.metamodel import ir, compiler as c

class Compiler(c.Compiler):
    def __init__(self):
        # No passes yet.
        super().__init__([])

    # TODO (azreika): Return type should be LQP IR once that's in
    def do_compile(self, model: ir.Model, options:dict={}):
        raise NotImplementedError("LQP compiler not implemented yet.")
