# combined-md.py

import os
import glob

# --- CONFIGURATION ---
# IMPORTANT: Update this path to the folder where your Markdown notes are stored.
NOTES_FOLDER_PATH = "/Users/viz1er/Codebase/obsidian-vault/05 Projects/Silsila Sacra - Publishing Services/Manuscripts for Publication/Arabic to English Translated Texts/40 Hadith of Imam An-Nawawi"

# The name for the final combined Markdown file.
COMBINED_FILENAME = "combined-output.md"
# --- END CONFIGURATION ---


def combine_markdown_files():
    """
    Finds all Markdown files in the specified folder, combines them into a
    single Markdown file, and uses each source filename as a Level 1 heading.
    It automatically strips YAML frontmatter from each file.
    """
    # Construct the full path for the output file
    combined_md_filepath = os.path.join(NOTES_FOLDER_PATH, COMBINED_FILENAME)

    # Find all Markdown files in the directory
    all_md_files = sorted(glob.glob(os.path.join(NOTES_FOLDER_PATH, "*.md")))

    # Filter out the output file itself to avoid it being included in subsequent runs
    files_to_combine = [
        f for f in all_md_files if os.path.basename(f) != COMBINED_FILENAME
    ]

    if not files_to_combine:
        print("❌ No Markdown files found to combine in the specified directory.")
        return

    print(f"Found {len(files_to_combine)} lesson files to combine.")

    try:
        # Open the output file in write mode
        with open(combined_md_filepath, "w", encoding="utf-8") as outfile:
            # Loop through each file to be combined
            for filepath in files_to_combine:
                # Get the filename without the extension to use as the title
                filename = os.path.basename(filepath)
                title = os.path.splitext(filename)[0]

                print(f"  -> Adding: {filename}")

                # Write the title as a Level 1 Markdown heading
                outfile.write(f"# {title}\n\n")

                # Open the lesson file and read its content
                with open(filepath, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    main_content = content

                    # Check for and strip YAML frontmatter
                    if content.startswith("---"):
                        # Split content by '---' at most twice
                        parts = content.split("---", 2)
                        # A valid YAML block will result in 3 parts
                        if len(parts) >= 3:
                            # The actual content is the last part.
                            # .lstrip() removes leading blank lines.
                            main_content = parts[2].lstrip()

                    # Write the processed content to the output file
                    outfile.write(main_content)

                # Add two newlines for separation between files
                outfile.write("\n\n")

        print(f"\n✅ Successfully combined all notes into: {combined_md_filepath}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


# This allows the script to be run from the command line
if __name__ == "__main__":
    combine_markdown_files()
