"""Generates the animated SVG cards used on the GitHub profile README.

Run:  python3 tools/gen_cards.py   (writes assets/projects/*.svg and assets/tech-marquee.svg)
"""
import html
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "projects")
os.makedirs(OUT, exist_ok=True)

W, H = 560, 280
CX, CY = 462, 128  # motif centre

FONT = "'Segoe UI','Inter',-apple-system,Helvetica,Arial,sans-serif"
MONO = "'Cascadia Code','JetBrains Mono',Consolas,monospace"


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- motifs
def m_neural(c1, c2):
    layers = [[-60, [-45, 0, 45]], [0, [-60, -20, 20, 60]], [60, [-30, 30]]]
    pts = [(CX + x, CY + y) for x, ys in layers for y in ys]
    edges = []
    for (x1, ys1), (x2, ys2) in zip(layers, layers[1:]):
        for a in ys1:
            for b in ys2:
                edges.append((CX + x1, CY + a, CX + x2, CY + b))
    s = []
    for i, (a, b, c, d) in enumerate(edges):
        s.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{c2}" stroke-width="1.2" stroke-dasharray="4 6" opacity=".55">'
                 f'<animate attributeName="stroke-dashoffset" from="0" to="-20" dur="{1.2 + (i % 4) * .3}s" repeatCount="indefinite"/></line>')
    for i, (x, y) in enumerate(pts):
        s.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{c1}" class="pulse" style="animation-delay:{i * .25:.2f}s"/>')
    return "".join(s)


def m_radar(c1, c2):
    s = [f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{c2}" stroke-opacity=".35"/>' for r in (30, 55, 80)]
    s.append(f'<line x1="{CX - 85}" y1="{CY}" x2="{CX + 85}" y2="{CY}" stroke="{c2}" stroke-opacity=".25"/>')
    s.append(f'<line x1="{CX}" y1="{CY - 85}" x2="{CX}" y2="{CY + 85}" stroke="{c2}" stroke-opacity=".25"/>')
    s.append(f'<g class="spin"><path d="M{CX} {CY} L{CX + 80} {CY} A80 80 0 0 0 {CX + 80 * math.cos(math.radians(-50)):.1f} {CY + 80 * math.sin(math.radians(-50)):.1f} Z" fill="url(#sweep)"/></g>')
    for i, (dx, dy) in enumerate([(35, -40), (-50, 20), (20, 55)]):
        s.append(f'<circle cx="{CX + dx}" cy="{CY + dy}" r="5" fill="{c1}" class="blip" style="animation-delay:{i * .9}s"/>')
    return "".join(s)


def m_orbit(c1, c2, core="🤖"):
    s = []
    for i, (r, d) in enumerate([(40, 6), (62, 9), (84, 13)]):
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{c2}" stroke-opacity=".3" stroke-dasharray="3 5"/>')
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{i * 120} {CX} {CY}" to="{i * 120 + (360 if i % 2 == 0 else -360)} {CX} {CY}" dur="{d}s" repeatCount="indefinite"/>'
                 f'<circle cx="{CX + r}" cy="{CY}" r="7" fill="{c1}"/></g>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="24" fill="{c1}" fill-opacity=".2" class="pulse"/>')
    s.append(f'<text x="{CX}" y="{CY + 9}" text-anchor="middle" font-size="26">{core}</text>')
    return "".join(s)


def m_bars(c1, c2):
    s = []
    hs = [50, 80, 62, 110, 90, 135]
    for i, h in enumerate(hs):
        x = CX - 78 + i * 28
        s.append(f'<rect x="{x}" y="{CY + 75 - h}" width="18" height="{h}" rx="4" fill="url(#g2)" class="grow" style="animation-delay:{i * .15:.2f}s"/>')
    s.append(f'<polyline points="' + " ".join(f"{CX - 69 + i * 28},{CY + 68 - h}" for i, h in enumerate(hs)) +
             f'" fill="none" stroke="{c2}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="400" class="draw"/>')
    return "".join(s)


