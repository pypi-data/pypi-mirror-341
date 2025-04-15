import sys
import os
import importlib
from CodeToClassDiagram.config import load_config, load_internal_config, init_config_file

def validate_config(config, internal_config):
    inp_type = config.get("input_filetype")
    out_type = config.get("output", {}).get("diagram")
    
    if inp_type not in internal_config.get("input_filetype_mapping", {}):
        print(f"Error: input_filetype '{inp_type}' is not supported in the internal config.")
        sys.exit(1)
    if out_type not in internal_config.get("output_diagram_mapping", {}):
        print(f"Error: diagram '{out_type}' is not supported in the internal config.")
        sys.exit(1)

def dynamic_import(module_path):
    module_dot = module_path.replace("/", ".").removesuffix(".py")
    try:
        return importlib.import_module(module_dot)
    except Exception as e:
        print(f"Error importing module '{module_dot}': {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  code2class init [config_file]  # Create the default config file")
        print("  code2class <folder_path> <config_file>  # Parse the project and generate the diagram")
        sys.exit(1)

    if sys.argv[1] == "init":
        config_path = sys.argv[2] if len(sys.argv) >= 3 else "config.json"
        init_config_file(config_path)
        sys.exit(0)

    if len(sys.argv) != 3:
        print("Usage: code2class <folder_path> <config_file>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    config_path = sys.argv[2]
    
    config = load_config(config_path)
    internal_config = load_internal_config()
    
    validate_config(config, internal_config)
    
    input_type = config.get("input_filetype")
    parser_module_path = internal_config["input_filetype_mapping"][input_type]
    parser_module = dynamic_import(parser_module_path)
    
    output_obj = config.get("output", {})
    output_type = output_obj.get("diagram")
    diagram_module_path = internal_config["output_diagram_mapping"][output_type]
    diagram_module = dynamic_import(diagram_module_path)
    
    # The new Tree-sitter based parser module is now dynamically loaded.
    classes = parser_module.parse_project(folder_path, exclude_files=config.get("exclude_files"))
    
    try:
        diagram_generator = diagram_module.create_generator(classes, output_obj)
    except AttributeError:
        print("Error: The diagram module does not provide a 'create_generator' function.")
        sys.exit(1)
    
    diagram = diagram_generator.generate()
    
    if output_obj.get("mode", "console") == "file":
        output_file = output_obj.get("file", "diagram.md")
        try:
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(diagram)
            print(f"Diagram written to {output_file}")
        except Exception as e:
            print(f"Error writing file: {e}")
    else:
        print("Generated diagram:")
        print(diagram)

if __name__ == "__main__":
    main()
