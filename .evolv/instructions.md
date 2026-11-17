# Review the assistant's change

The team wants the status line to show the port the service expects. A teammate
asked an AI coding assistant to make the change, and its proposal is on your desk:
the assistant's summary, the actual diff, and the teammate's next prompt, which is
one paste away from leaking a credential.

You do the human half of working with an AI assistant: write testable acceptance
criteria, check each claim against the real diff, make the review decision, and make
the help request safe to send. You write your answers into Markdown files that the
tests check. No AI model or app runs in this lab.

- **Time:** about 15 minutes. If you pass 20, pause and finish in self-study.
- **You need:** Python 3.11 or newer.
- **Offline:** no account, network or AI assistant.

## Your path

```text
Set up -> Run Tests: 7 fail -> Steps 3-5 (write 5 files) -> Run Tests: 7 pass -> Submit
```

In words: set the lab up and see all 7 checks fail, write your files in steps 3 to 5,
then select **Run Tests** again and select **Submit** when all 7 pass.

## Quick start

1. **Open a terminal** with **Terminal > New Terminal**. It starts in the project
   folder, the one that holds `src/`, `test/` and `fixtures/`.
2. **Set up the review desk, then run the tests:**

   ```text
   python test/setup_lab.py
   ```

   **Expect:** `Review desk ready in src/review-desk/.` Now select **Run Tests**.
   **All 7 checks fail at first. That is expected:** each failure message names what
   is missing. Then move into the review desk: `cd src/review-desk`. You read the
   shipped files there and leave them unchanged; everything you write goes into its
   `work/` folder, which is what you submit.
3. **Write testable acceptance criteria** for the story's three wishes in
   `work/acceptance-criteria.md`. Check name: `acceptance`.
4. **Check every claim against the diff.** Record a verdict per claim, then your
   decision and its evidence, in `work/review.md`, and a follow-up user story in
   `work/next-story.md`. Check names: `claims`, `decision`, `next_story`.
5. **Make the help request safe to send.** Sort the draft's material in
   `work/sharing-plan.md`, then redact a copy of the draft in
   `work/help-request-redacted.md`. Check names: `sharing_plan`, `redacted`.
6. **Prove it:** select **Run Tests** again.

   **Expect:** all 7 checks pass. **You are finished when all 7 pass.** Then select
   **Submit**.

**Check one step at a time.** From `src/review-desk`, put the step's check name
after `-k`:

```text
python -m pytest -q ../../test -k acceptance
```

**Expect:** `1 passed` (the other checks show as `deselected`). If it says `failed`, read the message under it. From the
project folder, the same check is `python -m pytest -q -k acceptance`, and
`python -m pytest -q` runs all 7, exactly as **Run Tests** does.

## Step-by-step guide

You can create and edit every file in the editor. Paths are relative to
`src/review-desk`.

### Step 3: Turn the story into testable acceptance criteria

Read `USER_STORY.md`. The story is fine, but the three stand-up wishes under it
cannot be checked: "It should work fine when nothing is configured" - fine according
to whom?

A testable criterion has a starting state (**Given**), an action (**When**) and an
observable result (**Then**). For example:

```text
Criterion 2: Given STATUS_PORT is not set, When status_message() is called, Then the line ends with "on port 8080".
```

Create `work/acceptance-criteria.md` with three lines, one per wish, each on one line
in this shape:

```text
Criterion 1: Given ... When ... Then ...
Criterion 2: Given ... When ... Then ...
Criterion 3: Given ... When ... Then ...
```

Use the facts the story already agreed (the `STATUS_PORT` variable and the `8080`
fallback), not the wish wording. You may use the example above as one of the three.

### Step 4: Check every claim against the diff

`PROPOSAL.md` makes three numbered claims. Open `proposal/change.diff` and look for
the lines that back each one. A claim with no diff line behind it is
**unsupported**, however plausible it sounds.

<details>
<summary>Hint</summary>

- Claim 1 is about `STATUS_PORT` and a fallback. Which `+` lines in
  `status_message.py` do that?
- Claim 2 is about a unit test. Is there a test file anywhere in the diff?
- Claim 3 is about the README. Is there a `README.md` change, and does it describe
  the new line?

