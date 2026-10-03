"""Build the static SVGs in assets/ (dividers, headings, cards, tech stack, footer, badges).

Run from anywhere:  python scripts/build_assets.py
The two stats cards are built separately by generate_stats.py.
"""
import textwrap
from pathlib import Path

from svgkit import ACCENT, CARD, CHIP, INK, INK2, arrow_up_right, chip, doc, slab, text, total_height

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def save(name, s):
    (ASSETS / name).write_text(s, encoding="utf-8", newline="\n")


# --- divider -----------------------------------------------------------------
save("divider.svg", doc(800, 28, "Divider", f'''  <rect width="800" height="28" rx="14" fill="#FFFAD3"/>
  <rect x="30" y="13" width="740" height="2.5" rx="1.25" fill="url(#gLine)"/>
  <g class="tv"><circle cx="60" cy="14" r="3.5" fill="{ACCENT}"/></g>
  <circle class="pu" cx="400" cy="14" r="7" fill="none" stroke="{ACCENT}" stroke-width="2"/>
  <circle cx="400" cy="14" r="7" fill="url(#gAccent)"/>
  <circle cx="400" cy="14" r="2.5" fill="#fff" fill-opacity=".8"/>
''', tv=680))

# --- section headings --------------------------------------------------------
for fn, label in [("h-featured-projects", "Featured Projects"), ("h-tech-stack", "Tech Stack"),
                  ("h-github-stats", "GitHub Stats"), ("h-lets-connect", "Let's Connect")]:
    half = len(label) * 28 * 0.55 / 2
    c = (text(300, 40, label, 30, 700, anchor="middle") +
         f'<circle cx="{300 - half - 26}" cy="29" r="4.5" fill="url(#gAccent)"/>'
         f'<circle cx="{300 + half + 26}" cy="29" r="4.5" fill="url(#gAccent)"/>'
         f'<rect class="ul" x="240" y="52" width="120" height="5" rx="2.5" fill="url(#gAccent)"/>')
    save(fn + ".svg", doc(600, total_height(64), label,
                          slab(600, 64, c, fill="gYellow", side="#EBDC96", delay=1.5)))

# --- about card --------------------------------------------------------------
decor = (f'<g class="dr"><circle cx="735" cy="30" r="120" fill="{ACCENT}" fill-opacity=".30"/>'
         f'<circle cx="640" cy="205" r="62" fill="{CHIP}" fill-opacity=".65"/>'
         f'<circle cx="560" cy="40" r="9" fill="{ACCENT}" fill-opacity=".6"/>'
         f'<circle cx="772" cy="150" r="7" fill="#fff" fill-opacity=".6"/></g>')
c = (f'<circle cx="108" cy="104" r="62" fill="#fff" fill-opacity=".45"/>'
     f'<circle cx="108" cy="104" r="54" fill="url(#gAccent)" stroke="#fff" stroke-opacity=".8" stroke-width="3"/>'
     + text(108, 124, "K", 60, 700, anchor="middle") +
     text(200, 98, "Keerthana", 56, 700) +
     text(202, 138, "B.E. CSE (AI & ML) · Machine Learning · NLP", 21, 400, INK2) +
     f'<rect x="202" y="156" width="72" height="6" rx="3" fill="url(#gAccent)"/>')
save("about-section.svg", doc(800, total_height(208),
     "Keerthana. B.E. CSE (AI & ML), Machine Learning, NLP", slab(800, 208, c, decor=decor, delay=0)))

# --- project cards -----------------------------------------------------------
CW, FH = 380, 196


def card(fn, title, desc, tags, alt, delay):
    size = 21 if len(title) <= 22 else 16
    c = (f'<rect x="26" y="26" width="40" height="6" rx="3" fill="url(#gAccent)"/>'
         f'<circle cx="344" cy="36" r="17" fill="#fff" fill-opacity=".5"/>'
         f'<circle cx="344" cy="36" r="15" fill="url(#gAccent)"/>' + arrow_up_right(344, 36) +
         text(26, 66, title, size, 700))
    for i, line in enumerate(textwrap.wrap(desc, 40)):
        c += text(26, 94 + i * 21, line, 14.5, 400, INK2)
    x = 26
    for t in tags:
        w, s = chip(x, FH - 26 - 24, t)
        c += s
        x += w + 8
    save(fn, doc(CW, total_height(FH), alt, slab(CW, FH, c, delay=delay)))


card("card-neurovocal.svg", "NeuroVocal AI", "AI-driven speech analysis for cognitive/psychological screening.",
     ["Python", "Librosa", "Flask"],
     "NeuroVocal AI: AI-driven speech analysis for cognitive and psychological screening. Python, Librosa, Flask", 0)
