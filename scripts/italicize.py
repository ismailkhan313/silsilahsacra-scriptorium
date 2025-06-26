import re
import argparse
import os


def is_date(text):
    """
    Checks if a given string is a date in the format 'd. YYYY/YYYY' or 'b. YYYY/YYYY'.
    This is designed to avoid italicizing specific historical date notations.
    """
    # This single regex pattern looks for 'd. ' or 'b. ' followed by 'YYYY/YYYY'.
    # e.g., (d. 1206/1791) or (b. 1180/1766)
    date_pattern = r"^(?:b|d)\.\s*\d{4}\/\d{4}$"

    if re.match(date_pattern, text.strip(), re.IGNORECASE):
        return True
    return False


def italicize_text_in_parentheses(match):
    """
    This is a callback function for re.sub.
    It receives a match object for text found inside parentheses.
    It checks if the text is a date. If not, it italicizes it.
    """
    # The first group of the match (.*?) captures the content *inside* the parentheses.
    content = match.group(1)

    # If the content is already italicized or is a date, don't change it.
    if content.startswith("*") and content.endswith("*"):
        return match.group(0)  # Return the full original match, e.g., (*text*)

    if is_date(content):
        return match.group(0)  # Return the original text, e.g., (d. 1206/1791)

    # If it's not a date, wrap the content in asterisks for italics.
    return f"(*{content}*)"


def process_markdown_file(input_path, output_path):
    """
    Reads a markdown file, processes its content, and writes to a new file.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # This regex finds text enclosed in parentheses.
        # It's non-greedy (.*?) to handle multiple sets of parentheses on one line correctly.
        # It looks for a closing parenthesis `\)` after an opening one `\(`.
        processed_content = re.sub(r"\((.*?)\)", italicize_text_in_parentheses, content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(processed_content)

        print(f"✅ Success! Processed file saved to: {output_path}")

    except FileNotFoundError:
        print(f"❌ Error: The file at '{input_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- How to use this script ---
    # 1. Save this script as a Python file (e.g., italicize-md.py), for instance in a 'scripts' folder.
    # 2. To run it, open your terminal and provide the path to your markdown file.
    #
    #    Example from the root folder:
    #    python scripts/italicize-md.py my_document.md
    #
    #    This will create a new file named 'my_document_formatted.md' in the same directory.
    #
    #    To specify an output file name/path:
    #    python scripts/italicize-md.py my_document.md -o path/for/new_file.md

    parser = argparse.ArgumentParser(
        description="A script to find text in parentheses in a Markdown file and italicize it, ignoring dates.",
        epilog="Example: python scripts/italicize-md.py ../my_document.md",
    )
    parser.add_argument("input_file", help="The path to the input Markdown file.")
    parser.add_argument(
        "-o", "--output_file", help="The path for the output file. (Optional)"
    )

    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file

    if not output_path:
        # If no output path is provided, create one automatically based on the input file's name.
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_formatted{ext}"

    print(f"📖 Reading from: {input_path}")
    process_markdown_file(input_path, output_path)
