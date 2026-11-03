#!/usr/bin/env python3
"""Capture web pages as crisp images for B-roll: a full page, the first screen, an element, or a strip
of screens for a scroll animation. Every capture is logged in assets.csv with its source and rights note,
so the edit can prove where each image comes from.

Usage:
  capture.py URL OUT.png [--width 1280] [--height 1600] [--scale 2] [--full] [--selector CSS]
             [--hide CSS ...] [--dark] [--wait 1500] [--owner own|third-party] [--note "..."]
             [--log assets.csv] [--claim "transcript sentence this image proves"]

Prefer your own pages (site, repo, docs, posts). A third-party page needs a reason in --note
(commentary, news, quote) and stays a decision for the human reviewer (statur-video-editor-pro flags it).
"""
import argparse, csv, datetime, json, os, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1280); ap.add_argument("--height", type=int, default=1600)
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--full", action="store_true", help="whole page height")
    ap.add_argument("--selector", default=None, help="capture only this element")
    ap.add_argument("--hide", nargs="*", default=[], help="CSS selectors to hide (cookie banners, chat widgets)")
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--wait", type=int, default=1500, help="ms to wait after load")
    ap.add_argument("--owner", choices=["own", "third-party"], default="own")
    ap.add_argument("--note", default="")
    ap.add_argument("--claim", default="", help="the spoken claim this capture supports")
    ap.add_argument("--log", default=None, help="assets.csv to append to (default: next to OUT)")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale,
                            color_scheme="dark" if a.dark else "light", locale="en-US")
        pg = ctx.new_page()
        pg.goto(a.url, wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(a.wait)
        for sel in a.hide:
            pg.add_style_tag(content=f"{sel}{{display:none !important}}")
        if a.selector:
            pg.locator(a.selector).first.screenshot(path=a.out)
        else:
            pg.screenshot(path=a.out, full_page=a.full)
        title = pg.title()
        b.close()
    log = a.log or os.path.join(os.path.dirname(os.path.abspath(a.out)), "assets.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "kind", "source", "title", "captured_at", "owner", "license_note", "claim"])
        w.writerow([os.path.basename(a.out), "page_capture", a.url, title,
                    datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    a.owner, a.note or ("own page" if a.owner == "own" else "THIRD PARTY: reviewer decides"), a.claim])
    print(json.dumps({"status": "DONE", "out": a.out, "title": title, "owner": a.owner}))

if __name__ == "__main__":
    main()
