# Sources: how each recording reaches the pipeline

Read this when the user points to a recording that is not a plain local file. Facts were checked on 2026-10-24; platforms change their tools often, so read the platform's help page when a path below does not match what the user sees.

Order of preference for every source: the user's own recording, then the platform's own download, then a download tool. Run the sync check (scripts/sync_check.py) on every file, whatever its origin.

## Your own recording

Record locally while you stream: OBS Studio, TikTok LIVE Studio, the local recordings of StreamYard or Riverside (one track per person when offered), the local recording of Zoom. You get the resolution you streamed and clean audio. For scale: our 1:40 vertical replay at 960x1920 weighed about 2.7 GB.

## Live replays on the platforms

| Platform | Where the replay is | How long it stays | Quality |
|---|---|---|---|
| TikTok LIVE | LIVE Center, Replays, then download | about 30 days, visible to the creator only ([TSL Agency, Oct 2026](https://tslagency.co.uk/can-you-rewatch-tiktok-lives-replays-explained-for-sellers/)) | 720p offered on our test of 2026-10-24, after a server preparation that can take more than an hour for a long live |
| YouTube Live | the archive is a regular video: YouTube Studio, Content, Live | archived automatically as a regular video for streams under 12 hours, no expiry stated ([YouTube Help](https://support.google.com/youtube/answer/6247592?hl=en)) | Studio download: MP4 at 720p or 360p ([YouTube Help](https://support.google.com/youtube/answer/56100?hl=en)) |
| Facebook Live | your Page or profile: download one by one or in bulk, or transfer to Dropbox or Google Drive | 30 days for lives since 2025-02-19 ([Meta](https://about.fb.com/news/2025/02/updating-our-facebook-live-video-storage-policy/)) | not documented |
| Instagram Live | the live archive in the app; turn on archiving before going live | sources disagree; Instagram lets you share the replay as a reel ([Instagram Help](https://help.instagram.com/562982737951475)) | not documented |
| LinkedIn Live | the recording of the streaming tool you used (StreamYard, Restream, OBS) | the replay stays as a post | no native download documented |
| Twitch | Creator Dashboard, Content, Video Producer, your past broadcast; "Store past broadcasts" must be on in Stream Settings | past broadcasts expire after 7, 14 or 60 days depending on the account ([Streamlabs](https://streamlabs.com/content-hub/post/how-to-watch-old-twitch-streams)) | the broadcast quality |
| Zoom, webinar platforms | the local recording folder, or the cloud recording download of the platform | the platform's retention settings | the recording settings |

Download replays the same week. A replay can start its audio late: on our TikTok replay, the audio started 1.71 s after the video and drifted 0.19 s over 100 minutes. The sync check finds it in seconds.

## Long YouTube videos

1. Best: the original file that was uploaded (the editor's export or the camera recording). Ask the user where it lives, often in Google Drive.
2. Your own channel: YouTube Studio, Content, the video, Options, Download. You get an MP4 at 720p or 360p ([YouTube Help](https://support.google.com/youtube/answer/56100?hl=en)).
3. All your uploads at once: Google Takeout, YouTube and YouTube Music, videos.
4. A download tool (yt-dlp): YouTube's terms allow downloads only through YouTube's own features or with prior written permission from YouTube and the rights holders. Use it only for videos the user owns or has written permission for, after the user confirms, and say that it sits outside YouTube's terms. Then:

```
python3 -m pip install --user -U yt-dlp
python3 scripts/fetch_source.py "<youtube link>" --root ~/Clips --i-own-this
```

A playlist link becomes one queue item per video. Never download someone else's video to clip it: platforms demote reposted content, and it is not yours to publish.

## Google Drive: one file or a whole folder

1. Google Drive for desktop (best, no size limit, nothing to share). The files appear as a local folder: on a Mac under `~/Library/CloudStorage/GoogleDrive-<your account>/My Drive/`, on Windows as a drive letter such as `G:\My Drive`. Ask the user for the folder path (Finder: right-click, hold Option, Copy as Pathname; Windows: Shift + right-click, Copy as path) and pass it to fetch_source.py like any local folder. In streaming mode, a file downloads when it is first read: a large video takes time the first time. Copy, never move, out of this folder.
2. A link shared as "anyone with the link" (Share, General access): fetch_source.py downloads it with gdown into `~/Clips/_inbox/`.

```
python3 -m pip install --user gdown
python3 scripts/fetch_source.py "<drive file or folder link>" --root ~/Clips
```

   A folder link downloads every file of the folder; compare the count with what the user sees in Drive. Do not change the sharing of client footage to make a download work: ask the owner.
3. Large private folders without Drive for desktop: rclone ([rclone.org/drive](https://rclone.org/drive/)). The user runs `rclone config` and signs in to Google in their browser. rclone's shared client ID is being retired during 2026, so the user creates their own Google client ID first (the rclone page explains it). Then:

```
rclone copy "drive:" ~/Clips/_inbox/<name> --drive-root-folder-id <FOLDER_ID> --include "*.{mp4,mov,mkv,webm,m4a,mp3,wav}" -P
```

   The folder ID is the last part of the folder's link. Add `--drive-shared-with-me` for a folder someone shared with the user.

A Google Drive connector in the assistant is fine to find a file, its folder and its owner. Move the video itself with Drive for desktop, gdown or rclone.

## Local files and folders

```
python3 scripts/fetch_source.py ~/Clips/_inbox ~/Movies/webinars --root ~/Clips
```

Files stay where they are. prep_source.sh copies each one into its project when the item is prepared (`MODE=link` for a symbolic link instead of a copy). Hidden files and folders starting with `_tmp` are skipped.

## The queue

`~/Clips/queue.json` holds one item per video: id, date added, kind (local, drive, youtube), source, file, size, status. Statuses used by the skill: new, prepped, transcribed, synced, planned, in_review, delivered, skipped. The agent updates the status after each step, so a routine or a new session picks up where the last one stopped.
