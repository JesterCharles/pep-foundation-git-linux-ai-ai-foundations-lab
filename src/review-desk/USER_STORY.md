# User story: show the expected port

> As the on-call teammate,
> I want the status line to show the port the service expects,
> so that a port mismatch is visible at a glance.

## Background

During the last incident, the health check was refused on port 8080 while the
service listened on 9091, and nobody could see either number without opening
the config. The team agreed the one-line status should name the expected port.

The team also agreed the port comes from the `STATUS_PORT` environment
variable, falling back to `8080` when it is not set, so that the helper works
out of the box on a developer machine.

## Wishes from the stand-up (too vague to test)

- "It should just show the port stuff."
- "It should work fine when nothing is configured."
- "The docs should be better."

Your first task is to turn these wishes into three testable acceptance
criteria. A testable criterion names a concrete starting state, an action and
an observable result; a vague one needs a judgement call to score.
