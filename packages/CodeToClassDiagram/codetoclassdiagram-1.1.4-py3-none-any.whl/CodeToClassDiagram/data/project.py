# data/project.py

from typing import Dict, List, Optional
from .parsed_type import ParsedType
from .namespace import Namespace

class Project:
    def __init__(self):
        self.namespaces: Dict[str, Namespace] = {}
        self.global_types: List[ParsedType] = []

    def add_type(self, parsed_type: ParsedType):
        ns_name = parsed_type.namespace or "Global"
        if ns_name == "Global":
            self.global_types.append(parsed_type)
        else:
            parts = ns_name.split('.')
            top = parts[0]
            if top not in self.namespaces:
                self.namespaces[top] = Namespace(top, full_name=top)
            current_ns = self.namespaces[top]
            for part in parts[1:]:
                if part not in current_ns.sub_namespaces:
                    full = current_ns.full_name + '.' + part
                    current_ns.sub_namespaces[part] = Namespace(part, full_name=full)
                current_ns = current_ns.sub_namespaces[part]
            current_ns.add_type(parsed_type)

    def __repr__(self):
        ns_count = len(self.namespaces)
        gt_count = len(self.global_types)
        return f"<Project: {ns_count} top-level namespaces, {gt_count} global types>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = [f"{pad}Project:"]
        lines.append(f"{pad}  Global Types:")
        if self.global_types:
            for typ in self.global_types:
                lines.append(typ.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        lines.append(f"{pad}  Namespaces:")
        if self.namespaces:
            for ns in self.namespaces.values():
                lines.append(ns.describe(indent + 2))
        else:
            lines.append(f"{pad}    None")
        return "\n".join(lines)
