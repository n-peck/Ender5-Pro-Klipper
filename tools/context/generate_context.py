from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import subprocess

@dataclass
class RepoFile:
    name: str
    path: Path
    relative: Path
    category: str
    lines: int
    headings: list[str] = field(default_factory=list)
    modified: datetime = None
    text: str = ""

@dataclass
class Repository:
    docs: list[RepoFile] = field(default_factory=list)
    hardware: list[RepoFile] = field(default_factory=list)
    machine: list[RepoFile] = field(default_factory=list)
    calibration: list[RepoFile] = field(default_factory=list)
    macros: list[RepoFile] = field(default_factory=list)

def find_repo_root():
    """
    Locate the repository root by searching upwards for README.md.
    """

    current = Path(__file__).resolve().parent

    while current != current.parent:

        if (current / "README.md").exists():
            return current

        current = current.parent

    raise RuntimeError("Repository root not found.")

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = find_repo_root()

TEMPLATE_DIR = SCRIPT_DIR / "templates"

OUTPUT_DIR = REPO_ROOT / "project" / "context"

DOCS_DIR = REPO_ROOT / "docs"
PROJECT_DIR = REPO_ROOT / "project"
CONFIG_DIR = REPO_ROOT

ROOT_FOLDERS = {
    "docs": ("docs", "*.md"),
    "hardware": ("hardware", "*.cfg"),
    "machine": ("machine", "*.cfg"),
    "calibration": ("calibration", "*.cfg"),
    "macros": ("macros", "*.cfg"),
}

