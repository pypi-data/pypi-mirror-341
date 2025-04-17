from .convert import convert
import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a document (html, markdown, text, ...) from YAML files using a Jinja2 templates."
    )
    parser.add_argument(
        "input_dir",
        help="Path to the directory containing YAML files. If the directory is nested, use recursive arg (-r, --recursive).",
    )
    parser.add_argument("template_path", help="Path to the Jinja2 template file.")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
        help="Loads the files recursively from the folder and subfolders.",
    )
    parser.add_argument(
        "-p",
        "--processor",
        required=False,
        help="A python module with process function to manipulate the loaded data before rendering.",
    )
    parser.add_argument(
        "--processor-path",
        required=False,
        help="The path of the processor module if not in the working dir.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default="output.html",
        help="Path to save the rendered document file.",
    )
    parser.add_argument(
        "-f",
        "--output_filename_template",
        required=False,
        default=None,
        help="Define a file template to generate multiple output files, one for each input file.",
    )
    parser.add_argument(
        "-l",
        "--list_structure",
        action="store_true",
        default=False,
        help="Lists the data structure (for analysis).",
    )
    return parser.parse_args()


def main():
    print("Running main function")
    # Get arguments
    args = parse_arguments()
    # Read data and convert
    result = convert(
        input_dir=args.input_dir,
        template_path=args.template_path,
        output=args.output,
        output_filename_template=args.output_filename_template,
        list_structure=args.list_structure,
        processor=args.processor,
        processor_path=args.processor_path,
        recursive=args.recursive,
    )

    # Generate output files
    for item in result:
        # Get filename and content
        filename = item["filename"]
        content = item["content"]
        # Write files
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        # Log
        print(f"Output file '{filename}' has been generated successfully.")


if __name__ == "__main__":
    main()
