# data/parameter.py

from typing import List, Optional

class Parameter:
    def __init__(self, param_type: str, name: str, annotations: Optional[List[str]] = None):
        self.param_type = param_type
        self.name = name
        self.annotations = annotations if annotations is not None else []

    def __repr__(self):
        return f"<Parameter {self.param_type} {self.name}>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = [
            f"{pad}Parameter:",
            f"{pad}  Type       : {self.param_type}",
            f"{pad}  Name       : {self.name}",
            f"{pad}  Annotations: {self.annotations}"
        ]
        return "\n".join(lines)
