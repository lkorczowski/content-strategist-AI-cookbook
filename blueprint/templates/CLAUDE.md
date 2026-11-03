# Rules for any agent working in this repository

## Start
1. Work on the latest version: `git pull` must finish without error, otherwise clone again. No up-to-date copy available: say so in one line and write nothing.
2. Read kb/00_INDEX.md. Read only the kb files the task needs.

## While working
- Drafts only: never send, publish, schedule or delete for a human. Passwords, payments, account creation and DNS stay with humans.
- Write a durable change in the file that is the source of truth (kb/00_INDEX.md, section 1), never in a copy.
- No invented numbers. Proofs come from kb/01_BRAND.md only.
- Public skills come from the cookbook by version. Do not copy them here. A private skill names the public skill it extends.

## End
1. Work on a branch from origin/main, commit with a clear message (imperative summary, then what and why), push the branch in the same session and open a pull request. A human merges. Nobody pushes to main. Push refused: stop, say so, never force.
2. Decisions and statuses go to their source of truth (kb file or tracker), never only in a chat.
