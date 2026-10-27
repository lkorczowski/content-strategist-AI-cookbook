#!/usr/bin/env python3
"""statur-social-analytics: your own short-form analytics base, in plain files your AI can query.

CSV files are the source of truth. analytics.db (SQLite) is rebuilt from them at every `build`.
Standard library only (Python 3.9+).

  python3 analytics.py init  <dir>                      create the folder layout and blank templates
  python3 analytics.py build <dir>                      rebuild analytics.db and TOTALS.md from the CSV files
  python3 analytics.py sql   <dir> "SELECT ..."         run any read-only SQL, print a tab-separated table
  python3 analytics.py dice  <dir> [--account KEY] [--min-days 7] [--min-views 1000]
                                                        per-format distribution on mature videos (the dice)
  python3 analytics.py winners <dir> [--account KEY] [--n 10]
                                                        mature videos ranked against their own format's median
  python3 analytics.py export-log <dir> [--account KEY] [--out FILE]
                                                        video log in the shape statur-video-post-mortem and
                                                        statur-content-learning read

Folder layout (see references/schema.md):
  accounts.csv                     one row per account you track or watch (the only file you edit by hand)
  formats.csv                      video_id -> format, hook_type (filled with the format review)
  raw/YYYY-MM-DD_<platform>_<handle>_<kind>.csv   one file per collection, never edited afterwards
       kind = videos | daily | retention | audience | posts
  proof/<platform>_<handle>/<video_id>_<tab>_<YYYY-MM-DD>.png    analytics screenshots
"""
import csv
import os
import re
import sqlite3
import statistics
import sys
from datetime import date

KINDS = {
    'videos': ['video_id', 'posted', 'length_s', 'views', 'likes', 'comments', 'shares', 'saves', 'new_followers',
               'avg_watch_s', 'ret_3s_pct', 'ret_10s_pct', 'ret_end_pct', 'views_d7', 'caption', 'url'],
    'daily': ['date', 'views', 'profile_views', 'likes', 'comments', 'shares', 'followers', 'reached'],
    'retention': ['video_id', 'second', 'pct_remaining'],
    'audience': ['video_id', 'dimension', 'label', 'pct'],
    'posts': ['post_id', 'posted', 'type', 'in_reply_to', 'views', 'replies', 'likes', 'reposts', 'quotes', 'bookmarks',
              'shares', 'profile_visits', 'link_clicks', 'new_follows', 'text', 'url'],
}
ACCOUNTS = ['key', 'owner', 'platform', 'handle', 'relation', 'access', 'route', 'window_start', 'window_end',
            'attribution', 'publish', 'notes']
FORMATS = ['video_id', 'format', 'hook_type', 'notes']
POST_LABELS = ['post_id', 'pillar', 'voice_mode', 'intent', 'formula', 'notes']
NUM = {'length_s', 'views', 'likes', 'comments', 'shares', 'saves', 'new_followers', 'avg_watch_s', 'ret_3s_pct',
       'ret_10s_pct', 'ret_end_pct', 'views_d7', 'profile_views', 'followers', 'reached', 'second', 'pct_remaining', 'pct',
       'replies', 'reposts', 'quotes', 'bookmarks', 'profile_visits', 'link_clicks', 'new_follows'}
RAW_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})_([a-z]+)_(.+)_(videos|daily|retention|audience|posts)\.csv$')


def num(x):
    """'12,400' -> 12400, '1.2M' -> 1200000, '318k' -> 318000, '' -> None."""
    if x is None:
        return None
    s = str(x).strip().replace('\u202f', '').replace('\xa0', '').replace(' ', '')
    m = re.match(r'^(-?[\d.,]+)([kKmM]?)$', s)
    if not m:
        return None
    v, suffix = m.groups()
    v = v.replace(',', '.') if suffix and v.count(',') == 1 and '.' not in v else v.replace(',', '')
    try:
        f = float(v) * {'k': 1e3, 'K': 1e3, 'm': 1e6, 'M': 1e6}.get(suffix, 1)
    except ValueError:
        return None
    return int(f) if f.is_integer() else f


def write_csv(path, cols, rows=()):
    if os.path.exists(path):
        return
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow(r)


