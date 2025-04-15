# data/method.py

from typing import List, Optional
from .parameter import Parameter
from .parsed_member import ParsedMember  # See below for ParsedMember

class ParsedMethod(ParsedMember):
    def __init__(
        self,
        name: str,
        return_type: Optional[str],
        parameters: Optional[List[Parameter]] = None,
        modifiers: Optional[List[str]] = None,
        body_ast=None
    ):
        super().__init__(name, modifiers)
        self.return_type = return_type
        self.parameters = parameters if parameters is not None else []
        self.body_ast = body_ast  # This can later reference the raw AST node for deeper parsing

    def __repr__(self):
        static_str = " static" if "static" in self.modifiers else ""
        params = ", ".join(f"{p.param_type} {p.name}" for p in self.parameters)
        ret = f": {self.return_type}" if self.return_type else ""
        return f"<Method{static_str} {self.name}({params}){ret}>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        static_str = "Yes" if "static" in self.modifiers else "No"
        lines = [
            f"{pad}Method:",
            f"{pad}  Name       : {self.name}",
            f"{pad}  Modifiers  : {self.modifiers}",
            f"{pad}  Return Type: {self.return_type}",
            f"{pad}  Parameters :"
        ]
        if self.parameters:
            for param in self.parameters:
                lines.append(param.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        return "\n".join(lines)
