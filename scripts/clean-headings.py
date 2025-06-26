import argparse
import os

# import re


def demote_headings_in_file(input_path, output_path):
    """
    Reads a Markdown file, demotes every heading by one level,
    and writes the result to a new file.

    For example, '## Heading 2' becomes '# Heading 1', and
    '# Heading 1' becomes 'Heading 1' (plain text).
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        processed_lines = []
        for line in lines:
            # A valid ATX heading starts with 1-6 '#' characters, followed by a space.
            # We will check for any line starting with at least one '#'.
            stripped_line = line.lstrip()
            if stripped_line.startswith("#"):
                # This is a heading. Remove the first '#' character to demote it.
                # We find the first '#' and slice the string from the character after it.
                # This correctly handles '## title' -> '# title'.
                # We preserve the original leading whitespace, if any.
                first_hash_index = line.find("#")
                new_line = line[:first_hash_index] + line[first_hash_index + 1 :]
                processed_lines.append(new_line)
            else:
                # This is not a heading, so keep it as is.
                processed_lines.append(line)

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(processed_lines)

        print(f"✅ Success! Processed file saved to: {output_path}")

    except FileNotFoundError:
        print(f"❌ Error: The file at '{input_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- How to use this script ---
    # 1. Save this script as a Python file (e.g., adjust_headings.py).
    # 2. Run it from your terminal, providing the path to your markdown file.
    #
    #    Example:
    #    python adjust_headings.py my_document.md
    #
    #    This creates a new file named 'my_document_adjusted.md'.
    #
    #    To specify a different output file:
    #    python adjust_headings.py my_document.md -o path/for/new_file.md

    parser = argparse.ArgumentParser(
        description="A script to demote all headings in a Markdown file by one level.",
        epilog="Example: python adjust_headings.py my_notes.md -o my_notes_fixed.md",
    )
    parser.add_argument("input_file", help="The path to the input Markdown file.")
    parser.add_argument(
        "-o", "--output_file", help="The path for the output file. (Optional)"
    )

    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file

    if not output_path:
        # If no output path is provided, create one automatically.
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_adjusted{ext}"

    print(f"📖 Reading from: {input_path}")
    demote_headings_in_file(input_path, output_path)
