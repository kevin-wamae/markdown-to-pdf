#!/usr/bin/env python3
"""Tidy an Obsidian-style Markdown note so pandoc renders it the way Obsidian does.

Usage:  python3 prep.py my-note.md        (writes build.md)
        python3 prep.py my-note.md -o other.md
        python3 prep.py my-note.md --no-line-breaks

What it fixes:
  * removes the YAML properties block at the top of the note
  * blank lines around headings, '---' rules and lists (Obsidian doesn't need them, pandoc does)
  * single newlines inside a paragraph become visible line breaks, as in Obsidian
  * [[wikilinks]], ![[image embeds]], ==highlights==, %%comments%% and > [!callouts]
Fenced code blocks are never touched.
"""
import argparse
import re
import sys
from pathlib import Path

LIST = re.compile(r"\s*([-*+]|\d+[.)])\s")
FENCE = re.compile(r"\s*(```|~~~)")


def strip_frontmatter(text: str) -> str:
    m = re.match(r"\A---\s*\n.*?\n(---|\.\.\.)\s*(\n|\Z)", text, flags=re.S)
    return text[m.end():] if m else text


def heading_anchor(text: str) -> str:
    s = re.sub(r"[^\w\s.-]", "", text.strip().lower())
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"^[^a-z]+", "", s)


def heading_link(m: re.Match) -> str:
    target = [p for p in m.group(1).split("#") if p][-1]
    return f"[{m.group(2) or target}](#{heading_anchor(target)})"


def inline_fixes(line: str) -> str:
    line = re.sub(r"!\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]", r"![](\1)", line)             # ![[img.png]]
    line = re.sub(r"\[\[#([^\]|]+)(?:\|([^\]]+))?\]\]", heading_link, line)            # [[#Heading|alias]] internal links
    line = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", line)                         # [[note|alias]]
    line = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("#")[0] or m.group(1), line)  # [[note]]
    line = re.sub(r"==(.+?)==", r"<mark>\1</mark>", line)                              # ==highlight==
    line = re.sub(r"%%.*?%%", "", line)                                                # %%comment%%
    m = re.match(r"^(\s*>\s*)\[!(\w+)\][+-]?\s*(.*)$", line)                           # > [!note] Title
    if m:
        line = f"{m.group(1)}**{m.group(3) or m.group(2).capitalize()}**\\"
    return line


def is_plain(line: str) -> bool:
    s = line.strip()
    return bool(s) and not (s.startswith(("#", "|", ">", "---", "***", "<")) or LIST.match(line) or FENCE.match(line))


def prepare(text: str, line_breaks: bool = True) -> str:
    lines = strip_frontmatter(text.replace("\r\n", "\n")).split("\n")
    # mark which lines sit inside fenced code blocks
    in_code, code = False, []
    for l in lines:
        if FENCE.match(l):
            code.append(True)
            in_code = not in_code
        else:
            code.append(in_code)

    out = []
    for i, line in enumerate(lines):
        if code[i]:
            out.append(line)
            continue
        line = inline_fixes(line)
        prev = out[-1] if out else ""
        prev_code = bool(out) and code[i - 1]
        is_block = line.strip() == "---" or line.startswith("#") or bool(FENCE.match(line))
        prev_block = prev.strip() == "---" or prev.startswith("#")
        starts_list = bool(LIST.match(line)) and not LIST.match(prev) and not prev.lstrip().startswith("|")
        if out and prev.strip() and not prev_code and (is_block or prev_block or starts_list):
            out.append("")
        elif out and prev_code and line.strip() and not FENCE.match(line):
            out.append("")
        nxt_ok = i + 1 < len(lines) and not code[i + 1] and is_plain(inline_fixes(lines[i + 1]))
        if line_breaks and is_plain(line) and nxt_ok and not line.rstrip().endswith(("\\", "  ")):
            line = line.rstrip() + "\\"
        out.append(line)
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="your Markdown file")
    ap.add_argument("-o", "--output", default="build.md", help="file to write (default: build.md)")
    ap.add_argument("--no-line-breaks", action="store_true", help="treat single newlines as spaces (standard Markdown)")
    a = ap.parse_args()
    src = Path(a.input)
    if not src.is_file():
        sys.exit(f"Cannot find {src}")
    Path(a.output).write_text(prepare(src.read_text(encoding="utf-8"), not a.no_line_breaks), encoding="utf-8")
    print(f"Wrote {a.output}")


if __name__ == "__main__":
    main()
