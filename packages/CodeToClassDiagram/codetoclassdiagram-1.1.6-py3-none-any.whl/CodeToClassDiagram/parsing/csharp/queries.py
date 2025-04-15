# parsing/csharp/queries.py

from tree_sitter import Query

# Query to match method_declaration nodes.
# Adjust the node types according to your installed grammar.
METHOD_QUERY = """
(
  (method_declaration
    name: (identifier) @method.name
    return_type: (type) @method.return_type
    parameter_list: (parameter_list) @method.parameters
    modifiers: (modifier) @method.modifier)?
)
"""

# Similarly, add queries for properties, namespaces, or other constructs.
PROPERTY_QUERY = """
(
  (property_declaration
    name: (identifier) @property.name
    type: (type) @property.type
    accessor_list: (accessor_list) @property.body
    modifiers: (modifier) @property.modifier)?
)
"""

# For a generic query, you can later combine different patterns.
