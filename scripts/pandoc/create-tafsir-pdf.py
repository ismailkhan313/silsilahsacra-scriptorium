#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil
import argparse
import glob


def check_for_latex():
    """Checks if a LaTeX distribution (like MacTeX) is installed."""
    if shutil.which("lualatex") is None:
        print("🔴 ERROR: lualatex not found.")
        print("Please ensure you have a full LaTeX distribution like MacTeX installed.")
        print("See: https://www.tug.org/mactex/")
        return False
    return True


def check_for_pandoc():
    """Checks if Pandoc is installed."""
    if shutil.which("pandoc") is None:
        print("🔴 ERROR: 'pandoc' command not found.")
        print("Please ensure Pandoc is installed. On macOS, use: brew install pandoc")
        return False
    return True


def create_pdf(directory_path):
    """
    Finds all Markdown files in a given directory, sorts them, and merges
    them into a single PDF with a book-like layout using Pandoc and LuaLaTeX.
    """
    if not (check_for_pandoc() and check_for_latex()):
        return

    # --- Book Layout Configuration ---
    # MODIFIED: These settings are now tailored for a book feel.
    output_directory = "/Users/viz1er/Codebase/silsilahsacra-scriptorium/published"
    font_size = "26pt"  # Increased from default 10pt for better readability.
    main_font = "Amiri"  # A good font with Unicode/Arabic support.

    # Tighter horizontal margins, with standard top/bottom space.
    # You can adjust these values as needed. e.g., hmargin=1.7cm
    geometry_settings = "hmargin=4.5cm, top=2.5cm, bottom=2.5cm"

    # Increases the space between lines by 10% for readability. Requires the 'setspace' package.
    line_spacing = "1.15"

    # --- Sanitize and Validate Input Path ---
    input_path = os.path.abspath(os.path.expanduser(directory_path))

    if not os.path.isdir(input_path):
        print(
            f"🔴 ERROR: The provided input path is not a valid directory: {input_path}"
        )
        return

    # --- Find and Sort Markdown Files ---
    print(f"🔎 Scanning for Markdown files in: {input_path}")
    input_files = sorted(glob.glob(os.path.join(input_path, "*.md")))

    if not input_files:
        print("🔴 ERROR: No Markdown (.md) files were found in this directory.")
        return

    print(f"Found {len(input_files)} files to combine:")
    for f in input_files:
        print(f"  - {os.path.basename(f)}")

    # --- Prepare Output Path ---
    try:
        os.makedirs(output_directory, exist_ok=True)
    except OSError as e:
        print(f"🔴 ERROR: Could not create output directory '{output_directory}'.")
        print(f"Reason: {e}")
        return

    folder_name = os.path.basename(input_path)
    file_name = f"{folder_name}.pdf"
    output_pdf_path = os.path.join(output_directory, file_name)

    doc_title = folder_name.replace("_", " ").replace("-", " ").title()

    # --- LaTeX Header & Footer Configuration ---
    # MODIFIED: Added 'setspace' package and \setstretch command for line spacing.
    latex_header_includes = (
        r"\usepackage{fancyhdr}"
        r"\usepackage{setspace}"  # ADDED: Package for line spacing
        r"\setstretch{" + line_spacing + r"}"  # ADDED: Apply the line spacing
        r"\pagestyle{fancy}"
        r"\fancyhead[C]{" + doc_title + r"}"
        r"\fancyfoot[C]{\thepage}"
    )

    # --- Build the Pandoc Command ---
    pandoc_command = [
        "pandoc",
        "--standalone",
    ]

    pandoc_command.extend(input_files)

    pandoc_command.extend(
        [
            "--output",
            output_pdf_path,
            "--variable",
            f"title:{doc_title}",
            "--variable",
            f"fontsize:{font_size}",  # ADDED: Pass the font size
            "--variable",
            f"geometry:{geometry_settings}",  # MODIFIED: Use new margin settings
            "--variable",
            f"header-includes:{latex_header_includes}",
            "--pdf-engine=lualatex",
            "--variable",
            f"mainfont:{main_font}",
        ]
    )

    # --- Execute the Command ---
    print(f"\n📑 Output will be saved to: {output_pdf_path}")
    print("🚀 Starting PDF generation with Pandoc (using LuaLaTeX)...")
    print("   This may take a moment.")

    try:
        process = subprocess.run(
            pandoc_command, check=True, capture_output=True, text=True
        )
        print(f"✅ Success! Your PDF has been created:\n   {output_pdf_path}")
        if process.stdout:
            print("\n--- Pandoc Output ---")
            print(process.stdout)
    except subprocess.CalledProcessError as e:
        print("🔴 ERROR: Pandoc failed during PDF creation.")
        print("This is often due to a LaTeX error or a missing font.")
        print("\n--- Pandoc Error Log ---")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine all Markdown files in a directory into a single, book-style PDF using Pandoc and LuaLaTeX.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the folder containing your .md files.\n"
        "Example: python3 %(prog)s ~/Documents/Yasin_Tafsir",
    )

    args = parser.parse_args()
    create_pdf(args.directory_path)
