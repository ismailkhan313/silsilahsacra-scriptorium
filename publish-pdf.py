#!/usr/bin/env python3
# flake8: noqa

import os
import subprocess
import sys

# --- Configuration ---
# Set the absolute paths for your markdown file, template, filter, and output directory.

# IMPORTANT: Set the path to your input Markdown file here.
MD_FILE_PATH = "/Users/viz1er/Codebase/obsidian-vault/Tafsīr al-Jīlānī -- Surah Yasin.md"

TEMPLATE_PATH = "/Users/viz1er/Codebase/SilsilahScriptoria/en-ar-template.tex"
FILTER_PATH = "/Users/viz1er/Codebase/SilsilahScriptoria/autotag-arabic.py"
OUTPUT_DIR = "/Users/viz1er/Codebase/SilsilahScriptoria/output"
PDF_ENGINE = "xelatex"

def check_dependencies():
    """Check if pandoc and the specified PDF engine are in the system's PATH."""
    dependencies = ['pandoc', PDF_ENGINE]
    for dep in dependencies:
        if subprocess.run(['which', dep], capture_output=True, text=True).returncode != 0:
            print(f"Error: '{dep}' not found in your system's PATH.")
            print("Please ensure Pandoc and XeLaTeX are installed and accessible.")
            sys.exit(1)

def main():
    """
    Main function to construct and run the pandoc command using hardcoded paths.
    """
    print("--- Pandoc PDF Generator ---")

    # 1. Check for required command-line tools
    check_dependencies()

    # 2. Ensure all required paths exist
    if not os.path.isfile(TEMPLATE_PATH):
        print(f"Error: Template file not found at '{TEMPLATE_PATH}'")
        sys.exit(1)
    if not os.path.isfile(FILTER_PATH):
        print(f"Error: Filter script not found at '{FILTER_PATH}'")
        sys.exit(1)
    if not os.path.isdir(OUTPUT_DIR):
        print(f"Creating output directory: '{OUTPUT_DIR}'")
        os.makedirs(OUTPUT_DIR)

    # 3. Validate the hardcoded input file path
    if not MD_FILE_PATH or not os.path.isfile(MD_FILE_PATH):
        print(f"Error: The file '{MD_FILE_PATH}' does not exist.")
        print("Please check the 'MD_FILE_PATH' variable in the script.")
        sys.exit(1)

    if not MD_FILE_PATH.lower().endswith('.md'):
        print(f"Warning: The file specified in MD_FILE_PATH does not have a '.md' extension: {MD_FILE_PATH}")

    # 4. Construct the output PDF path
    base_name = os.path.basename(MD_FILE_PATH)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{file_name_without_ext}.pdf")

    # 5. Build the Pandoc command
    pandoc_command = [
        'pandoc',
        MD_FILE_PATH,
        '-o', output_pdf_path,
        f'--template={TEMPLATE_PATH}',
        f'--pdf-engine={PDF_ENGINE}',
        f'--filter={FILTER_PATH}'
    ]

    print("\nRunning command:")
    print(' '.join(pandoc_command))
    print("...")

    # 6. Execute the command
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