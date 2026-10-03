"""Build the static SVGs in assets/ (dividers, headings, cards, tech stack, footer, badges).

Run from anywhere:  python scripts/build_assets.py
The two stats cards are built separately by generate_stats.py.

Layout rule: the profile is one 760px column. Every piece fills its whole area with the
theme background (no transparent margins), so no dark page shows between pieces.
Two 380px pieces make one 760px row; in a row the cards are 358px wide with a 12px
gutter in the middle and a 16px margin at the outer edges.
"""
import textwrap
from pathlib import Path

from svgkit import (ACCENT, CARD, CHIP, DARK, INK, INK2, NAVY0, D, arrow_up_right, chip, doc, pagebg, slab, sparkle,
                    text)

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FULL, HALF, M = 760, 380, 16  # column width, half-row width, outer margin
CARD_W = FULL - 2 * M          # card width inside a full-width piece
PAIR_W = HALF - M - 6          # card width inside a half-row piece


def save(name, s):
    (ASSETS / name).write_text(s, encoding="utf-8", newline="\n")


# --- divider -----------------------------------------------------------------
H = 36
save("divider.svg", doc(FULL, H, "Divider", pagebg(FULL, H, seed=11) + f'''  <rect x="40" y="17" width="{FULL - 80}" height="2.5" rx="1.25" fill="url(#gLine)"/>
  <g class="tv"><circle cx="70" cy="18" r="3.5" fill="{ACCENT}"/></g>
  <circle class="pu" cx="{FULL / 2}" cy="18" r="8" fill="none" stroke="{ACCENT}" stroke-width="2"/>
  <g class="rot"><rect x="{FULL / 2 - 6}" y="12" width="12" height="12" rx="3" fill="url(#gAccent)" transform="rotate(45 {FULL / 2} 18)"/></g>
  <circle cx="{FULL / 2}" cy="18" r="2.4" fill="{DARK}" fill-opacity=".55"/>
  {sparkle(FULL / 2 - 70, 18, .8, 0.5)}{sparkle(FULL / 2 + 70, 18, .8, 1.7)}
''', tv=FULL - 140))

# --- section headings --------------------------------------------------------
H = 76
for fn, label, seed in [("h-featured-projects", "Featured Projects", 21), ("h-tech-stack", "Tech Stack", 22),
                        ("h-github-stats", "GitHub Stats", 23), ("h-lets-connect", "Let's Connect", 24)]:
    half = len(label) * 32 * 0.55 / 2
    mid = FULL / 2
    c = (pagebg(FULL, H, seed=seed) + text(mid, 46, label, 32, 700, anchor="middle") +
         f'<rect x="{M + 24}" y="35" width="{mid - half - 70 - M - 24}" height="3" rx="1.5" fill="url(#gLine)"/>'
         f'<rect x="{mid + half + 70}" y="35" width="{mid - half - 70 - M - 24}" height="3" rx="1.5" fill="url(#gLine)"/>'
         + sparkle(mid - half - 36, 36, 1.2, 0) + sparkle(mid + half + 36, 36, 1.2, 1.4) +
         sparkle(mid - half - 52, 22, .6, .7) + sparkle(mid + half + 52, 50, .6, 2.1) +
         f'<rect class="ul" x="{mid - 54}" y="58" width="108" height="5" rx="2.5" fill="url(#gAccent)"/>')
    save(fn + ".svg", doc(FULL, H, label, c))

# --- about card --------------------------------------------------------------
TOP, FH = 22, 168
H = TOP + FH + D + 10
decor = (f'<g class="dr"><circle cx="{CARD_W - 40}" cy="20" r="112" fill="{ACCENT}" fill-opacity=".07"/>'
         f'<circle cx="{CARD_W - 130}" cy="{FH - 4}" r="56" fill="{CHIP}" fill-opacity=".55"/>'
         f'<circle cx="{CARD_W - 28}" cy="{FH - 40}" r="7" fill="{ACCENT}" fill-opacity=".5"/></g>')
