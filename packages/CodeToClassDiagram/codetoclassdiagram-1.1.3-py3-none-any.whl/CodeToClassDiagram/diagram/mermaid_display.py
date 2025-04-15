# diagram/mermaid_display.py

from .display_utils import extract_base_types, should_exclude_package

# Constant for whether to show the return type in method signatures.
SHOW_RETURN_TYPE_DOT = False  # Set to False to disable the display of the return type.

class MermaidDiagram:
    def __init__(self, project, output_config):
        """
        Initialize the MermaidDiagram generator.
        
        :param project: The project instance containing global_types and namespaces.
        :param output_config: Dictionary with output settings. Expected keys include:
            - "exclude_namespaces": list of namespace full names to exclude.
            - "hide_implemented_interface_methods": bool (optional)
            - "hide_implemented_interface_properties": bool (optional)
            - "show_dependencies": bool (optional) - Enable or disable dependency links.
        """
        self.project = project
        self.output_config = output_config or {}
        self.exclude_namespaces = set(self.output_config.get("exclude_namespaces", []))
        self.hide_methods = self.output_config.get("hide_implemented_interface_methods", True)
        self.hide_properties = self.output_config.get("hide_implemented_interface_properties", True)
        self.show_dependencies = self.output_config.get("show_dependencies", False)

    def generate(self):
        """
        Generate and return a Mermaid class diagram as a string.
        """
        diagram_lines = ["classDiagram"]

        # Build dictionaries mapping interface names to member signatures.
        interface_methods_dict = self.build_interface_methods_dict()
        interface_properties_dict = self.build_interface_properties_dict()

        # Render global (outside namespace) types.
        for ptype in self.project.global_types:
            diagram_lines.extend(
                self.render_type(
                    ptype,
                    indent="  ",
                    inside_namespace=False,
                    interface_methods=interface_methods_dict,
                    interface_properties=interface_properties_dict
                )
            )

        # Flatten all namespaces and render each as a flat block.
        all_namespaces = self.flatten_namespaces(self.project.namespaces)
        for ns_obj in sorted(all_namespaces, key=lambda ns: ns.full_name):
            if ns_obj.full_name in self.exclude_namespaces:
                continue
            ns_block = self.render_flat_namespace(
                ns_obj,
                indent="    ",
                interface_methods=interface_methods_dict,
                interface_properties=interface_properties_dict
            )
            if not ns_block:
                continue  # Skip empty namespaces.
            flat_ns = ns_obj.full_name.replace(".", "_")
            diagram_lines.append(f"  namespace {flat_ns} {{")
            diagram_lines.extend(ns_block)
            diagram_lines.append("  }")

        diagram_lines.append("")  # Blank line before relationships.

        # Gather all types (global and in flattened namespaces) to render inheritance and dependency relationships.
        all_types = self.project.global_types[:]
        for ns_obj in all_namespaces:
            all_types.extend(ns_obj.types)

        # Render inheritance relationships.
        for ptype in all_types:
            if should_exclude_package(ptype.namespace, self.exclude_namespaces):
                continue
            for base in ptype.bases:
                base_full_name = f"{ptype.namespace}_{base}" if ptype.namespace else base
                ptype_full_name = f"{ptype.namespace}_{ptype.name}" if ptype.namespace else ptype.name
                diagram_lines.append(f"  {ptype_full_name} --|> {base_full_name}")

        # Render dependency relationships if enabled.
        if self.show_dependencies:
            dependency_links = self.build_dependency_links(all_types, interface_methods_dict, interface_properties_dict)
            # Append a blank line for clarity.
            diagram_lines.append("")
            for dep_line in dependency_links:
                diagram_lines.append(f"  {dep_line}")

            # Render hidden dependencies with a distinct arrow style.
            hidden_dependency_links = self.build_hidden_dependency_links(all_types)
            if hidden_dependency_links:
                diagram_lines.append("")
                for hidden_link in hidden_dependency_links:
                    diagram_lines.append(f"  {hidden_link}")

        return "\n".join(diagram_lines)

    def build_dependency_links(self, all_types, interface_methods, interface_properties):
        """
        Build dependency links between types from visible dependencies.
        A dependency is added if a type uses another type in its properties or method signatures.
        If a dependency is already provided by an interface implementation (and hide flag is set), it will be omitted.

        Returns a sorted list of dependency link strings in Mermaid syntax (e.g. "A ..> B").
        """
        # Create a lookup of types by their simple name.
        type_lookup = {ptype.name: ptype for ptype in all_types}
        dependency_links = set()  # Use a set to avoid duplicates.

        for ptype in all_types:
            current_full_name = f"{ptype.namespace}_{ptype.name}" if ptype.namespace else ptype.name

            # For classes, collect dependency types from parent interfaces if configured.
            inherited_dependency_types = set()
            if ptype.kind == "class":
                for base_name in ptype.bases:
                    if base_name in type_lookup:
                        parent = type_lookup[base_name]
                        if parent.kind == "interface":
                            for prop in parent.properties:
                                inherited_dependency_types.add(prop.property_type.strip())
                            for method in parent.methods:
                                for param in method.parameters:
                                    inherited_dependency_types.add(param.param_type.strip())
                                if method.return_type:
                                    inherited_dependency_types.add(method.return_type.strip())

            # Process property dependencies.
            for prop in ptype.properties:
                base_types = extract_base_types(prop.property_type)
                for base in base_types:
                    if base in type_lookup:
                        base_full_name = f"{type_lookup[base].namespace}_{base}" if type_lookup[base].namespace else base
                        if base_full_name != current_full_name and base not in inherited_dependency_types:
                            dependency_links.add(f"{current_full_name} ..> {base_full_name}")

            # Process method dependencies.
            for method in ptype.methods:
                for param in method.parameters:
                    base_types = extract_base_types(param.param_type)
                    for base in base_types:
                        if base in type_lookup:
                            base_full_name = f"{type_lookup[base].namespace}_{base}" if type_lookup[base].namespace else base
                            if base_full_name != current_full_name and base not in inherited_dependency_types:
                                dependency_links.add(f"{current_full_name} ..> {base_full_name}")
                if method.return_type:
                    base_types = extract_base_types(method.return_type)
                    for base in base_types:
                        if base in type_lookup:
                            base_full_name = f"{type_lookup[base].namespace}_{base}" if type_lookup[base].namespace else base
                            if base_full_name != current_full_name and base not in inherited_dependency_types:
                                dependency_links.add(f"{current_full_name} ..> {base_full_name}")

        return sorted(dependency_links)

    def build_hidden_dependency_links(self, all_types):
        """
        Build dependency links based solely on the 'hidden_dependencies' field of each type.
        Hidden dependencies are typically those found inside method bodies (like instantiations).
        They are rendered with a distinct arrow style (here, using '..>>').
        
        Returns a sorted list of link strings.
        """
        type_lookup = {ptype.name: ptype for ptype in all_types}
        hidden_links = set()

        for ptype in all_types:
            current_full_name = f"{ptype.namespace}_{ptype.name}" if ptype.namespace else ptype.name
            for hidden_dep in ptype.hidden_dependencies:
                # For simplicity, assume hidden_dep is a simple name.
                if hidden_dep in type_lookup:
                    base_full_name = f"{type_lookup[hidden_dep].namespace}_{hidden_dep}" if type_lookup[hidden_dep].namespace else hidden_dep
                    if base_full_name != current_full_name:
                        hidden_links.add(f"{current_full_name} ..>> {base_full_name}")
        return sorted(hidden_links)

    def build_interface_methods_dict(self):
        """
        Build a dictionary mapping interface names to a set of method signatures.
        Only types with kind "interface" are included.
        """
        interface_methods = {}
        all_types = self.project.global_types[:]
        for ns_obj in self.flatten_namespaces(self.project.namespaces):
            all_types.extend(ns_obj.types)
        for ptype in all_types:
            if ptype.kind == "interface":
                sig_set = set()
                for method in ptype.methods:
                    sig_set.add(self.get_method_signature(method))
                interface_methods[ptype.name] = sig_set
        return interface_methods

    def build_interface_properties_dict(self):
        """
        Build a dictionary mapping interface names to a set of property signatures.
        Only types with kind "interface" are included.
        """
        interface_properties = {}
        all_types = self.project.global_types[:]
        for ns_obj in self.flatten_namespaces(self.project.namespaces):
            all_types.extend(ns_obj.types)
        for ptype in all_types:
            if ptype.kind == "interface":
                sig_set = set()
                for prop in ptype.properties:
                    sig_set.add(self.get_property_signature(prop))
                interface_properties[ptype.name] = sig_set
        return interface_properties

    @staticmethod
    def get_method_signature(method):
        """
        Build a method signature string of the form: methodName(paramType1,paramType2,...)
        """
        param_types = ",".join(p.param_type.strip() for p in method.parameters)
        return f"{method.name}({param_types})"

    @staticmethod
    def get_property_signature(prop):
        """
        Build a property signature string of the form: propertyName:propertyType
        """
        return f"{prop.name.strip()}:{prop.property_type.strip()}"

    def flatten_namespaces(self, ns_dict):
        """
        Recursively flatten a dictionary of Namespace objects (including sub-namespaces) into a flat list.
        """
        result = []
        for ns_obj in ns_dict.values():
            result.append(ns_obj)
            if ns_obj.sub_namespaces:
                result.extend(self.flatten_namespaces(ns_obj.sub_namespaces))
        return result

    def render_flat_namespace(self, ns_obj, indent="", interface_methods=None, interface_properties=None):
        """
        Render types within a namespace as a flat block.
        Returns a list of diagram lines.
        """
        lines = []
        for ptype in ns_obj.types:
            lines.extend(
                self.render_type(
                    ptype,
                    indent=indent,
                    inside_namespace=True,
                    interface_methods=interface_methods,
                    interface_properties=interface_properties
                )
            )
        return lines

    def render_type(self, ptype, indent="", inside_namespace=False, interface_methods=None, interface_properties=None):
        """
        Render a single ParsedType instance in Mermaid syntax.
        
        For classes:
          - Renders using the syntax: "class {name} { ... }".
          - Optionally hides methods and properties implemented via interfaces.
        For interfaces:
          - Renders as a class and, if rendered outside a namespace, adds a stereotype annotation.
        For enums:
          - Renders as a class with members.
        
        The flag inside_namespace controls additional annotation output.
        """
        lines = []
        kind = ptype.kind
        name = ptype.name
        namespace = ptype.namespace or "Global"
        full_name = f"{namespace}_{name}"  # Use namespace+name as the identifier
        interface_methods = interface_methods or {}
        interface_properties = interface_properties or {}

        if kind == "class":
            lines.append(f'{indent}class {full_name}["{name}"] {{')
            implemented_prop_signatures = set()
            if self.hide_properties:
                for base in ptype.bases:
                    if base in interface_properties:
                        implemented_prop_signatures |= interface_properties[base]
            for prop in ptype.properties:
                prop_sig = self.get_property_signature(prop)
                if self.hide_properties and prop_sig in implemented_prop_signatures:
                    continue
                prop_name = prop.name
                if getattr(prop, "static", False):
                    prop_name = f"«static» {prop_name}"
                lines.append(f"{indent}  +{prop_name}: {prop.property_type}")
            implemented_method_signatures = set()
            if self.hide_methods:
                for base in ptype.bases:
                    if base in interface_methods:
                        implemented_method_signatures |= interface_methods[base]
            for method in ptype.methods:
                sig = self.get_method_signature(method)
                if self.hide_methods and sig in implemented_method_signatures:
                    continue
                method_name = method.name
                if getattr(method, "static", False):
                    method_name = f"«static» {method_name}"
                params_str = ", ".join(f"{p.param_type} {p.name}" for p in method.parameters)
                ret = f"{':' if SHOW_RETURN_TYPE_DOT else ''} {method.return_type}" if method.return_type else ""
                lines.append(f"{indent}  +{method_name}({params_str}){ret}")
            lines.append(f"{indent}}}")
        elif kind == "interface":
            lines.append(f'{indent}class {full_name}["{name}"] {{')
            for prop in ptype.properties:
                prop_name = prop.name
                if getattr(prop, "static", False):
                    prop_name = f"«static» {prop_name}"
                lines.append(f"{indent}  +{prop_name}: {prop.property_type}")
            for method in ptype.methods:
                method_name = method.name
                if getattr(method, "static", False):
                    method_name = f"«static» {method_name}"
                params_str = ", ".join(f"{p.param_type} {p.name}" for p in method.parameters)
                ret = f"{':' if SHOW_RETURN_TYPE_DOT else ''} {method.return_type}" if method.return_type else ""
                lines.append(f"{indent}  +{method_name}({params_str}){ret}")
            lines.append(f"{indent}}}")
            if not inside_namespace:
                lines.append(f"{indent}<<interface>> {name}")
        elif kind == "enum":
            lines.append(f'{indent}class {full_name}["{name}"] {{')
            for member in ptype.members:
                lines.append(f"{indent}  +{member}")
            lines.append(f"{indent}}}")
            if not inside_namespace:
                lines.append(f"{indent}<<enum>> {name}")
        else:
            lines.append(f'{indent}class {full_name}["{name}"] {{}}')
        return lines

def create_generator(project, output_config):
    return MermaidDiagram(project, output_config)