def m_rings(c1, c2, core="☢️"):
    s = []
    for i in range(3):
        s.append(f'<circle cx="{CX}" cy="{CY}" r="20" fill="none" stroke="{c1}" stroke-width="2" class="ripple" style="animation-delay:{i}s"/>')
    s.append(f'<text x="{CX}" y="{CY + 12}" text-anchor="middle" font-size="34">{core}</text>')
    return "".join(s)


def m_mandala(c1, c2):
    s = []
    for k, (r, n, d, dirn) in enumerate([(30, 8, 12, 1), (55, 12, 18, -1), (80, 16, 26, 1)]):
        petals = "".join(
            f'<circle cx="{CX + r * math.cos(2 * math.pi * j / n):.1f}" cy="{CY + r * math.sin(2 * math.pi * j / n):.1f}" r="{4 + k}" fill="{c1 if j % 2 else c2}" opacity=".8"/>'
            for j in range(n))
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="{360 * dirn} {CX} {CY}" dur="{d}s" repeatCount="indefinite"/>{petals}</g>')
    s.append(f'<text x="{CX}" y="{CY + 10}" text-anchor="middle" font-size="28">🕉️</text>')
    return "".join(s)


def m_cards(c1, c2, symbols=("♠", "♥", "♦", "♣")):
    s = []
    for i, (ang, sym) in enumerate(zip((-24, -8, 8, 24), symbols)):
        col = "#ef4444" if sym in "♥♦" else "#0b1020"
        s.append(f'<g class="fan" style="--a:{ang}deg;animation-delay:{i * .12:.2f}s">'
                 f'<rect x="{CX - 30}" y="{CY - 50}" width="60" height="90" rx="8" fill="#f8fafc" stroke="{c1}" stroke-width="2"/>'
                 f'<text x="{CX}" y="{CY + 8}" text-anchor="middle" font-size="30" fill="{col}">{sym}</text></g>')
    return "".join(s)


def m_road(c1, c2):
    s = [f'<path d="M{CX - 40} {CY - 85} L{CX - 95} {CY + 85} L{CX + 95} {CY + 85} L{CX + 40} {CY - 85} Z" fill="#0b1020" fill-opacity=".7" stroke="{c2}" stroke-opacity=".5"/>']
    s.append(f'<line x1="{CX}" y1="{CY - 85}" x2="{CX}" y2="{CY + 85}" stroke="#fde047" stroke-width="4" stroke-dasharray="14 14">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur=".6s" repeatCount="indefinite"/></line>')
    for i, y in enumerate((-60, -20, 25)):
        s.append(f'<line x1="{CX - 80}" y1="{CY + y}" x2="{CX - 110}" y2="{CY + y}" stroke="{c1}" stroke-width="2" stroke-linecap="round" class="speed" style="animation-delay:{i * .2:.1f}s"/>')
        s.append(f'<line x1="{CX + 80}" y1="{CY + y + 10}" x2="{CX + 110}" y2="{CY + y + 10}" stroke="{c1}" stroke-width="2" stroke-linecap="round" class="speed" style="animation-delay:{i * .2 + .1:.1f}s"/>')
    s.append(f'<text x="{CX}" y="{CY + 55}" text-anchor="middle" font-size="34" class="bob">🏎️</text>')
    return "".join(s)


def m_chess(c1, c2):
    s = []
    size = 22
    ox, oy = CX - 2 * size, CY - 2 * size
    for r in range(4):
        for c in range(4):
            fill = c1 if (r + c) % 2 else "#e2e8f0"
            s.append(f'<rect x="{ox + c * size}" y="{oy + r * size}" width="{size}" height="{size}" fill="{fill}" fill-opacity="{.85 if (r + c) % 2 else .9}"/>')
    s.append(f'<rect x="{ox}" y="{oy}" width="{size * 4}" height="{size * 4}" fill="none" stroke="{c2}" stroke-width="2"/>')
    s.append(f'<text x="{ox + size * .5}" y="{oy + size * 3.75}" font-size="20" text-anchor="middle" fill="#0b1020">♞'
             f'<animate attributeName="x" values="{ox + size * .5};{ox + size * 2.5};{ox + size * 1.5};{ox + size * .5}" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{oy + size * 3.75};{oy + size * 2.75};{oy + size * .75};{oy + size * 3.75}" dur="4s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="{CX + 62}" y="{CY - 56}" font-size="22" class="bob">🔥</text>')
    return "".join(s)


