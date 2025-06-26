#!/usr/bin/env python3
# flake8: noqa

import os
import subprocess
import sys
import argparse

# --- Configuration ---
# Set the base paths for your project structure.
# This script is now configured for a flat template directory.
TEMPLATES_DIR = "/Users/viz1er/Codebase/silsilah-sacra-scriptorium/templates"
FILTER_PATH = "/Users/viz1er/Codebase/silsilah-sacra-scriptorium/scripts/autotag-arabic.py"
OUTPUT_DIR = "/Users/viz1er/Codebase/silsilah-sacra-scriptorium/published"

def check_dependencies(pdf_engine):
    """Check if pandoc and the specified PDF engine are in the system's PATH."""
    dependencies = ['pandoc', pdf_engine]
    for dep in dependencies:
        if subprocess.run(['which', dep], capture_output=True, text=True).returncode != 0:
            print(f"Error: '{dep}' not found in your system's PATH.")
            print("Please ensure Pandoc and your chosen LaTeX engine are installed and accessible.")
            sys.exit(1)

def main():
    """
    Main function to construct and run the pandoc command using command-line arguments.
    """
    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A Pandoc wrapper to convert Markdown files to PDF using LaTeX templates.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'input_file',
        help="Path to the input Markdown file."
    )
    parser.add_argument(
        '-t', '--template',
        default='old-article.tex',  # Default template is now a specific file
        help="Name of the template file in the templates directory (e.g., 'article.tex').\nDefault: 'old-article.tex'."
    )
    parser.add_argument(
        '-e', '--engine',
        default='lualatex',
        choices=['lualatex', 'xelatex'],
        help="The PDF engine to use.\nDefault: 'lualatex'."
    )
    args = parser.parse_args()

    print("--- Pandoc PDF Generator ---")

    # 2. Check for required command-line tools
    check_dependencies(args.engine)

    # 3. Construct paths from arguments and configuration
    md_file_path = args.input_file
    # UPDATED: The path is now constructed by joining the base dir and the template filename directly.
    template_path = os.path.join(TEMPLATES_DIR, args.template)

    # 4. Ensure all required paths exist
    if not os.path.isfile(md_file_path):
        print(f"Error: Input file not found at '{md_file_path}'")
        sys.exit(1)
    if not os.path.isfile(template_path):
        print(f"Error: Template file not found at '{template_path}'")
        print(f"(Searched for template file named '{args.template}')")
        sys.exit(1)
    if not os.path.isfile(FILTER_PATH):
        print(f"Error: Filter script not found at '{FILTER_PATH}'")
        sys.exit(1)
    if not os.path.isdir(OUTPUT_DIR):
        print(f"Creating output directory: '{OUTPUT_DIR}'")
        os.makedirs(OUTPUT_DIR)

    # 5. Construct the output PDF path
    base_name = os.path.basename(md_file_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{file_name_without_ext}.pdf")

    # 6. Build the Pandoc command dynamically
    pandoc_command = [
        'pandoc',
        md_file_path,
        '-o', output_pdf_path,
        f'--template={template_path}',
        f'--pdf-engine={args.engine}',
        f'--filter={FILTER_PATH}'
    ]

    print("\nRunning command:")
    print(' '.join(pandoc_command))
    print("...")

    # 7. Execute the command
    try:
        process = subprocess.run(
            pandoc_command,
            check=True,
            capture_output=True,
            text=True
        )
        print("\n✅ Success!")
        print(f"PDF created at: {output_pdf_path}")
        if process.stdout:
            print("\nPandoc Output:")
            print(process.stdout)

    except FileNotFoundError:
        print(f"\n❌ Error: The 'pandoc' command was not found.")
        print("Please ensure Pandoc is installed and in your system's PATH.")
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print("\n❌ Error: Pandoc failed to execute.")
        print(f"Return Code: {e.returncode}")
        print("\n--- Pandoc Stderr ---")
        print(e.stderr)
        print("\n--- Pandoc Stdout ---")
        print(e.stdout)
        sys.exit(1)

if __name__ == '__main__':
    main()