# third party libraries
import libcst as cst
import libcst.matchers as m
class AddProfileDecorator(cst.CSTTransformer):
    def __init__(self):
        super().__init__()
        self.modified_code = {}

    """CST Transformer to add @lprofile_ext decorator to function definitions."""
    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        has_profile = any(
            m.matches(deco, m.Decorator(decorator=m.Name("lprofile_ext")))
            for deco in updated_node.decorators
        )
        if not has_profile:
            new_decorators = [cst.Decorator(decorator=cst.Name("lprofile_ext"))] + list(updated_node.decorators)
            return updated_node.with_changes(decorators=new_decorators)
        return updated_node
    
    def get_modified_code(self, source):
        tree = cst.parse_module(source)
        modified_tree = tree.visit(self)
        modified_code = modified_tree.code
        return modified_code
    
    def set_modified_code(self, filename, modified_code):
        self.modified_code[filename] = modified_code

profile_decorator = AddProfileDecorator()

from line_profiler import LineProfiler 
profiler = LineProfiler()