card("card-youtube-sentiment.svg", "YouTube Comment Sentiment Analyzer", "Real-time sentiment from video comments.",
     ["Python", "Flask", "VADER", "Scikit-learn"],
     "YouTube Comment Sentiment Analyzer: real-time sentiment from video comments. Python, Flask, VADER, Scikit-learn", 0)
card("card-resume-analyzer.svg", "AI Resume Analyzer & Job Matcher", "Matches resumes to job descriptions with a match score.",
     ["Python", "Flask", "NLP", "Sentence-BERT"],
     "AI Resume Analyzer and Job Matcher: matches resumes to job descriptions with a match score. Python, Flask, NLP, Sentence-BERT", 3)

c = (text(CW / 2, 92, "View all repos", 26, 700, anchor="middle") +
     f'<circle cx="{CW / 2}" cy="132" r="21" fill="#fff" fill-opacity=".55"/>'
     f'<circle cx="{CW / 2}" cy="132" r="18" fill="{CARD}"/>'
     f'<g transform="translate({CW / 2 - 6},132)"><g class="nr"><path d="M-6 0 H8 M2 -6 L8 0 L2 6" fill="none" '
     f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g></g>')
save("card-view-all.svg", doc(CW, total_height(FH), "View all repos",
                              slab(CW, FH, c, fill="gAccent", side="#E89A9A", delay=3)))

# --- tech stack --------------------------------------------------------------
groups = [("Languages", ["C", "C++", "Java", "JavaScript", "Python", "PowerShell"]),
          ("Web", ["HTML", "CSS", "React", "jQuery", "Flask", "Streamlit", "Flutter"]),
          ("Databases", ["MySQL", "PostgreSQL", "SQLite"]),
          ("ML and AI", ["TensorFlow", "Keras", "PyTorch", "scikit-learn", "Transformers", "Librosa",
                         "Sentence-BERT", "OpenAI"]),
          ("Data", ["Pandas", "NumPy", "Matplotlib", "Power BI"]),
          ("Tools and cloud", ["Git", "GitHub", "VS Code", "PyCharm", "Jupyter", "Google Colab", "Docker", "Jira",
                               "Anaconda", "AWS", "Azure", "Heroku", "Render", "Canva", "Figma", "Solid Edge"])]
W, y, body, n = 800, 34, "", 0
for gi, (name, items) in enumerate(groups):
    x, cy = 210, y
    for t in items:
        w, _ = chip(0, 0, t)
        if x + w > W - 36:
            x, cy = 210, cy + 26 + 12
        _, s = chip(x, cy, t, delay=n * 0.04)
        body += s
        x += w + 10
        n += 1
    body += f'<circle cx="38" cy="{y + 13}" r="4.5" fill="url(#gAccent)"/>' + text(52, y + 19, name, 17, 700)
    y = cy + 26 + 26
    if gi < len(groups) - 1:
        body += f'<rect x="36" y="{y - 13}" width="{W - 72}" height="2" rx="1" fill="url(#gLine)"/>'
FHt = y - 26 + 34
save("tech-stack.svg", doc(W, total_height(FHt),
     "Tech stack. " + " ".join(f"{k}: {', '.join(v)}." for k, v in groups), slab(W, FHt, body, delay=2)))

# --- footer ------------------------------------------------------------------
dots = "".join(f'<circle class="bn" style="animation-delay:{i * .18:.2f}s" cx="{x}" cy="42" r="5" fill="url(#gAccent)"/>'
               for i, x in enumerate([230, 248, 266, 534, 552, 570]))
save("footer.svg", doc(800, total_height(76), "Thanks for visiting",
     slab(800, 76, dots + text(400, 48, "Thanks for visiting", 25, 700, anchor="middle"), delay=1)))


# --- badges ------------------------------------------------------------------
def badge(fn, label, icon, delay):
    c = ('<circle class="pu" cx="36" cy="26" r="15" fill="none" stroke="#fff" stroke-width="2"/>'
         '<circle cx="36" cy="26" r="17" fill="#fff" fill-opacity=".5"/>'
         f'<circle cx="36" cy="26" r="15" fill="{CARD}"/>' + icon + text(132, 33, label, 20, 700, anchor="middle"))
    save(fn, doc(220, total_height(52), label + " badge",
                 slab(220, 52, c, fill="gAccent", side="#E89A9A", r=26, delay=delay)))


badge("badge-linkedin.svg", "LinkedIn", arrow_up_right(36, 26), 0)
badge("badge-email.svg", "Email",
      f'<g transform="translate(36,26)"><rect x="-8.5" y="-6" width="17" height="12" rx="2.5" fill="none" '
      f'stroke="{INK}" stroke-width="2"/><path d="M-8 -5 L0 2 L8 -5" fill="none" stroke="{INK}" stroke-width="2" '
      f'stroke-linejoin="round"/></g>', 1.2)
print("built")
