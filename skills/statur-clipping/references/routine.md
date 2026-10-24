# The clipping routine

Switch it on only after one recording went through the whole chain with the user: source, transcript, plan, one clip, review, delivery. A routine that needs the user at every step adds work instead of saving it.

## What one run does

1. **Collect.** Scan the inbox folders the user granted (for example `~/Clips/_inbox` and a Google Drive for desktop folder such as `My Drive/Lives`) with `fetch_source.py --root ~/Clips`. New files become queue items. Remind the user of replays that expire within 7 days and are not downloaded yet (from the list of platforms in the context file).
2. **Prepare.** For each new item, oldest replay deadline first: `prep_source.sh`, `transcribe.py`, `sync_check.py`. Update the item's status after each step, so a stopped run resumes.
3. **Plan.** For each transcribed item, run the clip-plan method and write `TRAVAIL <code>/plan.md` (the table) and the specs of the top clips. How many: the context file says (default 3). Never more than the user can review in one sitting.
4. **Render.** `render_all.py` on those specs, then `qa_clip.py` on every master. A clip under 95% of planned words heard back, or off the loudness target, is marked "to check" with the reason.
5. **Review.** Publish one review page per recording (clip-review skill) and prepare a short message for the user: recording, number of clips, link, what to check. Leave the message as a draft or a notification; never post the clips.
6. **Log.** Append one line per item to `~/Clips/routine.log`: date, item, status, clips rendered, problems.

The run stops and reports, without guessing, when: a source cannot be read, the sync check cannot be resolved, the disk has less than 3 times the size of the source free, or a gate of the plan fails for every candidate.

## When it runs

- After each live: the user drops the recording in the inbox and the run starts on the next schedule tick.
- Weekly: Monday morning is a good default, so the clips of the week's lives wait for review at the start of the week.
- It must run on the computer that holds the footage and the tools (or on a machine with the same folders synced). A cloud-only run cannot reach files on the user's computer.

## How to switch it on

Pick what the user's assistant offers:
- **A scheduled task in the assistant** (Claude, ChatGPT and others offer them): ask "Create a scheduled task that runs the prompt below every Monday at 8:00 on this computer", paste the prompt, and check the folders it may use.
- **Claude Code in headless mode** with the system scheduler: a cron job or a launchd agent that runs, in the working folder, `claude -p "<the prompt below>"`. Allow only the tools the routine needs.

## The prompt (adapt the paths and numbers)

```
Run the clipping routine of the statur-clipping skill.
Working folder: ~/Clips. Inbox folders: ~/Clips/_inbox and <Drive for desktop folder>.
Read the company context file first (<path>). Clip length 60 seconds to 5 minutes. Top 3 clips per recording.
For each new or unfinished item of ~/Clips/queue.json: prepare, transcribe, check the sync, plan, render the
top clips, run the quality check, publish one review page per recording.
Never post, schedule, share or delete anything. Never move files out of synced folders.
End with a short report: items processed, clips rendered and their review links, clips to check and why,
replays that expire within 7 days, problems. Leave that report as a draft message for me.
```

## What stays with the user

Recording or downloading the replays, signing in, choosing among the planned clips when the plan is close, the review, the post button, and guests' consent.
