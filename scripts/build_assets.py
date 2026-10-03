"""Build the static SVGs in assets/ (dividers, headings, cards, tech stack, footer, badges).

Run from anywhere:  python scripts/build_assets.py
The two stats cards are built separately by generate_stats.py.

Layout rule: two 380px cards side by side make a 760px row, so every full-width
element is also 760px wide and all outer edges line up. In each pair the cards are
drawn 368px wide and pushed to opposite sides, leaving a 12px gutter in the middle.
"""
import textwrap
from pathlib import Path

from svgkit import ACCENT, CARD, CHIP, INK, INK2, arrow_up_right, chip, doc, slab, text, total_height

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FULL = 760  # width of every full-width element


def save(name, s):
    (ASSETS / name).write_text(s, encoding="utf-8", newline="\n")


# --- divider -----------------------------------------------------------------
save("divider.svg", doc(FULL, 30, "Divider", f'''  <g transform="translate(0,4)">
  <rect width="{FULL}" height="22" rx="11" fill="#FFFAD3"/>
  <rect x="30" y="10" width="{FULL - 60}" height="2.5" rx="1.25" fill="url(#gLine)"/>
  <g class="tv"><circle cx="60" cy="11" r="3.5" fill="{ACCENT}"/></g>
  <circle class="pu" cx="{FULL / 2}" cy="11" r="6" fill="none" stroke="{ACCENT}" stroke-width="2"/>
  <circle cx="{FULL / 2}" cy="11" r="6" fill="url(#gAccent)"/>
  <circle cx="{FULL / 2}" cy="11" r="2.2" fill="#fff" fill-opacity=".8"/>
  </g>
''', tv=FULL - 120))

# --- section headings --------------------------------------------------------
HFH = 52
for fn, label in [("h-featured-projects", "Featured Projects"), ("h-tech-stack", "Tech Stack"),
                  ("h-github-stats", "GitHub Stats"), ("h-lets-connect", "Let's Connect")]:
    half = len(label) * 28 * 0.55 / 2
    c = (text(300, 34, label, 28, 700, anchor="middle") +
         f'<circle cx="{300 - half - 24}" cy="25" r="4.5" fill="url(#gAccent)"/>'
         f'<circle cx="{300 + half + 24}" cy="25" r="4.5" fill="url(#gAccent)"/>'
         f'<rect class="ul" x="246" y="42" width="108" height="5" rx="2.5" fill="url(#gAccent)"/>')
    save(fn + ".svg", doc(600, total_height(HFH), label,
                          slab(600, HFH, c, fill="gYellow", side="#EBDC96", delay=1.5)))

# --- about card --------------------------------------------------------------
AFH = 168
decor = (f'<g class="dr"><circle cx="{FULL - 40}" cy="20" r="112" fill="{ACCENT}" fill-opacity=".30"/>'
         f'<circle cx="{FULL - 130}" cy="{AFH - 4}" r="56" fill="{CHIP}" fill-opacity=".65"/>'
         f'<circle cx="{FULL - 220}" cy="30" r="9" fill="{ACCENT}" fill-opacity=".6"/>'
         f'<circle cx="{FULL - 28}" cy="{AFH - 40}" r="7" fill="#fff" fill-opacity=".6"/></g>')
cy = AFH // 2
c = (f'<circle cx="96" cy="{cy}" r="58" fill="#fff" fill-opacity=".45"/>'
     f'<circle cx="96" cy="{cy}" r="50" fill="url(#gAccent)" stroke="#fff" stroke-opacity=".8" stroke-width="3"/>'
     + text(96, cy + 19, "K", 56, 700, anchor="middle") +
     text(180, cy - 6, "Keerthana", 54, 700) +
     text(182, cy + 32, "B.E. CSE (AI & ML) · Machine Learning · NLP", 20, 400, INK2) +
     f'<rect x="182" y="{cy + 48}" width="72" height="6" rx="3" fill="url(#gAccent)"/>')
save("about-section.svg", doc(FULL, total_height(AFH),
     "Keerthana. B.E. CSE (AI & ML), Machine Learning, NLP", slab(FULL, AFH, c, decor=decor, delay=0)))

# --- project cards -----------------------------------------------------------
DOC_W, CW, FH = 380, 368, 196


def card(fn, title, desc, tags, alt, delay, right):
    size = 21 if len(title) <= 22 else 16
    c = (f'<rect x="26" y="26" width="40" height="6" rx="3" fill="url(#gAccent)"/>'
         f'<circle cx="{CW - 36}" cy="34" r="17" fill="#fff" fill-opacity=".5"/>'
         f'<circle cx="{CW - 36}" cy="34" r="15" fill="url(#gAccent)"/>' + arrow_up_right(CW - 36, 34) +
         text(26, 68, title, size, 700))
    for i, line in enumerate(textwrap.wrap(desc, 42)):
        c += text(26, 96 + i * 21, line, 14.5, 400, INK2)
    x = 26
    for t in tags:
        w, s = chip(x, FH - 26 - 24, t)
        c += s
        x += w + 8
    save(fn, doc(DOC_W, total_height(FH), alt, slab(CW, FH, c, delay=delay, ox=DOC_W - CW if right else 0)))


