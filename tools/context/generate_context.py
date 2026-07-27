from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import subprocess

VERSION = "0.5.0"

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
    "docs": {
        "path": "docs",
        "pattern": "*.md",
    },
    "hardware": {
        "path": "hardware",
        "pattern": "*.cfg",
    },
    "machine": {
        "path": "machine",
        "pattern": "*.cfg",
    },
    "calibration": {
        "path": "calibration",
        "pattern": "*.cfg",
    },
    "macros": {
        "path": "macros",
        "pattern": "*.cfg",
    },
}

SESSION_DOCUMENTS = {
    "hardware": "HARDWARE.md",
    "commissioning": "COMMISSIONING.md",
    "calibration": "CALIBRATION.md",
    "known_issues": "KNOWN-ISSUES.md",
    "changelog": "MACHINE_CHANGELOG.md",
}

def get_timestamp():
    """Return generation timestamp."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_generator():
    """
    Return the generator name and version.
    """

    return f"Ender 5 Pro Context Generator v{VERSION}"

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

    print(
        f"Generated: {output_path.relative_to(REPO_ROOT)} "
        f"({get_generator()})"
    )

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

    for category, settings in ROOT_FOLDERS.items():

        folder = REPO_ROOT / settings["path"]
        pattern = settings["pattern"]

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

def build_config_section(title, configs):
    """
    Build a configuration section.
    """

    output = []

    output.append("=" * 60)
    output.append(title.upper())
    output.append("=" * 60)
    output.append("")

    for cfg in configs:

        output.append(f"## {cfg.name}")
        output.append("")

        output.append("```")
        output.append(cfg.text.rstrip())
        output.append("```")
        output.append("")
        output.append("-" * 60)
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
        "generator": get_generator(),

        "repository": build_repository_statistics(repo),

        "hardware": build_document(repo,
            SESSION_DOCUMENTS["hardware"],
        ),

        "commissioning": build_document(repo,
            SESSION_DOCUMENTS["commissioning"],
        ),

        "calibration": build_document(repo,
            SESSION_DOCUMENTS["calibration"],
        ),

        "known_issues": build_document(repo,
            SESSION_DOCUMENTS["known_issues"],
        ),

        "changelog": build_document(repo,
            SESSION_DOCUMENTS["changelog"],
        ),

        "git_history": get_git_history(),

        "briefing": build_ai_briefing(repo),

    }

    return render_template(
        template,
        replacements,
    )

def build_technical_reference(repo, templates):
    """
    Render the technical reference document.
    """

    template = templates["technical"]

    replacements = {

        "generated": get_timestamp(),
        "generator": get_generator(),

        "repository": build_repository_statistics(repo),

        "hardware": build_config_section(
            "Hardware",
            repo.hardware,
        ),

        "machine": build_config_section(
            "Machine",
            repo.machine,
        ),

        "calibration": build_config_section(
            "Calibration",
            repo.calibration,
        ),

        "macros": build_config_section(
            "Macros",
            repo.macros,
        ),

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
        "generator": get_generator(),
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
    print(get_generator())
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

    session = build_session_context(repo,templates,)

    write_output(
        "SESSION_CONTEXT.md",
        session,
    )

    technical = build_technical_reference(repo,templates,)

    write_output(
        "TECHNICAL_REFERENCE.md",
        technical,
    )

    print("\nContext generation complete.")

if __name__ == "__main__":
    main()