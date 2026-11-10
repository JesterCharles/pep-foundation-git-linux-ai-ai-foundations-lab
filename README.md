# Review the assistant's change

The status-page incident is fixed, and the team wants a follow-up: the status
line should show the port the service expects. A teammate asked an AI coding
assistant to make the change. The proposal is on your desk - the assistant's
summary, the actual diff, and the teammate's next prompt draft, which is one
paste away from leaking a credential.

Your job is the human half of working with an AI assistant: turn the user
story's vague wishes into testable acceptance criteria, check every claim in
the summary against the real diff, decide approve or request changes with
evidence, and make the teammate's help request safe to send.

You do not need an AI assistant for this lab: it practises the checking, not
the generating. About 15 minutes of your scheduled exercise block (an
estimate); if you pass 20, pause and finish in self-study, using
**Troubleshooting** if you are stuck.
Everything runs on your own computer, offline: no account, no network, no
container engine.

## Open the project

This repository is the whole lab. Clone it, then open the cloned folder in VS Code or any
other editor or IDE (in VS Code: **File > Open Folder**). Nothing in this lab runs in a browser.

Run every command below in a terminal at the repository root, the folder that holds this
README: in VS Code use **Terminal > New Terminal**, which opens there; with any other editor,
open a terminal and `cd` into the clone. The steps call this folder the lab folder.

This is a review practical on real files: you read a real diff and write your
criteria, review and redacted request into Markdown files that the tests check. It does not
run an AI model or the status-page app.

## What you edit

Setup (step 2) builds `starter/review-desk/`; everything you write goes into
its `work/` folder, and the shipped story, proposal, diff and draft stay
read-only evidence. The checks read five files you create:

| You create | What goes in it | Why the team needs it |
|---|---|---|
| `work/acceptance-criteria.md` | three one-line Given/When/Then criteria (step 3) | vague wishes cannot be tested or scored |
| `work/review.md` | a supported/unsupported verdict per claim, then the decision and its evidence (step 4) | the merge call must rest on the diff, not the summary |
| `work/next-story.md` | a one-line user story for the outstanding work (step 4) | request-changes without a follow-up stalls the work |
| `work/sharing-plan.md` | share/redact/never per item, plus the workspace pick (step 5) | the rules of use decide what may reach a prompt |
| `work/help-request-redacted.md` | a copy of the draft with the token and the email gone (step 5) | the help request must be safe to send and still useful |

Leave `tests/`, `fixtures/`, `expected/` and the shipped evidence
files as they are: the seven checks pass only when the review work is really
done.

One test command proves the lab, run from this lab folder (step 6):

```text
python -m unittest discover -s tests -v
```

Each failing check prints the next action to take.

## 1. Check your tools

Open a terminal at the repository root (the folder that holds this README).

```text
python --version
```

**Expect:** `Python 3.11` or newer.
If `python` is missing or old, try `python3 --version`; when that works, type
`alias python=python3` once for this terminal window (on Windows PowerShell:
`Set-Alias python py`).

## 2. Create the review desk

From this lab folder, run:

```text
python tests/setup_lab.py
```

**Expect:** `Review desk ready in starter/review-desk/.`

Everything you write goes into the `work/` folder setup created. Running setup
again resets the lab: `work/` is removed and every shipped file is restored.

Move in and look around:

```text
cd starter/review-desk
ls
```

