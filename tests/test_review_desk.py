"""Checks for the "Review the assistant's change" lab. Run from the lab folder:

    python -m unittest discover -s tests -v

Each failure message names the next action.
"""

import re
import unittest

from lab_support import (
    DESK,
    FIXTURES,
    LOG_LINE,
    REPORTER_EMAIL,
    TOKEN_VALUE,
    WORK,
)

SETUP_HINT = "Run `python tests/setup_lab.py` from the lab folder first."
CRITERION = re.compile(r"^Criterion [0-9]+: Given .+ When .+ Then .+$")
VAGUE = ["show the port stuff", "work fine", "should be better", "looks good", "user-friendly"]


def read(path):
    return path.read_text(encoding="utf-8")


class ReviewDeskTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not WORK.exists():
            raise unittest.SkipTest(f"The work folder is missing. {SETUP_HINT}")

    def work_file(self, name, hint):
        target = WORK / name
        self.assertTrue(target.exists(), f"work/{name} does not exist yet. {hint}")
        return read(target)

    def work_lines(self, name, hint):
        """The file's non-empty lines, stripped, matched whole: an unedited
        placeholder such as claim-1=your-verdict is not a verdict."""
        return [line.strip() for line in self.work_file(name, hint).splitlines() if line.strip()]

    def test_acceptance_criteria_are_testable(self):
        text = self.work_file(
            "acceptance-criteria.md",
            "Turn the three stand-up wishes into three one-line criteria, each on its own "
            "line in the form: Criterion N: Given ... When ... Then ...",
        )
        lines = [line.strip() for line in text.splitlines() if line.strip().startswith("Criterion")]
        self.assertGreaterEqual(
            len(lines),
            3,
            "Write three criteria lines, one per stand-up wish, each starting "
            "'Criterion N: Given ... When ... Then ...'.",
        )
        for line in lines:
            self.assertRegex(
                line,
                CRITERION,
                f"This line is not testable yet: {line!r}. A testable criterion names a "
                "starting state (Given), an action (When) and an observable result (Then).",
            )
        joined = "\n".join(lines)
        self.assertIn(
            "STATUS_PORT",
            joined,
            "At least one criterion must name the STATUS_PORT variable the team agreed on: "
            "that is the concrete, checkable part of the story.",
        )
        self.assertIn(
            "8080",
            joined,
            "At least one criterion must pin the agreed fallback value 8080; 'works fine "
            "when nothing is configured' is not checkable.",
        )
        lowered = joined.lower()
        for phrase in VAGUE:
            self.assertNotIn(
                phrase,
                lowered,
                f"The wish wording {phrase!r} is still there. Replace it with a concrete, "
                "observable result.",
            )

    def test_claims_are_checked_against_the_diff(self):
        lines = self.work_lines(
            "review.md",
            "Check each numbered claim in PROPOSAL.md against proposal/change.diff and "
            "record one verdict line per claim: claim-N=supported or claim-N=unsupported.",
        )
        expectations = {
            "claim-1": (
                "supported",
                "Claim 1 is supported: the diff adds the STATUS_PORT read with the 8080 "
                "fallback to status_message().",
            ),
            "claim-2": (
                "unsupported",
                "Claim 2 is unsupported: read the whole diff - no test file appears "
                "anywhere in it. A claim with no diff line behind it is unsupported, "
                "however confident the summary sounds.",
            ),
            "claim-3": (
                "supported",
                "Claim 3 is supported: the diff's second hunk adds the status-line format "
                "to README.md.",
            ),
        }
        for claim, (verdict, hint) in expectations.items():
            self.assertIn(
                f"{claim}={verdict}",
                lines,
                f"work/review.md needs the whole line {claim}={verdict} "
                f"(a left-over {claim}=your-verdict placeholder is not a verdict). {hint}",
            )
            other = "unsupported" if verdict == "supported" else "supported"
            self.assertNotIn(
                f"{claim}={other}",
                lines,
                f"work/review.md gives {claim} two verdicts. Keep exactly one line per "
                "claim; the diff decides which.",
            )

    def test_decision_cites_the_broken_claim(self):
        lines = self.work_lines(
            "review.md",
            "Finish work/review.md with your decision and its evidence, as two lines: "
            "decision=... and evidence=...",
        )
        self.assertIn(
            "decision=request-changes",
            lines,
            "One claim promised work the diff does not contain, so the decision line must "
            "be exactly decision=request-changes. Approving would merge an untested promise.",
        )
        evidence = [line for line in lines if line.startswith("evidence=")]
        self.assertTrue(
            evidence and "test" in evidence[0].lower(),
            "Add an evidence line that names what is missing, for example: "
            "evidence=the diff adds no test, so claim 2 has nothing behind it.",
        )

    def test_next_story_is_well_formed(self):
        text = self.work_file(
            "next-story.md",
            "Write the follow-up user story for the missing test, one line in the form: "
            "As ..., I want ..., so that ...",
        )
        lines = [line.strip() for line in text.splitlines() if line.strip().startswith("As ")]
        self.assertTrue(
            lines,
            "work/next-story.md needs one line starting 'As ' - the role comes first.",
        )
        story = lines[0]
        self.assertRegex(
            story,
            re.compile(r"^As .+, I want .+, so that .+\.?$"),
            f"This is not the full story shape yet: {story!r}. "
            "Name the role (As ...), the want (I want ...) and the reason (so that ...).",
        )
        self.assertIn(
            "test",
            story.lower(),
            "The story should ask for the work the proposal skipped: the missing test.",
        )

    def test_sharing_plan_sorts_the_material(self):
        lines = self.work_lines(
            "sharing-plan.md",
            "Sort the four items from the draft into share, redact or never, one "
            "item=verdict line each, plus the workspace line from step 5.",
        )
        for line, hint in [
            ("log-line=share", "The log line is project material with nothing personal: share it."),
            ("app-config=share", "The config facts are project material: share them."),
            (
                "customer-email=redact",
                "The report matters, the reporter's address does not: redact it first.",
            ),
            (
                "deploy-token=never",
                "A live credential never goes into a prompt, redacted or not.",
            ),
            (
                "workspace=project-folder",
                "The assistant needs the status-page project - config and logs - and "
                "nothing beyond it: workspace=project-folder.",
            ),
        ]:
            self.assertIn(
                line,
                lines,
                f"work/sharing-plan.md needs the whole line {line} "
                "(an unedited placeholder is not a verdict). " + hint,
            )

    def test_redacted_request_keeps_what_helps(self):
        text = self.work_file(
            "help-request-redacted.md",
            "Copy drafts/help-request.md to work/help-request-redacted.md and remove "
            "only what must not be shared.",
        )
        self.assertIn(
            LOG_LINE,
            text,
            "Keep the failing log line word for word: it is the part that helps.",
        )
        self.assertIn(
            "What should I check first?",
            text,
            "Keep the actual question: a redacted request must still ask for something.",
        )

    def test_redacted_request_leaks_nothing(self):
        text = self.work_file(
            "help-request-redacted.md",
            "Copy drafts/help-request.md to work/help-request-redacted.md and remove "
            "only what must not be shared.",
        )
        self.assertNotIn(
            TOKEN_VALUE,
            text,
            "The deploy token value is still in the redacted request. Remove the value "
            "itself; a placeholder like [deploy token removed] is fine.",
        )
        self.assertNotIn(
            REPORTER_EMAIL,
            text,
            "The reporter's email address is still in the redacted request. Keep the fact "
            "that a customer reported it; drop who.",
        )
        original = read(DESK / "drafts" / "help-request.md")
        self.assertEqual(
            read(FIXTURES / "drafts" / "help-request.md"),
            original,
            "Redact a copy in work/, never the original draft: reviewers must still be "
            "able to see what was nearly sent. Rerun setup to restore it.",
        )


if __name__ == "__main__":
    unittest.main()
