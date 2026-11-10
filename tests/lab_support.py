"""Shared paths and helpers for the "Review the assistant's change" lab.

Standard library only.
"""

import shutil
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = LAB_ROOT / "fixtures" / "review-desk"
STARTER = LAB_ROOT / "starter"
DESK = STARTER / "review-desk"
WORK = DESK / "work"

# Shipped starter files, restored from fixtures on every reset.
SHIPPED = [
    "USER_STORY.md",
    "PROPOSAL.md",
    "project/status_message.py",
    "project/README.md",
    "proposal/status_message.py",
    "proposal/change.diff",
    "drafts/help-request.md",
]

# Paths created by setup or by the learner; reset and cleanup remove them.
CREATED_PATHS = [
    WORK,
    LAB_ROOT / "tests" / "__pycache__",
]

# Ground truth the checks rely on.
TOKEN_VALUE = "dt-9f27c4b1a8"
REPORTER_EMAIL = "casey@customer.example"
LOG_LINE = (
    "2026-01-05T08:00:35Z ERROR health check GET http://localhost:8080/status "
    "failed: connection refused"
)


def inside(path, parent):
    """True when path resolves to parent or somewhere below it."""
    resolved = Path(path).resolve()
    base = Path(parent).resolve()
    return resolved == base or base in resolved.parents


def remove(path):
    """Remove a lab-created path after confirming it is inside the starter or tests folder."""
    path = Path(path)
    if not (inside(path, STARTER) or inside(path, LAB_ROOT / "tests")):
        raise RuntimeError(f"refusing to remove {path}: outside the lab")
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def write_fixture(source, target):
    """Copy fixture text with LF line endings so checked bytes are identical everywhere."""
    data = Path(source).read_bytes().replace(b"\r\n", b"\n")
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    Path(target).write_bytes(data)


def restore_starter_files():
    """Write the shipped starter bytes."""
    for local in SHIPPED:
        write_fixture(FIXTURES / local, DESK / local)


def reset_starter():
    """Remove learner-created paths and restore the shipped files."""
    for path in CREATED_PATHS:
        remove(path)
    restore_starter_files()