**Expect:** `USER_STORY.md`, `PROPOSAL.md`, `project/` (the code as it is
today), `proposal/` (the assistant's change), `drafts/` and `work/`.

## 3. Turn the story into testable acceptance criteria

Read `USER_STORY.md`. The story itself is fine; the three stand-up wishes
below it are not checkable. "It should work fine when nothing is configured"
cannot be scored - fine according to whom?

A testable criterion has three parts: a starting state (**Given**), an action
(**When**) and an observable result (**Then**). Compare:

- Vague: "It should work fine when nothing is configured."
- Testable: `Criterion 2: Given STATUS_PORT is not set, When status_message()
  is called, Then the line ends with "on port 8080".`

Create `work/acceptance-criteria.md` with three lines, one per wish, each in
exactly that one-line shape:

```text
Criterion 1: Given ... When ... Then ...
Criterion 2: Given ... When ... Then ...
Criterion 3: Given ... When ... Then ...
```

Use the concrete facts the team already agreed in the story - the
`STATUS_PORT` variable and the `8080` fallback - and do not reuse the wish
wording. (The example above is one of the three; write it in your own words
or take it as is, then write the other two.)

## 4. Check every claim against the diff

Read the assistant's summary in `PROPOSAL.md`: three numbered claims, written
with complete confidence. Now open `proposal/change.diff` and read the actual
change. For each claim, find the diff lines that back it:

- Claim 1 talks about `STATUS_PORT` and a fallback. Which `+` lines in
  `status_message.py` do that?
- Claim 2 talks about a unit test. Search the whole diff: which file would
  that be? Is there any test file in the diff at all?
- Claim 3 talks about the README. Does a `README.md` hunk exist, and does it
  describe the new line?

A claim with no diff line behind it is **unsupported** - it does not matter
how plausible it sounds. (If you want to see the full proposed file,
`proposal/status_message.py` is the after version; `project/status_message.py`
is the before.)

Record one verdict per claim in `work/review.md`, replacing each
`your-verdict` with either `supported` or `unsupported` - whichever the diff
backs:

```text
claim-1=your-verdict
claim-2=your-verdict
claim-3=your-verdict
```

Then make the call. Approve is the right call only when every claim has diff
lines behind it; if any claim promises work the diff does not contain, that
work is implemented-but-unverified at best, and merging an untested promise is
how the last incident started. Finish `work/review.md` with your decision and
the evidence it rests on:

```text
decision=your-decision
evidence=one line naming the diff evidence your decision rests on
```

Replace `your-decision` with `approve` or `request-changes`.

A decision that asks for changes needs a follow-up the team can plan, so write
the user story for the outstanding work as one line in `work/next-story.md`,
in the exact story shape with a role, a want and a reason:

```text
As ..., I want ..., so that ...
```

The want is whatever your claim check found outstanding - name the missing
work itself, not "fix the proposal" - and the reason is what that work
protects.

## 5. Make the help request safe to send

Read `drafts/help-request.md` - the prompt your teammate is about to send to
the assistant. It contains four kinds of material. Sort them before anything
reaches a prompt, using the three categories from the rules of use:

- **share**: project material that helps and exposes nothing personal and
  nothing secret;
- **redact**: useful content with a personal or identifying part - keep what
  helps, drop who it points at;
- **never**: secrets such as live credentials - a credential has no redacted
  form worth sending, and a leaked one is revoke-and-rotate territory.

The draft holds four items: the failing log line, the config facts, the
reporter's email address and the deploy token. Decide one verdict per item and
record it in `work/sharing-plan.md`, replacing each `your-verdict` with
`share`, `redact` or `never`:

```text
log-line=your-verdict
app-config=your-verdict
customer-email=your-verdict
deploy-token=your-verdict
workspace=your-pick
```

The `workspace` line answers a second question: how much of your machine does
the assistant get to see for this task? It must be able to help with the
status-page config, logs and helper, and it should see nothing beyond what the
task needs. Weigh the three candidates against both halves of that rule and
replace `your-pick` with `home-folder`, `project-folder` or `single-file`.

Now copy the draft and redact the copy - never the original, so reviewers can
still see what was nearly sent:

| Shell | Copy the draft |
|---|---|
| macOS, Linux, Git Bash | `cp drafts/help-request.md work/help-request-redacted.md` |
| PowerShell, cmd | `copy drafts\help-request.md work\help-request-redacted.md` |

Edit `work/help-request-redacted.md`: remove the token value and the
reporter's email address (a placeholder like `[deploy token removed]` is
fine), and keep the failing log line and the question word for word - they are
the part that helps.

## 6. Prove it

Return to the lab folder and run the checks:

```text
cd ../..
python -m unittest discover -s tests -v
```

(In Windows cmd, type `cd ..\..`.)

**Expect:** all seven checks report `ok`, then `OK` (see **Expected output** below).

## How the checks work

The test command is `python -m unittest discover -s tests -v`, run from this
lab folder. It reads your files in `work/`; it never needs the network.

| Check | What it confirms |
|---|---|
| `test_acceptance_criteria_are_testable` | three Given/When/Then criteria that pin `STATUS_PORT` and `8080`, with the vague wording gone |
| `test_claims_are_checked_against_the_diff` | each claim got exactly the verdict the diff supports |
| `test_decision_cites_the_broken_claim` | the decision is request-changes, with evidence naming the missing test |
| `test_next_story_is_well_formed` | the follow-up story has a role, a want naming the missing test, and a reason |
| `test_sharing_plan_sorts_the_material` | the four items and the workspace scope are sorted correctly |
| `test_redacted_request_keeps_what_helps` | the log line and the question survived redaction |
| `test_redacted_request_leaks_nothing` | the token value and the email are gone, and the original draft is untouched |

## Expected output

Right after setup, all seven checks fail, each with a message naming the next
action. On completion the output matches `expected/on-completion.txt`; only the
run time differs.

## Offline note

Setup and checks use only the Python standard library. The AI assistant in
this lab is a paper one: its proposal and summary are fixed files, so the lab
needs no account and no network.

## Cleanup

When you are finished, run this from the lab folder:

```text
python tests/cleanup_lab.py
```

It removes `starter/review-desk/work/` (including any file you added there)
and the Python cache in `tests/`, then restores the shipped files exactly as
they were shipped. It touches nothing outside this lab folder.

## Troubleshooting

| Symptom | What to do |
|---|---|
| `python: command not found`, or `python` opens the Microsoft Store | Go back to step 1: make `python` mean your Python 3 launcher for this terminal. |
| `The work folder is missing` | Run `python tests/setup_lab.py` from the lab folder. |
| A criterion is rejected as not testable | Keep it on one line in the exact shape `Criterion N: Given ... When ... Then ...` with a concrete result after Then. |
| `claim-2` keeps failing | Read the whole diff, not the summary. Count the files it touches; then re-read what claim 2 promises. |
| The redaction check fails on the log line | Keep the ERROR line exactly as it appears in the draft, including the timestamp. |
| You edited the original draft | Rerun `python tests/setup_lab.py` to restore it, then redact the copy in `work/`. |
| You are lost or past 20 minutes | Pause the exercise block and continue in self-study. If your lab state is broken, rerun `python tests/setup_lab.py` (it resets everything, including `work/`) and repeat the steps in order. |