def get_timestamp():
    """Return generation timestamp."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_templates():
    """Load all markdown templates."""

    templates = {}

    for template in TEMPLATE_DIR.glob("*.md"):
        templates[template.stem] = template.read_text(encoding="utf-8")

    return templates

def render_template(template, replacements):
    """Replace {{tokens}} in template."""

    output = template

    for key, value in replacements.items():
        output = output.replace(f"{{{{{key}}}}}", str(value))

    return output

def write_file(path, content):
    """Write UTF-8 file."""

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content, encoding="utf-8")

def write_output(filename, content):
    """
    Write a generated context document into the project/context folder.
    """

    output_path = OUTPUT_DIR / filename

    write_file(output_path, content)

    print(f"Generated: {output_path.relative_to(REPO_ROOT)}")

def read_file(path):
    """Read UTF-8 file safely."""

    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")

def run_git(command):
    """Run git command."""

    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()

def get_git_history():

    return run_git(["git", "log", "--oneline", "-10"])

def get_git_branch():

    return run_git(["git", "branch", "--show-current"])

def get_git_commit():

    return run_git(["git", "rev-parse", "--short", "HEAD"])

def scan_repository():
    """
    Scan the repository and return a Repository object.
    """

    repo = Repository()

    for category, (folder_name, pattern) in ROOT_FOLDERS.items():

        folder = REPO_ROOT / folder_name

        if not folder.exists():
            continue

        for file in sorted(folder.glob(pattern)):

            text = read_file(file)
            lines = text.splitlines()

            headings = [
                line.lstrip("# ").strip()
                for line in lines
                if line.startswith("#")
            ]

            entry = RepoFile(
                name=file.name,
                path=file,
                relative=file.relative_to(REPO_ROOT),
                category=category,
                lines=len(lines),
                headings=headings,
                modified=datetime.fromtimestamp(file.stat().st_mtime),
                text=text,
            )

            getattr(repo, category).append(entry)

    return repo

def build_repository_statistics(repo):
    """
    Build repository statistics section.
    """

    output = []

    output.append(f"Documentation Files : {len(repo.docs)}")
    output.append(f"Hardware Configs    : {len(repo.hardware)}")
    output.append(f"Machine Configs     : {len(repo.machine)}")
    output.append(f"Calibration Configs : {len(repo.calibration)}")
    output.append(f"Macro Files         : {len(repo.macros)}")
    output.append("")
    output.append(f"Git Branch          : {get_git_branch()}")
    output.append(f"Git Commit          : {get_git_commit()}")

    return "\n".join(output)

def build_repository_structure():
    """
    Build repository folder structure.
    """

    output = []

    for folder in ROOT_FOLDERS:
        output.append(f"- {folder}/")

    return "\n".join(output)

def build_documentation_summary(repo):
    """
    Build documentation inventory.
    """

    output = []

    for doc in repo.docs:

        status = "⚠ Empty" if doc.lines == 0 else "✓"

        output.append(
            f"- {doc.name:<25} {doc.lines:>4} lines   {status}"
        )

    return "\n".join(output)

def build_configuration_summary(repo):
    """
    Build configuration inventory.
    """

    output = []

    for section in ("hardware", "machine", "calibration", "macros"):

        configs = getattr(repo, section)

        output.append(f"### {section.title()} ({len(configs)})")

        for cfg in configs:
            output.append(f"- {cfg.name}")

        output.append("")

    return "\n".join(output)

def build_document(repo, filename):
    """
    Return the contents of a documentation file.
    """

    for doc in repo.docs:

        if doc.name.lower() == filename.lower():

            return doc.text.strip()

    return "*Document not found.*"

def build_ai_briefing(repo):

    return (
        "This project is currently in the commissioning stage.\n\n"
        "The configuration architecture has been separated into "
        "hardware, machine and calibration modules.\n\n"
        "Continue with the next outstanding commissioning or "
        "calibration task before making hardware changes."
    )

def build_session_context(repo, templates):

    template = templates["session"]

    replacements = {

        "generated": get_timestamp(),

        "repository": build_repository_statistics(repo),

        "hardware": build_document(repo, "HARDWARE.md"),

        "commissioning": build_document(repo, "COMMISSIONING.md"),

        "calibration": build_document(repo, "CALIBRATION.md"),

        "known_issues": build_document(repo, "KNOWN-ISSUES.md"),

        "changelog": build_document(repo, "MACHINE_CHANGELOG.md"),

        "git_history": get_git_history(),

        "briefing": build_ai_briefing(repo),

    }

    return render_template(
        template,
        replacements,
    )

def build_manifest(repo, templates):
    """
    Render the project manifest.
    """

    template = templates["manifest"]

    replacements = {
        "generated": get_timestamp(),
        "repository_root": REPO_ROOT,
        "repository_statistics": build_repository_statistics(repo),
        "repository_structure": build_repository_structure(),
        "documentation": build_documentation_summary(repo),
        "configuration": build_configuration_summary(repo),
    }

    return render_template(
        template,
        replacements,
    )

def main():

    print("=" * 60)
    print("Ender 5 Pro Context Generator")
    print("=" * 60)

    print("\nLoading templates...")
    templates = load_templates()

    print("Scanning repository...")
    repo = scan_repository()

    print("\nRepository")

    print(f"Repository Root : {REPO_ROOT}")
    print(f"Templates       : {len(templates)}")
    print(f"Documentation   : {len(repo.docs)}")
    print(f"Hardware Config : {len(repo.hardware)}")
    print(f"Machine Config  : {len(repo.machine)}")
    print(f"Calibration     : {len(repo.calibration)}")
    print(f"Macros          : {len(repo.macros)}")

    print("\nGit")

    print(f"Branch          : {get_git_branch()}")
    print(f"Commit          : {get_git_commit()}")

    print("\nDirectory Check")

    print(f"docs         : {(DOCS_DIR).exists()}")
    print(f"hardware     : {(CONFIG_DIR / 'hardware').exists()}")
    print(f"machine      : {(CONFIG_DIR / 'machine').exists()}")
    print(f"calibration  : {(CONFIG_DIR / 'calibration').exists()}")
    print(f"macros       : {(CONFIG_DIR / 'macros').exists()}")

    print("\nContext generator initialisation successful.")

    print("\nGenerating context documents...")

    manifest = build_manifest(repo, templates)

    write_output(
        "PROJECT_MANIFEST.md",
        manifest,
    )

    session = build_session_context(
    repo,
    templates,
    )

    write_output(
        "SESSION_CONTEXT.md",
        session,
    )

    print("\nContext generation complete.")

if __name__ == "__main__":
    main()