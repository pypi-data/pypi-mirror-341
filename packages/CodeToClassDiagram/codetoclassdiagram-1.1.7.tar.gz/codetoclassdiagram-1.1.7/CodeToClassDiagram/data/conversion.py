# data/conversion.py

import re
from typing import Any, Dict, Tuple
from .parsed_type import ParsedType
from .method import ParsedMethod
from .property import ParsedProperty
from .parameter import Parameter

def extract_generics(type_name: str) -> Tuple[str, str | None ]:
    match = re.match(r'(\w+)\s*<\s*([^>]+)\s*>', type_name)
    if match:
        return match.group(1), match.group(2)
    return type_name, None

def convert_method(raw_method: Dict[str, Any]) -> ParsedMethod:
    name = raw_method.get("name", "")
    modifiers = raw_method.get("modifiers", [])
    return_type = raw_method.get("return_type", None)
    parameters = []
    raw_params = raw_method.get("params", "")
    if raw_params:
        for param in raw_params.split(','): 
            param_data = (param.split(" "))[0]
            print(param_data)
            parameters.append(param_data)
    # body_ast is kept None here; later your AST parser can fill it.
    return ParsedMethod(name=name, return_type=return_type, parameters=parameters, modifiers=modifiers)

def convert_property(raw_property: Dict[str, Any]) -> ParsedProperty:
    name = raw_property.get("name", "")
    property_type = raw_property.get("type", "")
    modifiers = raw_property.get("modifiers", [])
    body = raw_property.get("body", "")
    return ParsedProperty(name=name, property_type=property_type, modifiers=modifiers, body=body)


def convert_parsed_type(raw: dict) -> ParsedType:
    kind = raw.get("kind", "")
    full_name = raw.get("name", "")
    base_name, generics = extract_generics(full_name)
    bases = raw.get("bases", [])
    namespace = raw.get("namespace", "Global")
    using_directives = raw.get("usings", [])
    
    parsed = ParsedType(
        kind=kind,
        name=base_name,
        namespace=namespace,
        generics=generics,
        bases=bases,
        using_directives=using_directives,
    )

    for raw_method in raw.get("methods", []):
        method = convert_method(raw_method)
        parsed.add_method(method)
    for raw_prop in raw.get("properties", []):
        prop = convert_property(raw_prop)
        parsed.add_property(prop)

    return parsed

def extract_hidden_dependencies(method_body: str) -> list:
    # A simple regex to search for "new <TypeName>(" patterns
    pattern = r'new\s+(?P<type>[\w\.<>]+)\s*\('
    matches = re.findall(pattern, method_body)
    return matches

