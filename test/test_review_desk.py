"""Trainer-authored tests — restored over the learner checkout at grade time.

One check per task. Each reads the files you write in src/review-desk/work/.
"""

from test.support import (
    LOG_LINE,
    QUESTION,
    REPORTER_EMAIL,
    SHARING,
    STORY,
    TOKEN_VALUE,
    assert_criteria_shape,
    assert_verdicts,
    criteria_lines,
    redacted_text,
    review_lines,
    story_line,
    work_lines,
)


def test_task1_acceptance_criteria_are_testable():
    lines = criteria_lines(1)
    assert_criteria_shape(1, lines)
    joined = "\n".join(lines)
    assert "STATUS_PORT" in joined, (
        "Task 1: at least one criterion must name the STATUS_PORT variable the team agreed on: "
        "that is the concrete, checkable part of the story."
    )
    assert "8080" in joined, (
        "Task 1: at least one criterion must pin the agreed fallback value 8080; 'works fine "
        "when nothing is configured' is not checkable."
    )


def test_task2_review_and_follow_up():
    lines = review_lines(2)
    assert_verdicts(2, lines)
    assert "decision=request-changes" in lines, (
        "Task 2: one claim promised work the diff does not contain, so the decision line must be "
        "exactly decision=request-changes. Approving would merge an untested promise."
    )
    story = story_line(2)
    assert STORY.match(story), (
        f"Task 2: work/next-story.md is not the full story shape yet: {story!r}. Name the role "
        "(As ...), the want (I want ...) and the reason (so that ...)."
    )


def test_task3_help_request_is_safe():
    lines = work_lines(
        3,
        "sharing-plan.md",
        "Sort the four items from the draft into share, redact or never, one item=verdict line "
        "each, plus the workspace line.",
    )
    for line, hint in SHARING:
        assert line in lines, (
            f"Task 3: work/sharing-plan.md needs the whole line {line} "
            f"(an unedited placeholder is not a verdict). {hint}"
        )
    text = redacted_text(3)
    assert LOG_LINE in text, "Task 3: keep the failing log line word for word: it is the part that helps."
    assert QUESTION in text, "Task 3: keep the actual question: a redacted request must still ask for something."
    assert TOKEN_VALUE not in text, (
        "Task 3: the deploy token value is still in the redacted request. Remove the value "
        "itself; a placeholder like [deploy token removed] is fine."
    )
    assert REPORTER_EMAIL not in text, (
        "Task 3: the reporter's email address is still in the redacted request. Keep the fact "
        "that a customer reported it; drop who."
    )
