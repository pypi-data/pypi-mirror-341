# data/namespace.py

from typing import Dict, List
from .parsed_type import ParsedType

class Namespace:
    def __init__(self, name: str, full_name: str | None = None):
        self.name = name
        self.full_name = full_name if full_name is not None else name
        self.types: List[ParsedType] = []
        self.sub_namespaces: Dict[str, "Namespace"] = {}

    def add_type(self, parsed_type: ParsedType):
        self.types.append(parsed_type)

    def add_subnamespace(self, sub_ns: "Namespace"):
        self.sub_namespaces[sub_ns.name] = sub_ns

    def __repr__(self):
        return f"<Namespace {self.full_name}: {len(self.types)} types, {len(self.sub_namespaces)} sub-namespaces>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = [
            f"{pad}Namespace:",
            f"{pad}  Name      : {self.name}",
            f"{pad}  Full Name : {self.full_name}",
            f"{pad}  Types     :"
        ]
        if self.types:
            for typ in self.types:
                lines.append(typ.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        lines.append(f"{pad}  Sub-namespaces:")
        if self.sub_namespaces:
            for sub_ns in self.sub_namespaces.values():
                lines.append(sub_ns.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        return "\n".join(lines)
