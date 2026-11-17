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
- **Offline:** no account, network or AI assistant.

## Your path

```text
Run Tests: 3 fail -> Tasks 1-3 (fill in the files in work/) -> Run Tests: 3 pass -> Submit
```

In words: run the tests and see all 3 fail, fill in your answer files for the three
tasks, then select **Run Tests** again and select **Submit** when all 3 pass.

## Quick start

1. Open `src/review-desk/`. Read the shipped files there and leave them unchanged.
   Everything you write goes into its `work/` folder, which already holds a starter
   file for each answer.
2. Select **Run Tests** before you change anything.

   **All 3 visible tests fail at first. That is expected: the answer files still hold
   placeholders.** Every failure message starts with its task number, such as
   `Task 2:`.
3. Work through the checklist below. After each task, select **Run Tests** again and
   read the remaining `Task N:` messages.
4. **You are finished when all 3 tests pass.** Then select **Submit**. Submitting also
   runs held-out tests you can't see.

## Checklist

- [ ] Task 1: testable acceptance criteria in `work/acceptance-criteria.md`
- [ ] Task 2: claim verdicts, decision and evidence in `work/review.md`, and a
  follow-up story in `work/next-story.md`
- [ ] Task 3: a sharing plan in `work/sharing-plan.md` and a redacted copy of the
  draft in `work/help-request-redacted.md`

A task is done when no failure message starts with its number.

## Task steps

Paths below are relative to `src/review-desk`. You can create and edit every file in
the editor.

### Task 1: Turn the story into testable acceptance criteria

Read `USER_STORY.md`. The story is fine, but the three stand-up wishes under it
cannot be checked: "It should work fine when nothing is configured" - fine according
to whom?

A testable criterion has a starting state (**Given**), an action (**When**) and an
observable result (**Then**). For example:

```text
Criterion 2: Given STATUS_PORT is not set, When status_message() is called, Then the line ends with "on port 8080".
```

Replace the three `TODO` lines in `work/acceptance-criteria.md` with one criterion per
wish, each on one line in this shape:

```text
Criterion 1: Given ... When ... Then ...
Criterion 2: Given ... When ... Then ...
Criterion 3: Given ... When ... Then ...
```

Use the facts the story already agreed (the `STATUS_PORT` variable and the `8080`
fallback), not the wish wording. You may use the example above as one of the three.

### Task 2: Check every claim against the diff

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

In `work/review.md`, replace each `your-verdict` with `supported` or `unsupported`,
`your-decision` with `approve` or `request-changes`, and `TODO` with one line naming
the diff evidence your decision rests on:

```text
claim-1=your-verdict
claim-2=your-verdict
claim-3=your-verdict
decision=your-decision
evidence=TODO
```

Approve only when every claim has diff lines behind it. Merging a promise the diff
does not keep is how the last incident started.

A request for changes needs a follow-up the team can plan. Replace the `TODO` line in
`work/next-story.md` with one line:

```text
As ..., I want ..., so that ...
```

The want names the missing work itself (not "fix the proposal"); the reason says what
that work protects.

### Task 3: Make the help request safe to send

`drafts/help-request.md` holds four items: the failing log line, the config facts,
the reporter's email address and the deploy token. Give each one a verdict:

- **share:** helps and exposes nothing personal or secret;
- **redact:** useful, but has a personal or identifying part to remove;
- **never:** a secret such as a live credential. A leaked one must be revoked and
  replaced.

Then choose how much of your machine the assistant may see. It must be able to help
with the status-page config, logs and helper, and see nothing beyond what the task
needs.

In `work/sharing-plan.md`, replace each `your-verdict` with `share`, `redact` or
`never`, and `your-pick` with `home-folder`, `project-folder` or `single-file`:

```text
log-line=your-verdict
app-config=your-verdict
customer-email=your-verdict
deploy-token=your-verdict
workspace=your-pick
```

Now copy the draft. Never edit the original; reviewers need to see what was nearly
sent. From a terminal in `src/review-desk`:

```text
cp drafts/help-request.md work/help-request-redacted.md
```

(or copy the file in the editor). In `work/help-request-redacted.md`, remove the
token value and the email address (a placeholder such as `[deploy token removed]` is
fine). Keep the failing log line and the question word for word: they are the part
that helps.

## Reference

- **What the 3 visible tests check:** your criteria's shape and the agreed facts;
  your claim verdicts, decision and follow-up story; your sharing plan and what your
  redacted copy kept and removed. They read the files in `work/` only.
- **Held-out tests**, run on Submit, also check for left-over wish wording, a single
  verdict per claim, evidence and a follow-up story that name what is missing, and
  that the original draft is unchanged.
- **Run Tests** runs `python -m pytest -q` in the project folder. To run one task's
  check only, add `-k` and the task: `python -m pytest -q -k task2`.
- **Edit only the files in `src/review-desk/work/`.** The tests in `test/` are
  restored to their original state before your work is graded, so changes to them do
  not count.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Task N: work/... does not exist yet` | Create the file in `src/review-desk/work/` with exactly that name. |
| A criterion is rejected as not testable | Keep it on one line as `Criterion N: Given ... When ... Then ...`, with a concrete result after Then. |
| `claim-2` keeps failing | Read the whole diff, not the summary. Count the files it touches, then reread claim 2. |
| The redaction check fails on the log line | Keep the ERROR line exactly as in the draft, including the timestamp. |
| `cp` is not recognised (Windows cmd) | Use `copy drafts\help-request.md work\help-request-redacted.md`, or copy the file in the editor. |
| You edited the original draft | Undo your changes to `drafts/help-request.md` (for example with `git checkout -- src/review-desk/drafts/help-request.md`), then redact the copy in `work/`. |
