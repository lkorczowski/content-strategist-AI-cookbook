#!/usr/bin/env python3
"""Rename public skills to the statur- prefix (v2.0.0, 2026-10-26).

Usage: python3 scripts/rename_skills.py [--repo PATH] [--stubs] [--dry-run] [paths to rewrite...]
- In the cookbook (default): git mv skills/<old> skills/<new>, set name and version in SKILL.md,
  rewrite every reference in text files (CHANGELOG.md history is kept), and with --stubs leave a
  README-only folder at each old path that points to the new name.
- In another repo (statur.co, a private instance): pass --repo and the folders to rewrite; only text is changed.
Safe to run twice: a name already prefixed is never matched again.
"""
import argparse, re, subprocess, sys
from pathlib import Path

MAP = {
    'video-post-mortem': 'statur-video-post-mortem',
    'format-dice-review': 'statur-format-review',
    'content-learning-session': 'statur-content-learning',
    'video-story-analysis': 'statur-story-analysis',
    'story-replication': 'statur-story-replication',
    'short-video-author-analysis': 'statur-author-analysis',
    'short-story-replication': 'statur-short-story-replication',
    'clip-plan': 'statur-clip-plan',
    'clip-edit': 'statur-clip-edit',
    'clip-review': 'statur-clip-review',
    'creative-led-growth-coach': 'statur-creative-led-growth',
    'performance-creator-program': 'statur-creator-program',
    'organic-to-paid': 'statur-organic-to-paid',
    'format-library-coach': 'statur-format-library',
    'comment-section-coach': 'statur-comment-section',
    'x-launch-week': 'statur-x-launch',
    'trades-video-coach': 'statur-trades-video',
    'trades-ai-setup': 'statur-trades-setup',
    'trades-morning-routine': 'statur-trades-morning-routine',
    'trades-admin-process': 'statur-trades-admin',
    'content-os-setup': 'statur-content-os-setup',
    'meta-ads-scaling-coach': 'statur-meta-ads-scaling',
    # skills still on unmerged branches
    'account-network-coach': 'statur-account-networks',
    'slideshow-maker': 'statur-slideshow-maker',
}
TEXT = {'.md', '.py', '.json', '.ts', '.js', '.mjs', '.astro', '.txt', '.csv', '.yml', '.yaml', '.html', '.sh', '.toml'}
PAT = re.compile(r'(?<![A-Za-z0-9_-])(' + '|'.join(sorted(map(re.escape, MAP), key=len, reverse=True)) + r')(?![A-Za-z0-9_-])')
SKIP_DIRS = {'.git', 'node_modules', 'dist', 'archive', '.astro'}

def rewrite(root: Path, keep=('CHANGELOG.md',), dry=False):
    changed = []
    for f in root.rglob('*'):
        if not f.is_file() or f.suffix not in TEXT or any(p in SKIP_DIRS for p in f.parts) or f.name in keep:
            continue
        if f.name == 'rename_skills.py':
            continue
        try:
            s = f.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        n = PAT.sub(lambda m: MAP[m.group(1)], s)
        if n != s:
            changed.append(str(f))
            if not dry:
                f.write_text(n, encoding='utf-8')
    return changed

STUB = """# {old} is now {new}

This skill was renamed on 2026-10-26, when every public skill took the statur- prefix (cookbook v2.0.0).

- New location: [skills/{new}](../{new}/)
- Install: `npx skills add lkorczowski/content-strategist-AI-cookbook --skill {new}`

This folder only keeps old links working. It holds no skill and will be removed after 2027-01-31.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--stubs', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('paths', nargs='*')
    a = ap.parse_args()
    root = Path(a.repo)
    cookbook = (root / 'skills').is_dir() and (root / 'scripts' / 'check_skills.py').exists()
    if cookbook:
        for old, new in MAP.items():
            src, dst = root / 'skills' / old, root / 'skills' / new
            if (src / 'SKILL.md').exists() and not dst.exists():
                print(f'mv skills/{old} -> skills/{new}')
                if not a.dry_run:
                    subprocess.run(['git', '-C', str(root), 'mv', f'skills/{old}', f'skills/{new}'], check=True)
                    md = dst / 'SKILL.md'
                    s = md.read_text(encoding='utf-8')
                    s = re.sub(r'(?m)^name:\s*\S+\s*$', f'name: {new}', s, count=1)
                    s = re.sub(r'(?m)^(\s+version:\s*)"?[0-9.]+"?\s*$', r'\g<1>"2.0.0"', s, count=1)
                    md.write_text(s, encoding='utf-8')
    targets = [root / p for p in a.paths] if a.paths else [root]
    total = []
    for t in targets:
        total += rewrite(t, dry=a.dry_run)
    print(f'rewritten files: {len(total)}')
    for f in total:
        print('  ' + f)
    if cookbook and a.stubs and not a.dry_run:
        for old, new in MAP.items():
            if (root / 'skills' / new / 'SKILL.md').exists():
                d = root / 'skills' / old
                d.mkdir(exist_ok=True)
                (d / 'README.md').write_text(STUB.format(old=old, new=new), encoding='utf-8')
        print('stubs written')

if __name__ == '__main__':
    sys.exit(main())
