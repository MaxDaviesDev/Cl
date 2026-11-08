"""Small helpers shared by the content files: boxes and SVG pictures."""

def box(kind, title, body):
    return ('<div class="box %s"><div class="boxhead">%s</div><div class="boxbody">%s</div></div>'
            % (kind, title, body))

def theorem(title, body): return box("theorem", "Key fact: " + title, body)
def method(title, body): return box("method", "Method: " + title, body)
def trap(body, title="Common trap"): return box("trap", title, body)
def why(title, body): return box("why", "Why it works: " + title, body)

_ex_counter = {"n": 0, "sec": None}

def example(sec, title, problem, solution, picture=""):
    if _ex_counter["sec"] != sec:
        _ex_counter["sec"] = sec
        _ex_counter["n"] = 0
    _ex_counter["n"] += 1
    head = "Worked example %s.%s &nbsp;<span class=\"extitle\">%s</span>" % (sec, _ex_counter["n"], title)
    return ('<div class="box example"><div class="boxhead">%s</div><div class="boxbody">'
            '<div class="problem">%s</div>%s<div class="exsol">%s</div></div></div>'
            % (head, problem, picture, solution))

def check(items, answers):
    lis = "".join("<li>%s</li>" % i for i in items)
    ans = " &nbsp;·&nbsp; ".join("<b>%d.</b> %s" % (k + 1, a) for k, a in enumerate(answers))
    return ('<div class="box check"><div class="boxhead">Quick check</div><div class="boxbody">'
            '<ol>%s</ol><div class="checkans"><span>Answers: %s</span></div></div></div>' % (lis, ans))

def fig(svg, caption=""):
    cap = '<div class="cap">%s</div>' % caption if caption else ""
    return '<div class="fig">%s%s</div>' % (svg, cap)

def figrow(*figs):
    return '<div class="figrow">%s</div>' % "".join(figs)

# ---------------------------------------------------------------- SVG pictures
INK = "#1f2933"
SHADE = "#aab4bf"
ACCENT = "#c0392b"
BLUE = "#2563a8"

def board(rows, cols, cell=18, fill=None, text=None, chess=False, cross=(), dots=(),
          thick=None, label_axes=False):
    """fill: dict (r,c)->colour; text: dict (r,c)->str; rows/cols 0-indexed from top-left."""
    fill = fill or {}
    text = text or {}
    pad = 16 if label_axes else 2
    W, H = cols * cell + pad + 2, rows * cell + pad + 2
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    for r in range(rows):
        for c in range(cols):
            col = fill.get((r, c))
            if col is None and chess:
                col = SHADE if (r + c) % 2 else "#ffffff"
            col = col or "#ffffff"
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="0.6"/>'
                       % (pad + c * cell, pad + r * cell, cell, cell, col, "#55606b"))
            if (r, c) in text:
                out.append('<text x="%.1f" y="%.1f" font-size="%d" text-anchor="middle" '
                           'dominant-baseline="central" fill="%s" font-family="KaTeX_Main">%s</text>'
                           % (pad + c * cell + cell / 2, pad + r * cell + cell / 2 + 0.5, int(cell * 0.55), INK, text[(r, c)]))
    for (r, c) in cross:
        x, y = pad + c * cell, pad + r * cell
        out.append('<path d="M%d %d L%d %d M%d %d L%d %d" stroke="%s" stroke-width="2"/>'
                   % (x + 4, y + 4, x + cell - 4, y + cell - 4, x + cell - 4, y + 4, x + 4, y + cell - 4, ACCENT))
    for (r, c) in dots:
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
                   % (pad + c * cell + cell / 2, pad + r * cell + cell / 2, cell * 0.28, INK))
    if thick:
        for (r0, c0, r1, c1) in thick:  # rectangles in cell coords, inclusive-exclusive
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2.2"/>'
                       % (pad + c0 * cell, pad + r0 * cell, (c1 - c0) * cell, (r1 - r0) * cell, INK))
    if label_axes:
        for r in range(rows):
            out.append('<text x="8" y="%.1f" font-size="9" text-anchor="middle" dominant-baseline="central" '
                       'fill="#667" font-family="KaTeX_Main">%d</text>' % (pad + r * cell + cell / 2, r + 1))
        for c in range(cols):
            out.append('<text x="%.1f" y="9" font-size="9" text-anchor="middle" fill="#667" '
                       'font-family="KaTeX_Main">%d</text>' % (pad + c * cell + cell / 2, c + 1))
    out.append('</svg>')
    return "".join(out)

