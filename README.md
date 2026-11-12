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
- **Offline:** no account, network, container or AI assistant.

## Your path

```text
Open project -> Set up -> Tests: 7 fail -> Steps 3-5 (write 5 files) -> Tests: 7 ok -> Stop
```

In words: open the project, set it up and see all 7 checks fail, write your files
in steps 3 to 5, then run the checks again and stop when all 7 pass.

## Quick start

1. **Open the project.** Open this lab's folder in VS Code. It is already on your
   machine, so you do not need to clone anything. Open a terminal with
   **Terminal > New Terminal**; it starts in the project folder, the one that holds
   this README.
2. **Set up, then run the starter tests:**

   ```text
   python tests/setup_lab.py
   python -m unittest discover -s tests -v
   ```

   **Expect:** `Review desk ready in starter/review-desk/.`, then all 7 checks
   `FAIL`. That is normal before you start: each failure message names what is
   missing. Now move into the review desk: `cd starter/review-desk`. You read the
   shipped files there and leave them unchanged; everything you write goes into its
   `work/` folder.
3. **Write testable acceptance criteria** for the story's three wishes in
   `work/acceptance-criteria.md`. Check name: `acceptance`.
4. **Check every claim against the diff.** Record a verdict per claim, then your
   decision and its evidence, in `work/review.md`, and a follow-up user story in
   `work/next-story.md`. Check names: `claims`, `decision`, `next_story`.
5. **Make the help request safe to send.** Sort the draft's material in
   `work/sharing-plan.md`, then redact a copy of the draft in
   `work/help-request-redacted.md`. Check names: `sharing_plan`, `redacted`.
6. **Prove it:** go back to the project folder and run every check:

   ```text
   cd ../..
   python -m unittest discover -s tests -v
   ```

   **Expect:** all 7 checks report `ok`, then `OK`. You are done: stop here.

**Check one step at a time.** From `starter/review-desk`, put the step's check
name after `-k`:

```text
python -m unittest discover -s ../../tests -v -k acceptance
```

**Expect:** that check reports `ok`. If it says `FAIL`, read the message under it.

## Step-by-step guide

You can create and edit every file in VS Code. Paths are relative to
`starter/review-desk`.

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
- **Expected output:** when everything passes, the output matches
  `expected/on-completion.txt`; only the run time differs.
- **Start again:** from the project folder, `python tests/setup_lab.py` resets the
  lab. It removes `work/` and restores every shipped file.
- **Clean up when finished:** from the project folder, `python tests/cleanup_lab.py`
  removes `work/` and restores the shipped files.
- **Leave these as they are:** `tests/`, `fixtures/`, `expected/` and the shipped
  files in `starter/review-desk/`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found`, or a version older than 3.11 | Run `python3 --version`. If that shows 3.11 or newer, type `alias python=python3` once in this terminal (Windows PowerShell: `Set-Alias python py`). |
| `The work folder is missing` | From the project folder, run `python tests/setup_lab.py`. |
| A test command fails with `No such file or directory` or finds no tests | Use `-s tests` in the project folder and `-s ../../tests` in `starter/review-desk`. |
| `cp` is not recognised (Windows cmd) | Use `copy drafts\help-request.md work\help-request-redacted.md`, or copy the file in VS Code. |
| A criterion is rejected as not testable | Keep it on one line as `Criterion N: Given ... When ... Then ...`, with a concrete result after Then. |
| `claim-2` keeps failing | Read the whole diff, not the summary. Count the files it touches, then reread claim 2. |
| The redaction check fails on the log line | Keep the ERROR line exactly as in the draft, including the timestamp. |
| You edited the original draft | From the project folder, run `python tests/setup_lab.py` to restore it, then redact the copy in `work/`. |

## Optional: work on your own computer

You only need this if you were not given the project. Clone
`https://github.com/JesterCharles/pep-foundation-git-linux-ai-ai-foundations-lab`,
open the cloned folder in VS Code or another editor, and start at **Quick start**.
