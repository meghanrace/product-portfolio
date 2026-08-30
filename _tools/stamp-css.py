#!/usr/bin/env python3
"""Stamp a content hash onto every local stylesheet link.

Browsers cache stylesheets hard, and GitHub Pages gives us no control over
cache headers. Without a version on the URL, a returning visitor keeps using
whatever styles.css they fetched last time, against freshly deployed HTML.
That is not a cosmetic problem: on 2026-08-30 a phone holding the previous
styles.css rendered the new Resources dropdown markup as five links of raw
text dumped into the mobile menu, because none of the .nav-menu rules existed
in the copy it had.

Hashing the file contents means the URL changes only when the CSS actually
changes, so caching still works, and fresh HTML can never pair with stale CSS.

Run after editing any .css, before committing:

    python3 _tools/stamp-css.py
"""

import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# href="/styles.css", href="styles.css", either already carrying a ?v= or not
LINK = re.compile(r'href="(/?[A-Za-z0-9_\-./]+\.css)(\?v=[0-9a-f]+)?"')

_hashes = {}


def digest(repo_path):
    """md5 of a stylesheet, memoised. None if the file isn't in the repo."""
    if repo_path not in _hashes:
        full = os.path.join(ROOT, repo_path)
        if not os.path.isfile(full):
            _hashes[repo_path] = None
        else:
            with open(full, "rb") as fh:
                _hashes[repo_path] = hashlib.md5(fh.read()).hexdigest()[:8]
    return _hashes[repo_path]


def stamp(html_path):
    rel_dir = os.path.dirname(os.path.relpath(html_path, ROOT))

    def sub(m):
        href = m.group(1)
        # Root-relative hrefs point at the repo root; bare ones are relative to
        # the page, which for these pages is always the root, but resolve it
        # properly rather than assuming.
        repo_path = href.lstrip("/") if href.startswith("/") else os.path.normpath(
            os.path.join(rel_dir, href))
        h = digest(repo_path)
        if h is None:
            return m.group(0)  # not ours to stamp
        return 'href="%s?v=%s"' % (href, h)

    src = open(html_path, encoding="utf-8").read()
    out = LINK.sub(sub, src)
    if out != src:
        open(html_path, "w", encoding="utf-8").write(out)
        return True
    return False


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # skip git internals and Jekyll-excluded source dirs
        dirnames[:] = [d for d in dirnames if d != ".git" and not d.startswith("_")]
        for name in filenames:
            if name.endswith(".html") and stamp(os.path.join(dirpath, name)):
                changed.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    for path in sorted(changed):
        print("stamped", path)
    print("\n%d page(s) updated" % len(changed))
    for css, h in sorted(_hashes.items()):
        if h:
            print("  %-28s v=%s" % (css, h))


if __name__ == "__main__":
    main()
