import os
import glob
import subprocess
import yaml  # You must run 'pip install PyYAML' for this to work
from datetime import date, datetime  # To get and format dates

# --- CONFIGURATION ---
# The folder where your Markdown notes are stored.
NOTES_FOLDER_PATH = "/Users/viz1er/Codebase/obsidian-vault/02 Literature Notes/WISE English Academy/Journey of Fiqh"

# The temporary name for the combined Markdown file.
COMBINED_FILENAME = "combined.md"

# The name for the final PDF output file.
PDF_FILENAME = "combined.pdf"
# --- END CONFIGURATION ---


def combine_and_convert():
    """
    Finds a '00' overview file, uses its metadata to build a rich title page
    and table of contents with custom headers/footers, and combines all notes into a single PDF.
    Includes fallback logic for fonts.
    """
    # --- Step 1: Find and Parse the Overview Note ---
    all_md_files = sorted(glob.glob(os.path.join(NOTES_FOLDER_PATH, "*.md")))
    overview_filepath = next(
        (f for f in all_md_files if os.path.basename(f).startswith("00")), None
    )

    if not overview_filepath:
        print(
            "❌ ERROR: Could not find an overview file starting with '00' in the folder."
        )
        return

    lesson_files = [
        f
        for f in all_md_files
        if f != overview_filepath
        and os.path.basename(f) not in [COMBINED_FILENAME, PDF_FILENAME]
    ]

    print(f"Found overview file: {os.path.basename(overview_filepath)}")
    print(f"Found {len(lesson_files)} lesson files to combine.")

    try:
        with open(overview_filepath, "r", encoding="utf-8") as f:
            content = f.read()
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(
                "The overview file does not contain a valid YAML frontmatter block."
            )
        metadata = yaml.safe_load(parts[1])
        overview_content = parts[2]
    except Exception as e:
        print(f"❌ ERROR: Failed to parse or read the overview file. Details: {e}")
        return

    # --- Step 2: Combine Files with Dynamic Metadata ---
    combined_md_filepath = os.path.join(NOTES_FOLDER_PATH, COMBINED_FILENAME)

    with open(combined_md_filepath, "w", encoding="utf-8") as outfile:
        # FONT CONFIGURATION
        preferred_font = "Amiri"
        fallback_font = "Times New Roman"

        # Date formatting
        today_date = date.today().strftime("%B %d, %Y")
        created_date_str = str(metadata.get("created", ""))
        try:
            parsed_date = datetime.strptime(created_date_str, "%Y-%m-%d")
            formatted_created_date = parsed_date.strftime("%B %d, %Y")
        except ValueError:
            formatted_created_date = created_date_str

        # Metadata block setup
        author_block = (
            f"Instructor: {metadata.get('instructor', 'N/A')} \\\\ \n"
            f"Institute: {metadata.get('institute', 'N/A')}"
        )
        matn_italicized = f"\\textit{{{metadata.get('matn', 'N/A')}}}"
        subtitle_block = (
            f"Based on {matn_italicized} by {metadata.get('author', 'N/A')}"
        )
        date_block = (
            f"Created: {formatted_created_date} \\\\ \n" f"Updated: {today_date}"
        )

        header_footer_config = [
            r"\usepackage{parskip}",
            r"\usepackage{fancyhdr}",
            r"\usepackage{titlesec}",
            r"\titleformat{\section}{\normalfont\Large\bfseries\centering}{}{0em}{}",
            r"\pagestyle{fancy}",
            r"\fancyhf{}",
            r"\fancyhead[C]{\textit{\leftmark}}",
            r"\fancyfoot[C]{\thepage}",
            r"\renewcommand{\headrulewidth}{0pt}",
            r"\renewcommand{\footrulewidth}{0pt}",
            r"\renewcommand{\sectionmark}[1]{\markboth{#1}{}}",
        ]

        final_metadata = {
            "title": metadata.get("course_name", "Untitled Course"),
            "subtitle": subtitle_block,
            "author": author_block,
            "date": date_block,
            "toc": True,
            "toc-depth": 3,
            "mainfont": preferred_font,  # Set the preferred font
            "geometry": "margin=1in",
            "fontsize": "12pt",
            "header-includes": header_footer_config,
        }

        outfile.write("---\n")
        yaml.dump(
            final_metadata,
            outfile,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )
        outfile.write("---\n\n")

        print("✅ Successfully created metadata for the document.")

        outfile.write(overview_content)
        outfile.write("\n\n\\newpage\n\n")

        for filepath in lesson_files:
            filename = os.path.basename(filepath)
            title = os.path.splitext(filename)[0]
            outfile.write(f"# {title}\n\n")
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
            outfile.write("\n\n\\newpage\n\n")

    print("✅ Successfully combined all notes.")

    # --- Step 3: Convert to PDF with Fallback Logic ---
    pdf_filepath = os.path.join(NOTES_FOLDER_PATH, PDF_FILENAME)
    print(
        f"\nConverting '{COMBINED_FILENAME}' to '{PDF_FILENAME}' (Attempt 1: {preferred_font})..."
    )

    pandoc_command = [
        "pandoc",
        combined_md_filepath,
        "-o",
        pdf_filepath,
        "--pdf-engine=lualatex",
    ]

    try:
        # First attempt with the preferred font
        subprocess.run(pandoc_command, check=True, capture_output=True, text=True)
        print(
            f"✅ Successfully created PDF file with '{preferred_font}' at: {pdf_filepath}"
        )

    except subprocess.CalledProcessError as e:
        # Check if the error is due to a missing font
        if 'fontspec error: "font-not-found"' in e.stderr:
            print(
                f"⚠️  WARNING: Font '{preferred_font}' not found. Falling back to '{fallback_font}'."
            )

            with open(combined_md_filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace the font and write back to the file
            modified_content = content.replace(
                f"mainfont: {preferred_font}", f"mainfont: '{fallback_font}'"
            )
            with open(combined_md_filepath, "w", encoding="utf-8") as f:
                f.write(modified_content)

            print(f"\nRetrying conversion (Attempt 2: {fallback_font})...")

            try:
                # Second attempt with the fallback font
                subprocess.run(
                    pandoc_command, check=True, capture_output=True, text=True
                )
                print(
                    f"✅ Successfully created PDF file with fallback font at: {pdf_filepath}"
                )
            except subprocess.CalledProcessError as e2:
                print(
                    f"❌ ERROR: Pandoc failed even with the fallback font. Error: {e2}"
                )
                print(
                    "\n--- LaTeX Error Log ---\n"
                    + e2.stderr
                    + "\n-----------------------"
                )
        else:
            # The error was not about a missing font
            print(f"❌ ERROR: Pandoc failed to convert the file. Error: {e}")
            print(
                "\n--- LaTeX Error Log ---\n" + e.stderr + "\n-----------------------"
            )

    except FileNotFoundError:
        print(
            "❌ ERROR: Pandoc/LaTeX not found. Ensure they are installed and in your system's PATH."
        )

    # --- Step 4: Clean up the temporary file ---
    finally:
        if os.path.exists(combined_md_filepath):
            os.remove(combined_md_filepath)
            print(f"\nCleaned up temporary file: {combined_md_filepath}")


if __name__ == "__main__":
    combine_and_convert()