`project/status_message.py` is the code before; `proposal/status_message.py` is the
code after.

</details>

Create `work/review.md`. Replace each `your-verdict` with `supported` or
`unsupported`, and `your-decision` with `approve` or `request-changes`:

```text
claim-1=your-verdict
claim-2=your-verdict
claim-3=your-verdict
decision=your-decision
evidence=one line naming the diff evidence your decision rests on
```

Approve only when every claim has diff lines behind it. Merging a promise the diff
does not keep is how the last incident started.

A request for changes needs a follow-up the team can plan. Write one line in
`work/next-story.md`:

```text
As ..., I want ..., so that ...
```

The want names the missing work itself (not "fix the proposal"); the reason says
what that work protects.

### Step 5: Make the help request safe to send

`drafts/help-request.md` holds four items: the failing log line, the config facts,
the reporter's email address and the deploy token. Give each one a verdict:

- **share:** helps and exposes nothing personal or secret;
- **redact:** useful, but has a personal or identifying part to remove;
- **never:** a secret such as a live credential. A leaked one must be revoked and
  replaced.

Then choose how much of your machine the assistant may see. It must be able to help
with the status-page config, logs and helper, and see nothing beyond what the task
needs.

Create `work/sharing-plan.md`. Replace each `your-verdict` with `share`, `redact` or
`never`, and `your-pick` with `home-folder`, `project-folder` or `single-file`:

```text
log-line=your-verdict
app-config=your-verdict
customer-email=your-verdict
deploy-token=your-verdict
workspace=your-pick
```

Now copy the draft. Never edit the original; reviewers need to see what was nearly
sent:

```text
cp drafts/help-request.md work/help-request-redacted.md
```

In `work/help-request-redacted.md`, remove the token value and the email address (a
placeholder such as `[deploy token removed]` is fine). Keep the failing log line and
the question word for word: they are the part that helps. Now do step 6.

## Reference

- **What the 7 checks look at:** your three criteria, your claim verdicts, your
  decision and evidence, your follow-up story, your sharing plan, and what your
  redacted copy kept and removed. They also confirm the original draft is unchanged.
  They read the files in `work/` only; nothing uses the network.
- **Run Tests** runs `python -m pytest -q` in the project folder. A check that could
  not run because the lab was never set up counts as a failure.
- **Expected output:** when everything passes, the output matches
  `expected/on-completion.txt`; only the run time differs.
- **Start again:** from the project folder, `python test/setup_lab.py` resets the
  lab. It removes `work/` and restores every shipped file.
- **Clean up when finished:** from the project folder, `python test/cleanup_lab.py`
  removes `work/` and restores the shipped files.
- **Leave these as they are:** `test/`, `fixtures/`, `expected/` and the shipped
  files in `src/review-desk/`. The tests in `test/` are restored to their original
  state before your work is graded, so changes to them do not count.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found`, or a version older than 3.11 | Run `python3 --version`. If that shows 3.11 or newer, type `alias python=python3` once in this terminal (Windows PowerShell: `Set-Alias python py`). |
| `Not run: The work folder is missing` | From the project folder, run `python test/setup_lab.py`, then select **Run Tests** again. |
| A test command fails with `file or directory not found` or finds no tests | Use `python -m pytest -q` in the project folder and `python -m pytest -q ../../test` in `src/review-desk`. |
| `cp` is not recognised (Windows cmd) | Use `copy drafts\help-request.md work\help-request-redacted.md`, or copy the file in the editor. |
| A criterion is rejected as not testable | Keep it on one line as `Criterion N: Given ... When ... Then ...`, with a concrete result after Then. |
| `claim-2` keeps failing | Read the whole diff, not the summary. Count the files it touches, then reread claim 2. |
| The redaction check fails on the log line | Keep the ERROR line exactly as in the draft, including the timestamp. |
| You edited the original draft | From the project folder, run `python test/setup_lab.py` to restore it, then redact the copy in `work/`. |
| Project files are missing, or setup cannot find them | Ask your trainer to repair the supplied project. Everything the lab needs is in this folder; do not download it from anywhere else. |
