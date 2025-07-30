# A Python script to convert Markdown to custom XML using Pandoc and a Lua filter.

import subprocess
import argparse
import sys
import os


def convert_markdown_to_xml(input_file, output_file):
    """
    Converts a Markdown file to a custom XML file using Pandoc.

    Args:
        input_file (str): The path to the input Markdown file.
        output_file (str): The path for the output XML file.
    """
    # The name of the Lua filter file.
    # It's assumed to be in the same directory as this script.
    filter_file = "custom-xml-tags.lua"
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filter_path = os.path.join(script_dir, filter_file)

    # Check if the Lua filter exists.
    if not os.path.exists(filter_path):
        print(f"Error: Lua filter '{filter_file}' not found in the script directory.")
        sys.exit(1)

    # Construct the Pandoc command.
    # -t xml: sets the output format to XML.
    # --lua-filter: specifies the custom Lua script to use.
    # -o: specifies the output file.
    command = [
        "pandoc",
        input_file,
        "-t",
        "xml",
        "--lua-filter",
        filter_path,
        "-o",
        output_file,
    ]

    print(f"Executing command: {' '.join(command)}")

    try:
        # Execute the Pandoc command.
        process = subprocess.run(
            command,
            check=True,  # Raises CalledProcessError if the command returns a non-zero exit code.
            capture_output=True,  # Captures stdout and stderr.
            text=True,  # Decodes stdout and stderr as text.
        )
        print(f"Successfully converted '{input_file}' to '{output_file}'.")
        if process.stdout:
            print("Pandoc output:\n", process.stdout)

    except FileNotFoundError:
        print("Error: 'pandoc' command not found.")
        print("Please ensure Pandoc is installed and in your system's PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during Pandoc conversion for '{input_file}'.")
        print(f"Return code: {e.returncode}")
        print("Pandoc stderr:\n", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Set up command-line argument parsing.
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to custom XML using Pandoc."
    )
    parser.add_argument("input_file", help="The input Markdown file to convert.")
    parser.add_argument("output_file", help="The name of the output XML file.")

    # Parse the arguments provided by the user.
    args = parser.parse_args()

    # Call the conversion function with the provided file paths.
    convert_markdown_to_xml(args.input_file, args.output_file)
