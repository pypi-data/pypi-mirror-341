import json
import sys
import os
import importlib.resources as pkg_resources

def load_config(config_path):
    """
    Load the external (user) configuration from the given path.
    If the file doesn't exist, it is created from the sample configuration.
    """
    if not os.path.exists(config_path):
        try:
            with pkg_resources.open_text('CodeToClassDiagram.configs', 'config.json') as src:
                default_config_data = src.read()
            with open(config_path, 'w', encoding='utf-8') as dest:
                dest.write(default_config_data)
            print(f"{config_path} created from the default configuration.")
        except Exception as e:
            print(f"Error creating config file: {e}")
            sys.exit(1)
    
    # Default user config values.
    default_config = {
        "exclude_files": [],
        "input_filetype": "Csharp",
        "output": {
            "mode": "console",
            "file": "diagram.md",
            "diagram": "MermaidClassDiagram",
            "hide_implemented_interface_methods": True,
            "hide_implemented_interface_properties": True,
            "exclude_namespaces": [],
            "show_dependencies": False
        }
    }
    try:
        with open(config_path, "r", encoding="utf-8") as cf:
            user_config = json.load(cf)
            default_config.update(user_config)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)
    return default_config

def load_internal_config():
    """
    Load the internal configuration embedded in the package.
    """
    try:
        with pkg_resources.open_text('CodeToClassDiagram.configs', 'internal_config.json') as f:
            internal_config = json.load(f)
    except Exception as e:
        print(f"Error loading internal configuration: {e}")
        sys.exit(1)
    return internal_config

def init_config_file(config_path):
    """
    Copy the default config file from the package to config_path.
    """
    try:
        with pkg_resources.open_text('CodeToClassDiagram.configs', 'config.json') as src:
            default_config_data = src.read()
        with open(config_path, 'w', encoding='utf-8') as dest:
            dest.write(default_config_data)
        print(f"Default configuration file created at {config_path}.")
    except Exception as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)
