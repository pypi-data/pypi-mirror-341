# data/parsed_type.py

from typing import List, Optional
from .method import ParsedMethod
from .property import ParsedProperty

class ParsedType:
    def __init__(
        self,
        kind: str,
        name: str,
        namespace: str,
        generics: Optional[str] = None,
        bases: Optional[List[str]] = None,
        using_directives: Optional[List[str]] = None
    ):
        self.kind = kind                # e.g., "class", "interface", "enum"
        self.name = name
        self.namespace = namespace
        self.generics = generics
        self.bases = bases if bases is not None else []
        self.using_directives = using_directives if using_directives is not None else []
        self.methods: List[ParsedMethod] = []
        self.properties: List[ParsedProperty] = []
        self.visible_dependencies: List[str] = []  # from signatures & property types
        self.hidden_dependencies: List[str] = []   # from within method bodies

    def add_method(self, method: ParsedMethod):
        self.methods.append(method)
        if method.return_type:
            self.visible_dependencies.append(method.return_type)
        for param in method.parameters:
            self.visible_dependencies.append(param.param_type)

    def add_property(self, prop: ParsedProperty):
        self.properties.append(prop)
        self.visible_dependencies.append(prop.property_type)

    def __repr__(self):
        gen = f"<{self.generics}>" if self.generics else ""
        return f"<ParsedType {self.kind} {self.namespace}.{self.name}{gen}>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        gen_str = self.generics if self.generics else "None"
        lines = [
            f"{pad}ParsedType:",
            f"{pad}  Kind               : {self.kind}",
            f"{pad}  Name               : {self.name}",
            f"{pad}  Generics           : {gen_str}",
            f"{pad}  Namespace          : {self.namespace}",
            f"{pad}  Bases              : {self.bases}",
            f"{pad}  Using Directives   : {self.using_directives}",
            f"{pad}  Visible Dependencies: {self.visible_dependencies}",
            f"{pad}  Hidden Dependencies : {self.hidden_dependencies}",
            f"{pad}  Methods            :"
        ]
        if self.methods:
            for m in self.methods:
                lines.append(m.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        lines.append(f"{pad}  Properties         :")
        if self.properties:
            for p in self.properties:
                lines.append(p.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        return "\n".join(lines)