cy = FH // 2
c = (f'<circle class="rot" cx="96" cy="{cy}" r="64" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-dasharray="3 9" stroke-linecap="round"/>'
     f'<circle cx="96" cy="{cy}" r="58" fill="{ACCENT}" fill-opacity=".12"/>'
     f'<circle cx="96" cy="{cy}" r="50" fill="url(#gAccent)" stroke="{CARD}" stroke-width="3"/>'
     + text(96, cy + 19, "K", 56, 700, DARK, "middle") +
     text(180, cy - 6, "Keerthana", 54, 700) +
     text(182, cy + 32, "B.E. CSE (AI & ML) · Machine Learning · NLP", 20, 400, INK2) +
     f'<rect x="182" y="{cy + 48}" width="72" height="6" rx="3" fill="url(#gAccent)"/>'
     + sparkle(CARD_W - 210, 36, 1.1, 0) + sparkle(CARD_W - 60, 120, .9, 1.2) + sparkle(CARD_W - 250, 140, .6, 2.2))
save("about-section.svg", doc(FULL, H, "Keerthana. B.E. CSE (AI & ML), Machine Learning, NLP",
     pagebg(FULL, H, top=True, seed=31) + slab(CARD_W, FH, c, decor=decor, delay=0, ox=M, oy=TOP)))

# --- project cards -----------------------------------------------------------
PT, FH = 8, 196
H = PT + FH + D + 4


def card(fn, title, desc, tags, alt, delay, right, seed):
    size = 21 if len(title) <= 22 else 16
    c = (f'<rect x="26" y="26" width="40" height="6" rx="3" fill="url(#gAccent)"/>'
         f'<circle cx="{PAIR_W - 36}" cy="34" r="17" fill="{ACCENT}" fill-opacity=".2"/>'
         f'<circle cx="{PAIR_W - 36}" cy="34" r="15" fill="url(#gAccent)"/>' + arrow_up_right(PAIR_W - 36, 34) +
         text(26, 68, title, size, 700))
    for i, line in enumerate(textwrap.wrap(desc, 40)):
        c += text(26, 96 + i * 21, line, 14.5, 400, INK2)
    x = 26
    for t in tags:
        w, s = chip(x, FH - 26 - 24, t, size=12)
        c += s
        x += w + 8
    ox = 6 if right else M
    save(fn, doc(HALF, H, alt, pagebg(HALF, H, seed=seed) + slab(PAIR_W, FH, c, delay=delay, ox=ox, oy=PT)))


card("card-neurovocal.svg", "NeuroVocal AI", "AI-driven speech analysis for cognitive/psychological screening.",
     ["Python", "Librosa", "Flask"],
     "NeuroVocal AI: AI-driven speech analysis for cognitive and psychological screening. Python, Librosa, Flask",
     0, False, 41)
card("card-youtube-sentiment.svg", "YouTube Comment Sentiment Analyzer", "Real-time sentiment from video comments.",
     ["Python", "Flask", "VADER", "Scikit-learn"],
     "YouTube Comment Sentiment Analyzer: real-time sentiment from video comments. Python, Flask, VADER, Scikit-learn",
     0, True, 42)
card("card-resume-analyzer.svg", "AI Resume Analyzer & Job Matcher", "Matches resumes to job descriptions with a match score.",
     ["Python", "Flask", "NLP", "Sentence-BERT"],
     "AI Resume Analyzer and Job Matcher: matches resumes to job descriptions with a match score. Python, Flask, NLP, Sentence-BERT",
     3, False, 43)

c = (text(PAIR_W / 2, 92, "View all repos", 26, 700, DARK, "middle") +
     f'<circle class="pu" cx="{PAIR_W / 2}" cy="132" r="18" fill="none" stroke="{DARK}" stroke-width="2"/>'
     f'<circle cx="{PAIR_W / 2}" cy="132" r="21" fill="{DARK}" fill-opacity=".18"/>'
     f'<circle cx="{PAIR_W / 2}" cy="132" r="18" fill="{CARD}"/>'
     f'<g transform="translate({PAIR_W / 2 - 6},132)"><g class="nr"><path d="M-6 0 H8 M2 -6 L8 0 L2 6" fill="none" '
     f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g></g>'
     + sparkle(40, 50, .9, 0, DARK) + sparkle(PAIR_W - 44, 160, 1, 1.1, DARK) + sparkle(PAIR_W - 70, 44, .6, 2, DARK))
save("card-view-all.svg", doc(HALF, H, "View all repos", pagebg(HALF, H, seed=44) +
     slab(PAIR_W, FH, c, fill="gAccent", side="#B8A66E", delay=3, ox=6, oy=PT)))

