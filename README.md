# AI Foundations lab: review the assistant's change

A teammate asked an AI coding assistant to make the status line show the service's
port. Its proposal is on your desk: the assistant's summary, the actual diff, and
the teammate's next prompt, which is one paste away from leaking a credential. You
do the human half of working with an AI assistant:
- write testable acceptance criteria (Given / When / Then);
- check each of the assistant's claims against the real diff;
- make the review decision and write a follow-up user story;
- decide what is safe to share and redact the help request.

The answers are Markdown files that 7 checks read. No AI model or app runs in this
lab.

The full learner instructions are in [`.evolv/instructions.md`](.evolv/instructions.md), which the lab platform shows as the lab's instructions.

## Layout

This repository follows the Exa coding-lab scaffold for Python.

| Path | What it is |
|---|---|
| `src/review-desk/` | The shipped proposal, story and draft the learner reviews |
| `src/review-desk/work/` | The learner's answers, created by setup |
| `test/test_review_desk.py` | Visible checks |
| `test/setup_lab.py` | Creates (or resets) the review desk |
| `test/cleanup_lab.py` | Removes `work/` and restores the shipped files |
| `test/lab_support.py` | Paths and ground truth the scripts and checks share |
| `test/conftest.py` | Counts a check that could not run (lab not set up) as a failure |
| `fixtures/review-desk/` | The shipped files that setup restores |
| `.evolv/instructions.md` | Learner instructions |
| `.evolv/grade.yml` | Grading manifest, used by Run Tests and by the grader |
| `requirements.txt` | pytest, the only dependency |
| `Dockerfile` | Grader image with the dependencies baked in |
| `expected/on-completion.txt` | The result of a finished lab |

There are no held-out tests in this lab: every check is visible.

## Run the tests

With Python 3.11 or later, set the lab up once, then run the checks:

```
python test/setup_lab.py
python -m pytest -q
```

On the platform, **Run Tests** runs the second command. All 7 checks fail until the
answers are written. That is expected. Grading never runs `test/setup_lab.py`.
