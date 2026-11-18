"""Shared paths, ground truth and helpers for the "Review the assistant's change" tests.

The tests read the files you write in src/review-desk/work/. Nothing runs, and
nothing uses the network.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DESK = ROOT / "src" / "review-desk"
WORK = DESK / "work"
DRAFT_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "review-desk" / "drafts" / "help-request.md"

# Ground truth the checks rely on.
TOKEN_VALUE = "dt-9f27c4b1a8"
REPORTER_EMAIL = "casey@customer.example"
LOG_LINE = (
    "2026-01-05T08:00:35Z ERROR health check GET http://localhost:8080/status "
    "failed: connection refused"
)
QUESTION = "What should I check first?"

CRITERION = re.compile(r"^Criterion [0-9]+: Given .+ When .+ Then .+$")
STORY = re.compile(r"^As .+, I want .+, so that .+\.?$")
VAGUE = ["show the port stuff", "work fine", "should be better", "looks good", "user-friendly"]

CLAIMS = {
    "claim-1": (
        "supported",
        "Claim 1 is supported: the diff adds the STATUS_PORT read with the 8080 fallback "
        "to status_message().",
    ),
    "claim-2": (
        "unsupported",
        "Claim 2 is unsupported: read the whole diff - no test file appears anywhere in it. "
        "A claim with no diff line behind it is unsupported, however confident the summary sounds.",
    ),
    "claim-3": (
        "supported",
        "Claim 3 is supported: the diff's second hunk adds the status-line format to README.md.",
    ),
}

SHARING = [
    ("log-line=share", "The log line is project material with nothing personal: share it."),
    ("app-config=share", "The config facts are project material: share them."),
    ("customer-email=redact", "The report matters, the reporter's address does not: redact it first."),
    ("deploy-token=never", "A live credential never goes into a prompt, redacted or not."),
    (
        "workspace=project-folder",
        "The assistant needs the status-page project - config and logs - and nothing beyond "
        "it: workspace=project-folder.",
    ),
]


def read(path):
    """Text with LF line endings, so a Windows editor makes no difference."""
    return Path(path).read_bytes().decode("utf-8").replace("\r\n", "\n")


def work_text(task, name, hint):
    target = WORK / name
    if not target.exists():
        pytest.fail(f"Task {task}: work/{name} does not exist yet. {hint}")
    return read(target)


def work_lines(task, name, hint):
    """The file's non-empty lines, stripped, matched whole: an unedited placeholder
    such as claim-1=your-verdict is not a verdict."""
    return [line.strip() for line in work_text(task, name, hint).splitlines() if line.strip()]


def criteria_lines(task):
    text = work_text(
        task,
        "acceptance-criteria.md",
        "Write three one-line criteria in the form: Criterion N: Given ... When ... Then ...",
    )
    return [line.strip() for line in text.splitlines() if line.strip().startswith("Criterion")]


def assert_criteria_shape(task, lines):
    assert len(lines) >= 3, (
        f"Task {task}: work/acceptance-criteria.md needs three criteria lines, one per stand-up "
        "wish, each starting 'Criterion N: Given ... When ... Then ...'."
    )
    for line in lines:
        assert CRITERION.match(line), (
            f"Task {task}: this line is not testable yet: {line!r}. A testable criterion names a "
            "starting state (Given), an action (When) and an observable result (Then)."
        )


def review_lines(task):
    return work_lines(
        task,
        "review.md",
        "Record one verdict line per claim (claim-N=supported or claim-N=unsupported), then "
        "decision=... and evidence=...",
    )


def assert_verdicts(task, lines):
    for claim, (verdict, hint) in CLAIMS.items():
        assert f"{claim}={verdict}" in lines, (
            f"Task {task}: work/review.md needs the whole line {claim}={verdict} "
            f"(a left-over {claim}=your-verdict placeholder is not a verdict). {hint}"
        )


def story_line(task):
    text = work_text(
        task,
        "next-story.md",
        "Write the follow-up user story for the missing work, one line in the form: "
        "As ..., I want ..., so that ...",
    )
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("As ")]
    assert lines, f"Task {task}: work/next-story.md needs one line starting 'As ' - the role comes first."
    return lines[0]


def redacted_text(task):
    return work_text(
        task,
        "help-request-redacted.md",
        "Copy drafts/help-request.md to work/help-request-redacted.md and remove only what must "
        "not be shared.",
    )
