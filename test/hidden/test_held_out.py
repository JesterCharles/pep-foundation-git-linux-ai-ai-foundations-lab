"""Held-out tests: graded on submit, never shown to the learner.

Each check first repeats its task's main result, so an untouched starter can
never pass one, then looks at an edge case.
"""

from test.support import (
    CLAIMS,
    DESK,
    DRAFT_FIXTURE,
    STORY,
    TOKEN_VALUE,
    VAGUE,
    assert_criteria_shape,
    assert_verdicts,
    criteria_lines,
    read,
    redacted_text,
    review_lines,
    story_line,
)


def test_task1_no_wish_wording_left():
    lines = criteria_lines(1)
    assert_criteria_shape(1, lines)
    lowered = "\n".join(lines).lower()
    for phrase in VAGUE:
        assert phrase not in lowered, (
            f"Task 1: the wish wording {phrase!r} is still there. Replace it with a concrete, "
            "observable result."
        )


def test_task2_one_verdict_per_claim():
    lines = review_lines(2)
    assert_verdicts(2, lines)
    for claim, (verdict, _hint) in CLAIMS.items():
        other = "unsupported" if verdict == "supported" else "supported"
        assert f"{claim}={other}" not in lines, (
            f"Task 2: work/review.md gives {claim} two verdicts. Keep exactly one line per claim; "
            "the diff decides which."
        )


def test_task2_evidence_and_story_name_the_missing_test():
    lines = review_lines(2)
    assert "decision=request-changes" in lines, "Task 2: the decision is not decision=request-changes."
    evidence = [line for line in lines if line.startswith("evidence=")]
    assert evidence and "test" in evidence[0].lower(), (
        "Task 2: the evidence line must name what is missing, for example: "
        "evidence=the diff adds no test, so claim 2 has nothing behind it."
    )
    story = story_line(2)
    assert STORY.match(story), f"Task 2: work/next-story.md is not in the story shape: {story!r}."
    assert "test" in story.lower(), (
        "Task 2: the follow-up story should ask for the work the proposal skipped: the missing test."
    )


def test_task3_original_draft_unchanged():
    text = redacted_text(3)
    assert TOKEN_VALUE not in text, "Task 3: the deploy token value is still in the redacted request."
    assert read(DESK / "drafts" / "help-request.md") == read(DRAFT_FIXTURE), (
        "Task 3: redact a copy in work/, never the original draft: reviewers must still be able "
        "to see what was nearly sent. Restore drafts/help-request.md."
    )