def m_tower(c1, c2):
    s = [f'<path d="M{CX - 70} {CY + 20} h18 v-50 h-6 v-12 h8 v8 h6 v-8 h8 v8 h6 v-8 h8 v12 h-6 v50 h18 v40 h-60 z" fill="{c1}" fill-opacity=".85"/>']
    s.append(f'<rect x="{CX - 46}" y="{CY - 25}" width="8" height="12" rx="4" fill="#0b1020"/>')
    for i in range(3):
        s.append(f'<circle r="4" fill="{c2}"><animateMotion dur="1.4s" begin="{i * .45:.2f}s" repeatCount="indefinite" path="M{CX - 35} {CY - 30} Q{CX + 15} {CY - 80} {CX + 70} {CY + 30}"/></circle>')
    for i, dy in enumerate((30, 50)):
        s.append(f'<text y="{CY + dy + 10}" font-size="20">👾<animate attributeName="x" from="{CX + 120}" to="{CX + 45}" dur="{3 + i}s" repeatCount="indefinite"/></text>')
    s.append(f'<rect x="{CX - 100}" y="{CY + 70}" width="200" height="4" rx="2" fill="{c2}" fill-opacity=".5"/>')
    return "".join(s)


def m_particles(c1, c2, core="💀"):
    s = []
    for i in range(8):
        x = CX - 70 + i * 20
        s.append(f'<circle cx="{x}" cy="{CY + 70}" r="{3 + i % 3}" fill="{c1 if i % 2 else c2}" class="rise" style="animation-delay:{i * .35:.2f}s"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="42" fill="{c1}" fill-opacity=".18" class="pulse"/>')
    s.append(f'<text x="{CX}" y="{CY + 14}" text-anchor="middle" font-size="40" class="bob">{core}</text>')
    return "".join(s)


def m_cube(c1, c2):
    # isometric cube with rotating hue + floating furniture glyphs
    a = 50
    top = f"M{CX} {CY - a} L{CX + a} {CY - a / 2} L{CX} {CY} L{CX - a} {CY - a / 2} Z"
    left = f"M{CX - a} {CY - a / 2} L{CX} {CY} L{CX} {CY + a} L{CX - a} {CY + a / 2} Z"
    right = f"M{CX + a} {CY - a / 2} L{CX} {CY} L{CX} {CY + a} L{CX + a} {CY + a / 2} Z"
    s = [f'<g class="bob"><path d="{top}" fill="{c2}" fill-opacity=".9"/><path d="{left}" fill="{c1}" fill-opacity=".85"/><path d="{right}" fill="{c1}" fill-opacity=".55"/>'
         f'<path d="{top} {left} {right}" fill="none" stroke="#fff" stroke-opacity=".35"/></g>']
    for i, (g, dx, dy) in enumerate([("🛋️", -85, -55), ("🪴", 70, -60), ("💡", 75, 55)]):
        s.append(f'<text x="{CX + dx}" y="{CY + dy}" font-size="22" class="float" style="animation-delay:{i * .7:.1f}s">{g}</text>')
    return "".join(s)


