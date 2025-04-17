import importlib
import sys
import yaml
import json
from jinja2 import Environment, FileSystemLoader
import os
import markdown
from pathlib import Path


def show_structure(data, indent=0):
    """
    Recursively prints the structure of a dictionary.

    Args:
        data (dict): The dictionary to show the structure of.
        indent (int): The current indentation level (used for nested structures).
    """
    for key, value in data.items():
        print(" " * indent + f"{key}: {type(value).__name__}")
        if isinstance(value, dict):
            show_structure(value, indent + 2)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            print(" " * (indent + 2) + "[" + str(len(value)) + "]")
            show_structure(value[0], indent + 4)


def load_yaml_files_recursively(directory):
    all_data = {
        "elements": [],
        "children": {},
        "directory": directory,
        "dirname": os.path.basename(directory),
    }

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        exit(1)

    for filename in sorted(os.listdir(directory)):
        # For all yaml files
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            print("Entering directory: ", filepath)
            all_data["children"][filename] = load_yaml_files_recursively(filepath)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            print("Reading file:", filepath)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file) or {}  # Handle empty files
                    data.setdefault("filename", filename)
                    data.setdefault("filepath", filepath)
                    data.setdefault("directory", directory)
                    data.setdefault("group", filepath.split("/")[::-1])
                    data.setdefault("key", Path(filename).stem)
                    # Add data
                    all_data["elements"].append(data)
            except yaml.YAMLError as e:
                print(f"Error parsing {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error with {filename}: {e}")
    # Return datasets
    return all_data


def load_yaml_files(directory):
    """Load and merge YAML files from the given directory."""
    all_data = []
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        exit(1)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(directory, filename)
            print("Reading file:", filepath)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file) or {}  # Handle empty files
                    data["filename"] = filename
                    all_data.append(data)
            except yaml.YAMLError as e:
                print(f"Error parsing {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error with {filename}: {e}")

    return all_data


# Define the custom filter
def markdown_to_html(text):
    if text is None:
        return ""
    return markdown.markdown(text)


def to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


def render_template(template_path, merged_data):
    """Render the Jinja2 template with the provided data."""
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters["markdown"] = markdown_to_html
    env.filters["json"] = to_json
    template = env.get_template(template_file)
    return template.render(merged_data)


def convert(
    input_dir,
    template_path,
    output=None,
    output_filename_template=None,
    list_structure=False,
    processor=None,
    processor_path=None,
    recursive=False,
):
    # Load from each data file and merge data
    if recursive:
        merged_data = load_yaml_files_recursively(input_dir)
    else:
        merged_data = load_yaml_files(input_dir)

    # Check if processor is specified
    if processor and processor_path:
        print("Loading processor module", processor)
        sys.path.append(os.path.abspath(processor_path))
        processor_module = importlib.import_module(processor)
        if hasattr(processor_module, "process"):
            print("Processing data")
            merged_data = processor_module.process(merged_data)
        else:
            print("The specified module does not have a 'filter_function'.")
    # Print structure
    if list_structure:
        show_structure(merged_data)
    # Initialize return data
    return_data = []
    # Check if multiple output files
    if output_filename_template:
        # Generate multiple output files based on the template
        for data in merged_data:
            # Generate filename
            filename = output_filename_template.format(**data)
            # Render data
            content = render_template(template_path, data)
            # Create putput structure
            return_data.append({"filename": filename, "content": content})
    else:
        # Render the Jinja2 template with the merged data
        content = render_template(template_path, {"data": merged_data})
        # Generate return data
        return_data.append({"filename": output, "content": content})
    # Return rendered data
    return return_data
