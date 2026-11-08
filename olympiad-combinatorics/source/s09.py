from lib import *

def demo_graph():
    pts = {"a": (0.0, 0.2), "b": (0.45, 0.0), "c": (0.95, 0.25), "d": (0.6, 0.75), "e": (0.1, 0.95), "f": (1.0, 0.95)}
    E = [("a", "b"), ("b", "c"), ("b", "d"), ("c", "d"), ("a", "e"), ("d", "f")]
    lab = {k: (0, -12) for k in pts}
    lab["e"] = (0, 13); lab["f"] = (0, 13); lab["d"] = (-11, 6)
    return graph(pts, E, size=(180, 140), labels=lab)

def tree_graph():
    pts = {"1": (0.5, 0.0), "2": (0.2, 0.45), "3": (0.8, 0.45), "4": (0.05, 1.0), "5": (0.35, 1.0), "6": (0.8, 1.0)}
    return graph(pts, [("1", "2"), ("1", "3"), ("2", "4"), ("2", "5"), ("3", "6")], size=(150, 130))

def bip_graph():
    L = {"x%d" % i: (0.0, i / 3) for i in range(4)}
    R = {"y%d" % i: (1.0, (i + 0.5) / 3) for i in range(3)}
    pts = dict(L); pts.update(R)
    E = [("x0", "y0"), ("x1", "y0"), ("x1", "y1"), ("x2", "y1"), ("x2", "y2"), ("x3", "y2"), ("x0", "y2")]
    return graph(pts, E, size=(130, 130))

