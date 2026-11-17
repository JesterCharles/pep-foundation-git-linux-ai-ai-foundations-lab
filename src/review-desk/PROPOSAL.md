# Assistant proposal: show the expected port

An AI coding assistant produced the change in `proposal/` for the user story.
Its summary makes three claims. Check every claim against `proposal/change.diff`
before you believe any of them.

## Summary written by the assistant

I implemented the port display end to end:

1. `status_message()` now includes the expected port, read from the
   `STATUS_PORT` environment variable with an `8080` fallback.
2. I added a unit test that covers the `8080` fallback when `STATUS_PORT`
   is not set.
3. I updated the README so the new status line format is documented.

The change is small, backwards-compatible and ready to merge.
