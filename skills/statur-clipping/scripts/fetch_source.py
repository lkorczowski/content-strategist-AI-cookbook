#!/usr/bin/env python3
"""Bring a source into the clipping queue: a local file or folder, a Google Drive file or folder link,
or a YouTube video or playlist link. Every source becomes one or more items of ROOT/queue.json.

Usage:
  fetch_source.py SOURCE [SOURCE ...] --root ~/Clips [--i-own-this] [--dry-run]

SOURCE can be:
  - a local video or audio file, or a folder (scanned recursively, hidden files skipped)
  - a Google Drive file or folder link (shared as "anyone with the link"): downloaded with gdown
    into ROOT/_inbox/. For private files, use the Google Drive for desktop folder path instead.
  - a YouTube video, live or playlist link: only with --i-own-this, after the user confirms the video is
    theirs or that they have written permission. Without the flag the script prints the official options
    (the original file, YouTube Studio download, Google Takeout) and exits with code 2.
  - any other link (TikTok, Instagram, Facebook, LinkedIn, Twitch, Zoom): the script prints how to get
    the file with the platform's own download and exits with code 2.

Local files are registered where they are (never moved). Downloads land in ROOT/_inbox/.
Prints one JSON line: {"status": "QUEUED" | "NEEDS_FILE" | "ERROR", "items": [...], "help": [...]}
Standard library only; gdown and yt-dlp are optional command-line tools.
"""
import argparse, datetime, glob, json, os, re, shutil, subprocess, sys

MEDIA = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".ts", ".mts", ".m2ts", ".avi", ".flv",
         ".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg", ".opus"}

YT = re.compile(r"^https?://(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", re.I)
DRIVE_FOLDER = re.compile(r"drive\.google\.com/drive/(?:u/\d+/)?folders/([A-Za-z0-9_-]+)", re.I)
DRIVE_FILE = re.compile(r"drive\.google\.com/(?:file/d/([A-Za-z0-9_-]+)|(?:open|uc)\?(?:.*&)?id=([A-Za-z0-9_-]+))", re.I)

