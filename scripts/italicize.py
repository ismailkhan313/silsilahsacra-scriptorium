import re
import argparse
import os


def is_date(text):
    """
    Checks if a given string is a date in the format 'd.YYYY/YYYY' or 'b.YYYY/YYYY'.
    This is designed to avoid italicizing specific historical date notations.
    The check is case-insensitive and handles surrounding whitespace.
    """
    # This regex looks for 'd. ' or 'b. ' followed by 'YYYY/YYYY'.
    date_pattern = r"^(?:b|d)\.\s*\d{4}\/\d{4}$"
    if re.match(date_pattern, text.strip(), re.IGNORECASE):
        return True
    return False


def italicize_text_in_parentheses(match):
    """
    A callback function for re.sub that processes text found inside parentheses.

    It italicizes the content unless it meets any of the following conditions:
    1. It is a specific date format (e.g., d. 1206/1791).
    2. It already contains asterisks (*) or underscores (_), suggesting existing formatting.
    3. It is empty or contains only whitespace.
    """
    # group(1) captures the content *inside* the parentheses.
    original_content = match.group(1)

    # First, check for the specific date format to exclude it from formatting.
    if is_date(original_content):
        return match.group(0)  # Return original: (d. 1206/1791)

    # Next, check if the content contains any asterisks or underscores. This is a
    # smart heuristic to avoid altering existing manual formatting like *italics*,
    # _italics_, **bold**, or partially formatted text (see *figure 1*).
    if "*" in original_content or "_" in original_content:
        return match.group(0)

    # Strip whitespace from the content to handle cases like `(  text  )`.
    stripped_content = original_content.strip()

    # If the stripped content is not empty, wrap it in asterisks for italics.
    if stripped_content:
        return f"(*{stripped_content}*)"
    else:
        # If parentheses are empty `()` or just contain whitespace `(   )`,
        # return them unchanged.
        return match.group(0)


def process_markdown_file(input_path, output_path):
    """
    Reads a markdown file, processes its content to italicize text in
    parentheses based on the defined rules, and writes to a new file.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # This regex finds text enclosed in parentheses. The `(.*?)` is non-greedy
        # to correctly handle multiple sets of parentheses on the same line.
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
    # 1. Save this script as a Python file (e.g., italicize_md.py).
    # 2. Run it from your terminal, providing the path to your markdown file.
    #
    #    Example:
    #    python italicize_md.py my_document.md
    #
    #    This creates a new file named 'my_document_formatted.md'.
    #
    #    To specify a different output file:
    #    python italicize_md.py my_document.md -o path/for/new_file.md

    parser = argparse.ArgumentParser(
        description="A script to find text in parentheses in a Markdown file and italicize it, ignoring dates and already-formatted text.",
        epilog="Example: python italicize_md.py ../my_document.md",
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
        output_path = f"{base}_formatted{ext}"

    print(f"📖 Reading from: {input_path}")
    process_markdown_file(input_path, output_path)