# --- tech stack --------------------------------------------------------------
groups = [("Languages", ["C", "C++", "Java", "JavaScript", "Python", "PowerShell"]),
          ("Web", ["HTML", "CSS", "React", "jQuery", "Flask", "Streamlit", "Flutter"]),
          ("Databases", ["MySQL", "PostgreSQL", "SQLite"]),
          ("ML and AI", ["TensorFlow", "Keras", "PyTorch", "scikit-learn", "Transformers", "Librosa",
                         "Sentence-BERT", "OpenAI"]),
          ("Data", ["Pandas", "NumPy", "Matplotlib", "Power BI"]),
          ("Tools and cloud", ["Git", "GitHub", "VS Code", "PyCharm", "Jupyter", "Google Colab", "Docker", "Jira",
                               "Anaconda", "AWS", "Azure", "Heroku", "Render", "Canva", "Figma", "Solid Edge"])]
X0, PAD = 196, 30
y, body, n = 28, "", 0
for gi, (name, items) in enumerate(groups):
    x, cy = X0, y
    for t in items:
        w, _ = chip(0, 0, t)
        if x + w > CARD_W - PAD:
            x, cy = X0, cy + 26 + 10
        _, s = chip(x, cy, t, delay=n * 0.04)
        body += s
        x += w + 8
        n += 1
    body += f'<circle cx="{PAD + 8}" cy="{y + 13}" r="4.5" fill="url(#gAccent)"/>' + text(PAD + 22, y + 19, name, 17, 700)
    end = cy + 26
    if gi < len(groups) - 1:
        body += f'<rect x="{PAD}" y="{end + 9}" width="{CARD_W - 2 * PAD}" height="2" rx="1" fill="url(#gLine)"/>'
        y = end + 19
FHt = end + 28
H = 8 + FHt + D + 8
body += sparkle(CARD_W - 28, 24, 1, 0) + sparkle(CARD_W - 56, FHt - 24, .7, 1.5)
save("tech-stack.svg", doc(FULL, H, "Tech stack. " + " ".join(f"{k}: {', '.join(v)}." for k, v in groups),
     pagebg(FULL, H, seed=51) + slab(CARD_W, FHt, body, delay=2, ox=M, oy=8)))

# --- footer ------------------------------------------------------------------
FFH = 60
H = 6 + FFH + D + 16
mid = CARD_W / 2
dots = "".join(f'<circle class="bn" style="animation-delay:{i * .18:.2f}s" cx="{x}" cy="{FFH // 2 + 4}" r="5" '
               f'fill="url(#gAccent)"/>' for i, x in enumerate([mid - 186, mid - 168, mid - 150, mid + 150, mid + 168, mid + 186]))
save("footer.svg", doc(FULL, H, "Thanks for visiting", pagebg(FULL, H, bottom=True, seed=61) +
     slab(CARD_W, FFH, dots + text(mid, FFH // 2 + 9, "Thanks for visiting", 24, 700, anchor="middle"),
          delay=1, ox=M, oy=6)))


# --- badges ------------------------------------------------------------------
def badge(fn, label, icon, delay, seed):
    H = 8 + 52 + D + 8
    c = (f'<circle class="pu" cx="36" cy="26" r="15" fill="none" stroke="{DARK}" stroke-width="2"/>'
         f'<circle cx="36" cy="26" r="17" fill="{DARK}" fill-opacity=".2"/>'
         f'<circle cx="36" cy="26" r="15" fill="{CARD}"/>' + icon + text(132, 33, label, 20, 700, DARK, "middle"))
    save(fn, doc(HALF, H, label + " badge", pagebg(HALF, H, seed=seed) +
         slab(220, 52, c, fill="gAccent", side="#B8A66E", r=26, delay=delay, ox=(HALF - 220) // 2, oy=8)))


badge("badge-linkedin.svg", "LinkedIn", arrow_up_right(36, 26, color=INK), 0, 71)
badge("badge-email.svg", "Email",
      f'<g transform="translate(36,26)"><rect x="-8.5" y="-6" width="17" height="12" rx="2.5" fill="none" '
      f'stroke="{INK}" stroke-width="2"/><path d="M-8 -5 L0 2 L8 -5" fill="none" stroke="{INK}" stroke-width="2" '
      f'stroke-linejoin="round"/></g>', 1.2, 72)
print("built")