def tiling(grid, cell=20, hole_colour="#333"):
    """grid: list of rows of piece ids; draw thick borders between different pieces."""
    R, C = len(grid), len(grid[0])
    p = 2
    W, H = C * cell + 2 * p, R * cell + 2 * p
    palette = ["#dbe7f3", "#f6e3c7", "#dff0dc", "#f1dcea", "#e6e1f5", "#f7f0c6"]
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    for r in range(R):
        for c in range(C):
            v = grid[r][c]
            col = hole_colour if v is None else palette[v % len(palette)]
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#9aa" stroke-width="0.4"/>'
                       % (p + c * cell, p + r * cell, cell, cell, col))
    for r in range(R):
        for c in range(C):
            x, y = p + c * cell, p + r * cell
            if c + 1 < C and grid[r][c] != grid[r][c + 1]:
                out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + cell, y, x + cell, y + cell, INK))
            if r + 1 < R and grid[r][c] != grid[r + 1][c]:
                out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x, y + cell, x + cell, y + cell, INK))
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2.2"/>' % (p, p, C * cell, R * cell, INK))
    out.append('</svg>')
    return "".join(out)

def lattice(m, n, path=None, mark=None, cell=26):
    """Grid of points (0..m) x (0..n); path is a string of 'R'/'U'."""
    p = 14
    W, H = m * cell + 2 * p, n * cell + 2 * p
    X = lambda x: p + x * cell
    Y = lambda y: H - p - y * cell
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    for x in range(m + 1):
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c8ced6" stroke-width="1"/>' % (X(x), Y(0), X(x), Y(n)))
    for y in range(n + 1):
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c8ced6" stroke-width="1"/>' % (X(0), Y(y), X(m), Y(y)))
    if path:
        x = y = 0
        pts = [(X(0), Y(0))]
        for s in path:
            if s == "R": x += 1
            else: y += 1
            pts.append((X(x), Y(y)))
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
                   % (" ".join("%d,%d" % q for q in pts), BLUE))
    for x in range(m + 1):
        for y in range(n + 1):
            out.append('<circle cx="%d" cy="%d" r="2.2" fill="%s"/>' % (X(x), Y(y), INK))
    if mark:
        out.append('<circle cx="%d" cy="%d" r="5" fill="none" stroke="%s" stroke-width="2"/>' % (X(mark[0]), Y(mark[1]), ACCENT))
    out.append('</svg>')
    return "".join(out)

def graph(points, edges, size=(170, 150), labels=None, colours=None, dashed=(), r=4.5):
    """points: dict name->(x,y) in [0,1]^2; edges: list of (a,b); colours: dict edge->colour."""
    W, H = size
    m = 18
    P = {k: (m + x * (W - 2 * m), m + y * (H - 2 * m)) for k, (x, y) in points.items()}
    colours = colours or {}
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    for e in edges:
        a, b = e
        col = colours.get(e, colours.get((b, a), INK))
        da = ' stroke-dasharray="4 3"' if (e in dashed or (b, a) in dashed) else ""
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"%s/>'
                   % (P[a][0], P[a][1], P[b][0], P[b][1], col, da))
    for k, (x, y) in P.items():
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" stroke="%s" stroke-width="1.6"/>' % (x, y, r, INK))
        if labels and k in labels:
            lx, ly = labels[k]
            out.append('<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle" dominant-baseline="central" '
                       'font-family="KaTeX_Main" font-style="italic" fill="%s">%s</text>' % (x + lx, y + ly, INK, k))
    out.append('</svg>')
    return "".join(out)

def polygon_points(n, rot=-90, cx=0.5, cy=0.5, rad=0.5):
    import math
    pts = {}
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        pts[i] = (cx + rad * math.cos(a), cy + rad * math.sin(a))
    return pts
