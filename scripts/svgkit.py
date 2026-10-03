"""Shared look for the profile SVGs: 3D slab cards, gloss, shine sweep, float animation.

Flat SVG only: no scripts, no external resources. Animations are plain CSS and are
switched off for viewers who prefer reduced motion.
"""

FONT = "'Segoe UI', Arial, sans-serif"
INK, INK2 = "#4A2C1D", "#7A5240"
PAGE, CARD, CHIP, ACCENT = "#FFFAD3", "#FFDBB0", "#FFCCB8", "#FFB1B1"
MT, D = 4, 8  # top margin for the float animation, depth of the 3D edge

DEFS = f"""  <defs>
    <linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9CC"/><stop offset=".55" stop-color="{CARD}"/><stop offset="1" stop-color="#FFD2A2"/></linearGradient>
    <linearGradient id="gYellow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFEC"/><stop offset=".55" stop-color="{PAGE}"/><stop offset="1" stop-color="#FFF0B3"/></linearGradient>
    <linearGradient id="gAccent" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC9C9"/><stop offset=".55" stop-color="{ACCENT}"/><stop offset="1" stop-color="#FFA0A0"/></linearGradient>
    <linearGradient id="gChip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFDDD0"/><stop offset="1" stop-color="{CHIP}"/></linearGradient>
    <linearGradient id="gEdge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity=".15"/></linearGradient>
    <linearGradient id="gGloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="gShine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CHIP}" stop-opacity="0"/><stop offset=".2" stop-color="{CHIP}"/><stop offset=".8" stop-color="{CHIP}"/><stop offset="1" stop-color="{CHIP}" stop-opacity="0"/></linearGradient>
  </defs>
"""

CSS = """
.fl{animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.sh{animation:sh 8s ease-in-out infinite}
@keyframes sh{0%{transform:translateX(0)}45%,100%{transform:translateX(SHWpx)}}
.dr{animation:dr 9s ease-in-out infinite}
@keyframes dr{0%,100%{transform:translate(0,0)}50%{transform:translate(-10px,8px)}}
.up{animation:up .7s ease-out both}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.gr{transform-box:fill-box;transform-origin:0 50%;animation:gr 1.3s cubic-bezier(.2,.8,.2,1) both}
@keyframes gr{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.nu{animation:nu 2.4s ease-in-out infinite}
@keyframes nu{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}
.nr{animation:nr 2.4s ease-in-out infinite}
@keyframes nr{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.pu{transform-box:fill-box;transform-origin:center;animation:pu 2.6s ease-out infinite}
@keyframes pu{0%{transform:scale(1);opacity:.9}100%{transform:scale(1.9);opacity:0}}
.bn{animation:bn 1.6s ease-in-out infinite}
@keyframes bn{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.ul{transform-box:fill-box;transform-origin:center;animation:ul 3.2s ease-in-out infinite}
@keyframes ul{0%,100%{transform:scaleX(.55)}50%{transform:scaleX(1)}}
.tv{animation:tv 7s ease-in-out infinite alternate}
@keyframes tv{from{transform:translateX(0)}to{transform:translateX(TVWpx)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#8217;")


def text(x, y, s, size, weight=400, fill=INK, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{extra}>{esc(s)}</text>\n')


def doc(W, H, title, body, tv=0):
    css = CSS.replace("SHW", str(W + 320)).replace("TVW", str(tv))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{esc(title)}">\n  <title>{esc(title)}</title>\n{DEFS}'
            f'  <style>{css}</style>\n{body}</svg>\n')


def slab(W, FH, content, fill="gCard", side="#EDBE93", r=16, delay=0, shine=True, decor="", ox=0):
    """A rounded card with a solid 3D edge underneath, gloss on top and a moving shine.
    `content` is drawn in card coordinates (0,0 is the card's top-left corner).
    `ox` shifts the card sideways so a pair of cards can sit flush at both outer edges."""
    clip = f'<clipPath id="face"><rect width="{W}" height="{FH}" rx="{r}"/></clipPath>'
    sh = (f'<g class="sh" style="animation-delay:-{delay}s"><rect x="-170" y="-20" width="80" '
          f'height="{FH + 40}" fill="url(#gShine)" transform="skewX(-20)"/></g>') if shine else ""
    return (f'  <g transform="translate({ox},{MT})">\n    {clip}\n'
            f'    <rect y="{D}" width="{W}" height="{FH}" rx="{r}" fill="{side}"/>\n'
            f'    <g class="fl" style="animation-delay:-{delay}s">\n'
            f'      <rect x=".75" y=".75" width="{W - 1.5}" height="{FH - 1.5}" rx="{r}" fill="url(#{fill})" '
            f'stroke="url(#gEdge)" stroke-width="1.5"/>\n'
            f'      <g clip-path="url(#face)">{decor}<rect width="{W}" height="{FH // 2}" fill="url(#gGloss)"/>{sh}</g>\n'
            f'      {content}\n    </g>\n  </g>\n')


def total_height(FH):
    return MT + FH + D


def chip(x, y, label, size=13, h=26, delay=None):
    w = round(len(label) * size * 0.56 + 24)
    cls = f' class="up" style="animation-delay:{delay:.2f}s"' if delay is not None else ""
    return w, (f'<g{cls}><rect x="{x}" y="{y + 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#F2B4A0"/>'
               f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="url(#gChip)"/>'
               + text(x + w / 2, y + h / 2 + 4.5, label, size, 500, anchor="middle") + '</g>\n')


def arrow_up_right(cx, cy, cls="nu"):
    return (f'<g transform="translate({cx},{cy})"><g class="{cls}"><path d="M-5 5 L5 -5 M-2 -5 H5 V2" fill="none" '
            f'stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g></g>')


def header_bar(title):
    """Accent pill and title used at the top of the stats cards."""
    return (text(24, 44, title, 22, 700) +
            f'<rect x="24" y="54" width="40" height="5" rx="2.5" fill="url(#gAccent)"/>')
