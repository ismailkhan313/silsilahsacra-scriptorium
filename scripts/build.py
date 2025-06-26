import subprocess
import sys
import os

# --- Configuration ---
# Input Markdown file (your main article)
MD_FILE = "Introduction to The Ten Essentials (المبادئ العشرة) Poem copy.md"

# Output PDF file
PDF_FILE = "article_output.pdf"

# Location of the LaTeX template
TEMPLATE_FILE = os.path.join("templates", "article.tex")

# Location of your bibliography file
BIB_FILE = "references.bib"
# ---------------------


def check_dependencies():
    """Checks if pandoc and lualatex are in the system's PATH."""
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: pandoc is not installed or not in your system's PATH.")
        sys.exit(1)

    try:
        subprocess.run(["lualatex", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: lualatex is not installed or not in your system's PATH.")
        print("Please install a TeX distribution like TeX Live, MiKTeX, or MacTeX.")
        sys.exit(1)


def build_pdf():
    """Constructs and runs the pandoc command to build the PDF."""
    print(f"Starting compilation of '{MD_FILE}'...")

    # Check if all required files exist before attempting to build
    required_files = [MD_FILE, TEMPLATE_FILE]
    if os.path.exists(BIB_FILE):
        required_files.append(BIB_FILE)

    for f in required_files:
        if not os.path.exists(f):
            print(f"Error: Required file not found: {f}")
            sys.exit(1)

    # Pandoc command as a list of arguments
    command = [
        "pandoc",
        MD_FILE,
        "--output",
        PDF_FILE,
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
        ".:./templates",
    ]

    try:
        # The 'text=True' argument is good practice for cleaner output
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Success! PDF created at '{PDF_FILE}'.")
        # Uncomment the line below if you want to see pandoc's output
        # print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("--- Pandoc Compilation Failed ---", file=sys.stderr)
        print(f"Pandoc returned a non-zero exit code: {e.returncode}", file=sys.stderr)
        print("\n--- Pandoc Error Output ---", file=sys.stderr)
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
