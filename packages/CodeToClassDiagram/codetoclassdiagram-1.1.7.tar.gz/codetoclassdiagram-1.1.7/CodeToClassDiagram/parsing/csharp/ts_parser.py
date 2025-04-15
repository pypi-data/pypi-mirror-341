# parsing/csharp/ts_parser.py

import os
from tree_sitter import Language, Parser
import tree_sitter_c_sharp  as tscsharp
from typing import List
from CodeToClassDiagram.data import Project, convert_parsed_type

# Load the compiled C# language from the shared library
CSHARP_LANGUAGE = Language(tscsharp.language())

# Create and configure the Tree-sitter parser.
ts_parser = Parser()
ts_parser.language = CSHARP_LANGUAGE

def get_node_text(node, source_code: bytes) -> str:
    """Extract the UTF-8 text of a node from the source code."""
    return source_code[node.start_byte:node.end_byte].decode('utf-8')

def get_namespace_name(namespace_node, source_code: bytes) -> str:
    """
    Given a namespace_declaration node, extract its full name.
    This implementation looks for a child node of type "qualified_name".
    """
    for child in namespace_node.children:
        if child.type == "qualified_name":
            return get_node_text(child, source_code)
    return "Global"

def extract_method_info(method_node, source_code: bytes) -> dict:
    """
    Extract a raw dictionary for a method declaration.
    It assumes:
      - The method name is in an 'identifier' node.
      - The return type is in a child of type 'type' or 'predefined_type'.
      - The parameter list is contained in a 'parameter_list' node.
      - Modifiers are contained in child nodes of type 'modifier'.
    """
    modifiers = []
    method = {
        "name": "",
        "return_type": "",
        "params": "",
        "modifiers": modifiers
    }
    for child in method_node.children:
        if child.type == "identifier" and not method["name"]:
            method["name"] = get_node_text(child, source_code)
        elif child.type in {"type", "predefined_type"} and not method["return_type"]:
            method["return_type"] = get_node_text(child, source_code)
        elif child.type == "parameter_list":
            method["params"] = get_node_text(child, source_code)
        elif child.type == "modifier":
            method["modifiers"].append(get_node_text(child, source_code))
    return method

def extract_property_info(prop_node, source_code: bytes) -> dict:
    """
    Extract a raw dictionary for a property declaration.
    It assumes:
      - The property type is in a node of type 'type' or 'predefined_type'.
      - The property name is in an 'identifier' node.
      - The accessor list (body) is in an 'accessor_list' node.
      - Modifiers are in nodes of type 'modifier'.
    """
    modifiers= []
    prop = {
        "name": "",
        "type": "",
        "body": "",
        "modifiers": modifiers
    }
    for child in prop_node.children:
        if child.type in {"type", "predefined_type"} and not prop["type"]:
            prop["type"] = get_node_text(child, source_code)
        elif child.type == "identifier" and not prop["name"]:
            prop["name"] = get_node_text(child, source_code)
        elif child.type == "modifier":
            prop["modifiers"].append(get_node_text(child, source_code))
        elif child.type == "accessor_list":
            prop["body"] = get_node_text(child, source_code)
    return prop

def extract_type_info(type_node, source_code: bytes) -> dict:
    """
    Extract a raw dictionary for a type declaration (class, interface, or enum).
    It extracts the name, any base types, and iterates over member declarations.
    """
    methods= []
    bases= []
    usings= []
    properties= []
    type_info= {
        "kind": "",
        "name": "",
        "bases": bases, 
        "methods": methods, 
        "properties": properties, 
        "namespace": None,
        "usings": usings
        # To be filled in later from file-level using directives.
    }
    if type_node.type == "class_declaration":
        type_info["kind"] = "class"
    elif type_node.type == "interface_declaration":
        type_info["kind"] = "interface"
    elif type_node.type == "enum_declaration":
        type_info["kind"] = "enum"

    for child in type_node.children:
        if child.type == "identifier" and not type_info["name"]:
            type_info["name"] = get_node_text(child, source_code)
        elif child.type == "base_list":
            bases_text = get_node_text(child, source_code)
            if bases_text.startswith(":"):
                bases_text = bases_text[1:]
            type_info["bases"] = [b.strip() for b in bases_text.split(",") if b.strip()]
        elif child.type == "declaration_list":
            for member in child.children:
                if member.type == "method_declaration":
                    method = extract_method_info(member, source_code)
                    type_info["methods"].append(method)
                elif member.type == "property_declaration":
                    prop = extract_property_info(member, source_code)
                    type_info["properties"].append(prop)
                # Additional member types (fields, events, etc.) can be added here.
    return type_info

def extract_types_from_tree(root_node, source_code: bytes, current_namespace="Global") -> list:
    """
    Recursively traverse the AST starting at root_node to extract type declarations.
    If a namespace_declaration is found, update the current namespace.
    """
    types = []
    for child in root_node.children:
        if child.type == "namespace_declaration":
            ns = get_namespace_name(child, source_code)
            types.extend(extract_types_from_tree(child, source_code, current_namespace=ns))
        elif child.type in {"class_declaration", "interface_declaration", "enum_declaration"}:
            type_info = extract_type_info(child, source_code)
            type_info["namespace"] = current_namespace
            types.append(type_info)
        else:
            # Recurse into other nodes.
            types.extend(extract_types_from_tree(child, source_code, current_namespace))
    return types

def extract_using_directives(root_node, source_code: bytes) -> list:
    """
    Traverse the AST to extract using_directive nodes.
    Returns a list of raw using directive strings.
    """
    usings = []
    cursor = root_node.walk()
    reached_root = False
    while not reached_root:
        node = cursor.node
        if node.type == "using_directive":
            using_text = get_node_text(node, source_code)
            usings.append(using_text.strip())
        if cursor.goto_first_child():
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
            if cursor.goto_next_sibling():
                retracing = False
    return usings

def parse_cs_file_ts(file_path: str) -> list:
    """
    Parse a C# file using Tree-sitter and return a list of raw type dictionaries.
    Each dictionary is in the format expected by the conversion helper.
    """
    with open(file_path, 'rb') as f:
        source_code = f.read()
    tree = ts_parser.parse(source_code)
    root_node = tree.root_node

    # Extract file-level using directives.
    usings = extract_using_directives(root_node, source_code)
    # Extract type declarations along with their current namespace.
    types_raw = extract_types_from_tree(root_node, source_code)
    # Attach the using directives to each type dictionary.
    for t in types_raw:
        t["usings"] = usings
    return types_raw

def parse_project(folder_path: str, exclude_files=None) -> Project:
    """
    Traverse folder_path, parse all C# files using Tree-sitter,
    convert raw data into the intermediate representation,
    and return a Project object.
    """
    raw_types = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                if exclude_files and any(pattern in file_path for pattern in exclude_files):
                    continue
                raw_types.extend(parse_cs_file_ts(file_path))
    project = Project()
    # Convert each raw type dictionary into a ParsedType instance.
    for raw in raw_types:
        project.add_type(convert_parsed_type(raw))
    return project
