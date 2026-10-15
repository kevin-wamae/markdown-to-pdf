# md-to-pdf

Turn an Obsidian note (or any Markdown file) into a clean PDF, using two commands and your browser's **Save as PDF**.

```
my-note.md ──prep.py──▶ build.md ──pandoc + style.css──▶ output.html ──browser Print──▶ PDF
```

- `prep.py` tidies the note so it renders the way it looks in Obsidian.
- [pandoc](https://pandoc.org) converts the Markdown to HTML.
- `style.css` controls the look. A ready-made compact CV style is in `styles/cv.css`.

It works on macOS, Linux and Windows. Where the steps differ by system, there is a sub-section for each.

## What is in this repo

| File                   | Purpose                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `prep.py`            | Cleans up an Obsidian note before conversion.                                            |
| `style.css`          | Default look for notes and documents (A4, 10.5 pt, accent colour, tables, code, quotes). |
| `styles/cv.css`      | Compact two-page CV look: small text, uppercase section headings, shaded skills table.   |
| `example/example.md` | A sample note that exercises headings, lists, a table, a callout, links and code.        |

## 1. Install the dependencies

You need **Python 3** (3.8 or newer, no extra packages) and **pandoc**.

### macOS

Install [Homebrew](https://brew.sh) if you don't have it, then:

```bash
brew install python pandoc
```

### Linux

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install python3 pandoc

# Fedora
sudo dnf install python3 pandoc

# Arch
sudo pacman -S python pandoc
```

### Windows

In PowerShell:

```powershell
winget install Python.Python.3.12
winget install JohnMacFarlane.Pandoc
```

Close and reopen PowerShell afterwards so the new programs are found. If `python` opens the Microsoft Store, finish installing Python from there, or use `py` instead of `python` below.

### Check the install

```bash
python3 --version     # on Windows: python --version
pandoc --version
```

## 2. Get the project

```bash
git clone https://github.com/kevin-wamae/markdown-to-pdf.git
cd markdown-to-pdf
```

No git? Use **Code → Download ZIP** on GitHub, unzip it, and open a terminal in that folder.

Copy your note into this folder (or use `example/example.md` to try it first).

## 3. Convert to HTML

Two commands. The only difference between systems is the Python program name.

### macOS and Linux

```bash
python3 prep.py my-note.md
pandoc build.md -f markdown-yaml_metadata_block -t html5 -s --metadata pagetitle="My note" -c style.css -o output.html
```

### Windows (PowerShell)

```powershell
python prep.py my-note.md
pandoc build.md -f markdown-yaml_metadata_block -t html5 -s --metadata pagetitle="My note" -c style.css -o output.html
```

Notes:

- Replace `my-note.md` with your file name, and `My note` with the title for the page.
- Keep `output.html` in the same folder as `style.css`, because it links to it. Images should sit next to the HTML too.
- For the CV look, use `-c styles/cv.css` instead of `-c style.css`.
- Single newlines inside a paragraph are kept as line breaks, like Obsidian. Add `--no-line-breaks` to `prep.py` for standard Markdown behaviour.

## 4. Save as PDF in your browser

Open `output.html`, press **Cmd+P** (macOS) or **Ctrl+P** (Windows, Linux) and choose Save as PDF.

### macOS: Safari

1. File → Print, then the **PDF** menu at the bottom left → **Save as PDF**.
2. Paper size **A4**, and tick **Print backgrounds** in the Safari options.
3. Safari sometimes ignores CSS margins. Check the preview and adjust the scale if needed.

### macOS or Linux: Firefox

1. Print → destination **Save to PDF**.
2. Paper size **A4**, margins **Default**, tick **Print backgrounds**, untick **Print headers and footers**.

### Windows: Edge (or any Chromium browser)

1. Print → printer **Save as PDF**.
2. Paper size **A4**, margins **Default**, scale **100%**, untick **Headers and footers**, tick **Background graphics**.

### Linux: other browsers

Use the same settings as above: A4, default margins, headers and footers off, backgrounds on.

## What `prep.py` handles

| In your Obsidian note                                     | In the PDF                             |
| --------------------------------------------------------- | -------------------------------------- |
| Properties block (`---` YAML at the top)                | Removed                                |
| Heading or list directly after a paragraph, no blank line | Fixed                                  |
| `---` directly followed by a heading                    | Fixed                                  |
| Lines typed one under another                             | Kept as separate lines                 |
| `[[Note]]`, `[[Note\|alias]]`                          | Plain text (the alias if there is one) |
| `![[image.png]]`                                        | Normal image link                      |
| `==highlight==`                                         | Highlighted text                       |
| `%%comment%%`                                           | Removed                                |
| `> [!note] Title` callouts                              | Quote with a bold title                |
| Fenced code blocks                                        | Left untouched                         |

Not supported: embedded notes (`![[Other note]]`), Dataview queries, canvas files and plugin-specific syntax.

## Changing the look

Everything is in the CSS file you pass to pandoc. In `style.css`:

- **Text size:** `font-size: 10.5pt;` in `body`.
- **Line spacing:** `line-height: 1.5;` in `body`.
- **Accent colour:** `--accent: #1a3a5c;` at the top.
- **Page margins:** `margin: 18mm 18mm;` in the `@page` rule (top/bottom, then left/right).
- **Font:** the `font-family` list in `body`.

In `styles/cv.css` the same settings exist, but the text is smaller (9 pt) so a CV fits on two pages. Lower `line-height` there (for example `1.2`) if it runs onto a third page.

Save the CSS, re-run the `pandoc` command, then refresh `output.html` in your browser.

## Troubleshooting

**`pandoc: command not found`.** Install it (step 1), then close and reopen your terminal.

**Headings, lists or tables look like plain text.** Run `prep.py` first and convert `build.md`, not your original file.

**Colours or shaded table cells are missing in the PDF.** Turn on "Background graphics" or "Print backgrounds".

**A date or URL appears in the page header or footer.** Turn off "Headers and footers" in the print dialog.

**Windows says `python` is not recognised.** Reopen PowerShell after installing, or use `py prep.py my-note.md`.

**The document is longer than you want.** Lower `font-size`, `line-height` or the `@page` margins in the CSS.

## Licence

MIT — see [LICENSE](LICENSE).
