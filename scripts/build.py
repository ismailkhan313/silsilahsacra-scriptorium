import subprocess
import sys
import os

# --- Configuration ---
# Input Markdown file (your main article)
MD_FILE = "Introduction to The Ten Essentials (المبادئ العشرة) Poem copy_adjusted.md"

# Directory where the final PDF will be stored
OUTPUT_DIR = "published"

# Location of the LaTeX template
TEMPLATE_FILE = os.path.join("templates", "article.tex")

# Location of your bibliography file
BIB_FILE = "references.bib"

# Directories where Pandoc should look for resource files (e.g., images, included .tex files)
# The script will automatically add the 'shared' directory.
RESOURCE_DIRS = [".", "templates", "shared"]

# The specific publisher file we need to ensure exists
PUBLISHER_INFO_FILE = os.path.join("shared", "publisher-info.tex")
# ---------------------


def check_dependencies():
    """Checks if pandoc and lualatex are in the system's PATH."""
    try:
        subprocess.run(
            ["pandoc", "--version"], capture_output=True, check=True, text=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: pandoc is not installed or not in your system's PATH.")
        sys.exit(1)

    try:
        subprocess.run(
            ["lualatex", "--version"], capture_output=True, check=True, text=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: lualatex is not installed or not in your system's PATH.")
        print("Please install a TeX distribution like TeX Live, MiKTeX, or MacTeX.")
        sys.exit(1)


def build_pdf():
    """Constructs and runs the pandoc command to build the PDF."""
    print(f"Starting compilation of '{MD_FILE}'...")

    # --- 1. Set up dynamic output path ---
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get the base name of the markdown file (e.g., "my-article")
    pdf_basename = os.path.splitext(os.path.basename(MD_FILE))[0]

    # Create the full output path (e.g., "published/my-article.pdf")
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{pdf_basename}.pdf")

    # --- 2. Check if all required files exist before attempting to build ---
    required_files = [MD_FILE, TEMPLATE_FILE, PUBLISHER_INFO_FILE]
    if os.path.exists(BIB_FILE):
        required_files.append(BIB_FILE)

    for f in required_files:
        if not os.path.exists(f):
            print(f"Error: Required file not found: {f}")
            print(
                "Please ensure you are running this script from your project's root directory."
            )
            sys.exit(1)

    # --- 3. Construct and run the Pandoc command ---

    # Build the resource path string in an OS-agnostic way
    # This joins the directories with ':' on macOS/Linux and ';' on Windows
    resource_path_str = os.path.pathsep.join(RESOURCE_DIRS)

    print(f"Using resource path: {resource_path_str}")

    command = [
        "pandoc",
        MD_FILE,
        "--output",
        output_pdf_path,
        "--from",
        "markdown+citations",
        "--template",
        TEMPLATE_FILE,
        "--pdf-engine",
        "lualatex",
        "--biblatex",
        "--bibliography",
        BIB_FILE,
        "--resource-path",
        resource_path_str,  # Use the new, OS-agnostic resource path
    ]

    try:
        # The 'text=True' argument is good practice for cleaner output
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8"
        )
        print(f"\nSuccess! PDF created at '{output_pdf_path}'.")
        # Uncomment the line below if you want to see pandoc's detailed output
        # print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("--- Pandoc Compilation Failed ---", file=sys.stderr)
        print(f"Pandoc returned a non-zero exit code: {e.returncode}", file=sys.stderr)
        print("\n--- Pandoc Error Output ---", file=sys.stderr)
        # Pandoc's stderr often contains the specific LaTeX error message
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError:
        print("Error: 'pandoc' command not found.", file=sys.stderr)
        print(
            "Please ensure Pandoc is installed and in your system's PATH.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    check_dependencies()
    build_pdf()
