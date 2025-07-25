#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts a source file, like Markdown or HTML, to a pre-defined styled PDF.

This script uses Pandoc with the WeasyPrint engine to create a high-quality
PDF. It can optionally apply a Pandoc filter (e.g., for auto-tagging
Arabic text) and a CSS stylesheet.

How to run this script: python3 scripts/html-to-pdf.py '<source html location>' --filter scripts/pandoc/autotag-arabic.py -c styles/study-notes.css
"""

import argparse
import os
import subprocess
import sys


def convert_to_pdf(input_file, output_file=None, css_file=None, filter_script=None):
    """
    Constructs and executes the Pandoc command to convert a file to PDF.
    """
    # --- 1. Validate Input and Filter Files ---
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found at '{input_file}'")
        sys.exit(1)

    # --- 2. Determine Output Filename ---
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.pdf"

    # --- 3. Build the Pandoc Command ---
    command = [
        "pandoc",
        input_file,
        "--pdf-engine=weasyprint",
        "--toc",
        "-o",
        output_file,
    ]

    # --- 4. Add Filter if Provided (NEW) ---
    if filter_script:
        if os.path.exists(filter_script):
            command.extend(["--filter", filter_script])
        else:
            print(
                f"⚠️ Warning: Filter not found at '{filter_script}'. Proceeding without it."
            )

    # --- 5. Add CSS Stylesheet if Provided ---
    if css_file:
        if os.path.exists(css_file):
            command.extend(["--css", css_file])
        else:
            print(
                f"⚠️ Warning: CSS file not found at '{css_file}'. Proceeding without it."
            )

    # --- 6. Execute the Command ---
    print(f"🔄 Generating PDF from '{input_file}'...")
    print(f"   Running command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8"
        )
        print(f"\n✅ Success! PDF created at: {output_file}")
        if result.stderr:
            print(f"\nℹ️ Conversion Log:\n{result.stderr}")

    except FileNotFoundError:
        print("\n❌ Error: 'pandoc' command not found.")
        print("   Please ensure Pandoc is installed and in your system's PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: Pandoc failed with exit code {e.returncode}.")
        print("\nPandoc Error Output:\n" + e.stderr)
        sys.exit(1)


def main():
    """
    Parses command-line arguments and initiates the conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert a source file (e.g., Markdown) to PDF using Pandoc.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Basic conversion (from Markdown)
  python %(prog)s my-document.md

  # Apply custom CSS and specify output
  python %(prog)s my-document.md --css style.css --output styled.pdf
  
  # Apply the Arabic filter and CSS
  python %(prog)s arabic-doc.md --filter ./autotag-arabic.py --css style.css
""",
    )
    parser.add_argument(
        "input_file", help="The input file to convert (e.g., a .md file)."
    )
    parser.add_argument(
        "-o", "--output", dest="output_file", help="The name of the output PDF file."
    )
    parser.add_argument(
        "-c", "--css", dest="css_file", help="Path to the optional CSS stylesheet."
    )
    # --- New Argument for the Filter ---
    parser.add_argument(
        "-f",
        "--filter",
        dest="filter_script",
        help="Path to an optional Pandoc filter script.",
    )

    args = parser.parse_args()
    convert_to_pdf(args.input_file, args.output_file, args.css_file, args.filter_script)


if __name__ == "__main__":
    main()