HELP_YOUTUBE = [
    "Best: the original file you uploaded (your editor's export or your recording).",
    "Your own channel: YouTube Studio > Content > the video > Options > Download (MP4 at 720p or 360p).",
    "All your uploads at once: Google Takeout, YouTube and YouTube Music, videos.",
    "A third-party downloader (yt-dlp) falls outside YouTube's terms, which allow downloads only through "
    "YouTube's own features or with written permission. Use it only for videos you own or have written "
    "permission for: confirm with the user, then run again with --i-own-this.",
]
HELP_DRIVE_PRIVATE = [
    "Google Drive for desktop: give the local path of the file or folder (Finder: right-click, hold Option, "
    "Copy as Pathname; Windows: Shift + right-click, Copy as path). No size limit, nothing to share.",
    "Or a link shared as 'anyone with the link' (Share > General access). Do not change the sharing of "
    "client footage just to make a download work: ask the owner first.",
    "Or rclone with your own Google client ID (rclone.org/drive) for large private folders.",
]
HELP_PLATFORM = [
    "Download the replay with the platform's own tool, then give the file path:",
    "TikTok: LIVE Center > Replays > download (replays stay about 30 days).",
    "Facebook: download the live from your Page or profile before day 30.",
    "Instagram: the live archive in the Instagram app (turn on 'Save live to archive' before going live).",
    "Twitch: Creator Dashboard > Content > Video Producer > your past broadcast > Download (past broadcasts expire after 7 to 60 days depending on the account).",
    "LinkedIn Live, Zoom, StreamYard, Riverside: the recording of the streaming tool you used.",
]


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def load_queue(root):
    p = os.path.join(root, "queue.json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {"items": []}


def save_queue(root, q):
    p = os.path.join(root, "queue.json")
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(q, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def media_files(folder):
    out = []
    for dp, dn, fn in os.walk(folder):
        dn[:] = sorted(d for d in dn if not d.startswith((".", "_tmp")))
        for n in sorted(fn):
            if not n.startswith(".") and os.path.splitext(n)[1].lower() in MEDIA:
                out.append(os.path.join(dp, n))
    return out


def add(q, file, source, kind):
    file = os.path.abspath(file)
    for it in q["items"]:
        if it["file"] == file:
            return it, False
    it = {"id": f"Q{len(q['items']) + 1:03d}", "added": now(), "kind": kind, "source": source,
          "file": file, "size_mb": round(os.path.getsize(file) / 1e6, 1), "status": "new"}
    q["items"].append(it)
    return it, True


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def have_gdown():
    return run([sys.executable, "-m", "gdown", "--version"])[0] == 0


def fetch_drive(url, inbox, folder):
    if not have_gdown():
        return None, ["gdown is not installed: python3 -m pip install --user gdown"] + HELP_DRIVE_PRIVATE
    before = set(media_files(inbox))
    target = inbox + os.sep
    if folder:
        m = DRIVE_FOLDER.search(url)
        target = os.path.join(inbox, f"drive_{m.group(1)[:12]}") + os.sep
        cmd = [sys.executable, "-m", "gdown", "--folder", "--continue", url, "-O", target]
    else:
        cmd = [sys.executable, "-m", "gdown", "--continue", url, "-O", target]
    code, out, err = run(cmd)
    got = sorted(set(media_files(inbox)) - before)
    if code != 0 or not got:
        tail = (err or out).strip().splitlines()[-3:]
        return None, ["gdown could not download it (private file, quota or not a video): " + " | ".join(tail)] + HELP_DRIVE_PRIVATE
    return got, []


def fetch_youtube(url, inbox):
    if not shutil.which("yt-dlp"):
        return None, ["yt-dlp is not installed: python3 -m pip install --user yt-dlp (it also needs ffmpeg)."]
    tpl = os.path.join(inbox, "%(upload_date)s %(title).80B [%(id)s].%(ext)s")
    cmd = ["yt-dlp", "--no-progress", "-f", "bv*+ba/b", "--merge-output-format", "mp4", "--yes-playlist",
           "-o", tpl, "--print", "after_move:filepath", url]
    code, out, err = run(cmd)
    got = [ln.strip() for ln in out.splitlines() if ln.strip() and os.path.exists(ln.strip())]
    if code != 0 and not got:
        return None, ["yt-dlp failed: " + " | ".join(err.strip().splitlines()[-3:])]
    return got, []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--root", required=True, help="working folder that holds _inbox/, queue.json and the projects")
    ap.add_argument("--i-own-this", action="store_true",
                    help="the user confirmed they own the YouTube video(s) or have written permission")
    ap.add_argument("--dry-run", action="store_true", help="classify the sources, download nothing")
    a = ap.parse_args()
    root = os.path.abspath(os.path.expanduser(a.root))
    inbox = os.path.join(root, "_inbox")
    os.makedirs(inbox, exist_ok=True)
    q = load_queue(root)
    items, helps, status = [], [], "QUEUED"

    for src in a.sources:
        s = os.path.expanduser(src)
        if os.path.isfile(s):
            kind, files = "local", ([s] if os.path.splitext(s)[1].lower() in MEDIA else [])
            if not files:
                helps.append(f"Not a video or audio file: {src}")
        elif os.path.isdir(s):
            kind, files = "local", media_files(s)
            if not files:
                helps.append(f"No video or audio file found in {src}")
        elif DRIVE_FOLDER.search(s) or DRIVE_FILE.search(s):
            kind = "drive"
            if a.dry_run:
                items.append({"source": src, "kind": kind, "status": "would download with gdown"}); continue
            files, h = fetch_drive(s, inbox, folder=bool(DRIVE_FOLDER.search(s)))
            helps += h
        elif YT.search(s):
            kind = "youtube"
            if not a.i_own_this:
                status = "NEEDS_FILE"; helps += HELP_YOUTUBE; continue
            if a.dry_run:
                items.append({"source": src, "kind": kind, "status": "would download with yt-dlp"}); continue
            files, h = fetch_youtube(s, inbox)
            helps += h
        elif re.match(r"^https?://", s, re.I):
            status = "NEEDS_FILE"; helps += HELP_PLATFORM; continue
        else:
            helps.append(f"Not found: {src}"); continue
        if not files:
            status = "NEEDS_FILE" if status == "QUEUED" else status
            continue
        for f in files:
            if a.dry_run:
                items.append({"source": src, "kind": kind, "file": os.path.abspath(f), "status": "would queue"})
                continue
            it, new = add(q, f, src, kind)
            items.append(dict(it, new=new))

    if not a.dry_run:
        save_queue(root, q)
    if not items and status == "QUEUED":
        status = "ERROR"
    # de-duplicate the help lines, keep their order
    seen, uniq = set(), []
    for h in helps:
        if h not in seen:
            seen.add(h); uniq.append(h)
    print(json.dumps({"status": status, "root": root, "items": items, "help": uniq}, ensure_ascii=False, indent=1))
    sys.exit(0 if status == "QUEUED" else 2)


if __name__ == "__main__":
    main()