def m_curve(c1, c2):
    s = [f'<line x1="{CX - 85}" y1="{CY + 70}" x2="{CX + 85}" y2="{CY + 70}" stroke="{c2}" stroke-opacity=".4"/>',
         f'<line x1="{CX - 85}" y1="{CY - 75}" x2="{CX - 85}" y2="{CY + 70}" stroke="{c2}" stroke-opacity=".4"/>']
    pts = [(CX - 80 + i * 8, CY - 65 + 130 * (1 - math.exp(-i / 5)) + (6 * math.sin(i * 1.7))) for i in range(21)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    s.append(f'<path d="{d}" fill="none" stroke="url(#g2)" stroke-width="3" stroke-linecap="round" stroke-dasharray="600" class="draw"/>')
    s.append(f'<text x="{CX + 20}" y="{CY - 45}" font-family="{MONO}" font-size="12" fill="{c2}">loss ↓</text>')
    s.append(f'<text x="{CX + 20}" y="{CY - 28}" font-family="{MONO}" font-size="11" fill="#94a3b8">LoRA · QLoRA</text>')
    return "".join(s)


def m_forge(c1, c2):
    s = [f'<path d="M{CX - 60} {CY + 20} h120 l-20 25 h-80 z" fill="{c1}" fill-opacity=".8"/>',
         f'<rect x="{CX - 25}" y="{CY + 45}" width="50" height="30" fill="{c1}" fill-opacity=".6"/>']
    for i in range(10):
        ang = -150 + i * 12
        dx = 70 * math.cos(math.radians(ang))
        dy = 70 * math.sin(math.radians(ang))
        s.append(f'<circle cx="{CX}" cy="{CY + 15}" r="2.5" fill="{"#fde047" if i % 2 else c2}">'
                 f'<animate attributeName="cx" values="{CX};{CX + dx:.1f}" dur="1.1s" begin="{i * .11:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{CY + 15};{CY + 15 + dy:.1f}" dur="1.1s" begin="{i * .11:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;0" dur="1.1s" begin="{i * .11:.2f}s" repeatCount="indefinite"/></circle>')
    s.append(f'<text x="{CX + 8}" y="{CY - 5}" font-size="30" class="hammer">🔨</text>')
    return "".join(s)


def m_sweep(c1, c2):
    s = []
    for i in range(9):
        y = CY - 40 + (i % 3) * 30
        s.append(f'<rect x="{CX - 60 + (i // 3) * 22}" y="{y}" width="14" height="14" rx="3" fill="{c2 if i % 2 else c1}" class="dust" style="animation-delay:{i * .2:.1f}s"/>')
    s.append(f'<text x="{CX + 25}" y="{CY + 35}" font-size="42" class="brush">🧹</text>')
    return "".join(s)


def m_ledger(c1, c2):
    s = [f'<rect x="{CX - 55}" y="{CY - 75}" width="110" height="150" rx="10" fill="#f8fafc" fill-opacity=".95"/>',
         f'<rect x="{CX - 55}" y="{CY - 75}" width="110" height="26" rx="10" fill="{c1}"/>',
         f'<text x="{CX}" y="{CY - 57}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#fff" font-weight="700">GST BILL</text>']
    for i in range(5):
        y = CY - 35 + i * 18
        s.append(f'<rect x="{CX - 42}" y="{y}" width="{50 + (i * 13) % 30}" height="6" rx="3" fill="#94a3b8" class="type" style="animation-delay:{i * .4:.1f}s"/>')
        s.append(f'<rect x="{CX + 22}" y="{y}" width="20" height="6" rx="3" fill="{c1}" class="type" style="animation-delay:{i * .4 + .2:.1f}s"/>')
    s.append(f'<text x="{CX}" y="{CY + 66}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{c1}">₹ TOTAL</text>')
    s.append(f'<text x="{CX + 55}" y="{CY - 70}" font-size="24" class="bob">🧾</text>')
    return "".join(s)


# ---------------------------------------------------------------- projects
PROJECTS = [
    # slug, emoji, title, tagline lines, chips, colours, motif, status
    ("ai-interview-coach", "🎯", "AI Interview Coach",
     ["AI panel from dev to CEO, live", "proctoring & offline compilers"],
     ["MAUI", "Local LLMs", "SignalR"], ("#7c5cff", "#22d3ee"), m_radar, "IN DEVELOPMENT"),
    ("custom-llm-studio", "🧠", "Custom LLM Studio",
     ["Train models from scratch, build", "scope-locked agents & bots"],
     [".NET", "LLM Training", "Agents"], ("#a855f7", "#f472b6"), m_neural, "IN DEVELOPMENT"),
    ("offline-agent-platform", "🤖", "Offline Agents",
     ["100% offline multi-agent platform", "with RAG & any database"],
     ["Clean Arch", "DDD", "Ollama", "RAG"], ("#06b6d4", "#3b82f6"), lambda a, b: m_orbit(a, b, "🤖"), "IN DEVELOPMENT"),
    ("offline-local-ai-trainer", "🧪", "Local AI Trainer",
     ["Test Ollama models, manage data,", "orchestrate LoRA fine-tuning"],
     [".NET 10", "Blazor Hybrid", "Python"], ("#10b981", "#22d3ee"), m_curve, "IN DEVELOPMENT"),
    ("llm-forge", "⚒️", "LLM Forge",
     ["Run & fine-tune local LLMs", "on Android & Windows, offline"],
     ["MAUI", "Android", "Windows"], ("#f97316", "#f43f5e"), m_forge, "IN DEVELOPMENT"),
    ("design-studio-3d", "🏠", "Design Studio 3D",
     ["Interior & exterior 3D design", "with an on-device AI assistant"],
     ["MAUI", "3D", "Local LLM"], ("#ec4899", "#8b5cf6"), m_cube, "IN DEVELOPMENT"),
    ("kirana-ledger", "🧾", "Kirana Ledger",
     ["SaaS for Indian general stores —", "GST billing, stock & udhar"],
     ["Blazor", "MudBlazor", "MAUI"], ("#16a34a", "#84cc16"), m_ledger, "IN DEVELOPMENT"),
    ("last-pride-standing", "🏰", "Last Pride Standing",
     ["Endless offline tower defence —", "Tower Defence edition"],
     ["C#", "MonoGame", "Windows"], ("#eab308", "#f97316"), m_tower, "LIVE ON MICROSOFT STORE"),
    ("rook-and-roast", "♟️", "Rook & Roast",
     ["Self-learning, always-hard chess AI", "that roasts every move you make"],
     ["MAUI", "Win", "Android", "iOS"], ("#64748b", "#f97316"), m_chess, "IN DEVELOPMENT"),
    ("redline-rush", "🏎️", "Redline Rush",
     ["Arcade racing — one C# codebase", "for Windows, Android & iOS"],
     ["MonoGame", "C#"], ("#ef4444", "#f59e0b"), m_road, "IN DEVELOPMENT"),
    ("card-hero-battle", "⚔️", "Card Hero Battle",
     ["Competitive hero card battler,", "LAN & online ranked matches"],
     ["Stride", ".NET 10", "ASP.NET Core"], ("#6366f1", "#ef4444"), lambda a, b: m_cards(a, b, ("⚔", "🛡", "★", "⚡")), "IN DEVELOPMENT"),
    ("royal-sweep", "🃏", "Royal Sweep",
     ["Classic Indian Seep — vs AI,", "LAN & room-code online"],
     [".NET 10", "MAUI"], ("#b45309", "#facc15"), m_cards, "IN DEVELOPMENT"),
    ("bonecaller", "💀", "BoneCaller",
     ["Necromancer action game — raise", "your undead army"],
     ["C#", "Windows", "Android"], ("#22c55e", "#a855f7"), m_particles, "IN DEVELOPMENT"),
    ("mypanditg", "🕉️", "MyPanditG",
     ["Offline panchang, kundali,", "matching & puja vidhi"],
     ["MAUI", "Android", "Windows"], ("#f97316", "#facc15"), m_mandala, "IN DEVELOPMENT"),
    ("doomsday", "☢️", "Doomsday",
     ["Offline survival handbook —", "works when nothing else does"],
     ["MAUI", "Android", "Windows"], ("#84cc16", "#eab308"), m_rings, "IN DEVELOPMENT"),
    ("cleansweep", "🧹", "CleanSweep",
     ["Mobile cache cleaner — reclaim", "space in one tap"],
     [".NET MAUI", "Android"], ("#0ea5e9", "#22d3ee"), m_sweep, "IN DEVELOPMENT"),
]


def card(slug, emoji, title, lines, chips, colours, motif, status):
    c1, c2 = colours
    live = status.startswith("LIVE")
    pill_col = "#22c55e" if live else c1
    pill_w = 30 + len(status) * 7.6
    chip_svg, x = [], 28
    for ch in chips:
        w = 16 + len(ch) * 7
        chip_svg.append(f'<rect x="{x}" y="226" width="{w}" height="24" rx="12" fill="{c1}" fill-opacity=".18" stroke="{c1}" stroke-opacity=".6"/>'
                        f'<text x="{x + w / 2}" y="242" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#e2e8f0">{esc(ch)}</text>')
        x += w + 8
    tagline = "".join(f'<text x="28" y="{150 + i * 22}" font-family="{FONT}" font-size="14.5" fill="#cbd5e1">{esc(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)} — {esc(' '.join(lines))}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#151b3b"/></linearGradient>
  <linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{c1}"><animate attributeName="stop-color" values="{c1};{c2};{c1}" dur="6s" repeatCount="indefinite"/></stop>
    <stop offset="1" stop-color="{c2}"><animate attributeName="stop-color" values="{c2};{c1};{c2}" dur="6s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="{c1}" stop-opacity=".45"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c2}" stop-opacity="0"/><stop offset="1" stop-color="{c2}" stop-opacity=".55"/></linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <style>
    .in   {{ animation: in .9s ease-out backwards; }}
    @keyframes in {{ from {{ opacity:0; transform: translateY(10px); }} }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ 0%,100% {{ opacity:.55; transform: scale(.9); }} 50% {{ opacity:1; transform: scale(1.12); }} }}
    .spin {{ animation: spin 3s linear infinite; transform-origin: {CX}px {CY}px; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .blip {{ animation: blip 2.7s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes blip {{ 0% {{ opacity:0; transform: scale(.4); }} 15% {{ opacity:1; transform: scale(1.4); }} 100% {{ opacity:0; }} }}
    .ripple {{ animation: ripple 3s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes ripple {{ from {{ transform: scale(1); opacity:.9; }} to {{ transform: scale(4.2); opacity:0; }} }}
    .grow {{ animation: grow 2.8s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: bottom; }}
    @keyframes grow {{ from {{ transform: scaleY(.35); }} to {{ transform: scaleY(1); }} }}
    .draw {{ animation: draw 4s ease-in-out infinite; }}
    @keyframes draw {{ 0% {{ stroke-dashoffset: 600; }} 60%,100% {{ stroke-dashoffset: 0; }} }}
    .fan {{ animation: fan 3.2s ease-in-out infinite alternate; transform-origin: {CX}px {CY + 70}px; }}
    @keyframes fan {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(var(--a)); }} }}
    .bob {{ animation: bob 2.2s ease-in-out infinite; }}
    @keyframes bob {{ 50% {{ transform: translateY(-6px); }} }}
    .float {{ animation: float 3.6s ease-in-out infinite; }}
    @keyframes float {{ 50% {{ transform: translateY(-10px); opacity:.7; }} }}
    .speed {{ animation: speed .9s linear infinite; }}
    @keyframes speed {{ from {{ transform: translateY(-30px); opacity:0; }} 50% {{ opacity:1; }} to {{ transform: translateY(40px); opacity:0; }} }}
    .rise {{ animation: rise 2.8s ease-in infinite; }}
    @keyframes rise {{ from {{ transform: translateY(0); opacity:0; }} 20% {{ opacity:1; }} to {{ transform: translateY(-140px); opacity:0; }} }}
    .hammer {{ animation: hammer 1.1s ease-in-out infinite; transform-box: fill-box; transform-origin: 80% 80%; }}
    @keyframes hammer {{ 0%,100% {{ transform: rotate(0); }} 40% {{ transform: rotate(-35deg); }} }}
    .dust {{ animation: dust 2.6s ease-in infinite; }}
    @keyframes dust {{ 0%,30% {{ transform: translate(0,0); opacity:1; }} 100% {{ transform: translate(-60px,-50px) rotate(90deg); opacity:0; }} }}
    .brush {{ animation: brush 1.3s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: top; }}
    @keyframes brush {{ from {{ transform: rotate(18deg); }} to {{ transform: rotate(-18deg); }} }}
    .type {{ animation: type 3.5s ease-out infinite; transform-box: fill-box; transform-origin: left; }}
    @keyframes type {{ 0% {{ transform: scaleX(0); }} 25%,100% {{ transform: scaleX(1); }} }}
    .scan {{ animation: scan 5s linear infinite; }}
    @keyframes scan {{ from {{ transform: translateY(-80px); }} to {{ transform: translateY({H}px); }} }}
    .live {{ animation: blink 1.4s ease-in-out infinite; }}
    @keyframes blink {{ 50% {{ opacity:.25; }} }}
  </style>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <circle cx="{CX}" cy="{CY}" r="150" fill="url(#glow)"/>
  <g>{motif(c1, c2)}</g>
  <rect class="scan" x="0" y="0" width="{W}" height="80" fill="url(#scan)"/>
  <g class="in">
    <rect x="28" y="28" width="{pill_w:.0f}" height="22" rx="11" fill="{pill_col}" fill-opacity=".18" stroke="{pill_col}" stroke-opacity=".7"/>
    <circle cx="40" cy="39" r="4" fill="{pill_col}" class="live"/>
    <text x="50" y="43" font-family="{MONO}" font-size="11" font-weight="700" fill="{pill_col}" letter-spacing=".5">{esc(status)}</text>
  </g>
  <g class="in" style="animation-delay:.2s">
    <text x="28" y="105" font-family="{FONT}" font-size="26" font-weight="800" fill="#fff">{emoji} {esc(title)}</text>
  </g>
  <g class="in" style="animation-delay:.4s">{tagline}</g>
  <g class="in" style="animation-delay:.6s">{"".join(chip_svg)}</g>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#bd)" stroke-width="2"/>
</svg>'''


for p in PROJECTS:
    with open(os.path.join(OUT, p[0] + ".svg"), "w", encoding="utf-8") as f:
        f.write(card(*p))


# ---------------------------------------------------------------- tech marquee
TECH = ["C#", ".NET 10", "ASP.NET Core", "Web API", "Blazor", ".NET MAUI", "EF Core", "LINQ", "SignalR", "gRPC", "OData",
        "SQL Server", "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Azure", "Key Vault", "Blob Storage", "App Service",
        "Docker", "Kubernetes", "CI/CD", "GitHub Actions", "React", "Angular", "TypeScript", "MudBlazor", "DevExpress",
        "MonoGame", "Stride", "Ollama", "Local LLMs", "RAG", "LoRA / QLoRA", "Hugging Face", "Python", "AI Agents",
        "AES-256-GCM", "JWT / JWE", "2FA / OTP", "Microsoft Graph", "CQRS", "DDD", "Microservices", "MSTest", "TDD"]
cols = ["#7c5cff", "#22d3ee", "#a78bfa", "#38bdf8", "#f472b6", "#34d399"]


def row(items, y, dur, reverse=False):
    x, parts = 0, []
    for i, t in enumerate(items):
        w = 26 + len(t) * 8.2
        c = cols[i % len(cols)]
        parts.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="17" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".55"/>'
                     f'<text x="{x + w / 2:.0f}" y="{y + 22}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#e2e8f0">{esc(t)}</text>')
        x += w + 12
    total = x
    body = "".join(parts)
    frm, to = (f"-{total:.0f}", "0") if reverse else ("0", f"-{total:.0f}")
    return (f'<g><animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" dur="{dur}s" repeatCount="indefinite"/>'
            f'{body}<g transform="translate({total:.0f} 0)">{body}</g></g>')


half = len(TECH) // 2
marquee = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110" role="img" aria-label="Tech stack: {esc(', '.join(TECH))}">
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".06" stop-color="#fff" stop-opacity="1"/>
    <stop offset=".94" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="1200" height="110" fill="url(#fade)"/></mask>
  <clipPath id="c"><rect width="1200" height="110" rx="16"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="1200" height="110" fill="#0b1020"/>
  <g mask="url(#m)">
    {row(TECH[:half], 12, 60)}
    {row(TECH[half:], 62, 70, reverse=True)}
  </g>
</g>
</svg>'''
with open(os.path.join(ROOT, "assets", "tech-marquee.svg"), "w", encoding="utf-8") as f:
    f.write(marquee)

print(f"wrote {len(PROJECTS)} cards + tech marquee")
