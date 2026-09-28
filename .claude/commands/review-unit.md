---
description: Review one or more C3 units and write proposed edits to review/findings/
argument-hint: <UNIT-ID> [UNIT-ID ...]   e.g. B1  or  A0 A1 A2
---

Review these units: $ARGUMENTS

1. Run `python review/lint_units.py $ARGUMENTS` so `review/lint-report.md` is current.
   (If the lint report for the whole course is older than any unit file, run it with no arguments
   instead — the REPEAT check needs every unit.)
2. For each unit ID, find its file under `0*-*/` and launch the `unit-reviewer` agent on it.
   Launch them in parallel. Pass each agent only: the unit file path and "follow your instructions".
3. When all finish, print one table: Unit · P1 · P2 · est. % cut · verdict.
4. Tell me to open `review/findings/<ID>.md`, tick `[x] accept` on the findings I want, then run
   `/apply-review <ID>`.

Do not edit any unit file in this command.
