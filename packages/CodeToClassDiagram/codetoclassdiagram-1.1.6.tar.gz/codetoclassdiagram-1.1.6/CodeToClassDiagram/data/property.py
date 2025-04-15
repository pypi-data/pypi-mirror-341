# data/property.py

from typing import List, Optional
from .parsed_member import ParsedMember

class ParsedProperty(ParsedMember):
    def __init__(self, name: str, property_type: str, modifiers: Optional[List[str]] = None, body: Optional[str] = None):
        super().__init__(name, modifiers)
        self.property_type = property_type
        self.body = body  # The accessor code or expression, if needed

    def __repr__(self):
        static_str = " static" if "static" in self.modifiers else ""
        return f"<Property{static_str} {self.property_type} {self.name}>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        static_str = "Yes" if "static" in self.modifiers else "No"
        lines = [
            f"{pad}Property:",
            f"{pad}  Name       : {self.name}",
            f"{pad}  Type       : {self.property_type}",
            f"{pad}  Modifiers  : {self.modifiers}",
            f"{pad}  Body       : {self.body}"
        ]
        return "\n".join(lines)
