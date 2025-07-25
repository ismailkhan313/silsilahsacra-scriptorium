import os
import glob
import subprocess

# --- CONFIGURATION ---
# The folder where your Markdown notes are stored.
NOTES_FOLDER_PATH = "/Users/viz1er/Codebase/obsidian-vault/02 Literature Notes/WISE English Academy/Journey of Fiqh"

# The temporary name for the combined Markdown file.
# This file will be created inside the NOTES_FOLDER_PATH and then deleted.
COMBINED_FILENAME = "combined.md"

# The name for the final PDF output file.
PDF_FILENAME = "final_notes.pdf"
# --- END CONFIGURATION ---


def combine_and_convert():
    """
    Finds all .md files, combines them using each filename as a Level 1 Heading,
    and then uses Pandoc to convert the result to a PDF file.

    Requires Pandoc and a LaTeX distribution (like MiKTeX, MacTeX, or TeX Live)
    to be installed and available in the system's PATH.
    """
    # --- Step 1: Combine Markdown Files ---

    combined_md_filepath = os.path.join(NOTES_FOLDER_PATH, COMBINED_FILENAME)
    all_md_files = glob.glob(os.path.join(NOTES_FOLDER_PATH, "*.md"))
    source_md_files = sorted(
        [
            f
            for f in all_md_files
            if os.path.basename(f) not in [COMBINED_FILENAME, PDF_FILENAME]
        ]
    )

    if not source_md_files:
        print(
            f"Warning: No source Markdown files found in the '{NOTES_FOLDER_PATH}' folder."
        )
        return

    print(
        f"Found {len(source_md_files)} files. Combining them into '{combined_md_filepath}'..."
    )

    with open(combined_md_filepath, "w", encoding="utf-8") as outfile:
        # YAML frontmatter. Using 'titlesec' for explicit control over heading spaces.
        outfile.write("---\n")
        outfile.write("title: 'Journey of Fiqh'\n")
        outfile.write("author: 'WISE English Academy'\n")
        outfile.write(f"date: '{'July 24, 2025'}'\n")
        outfile.write("mainfont: 'Times New Roman'\n")
        outfile.write("geometry: 'margin=1in'\n")
        outfile.write("fontsize: 12pt\n")
        outfile.write("header-includes:\n")
        # Load titlesec and explicitly set spacing for \section (which is '#')
        outfile.write("  - \\usepackage{titlesec}\n")
        outfile.write(
            "  - \\titlespacing*{\\section}{0pt}{3.5ex plus 1ex minus .2ex}{2.3ex plus .2ex}\n"
        )
        outfile.write("---\n\n")

        for filepath in source_md_files:
            filename = os.path.basename(filepath)
            title = os.path.splitext(filename)[0]
            outfile.write(f"# {title}\n\n")
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
            outfile.write("\n\n\\newpage\n\n")

    print("✅ Successfully combined all notes.")

    # --- Step 2: Convert to PDF using Pandoc ---
    pdf_filepath = os.path.join(NOTES_FOLDER_PATH, PDF_FILENAME)
    print(f"\nConverting '{COMBINED_FILENAME}' to '{PDF_FILENAME}' using Pandoc...")

    try:
        subprocess.run(
            [
                "pandoc",
                combined_md_filepath,
                "-o",
                pdf_filepath,
                "--pdf-engine=lualatex",
            ],
            check=True,
        )
        print(f"✅ Successfully created PDF file at: {pdf_filepath}")

    except FileNotFoundError:
        print("\n--- ERROR ---")
        print(
            "Pandoc command not found. Ensure Pandoc and LaTeX are installed and in your PATH."
        )
        print("-----------------")
        return

    except subprocess.CalledProcessError as e:
        print("\n--- ERROR ---")
        print(f"Pandoc failed to convert the file. Error: {e}")
        print("Check the pandoc output for LaTeX errors.")
        print("-----------------")
        return

    # --- Step 3: Clean up the temporary file ---
    finally:
        if os.path.exists(combined_md_filepath):
            os.remove(combined_md_filepath)
            print(f"\nCleaned up temporary file: {combined_md_filepath}")


if __name__ == "__main__":
    combine_and_convert()