def init(d):
    for sub in ('raw', 'proof'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    write_csv(os.path.join(d, 'accounts.csv'), ACCOUNTS, [
        ['me-tiktok', 'Me', 'tiktok', 'myhandle', 'own', 'owner', 'studio', '', '', 'full', 'named', 'example row: replace'],
        ['watch-1', 'A creator I study', 'tiktok', 'somecreator', 'watch', 'none', 'public', '', '', 'none', 'none', 'watchlist: never counted in my totals'],
    ])
    write_csv(os.path.join(d, 'formats.csv'), FORMATS)
    write_csv(os.path.join(d, 'post_labels.csv'), POST_LABELS)
    print(f'initialized {d}: accounts.csv, formats.csv, post_labels.csv, raw/, proof/')


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def build(d, quiet=False):
    db_path = os.path.join(d, 'analytics.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    con = sqlite3.connect(db_path)
    c = con.cursor()
    c.execute(f'CREATE TABLE accounts ({", ".join(a + " TEXT" for a in ACCOUNTS)})')
    acc = read_csv(os.path.join(d, 'accounts.csv')) if os.path.exists(os.path.join(d, 'accounts.csv')) else []
    c.executemany(f'INSERT INTO accounts VALUES ({",".join("?" * len(ACCOUNTS))})', [[r.get(k, '') for k in ACCOUNTS] for r in acc])
    by_handle = {(r.get('platform', ''), r.get('handle', '').lstrip('@').lower()): r['key'] for r in acc}
    for kind, cols in KINDS.items():
        defs = ', '.join(f'{col} {"REAL" if col in NUM else "TEXT"}' for col in cols)
        c.execute(f'CREATE TABLE raw_{kind} (account TEXT, platform TEXT, read_date TEXT, file TEXT, {defs})')
    skipped = []
    for name in sorted(os.listdir(os.path.join(d, 'raw'))) if os.path.isdir(os.path.join(d, 'raw')) else []:
        m = RAW_RE.match(name)
        if not m:
            if name.endswith('.csv'):
                skipped.append(name)
            continue
        read_date, platform, handle, kind = m.groups()
        key = by_handle.get((platform, handle.lower()), f'{platform}:{handle}')
        cols = KINDS[kind]
        rows = []
        for r in read_csv(os.path.join(d, 'raw', name)):
            vals = [num(r.get(col)) if col in NUM else (r.get(col) or '').strip() for col in cols]
            rows.append([key, platform, read_date, name] + vals)
        c.executemany(f'INSERT INTO raw_{kind} VALUES ({",".join("?" * (len(cols) + 4))})', rows)
    c.execute(f'CREATE TABLE formats ({", ".join(f + " TEXT" for f in FORMATS)})')
    fpath = os.path.join(d, 'formats.csv')
    if os.path.exists(fpath):
        c.executemany(f'INSERT INTO formats VALUES ({",".join("?" * len(FORMATS))})', [[r.get(k, '') for k in FORMATS] for r in read_csv(fpath)])
    c.execute(f'CREATE TABLE post_labels ({", ".join(f + " TEXT" for f in POST_LABELS)})')
    lpath = os.path.join(d, 'post_labels.csv')
    if os.path.exists(lpath):
        c.executemany(f'INSERT INTO post_labels VALUES ({",".join("?" * len(POST_LABELS))})', [[r.get(k, '') for k in POST_LABELS] for r in read_csv(lpath)])
    # latest reading of each video, of each day, of each retention curve
    c.executescript('''
    CREATE VIEW videos AS
      SELECT v.*, CAST(julianday(v.read_date) - julianday(v.posted) AS INTEGER) AS days_live
      FROM raw_videos v
      WHERE v.read_date = (SELECT MAX(read_date) FROM raw_videos x WHERE x.account = v.account AND x.video_id = v.video_id);
    CREATE VIEW daily AS
      SELECT d.* FROM raw_daily d
      WHERE d.read_date = (SELECT MAX(read_date) FROM raw_daily x WHERE x.account = d.account AND x.date = d.date);
    CREATE VIEW retention AS
      SELECT r.* FROM raw_retention r
      WHERE r.read_date = (SELECT MAX(read_date) FROM raw_retention x WHERE x.account = r.account AND x.video_id = r.video_id);
    CREATE VIEW audience AS
      SELECT a.* FROM raw_audience a
      WHERE a.read_date = (SELECT MAX(read_date) FROM raw_audience x WHERE x.account = a.account AND x.video_id = a.video_id);
    CREATE VIEW video_log AS
      SELECT v.video_id, v.platform, v.posted AS publish_date, v.read_date, v.days_live, 'main_feed' AS distribution,
             f.format, f.hook_type, v.length_s, v.views, v.likes, v.comments, v.saves, v.shares, v.new_followers,
             v.avg_watch_s, v.ret_3s_pct, v.ret_10s_pct, v.ret_end_pct, '' AS transcript_file, v.caption AS notes, v.account
      FROM videos v LEFT JOIN formats f ON f.video_id = v.video_id;
    CREATE VIEW posts AS
      SELECT p.*, CAST(julianday(p.read_date) - julianday(p.posted) AS INTEGER) AS days_live
      FROM raw_posts p
      WHERE p.read_date = (SELECT MAX(read_date) FROM raw_posts x WHERE x.account = p.account AND x.post_id = p.post_id);
    CREATE VIEW post_log AS
      SELECT p.account, p.platform, p.post_id, p.posted, p.read_date, p.days_live, p.type, p.in_reply_to,
             l.pillar, l.voice_mode, l.intent, l.formula, p.views, p.replies, p.likes, p.reposts, p.quotes, p.bookmarks,
             p.shares, p.profile_visits, p.link_clicks, p.new_follows, p.url
      FROM posts p LEFT JOIN post_labels l ON l.post_id = p.post_id;
    ''')
    con.commit()
    totals(con, d)
    n = c.execute('SELECT COUNT(*) FROM videos').fetchone()[0]
    npost = c.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    con.close()
    if not quiet:
        print(f'built {db_path}: {n} videos, {npost} posts' + (f'; skipped files with an unknown name: {", ".join(skipped)}' if skipped else ''))


def totals(con, d):
    c = con.cursor()
    rows = c.execute('''
      SELECT a.key, a.owner, a.platform, a.handle, a.relation, a.attribution, a.window_start, a.window_end,
             COUNT(v.video_id), SUM(v.views),
             SUM(CASE WHEN v.posted >= COALESCE(NULLIF(a.window_start, ''), '0000') AND v.posted <= COALESCE(NULLIF(a.window_end, ''), '9999') THEN v.views END),
             MAX(v.read_date)
      FROM accounts a LEFT JOIN videos v ON v.account = a.key GROUP BY a.key ORDER BY SUM(v.views) DESC''').fetchall()
    counted = pending = 0
    lines = []
    for key, owner, plat, handle, rel, att, ws, we, n, lt, win, read in rows:
        cnt = (lt if att == 'full' else win if att == 'window' else 0) or 0
        if rel != 'watch':
            counted += cnt
            pending += (win or lt or 0) if att == 'tbd' else 0
        lines.append(f'| {owner} | {plat} | {handle} | {rel} | {n or 0} | {fmt(lt)} | {ws} to {we or "today"} | {fmt(win)} | {att} | {fmt(cnt)} | {read or ""} |')
    out = ['# Totals (generated by analytics.py build, do not edit)', '',
           f'- Views counted: {fmt(counted)}', f'- Views waiting for a window decision (attribution tbd): {fmt(pending)}',
           '- Watchlist accounts are listed for comparison and never counted.', '',
           '| Owner | Platform | Handle | Relation | Videos | Views | Window | Views in window | Attribution | Counted | Read |',
           '|---|---|---|---|---|---|---|---|---|---|---|', *lines, '',
           'A video counts when it was published inside the window of accounts.csv. Rounded public counts stay rounded.']
    with open(os.path.join(d, 'TOTALS.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')


def fmt(x):
    return '' if x in (None, '') else f'{int(x):,}'


def connect(d):
    p = os.path.join(d, 'analytics.db')
    if not os.path.exists(p):
        build(d, quiet=True)
    con = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
    return con


def cellfmt(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f'{v:.4g}' if abs(v) < 1000 else f'{v:.1f}'
    return str(v)


def show(cur):
    cols = [x[0] for x in cur.description]
    print('\t'.join(cols))
    for r in cur.fetchall():
        print('\t'.join(cellfmt(v) for v in r))


def opt(args, name, default=None, cast=str):
    if name in args:
        i = args.index(name)
        return cast(args[i + 1])
    return default


def mature(con, account, min_days, min_views):
    q = 'SELECT v.*, f.format FROM videos v LEFT JOIN formats f ON f.video_id = v.video_id WHERE days_live >= ? AND views >= ?'
    p = [min_days, min_views]
    if account:
        q += ' AND v.account = ?'
        p.append(account)
    cur = con.execute(q, p)
    cols = [x[0] for x in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def pct(vals, q):
    vals = sorted(vals)
    if not vals:
        return None
    k = (len(vals) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
    return vals[lo] + (vals[hi] - vals[lo]) * (k - lo)


def dice(con, args):
    rows = mature(con, opt(args, '--account'), opt(args, '--min-days', 7, int), opt(args, '--min-views', 1000, int))
    groups = {}
    for r in rows:
        groups.setdefault(r['format'] or '(untagged)', []).append(r)
    print('format\tn\tfloor\tp25\tmedian\tp75\ttop\tsaves_per_1k\tshares_per_1k\tret_3s_median')
    for fmt_name, g in sorted(groups.items(), key=lambda kv: -statistics.median([x['views'] for x in kv[1]])):
        v = [x['views'] for x in g]
        sv = [1000 * x['saves'] / x['views'] for x in g if x['saves'] is not None and x['views']]
        sh = [1000 * x['shares'] / x['views'] for x in g if x['shares'] is not None and x['views']]
        r3 = [x['ret_3s_pct'] for x in g if x['ret_3s_pct'] is not None]
        md = lambda a: f'{statistics.median(a):.1f}' if a else ''
        print(f'{fmt_name}\t{len(g)}\t{min(v):.0f}\t{pct(v, .25):.0f}\t{statistics.median(v):.0f}\t{pct(v, .75):.0f}\t{max(v):.0f}\t{md(sv)}\t{md(sh)}\t{md(r3)}')
    print(f'# {len(rows)} mature videos (at least {opt(args, "--min-days", 7, int)} days live and {opt(args, "--min-views", 1000, int)} views). Untagged videos need a line in formats.csv.')


def winners(con, args):
    rows = mature(con, opt(args, '--account'), opt(args, '--min-days', 7, int), opt(args, '--min-views', 1000, int))
    n = opt(args, '--n', 10, int)
    med = {}
    for r in rows:
        med.setdefault(r['format'] or '(untagged)', []).append(r['views'])
    med = {k: statistics.median(v) for k, v in med.items()}
    for r in rows:
        r['x_format_median'] = r['views'] / med[r['format'] or '(untagged)'] if med[r['format'] or '(untagged)'] else 0
    rows.sort(key=lambda r: -r['x_format_median'])
    print('rank\tvideo_id\taccount\tformat\tposted\tviews\tx_format_median\tcaption')
    for label, part in (('top', rows[:n]), ('bottom', rows[-n:][::-1] if len(rows) > n else [])):
        for i, r in enumerate(part, 1):
            print(f'{label}{i}\t{r["video_id"]}\t{r["account"]}\t{r["format"] or ""}\t{r["posted"]}\t{r["views"]:.0f}\t{r["x_format_median"]:.2f}\t{(r["caption"] or "")[:60]}')


def export_log(con, d, args):
    q = 'SELECT * FROM video_log'
    p = []
    if opt(args, '--account'):
        q += ' WHERE account = ?'
        p.append(opt(args, '--account'))
    cur = con.execute(q + ' ORDER BY publish_date DESC', p)
    cols = [x[0] for x in cur.description if x[0] != 'account']
    out = opt(args, '--out', os.path.join(d, 'video-log.csv'))
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in cur.fetchall():
            w.writerow([cellfmt(v) for v in r[:len(cols)]])
    print(f'wrote {out}')


def main(argv):
    if len(argv) < 3 or argv[1] not in ('init', 'build', 'sql', 'dice', 'winners', 'export-log'):
        print(__doc__)
        return 1
    cmd, d, rest = argv[1], argv[2], argv[3:]
    if cmd == 'init':
        init(d)
    elif cmd == 'build':
        build(d)
    elif cmd == 'sql':
        if not rest:
            print('give a SQL query')
            return 1
        show(connect(d).execute(rest[0]))
    elif cmd == 'dice':
        dice(connect(d), rest)
    elif cmd == 'winners':
        winners(connect(d), rest)
    elif cmd == 'export-log':
        export_log(connect(d), d, rest)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
