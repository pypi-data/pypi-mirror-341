# data/parsed_member.py

from typing import List, Optional

class ParsedMember:
    def __init__(self, name: str, modifiers: Optional[List[str]] = None):
        self.name = name
        self.modifiers = modifiers if modifiers is not None else []

    def __repr__(self):
        return f"<Member {self.name} with modifiers {self.modifiers}>"

    def describe(self, indent: int = 0) -> str:
        pad = "  " * indent
        return f"{pad}Member: {self.name} (Modifiers: {self.modifiers})"