def koenig():
    pts = {"N": (0.5, 0.0), "S": (0.5, 1.0), "I": (0.3, 0.5), "E": (1.0, 0.5)}
    lab = {"N": (0, -13), "S": (0, 13), "I": (-13, 0), "E": (13, 0)}
    # multigraph: draw with curves
    W, H = 170, 140
    m = 18
    P = {k: (m + x * (W - 2 * m), m + y * (H - 2 * m)) for k, (x, y) in pts.items()}
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    def curve(a, b, bend):
        (x1, y1), (x2, y2) = P[a], P[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#1f2933" stroke-width="1.8"/>' % (x1, y1, cx, cy, x2, y2))
    curve("N", "I", 0.25); curve("N", "I", -0.25)
    curve("S", "I", 0.25); curve("S", "I", -0.25)
    curve("N", "E", 0); curve("S", "E", 0); curve("I", "E", 0)
    for k, (x, y) in P.items():
        out.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#1f2933" stroke-width="1.6"/>' % (x, y))
        lx, ly = lab[k]
        out.append('<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle" dominant-baseline="central" font-family="KaTeX_Main" font-style="italic">%s</text>' % (x + lx, y + ly, k))
    out.append('</svg>')
    return "".join(out)

def r33():
    pts = polygon_points(5)
    red, blue = "#c0392b", "#2563a8"
    E, col, dash = [], {}, []
    for i in range(5):
        for j in range(i + 1, 5):
            E.append((i, j))
            if (j - i) % 5 in (1, 4):
                col[(i, j)] = red
            else:
                col[(i, j)] = blue
                dash.append((i, j))
    return graph(pts, E, size=(150, 145), colours=col, dashed=dash)

teach = r"""
<p>A huge number of olympiad problems are about things connected to other things: people and friendships, towns and
roads, teams and matches. A <b>graph</b> is the language for all of them. Learning the basic vocabulary and a few facts lets
you strip the story away and see the structure.</p>

<h2>Vocabulary</h2>
""" + figrow(fig(demo_graph(), "a graph with 6 vertices and 6 edges"), fig(tree_graph(), "a tree"), fig(bip_graph(), "a bipartite graph")) + r"""
<ul>
<li>A <b>graph</b> is a set of <b>vertices</b> (dots), some pairs of which are joined by <b>edges</b> (lines). In the
first picture, $b$ and $d$ are <b>adjacent</b> (joined), $a$ and $c$ are not.</li>
<li>The <b>degree</b> of a vertex is the number of edges at it. Above, $\deg b=3$, $\deg e=1$. By the handshake lemma
(Section 7), $\sum\deg v=2|E|$: here $2+3+2+3+1+1=12=2\times6$.</li>
<li>A <b>path</b> is a sequence of distinct vertices, each joined to the next ($e,a,b,d,f$). A <b>cycle</b> is a path that
returns to its start ($b,c,d,b$).</li>
<li>A graph is <b>connected</b> if any two vertices are joined by a path.</li>
<li>A <b>tree</b> is a connected graph with no cycles. A <b>leaf</b> is a vertex of degree 1.</li>
<li>The <b>complete graph</b> $K_n$ has $n$ vertices and all $\binom n2$ possible edges.</li>
<li>A graph is <b>bipartite</b> if its vertices can be split into two groups with every edge going between the groups
(equivalently, it can be coloured with 2 colours so that each edge joins different colours).</li>
</ul>

""" + theorem("facts worth knowing",
r"""<ul>
<li><b>Handshake lemma:</b> $\sum_v\deg v=2|E|$, so the number of odd-degree vertices is even.</li>
<li><b>Trees:</b> every tree on $n$ vertices has exactly $n-1$ edges (Question 9.2), and every tree with at least 2 vertices
has a leaf.</li>
<li><b>Bipartite:</b> a graph is bipartite if and only if it has no cycle of odd length.</li>
<li><b>Euler:</b> a connected graph has a closed walk using every edge exactly once if and only if every vertex has even degree.</li>
</ul>""") + r"""

""" + example(9, "two vertices of the same degree",
r"""Prove that at any party with at least 2 people, two people have the same number of friends at the party.""",
r"""<p><b>Model.</b> People are vertices, friendships are edges. With $n$ people, each degree is one of $0,1,\dots,n-1$: that's
$n$ possible values for $n$ people, so pigeonhole doesn't immediately work.</p>
<p><b>The extra observation.</b> The values $0$ and $n-1$ can't <i>both</i> occur: a person of degree $n-1$ is friends with
everyone, so nobody has degree 0. So the degrees take at most $n-1$ different values, and by pigeonhole two of the $n$ people
share a degree. $\blacksquare$</p>""") + r"""

""" + example(9, "the bridges of Königsberg",
r"""A city has four land areas joined by seven bridges, as in the picture (land areas are vertices, bridges are edges). Can you
take a walk that crosses every bridge exactly once and returns to the start?""",
r"""<p>Each time a closed walk passes through a vertex, it uses one edge to arrive and one to leave. So every vertex is met by an
<b>even</b> number of the walk's edges. A walk using every edge exactly once would therefore need every degree to be even. Here
the degrees are $\deg N=3$, $\deg S=3$, $\deg E=3$, $\deg I=5$: all odd. So it's impossible.</p>
<p>(Even an open walk, ending somewhere else, needs all but at most two degrees to be even. So that's impossible too.)</p>""",
fig(koenig())) + r"""

""" + method("model it as a graph",
r"""<ul>
<li>Decide what the vertices and edges are. Draw the small cases.</li>
<li>Think about <b>degrees</b> (handshake lemma, pigeonhole on degrees).</li>
<li>Think about <b>longest paths</b> (extremal principle: the end of a longest path has all its neighbours on the path).</li>
<li><b>Colour</b> the edges (for “friends or strangers” problems) or the vertices (for bipartite arguments).</li>
<li><b>Count edges two ways</b> (Section 7).</li>
</ul>""") + trap(r"""<p>Be careful about which graph you mean. “Friends” and “strangers” are two different graphs on the same vertices
(complements of each other). In Ramsey-type problems it's clearer to think of <i>one</i> complete graph whose edges are
coloured in two colours.</p>""") + check([
r"""A graph has 7 vertices with degrees $1,2,2,3,3,4,4$. Is that possible?""",
r"""How many edges does $K_{10}$ have?""",
r"""A tree has 4 vertices of degree 3 and all other vertices are leaves. How many leaves are there?"""],
[r"""No: the degree sum 19 is odd""", r"""$45$""", r"""$6$ (if $\ell$ leaves: $12+\ell=2(4+\ell-1)$)"""])

Q = []
Q.append(dict(id="9.1", tag="Ramsey $R(3,3)=6$",
stmt=r"""Prove that among any 6 people there are either 3 mutual friends or 3 mutual strangers. Show this can fail for 5 people.""",
hint=r"""Pick one person. Of the 5 others, at least 3 have the same relationship to them.""",
key=r"""Colour each pair red (friends) or blue (strangers). One person has 5 edges, so at least 3 have the same colour, say red.
Among those 3 people, either some edge is red, completing a red triangle, or all are blue.""",
sol=r"""<p>Colour each pair of people red (friends) or blue (strangers). Fix a person $v$. Of the 5 edges at $v$, at least
$\lceil5/2\rceil=3$ have the same colour; say $va,vb,vc$ are red (the blue case is the same with colours swapped).</p>
<ul>
<li>If any of $ab,bc,ca$ is red, say $ab$, then $v,a,b$ are mutual friends.</li>
<li>Otherwise $ab,bc,ca$ are all blue, and $a,b,c$ are mutual strangers.</li>
</ul>
<p><b>Five is not enough.</b> Seat 5 people round a table; neighbours are friends (red, solid), everyone else strangers (blue,
dashed). Red edges form a 5-cycle and blue edges the “pentagram” 5-cycle; neither contains a triangle.
$\blacksquare$</p>""" + fig(r33())))

Q.append(dict(id="9.2", tag="trees",
stmt=r"""Prove that every tree with $n\ge1$ vertices has exactly $n-1$ edges.""",
hint=r"""First show a tree with at least 2 vertices has a vertex of degree 1 (consider a longest path). Then remove it and use
induction.""",
key=r"""An endpoint of a longest path must be a leaf: another neighbour would give a cycle or a longer path. Removing a leaf leaves
a smaller tree with one fewer edge.""",
sol=r"""<p><b>Lemma: a tree with $n\ge2$ vertices has a leaf.</b> The tree is connected with at least 2 vertices, so it has an edge.
Take a longest path $v_0v_1\dots v_\ell$ ($\ell\ge1$). If $v_0$ had a neighbour $w\ne v_1$: if $w$ is on the path, that gives a
cycle; if not, $wv_0\dots v_\ell$ is a longer path. Both are impossible, so $\deg v_0=1$.</p>
<p><b>Induction on $n$.</b> $n=1$: no edges. For $n\ge2$, remove a leaf $v$ and its edge. What remains is still connected (no path
between two other vertices passes through a degree-1 vertex) and has no cycles, so it's a tree on $n-1$ vertices. By induction
it has $n-2$ edges, so the original has $n-1$. $\blacksquare$</p>"""))

Q.append(dict(id="9.3", tag="Mantel's theorem",
stmt=r"""Prove that a graph with $n$ vertices and more than $\dfrac{n^2}4$ edges contains a triangle. Show the bound is sharp.""",
hint=r"""If there's no triangle, the endpoints of an edge $uv$ have no common neighbour, so $\deg u+\deg v\le n$. Sum over edges,
then use Cauchy–Schwarz or QM–AM.""",
key=r"""Triangle-free means each edge's endpoints share no neighbour, so $\deg u+\deg v\le n$. Summing over edges gives
$\sum\deg^2\le nE$. Cauchy–Schwarz gives $\sum\deg^2\ge(2E)^2/n$. Together, $E\le n^2/4$.""",
sol=r"""<p>Suppose the graph is triangle-free, with $E$ edges and degrees $d_v$.</p>
<p><b>Edge bound.</b> For an edge $uv$, no vertex is adjacent to both $u$ and $v$ (that would make a triangle). The
neighbourhoods of $u$ and $v$ are disjoint subsets of the $n$ vertices, so $d_u+d_v\le n$.</p>
<p><b>Sum over edges.</b> $\sum_{uv\in E}(d_u+d_v)=\sum_vd_v^2$, since vertex $v$ appears in $d_v$ edges. So
$\sum_vd_v^2\le nE$.</p>
<p><b>Cauchy–Schwarz.</b> $\sum_vd_v^2\ge\frac1n\left(\sum_vd_v\right)^2=\frac{(2E)^2}n$. Hence $\frac{4E^2}n\le nE$, i.e.
$E\le\frac{n^2}4$. So more than $\frac{n^2}4$ edges forces a triangle.</p>
<p><b>Sharp.</b> For even $n$, split the vertices into two halves of $\frac n2$ and join every vertex in one half to every vertex in
the other. This has $\frac{n^2}4$ edges, and no triangle, since any triangle would need two vertices in the same half.
$\blacksquare$</p>"""))

SECTION = dict(num=9, title="Graph theory",
               blurb="vertices, edges, degrees, trees, bipartite graphs, Ramsey and Mantel",
               intro="Strip away the story: dots and lines.", teach=teach, questions=Q)