card("card-neurovocal.svg", "NeuroVocal AI", "AI-driven speech analysis for cognitive/psychological screening.",
     ["Python", "Librosa", "Flask"],
     "NeuroVocal AI: AI-driven speech analysis for cognitive and psychological screening. Python, Librosa, Flask",
     0, False)
card("card-youtube-sentiment.svg", "YouTube Comment Sentiment Analyzer", "Real-time sentiment from video comments.",
     ["Python", "Flask", "VADER", "Scikit-learn"],
     "YouTube Comment Sentiment Analyzer: real-time sentiment from video comments. Python, Flask, VADER, Scikit-learn",
     0, True)
card("card-resume-analyzer.svg", "AI Resume Analyzer & Job Matcher", "Matches resumes to job descriptions with a match score.",
     ["Python", "Flask", "NLP", "Sentence-BERT"],
     "AI Resume Analyzer and Job Matcher: matches resumes to job descriptions with a match score. Python, Flask, NLP, Sentence-BERT",
     3, False)

c = (text(CW / 2, 92, "View all repos", 26, 700, anchor="middle") +
     f'<circle cx="{CW / 2}" cy="132" r="21" fill="#fff" fill-opacity=".55"/>'
     f'<circle cx="{CW / 2}" cy="132" r="18" fill="{CARD}"/>'
     f'<g transform="translate({CW / 2 - 6},132)"><g class="nr"><path d="M-6 0 H8 M2 -6 L8 0 L2 6" fill="none" '
     f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g></g>')
save("card-view-all.svg", doc(DOC_W, total_height(FH), "View all repos",
                              slab(CW, FH, c, fill="gAccent", side="#E89A9A", delay=3, ox=DOC_W - CW)))

# --- tech stack --------------------------------------------------------------
groups = [("Languages", ["C", "C++", "Java", "JavaScript", "Python", "PowerShell"]),
          ("Web", ["HTML", "CSS", "React", "jQuery", "Flask", "Streamlit", "Flutter"]),
          ("Databases", ["MySQL", "PostgreSQL", "SQLite"]),
          ("ML and AI", ["TensorFlow", "Keras", "PyTorch", "scikit-learn", "Transformers", "Librosa",
                         "Sentence-BERT", "OpenAI"]),
          ("Data", ["Pandas", "NumPy", "Matplotlib", "Power BI"]),
          ("Tools and cloud", ["Git", "GitHub", "VS Code", "PyCharm", "Jupyter", "Google Colab", "Docker", "Jira",
                               "Anaconda", "AWS", "Azure", "Heroku", "Render", "Canva", "Figma", "Solid Edge"])]
X0, PAD = 196, 30  # where chips start, side padding
y, body, n = 28, "", 0
for gi, (name, items) in enumerate(groups):
    x, cy = X0, y
    for t in items:
        w, _ = chip(0, 0, t)
        if x + w > FULL - PAD:
            x, cy = X0, cy + 26 + 10
        _, s = chip(x, cy, t, delay=n * 0.04)
        body += s
        x += w + 8
        n += 1
    body += f'<circle cx="{PAD + 8}" cy="{y + 13}" r="4.5" fill="url(#gAccent)"/>' + text(PAD + 22, y + 19, name, 17, 700)
    end = cy + 26
    if gi < len(groups) - 1:
        body += f'<rect x="{PAD}" y="{end + 9}" width="{FULL - 2 * PAD}" height="2" rx="1" fill="url(#gLine)"/>'
        y = end + 19
FHt = end + 28
save("tech-stack.svg", doc(FULL, total_height(FHt),
     "Tech stack. " + " ".join(f"{k}: {', '.join(v)}." for k, v in groups), slab(FULL, FHt, body, delay=2)))

# --- footer ------------------------------------------------------------------
FFH = 60
mid = FULL / 2
dots = "".join(f'<circle class="bn" style="animation-delay:{i * .18:.2f}s" cx="{x}" cy="{FFH // 2 + 4}" r="5" '
               f'fill="url(#gAccent)"/>' for i, x in enumerate([mid - 186, mid - 168, mid - 150, mid + 150, mid + 168, mid + 186]))
save("footer.svg", doc(FULL, total_height(FFH), "Thanks for visiting",
     slab(FULL, FFH, dots + text(mid, FFH // 2 + 9, "Thanks for visiting", 24, 700, anchor="middle"), delay=1)))


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
