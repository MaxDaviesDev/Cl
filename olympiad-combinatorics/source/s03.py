from lib import *

def square_split(k, pts=(), size=120):
    c = size / k
    out = ['<svg width="%d" height="%d" viewBox="-4 -4 %d %d">' % (size + 8, size + 8, size + 8, size + 8)]
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="#fff" stroke="#1f2933" stroke-width="1.8"/>' % (size, size))
    for i in range(1, k):
        out.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" stroke="#2563a8" stroke-dasharray="4 3"/>' % (i * c, i * c, size))
        out.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#2563a8" stroke-dasharray="4 3"/>' % (i * c, size, i * c))
    for (x, y) in pts:
        out.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#c0392b"/>' % (x * size, y * size))
    out.append('</svg>')
    return "".join(out)

teach = r"""
<p>The pigeonhole principle sounds too obvious to be useful: if you put more pigeons than boxes, two pigeons share a
box. But it is one of the most powerful tools for “prove that there exist…” problems, because it proves that
something exists <i>without finding it</i>. All the skill is in choosing the boxes.</p>

""" + theorem("the pigeonhole principle",
r"""<p>If more than $k$ objects are put into $k$ boxes, some box contains at least two objects.</p>
<p><b>General form.</b> If $N$ objects go into $k$ boxes, some box contains at least $\lceil N/k\rceil$ objects.</p>
<p><i>Proof.</i> If every box had at most $\lceil N/k\rceil-1$ objects, then since $\lceil N/k\rceil-1\lt N/k$, the total would be
less than $k\cdot N/k = N$. Contradiction.</p>""") + r"""
<p><b>Warm-up.</b> Among 13 people, two have birthdays in the same month (13 people, 12 months). Among 100 people,
some month contains at least $\lceil100/12\rceil=9$ birthdays. Among any 3 integers, two have the same parity (3
integers, 2 parities), so their sum is even.</p>

<h2>Choosing the boxes</h2>
<p>In a real problem nobody tells you what the boxes are. The trick is to work backwards: <i>what would two objects in
the same box need to have in common for me to be finished?</i> Then design the boxes so that sharing a box gives
exactly that.</p>

""" + example(3, "remainders as boxes",
r"""Prove that among any 5 integers, there are 3 whose sum is divisible by 3.""",
r"""<p><b>Boxes.</b> Sort the integers by remainder mod 3: boxes $0,1,2$.</p>
<p><b>Why these boxes?</b> Three numbers from the same box have sum $\equiv 3r\equiv0$. Three numbers from three
different boxes have sum $\equiv0+1+2\equiv0$. So we're done if either some box has 3 numbers, or every box is used.</p>
<p><b>Finish.</b> Suppose no box has 3 numbers, so each box has at most 2. If only two boxes were used, there would be
at most $2+2=4$ numbers, but we have 5. So all three boxes are used. Either way, we find three numbers with sum
divisible by 3. $\blacksquare$</p>
<p><b>Is 5 needed?</b> Yes: $0,0,1,1$ (remainders) has no such triple. Always check whether your bound is sharp.</p>""") + r"""

""" + example(3, "prefix sums",
r"""Prove that for any $n$ integers $a_1,\dots,a_n$, there is a block of consecutive terms $a_{i+1}+a_{i+2}+\dots+a_j$
(with $i\lt j$) whose sum is divisible by $n$.""",
r"""<p><b>The key idea.</b> A block sum is a difference of two prefix sums. Let $S_0=0$ and $S_j=a_1+\dots+a_j$. Then
$a_{i+1}+\dots+a_j=S_j-S_i$.</p>
<p><b>Pigeonhole.</b> The $n+1$ numbers $S_0,S_1,\dots,S_n$ have only $n$ possible remainders mod $n$. So two of them,
$S_i$ and $S_j$ with $i\lt j$, have the same remainder. Then $n\mid S_j-S_i=a_{i+1}+\dots+a_j$. $\blacksquare$</p>
<p><b>Lesson.</b> We had $n$ numbers but needed $n+1$ pigeons. Including $S_0=0$ is the small trick that makes it work.
“Differences of prefix sums” is a standard way to handle consecutive blocks.</p>""") + r"""

""" + example(3, "geometric boxes",
r"""51 points are placed in a unit square. Prove that some 3 of them lie inside a square of side $\tfrac15$.""",
r"""<p>Cut the unit square into a $5\times5$ grid of 25 small squares of side $\frac15$ (points on a dividing line can be
assigned to either neighbouring square). With 51 points and 25 boxes, some small square contains at least
$\lceil51/25\rceil=3$ points. $\blacksquare$</p>""", fig(square_split(5, [(0.07, 0.12), (0.15, 0.05), (0.12, 0.17), (0.5, 0.6), (0.85, 0.3), (0.32, 0.88)], 110))) + r"""

""" + method("pigeonhole checklist",
r"""<ul>
<li><b>Numbers:</b> boxes are remainders mod $k$; pairs $\{1,2\},\{3,4\},\dots$; or classes by odd part ($x=2^a m$, $m$ odd).</li>
<li><b>Geometry:</b> cut the region into small pieces, small enough that two points in the same piece are close.</li>
<li><b>Subsets:</b> there are $2^n$ subsets but only a few possible sums, so two subsets have the same sum.</li>
<li><b>Sequences:</b> label each term with a number (e.g. the length of the longest run starting there); the labels are the boxes.</li>
<li>Count carefully: you need <b>strictly more</b> pigeons than boxes (or use $\lceil N/k\rceil$).</li>
<li>Show the bound is <b>sharp</b>: give an example with one fewer pigeon where the conclusion fails.</li>
</ul>""") + trap(r"""<p>Pigeonhole tells you two objects share a box, but <b>not which ones</b>. Your argument must work for whichever
pair it turns out to be. Also, the boxes must cover every possibility: in geometry, say which box a point on a
boundary belongs to.</p>""") + check([
r"""How many cards must you draw from a standard 52-card deck to be sure of getting two of the same suit?""",
r"""Show that among any 6 integers, two have a difference divisible by 5.""",
r"""A bag has socks of 4 colours. How many must you take out to be sure of 3 of the same colour?"""],
[r"""$5$""", r"""6 integers, 5 remainders mod 5""", r"""$2\cdot4+1=9$"""])

Q = []
Q.append(dict(id="3.1", tag="two classics",
stmt=r"""Let $S$ be a set of $n+1$ numbers chosen from $\{1,2,\dots,2n\}$. Prove that
<br>(a) $S$ contains two numbers that are coprime;
<br>(b) $S$ contains two numbers one of which divides the other.
<br>Show that both statements can fail for $n$ numbers.""",
hint=r"""(a) Boxes $\{1,2\},\{3,4\},\dots$. (b) Write each number as $2^k\cdot m$ with $m$ odd; use the odd part $m$ as the box.""",
key=r"""(a) Pair up consecutive numbers, which are always coprime. (b) Sort by odd part; two numbers with the same odd part
differ by a power of 2, so one divides the other.""",
sol=r"""<p><b>(a)</b> Use the $n$ boxes $\{1,2\},\{3,4\},\dots,\{2n-1,2n\}$. With $n+1$ numbers, two are in the same box, so they
are consecutive integers $t,t+1$. Any common divisor divides $(t+1)-t=1$, so they are coprime.</p>
<p><b>(b)</b> Write each $x\in S$ as $x=2^km$ with $m$ odd. The odd part $m$ is one of $1,3,\dots,2n-1$: only $n$ values.
With $n+1$ numbers, two have the same odd part: $x=2^km$, $y=2^lm$ with $k\lt l$. Then $x\mid y$.</p>
<p><b>Sharpness.</b> $\{2,4,\dots,2n\}$ has $n$ elements, no two coprime. And $\{n+1,\dots,2n\}$ has $n$ elements with no
divisibility: if $a\mid b$ with $a\lt b$, then $b\ge2a\ge2n+2$. $\blacksquare$</p>"""))

Q.append(dict(id="3.2", tag="geometric pigeonhole",
stmt=r"""Five points are placed in a square of side 1 (possibly on the boundary). Prove that two of them are at distance at
most $\frac{\sqrt2}{2}$.""",
hint=r"""Cut the square into four smaller squares.""",
key=r"""Four boxes, five points. The boxes must be small enough that two points in the same box are close: squares of side
$\frac12$ have diameter $\frac{\sqrt2}2$.""",
sol=r"""<p>Divide the square into four closed squares of side $\frac12$ by joining the midpoints of opposite sides. Every point
lies in at least one of them; assign each point to one square containing it. Five points, four squares, so two points
$P,Q$ are in the same small square.</p>
<p>The greatest distance between two points of a square of side $\frac12$ is its diagonal, $\frac{\sqrt2}2$. So
$PQ\le\frac{\sqrt2}{2}$. $\blacksquare$</p>""" + fig(square_split(2, [(0.1, 0.15), (0.38, 0.3), (0.75, 0.2), (0.3, 0.8), (0.8, 0.7)], 110)) + r"""
<p><b>Sharpness.</b> The four corners and the centre show that $\frac{\sqrt2}2$ cannot be improved.</p>"""))

Q.append(dict(id="3.3", tag="IMO 1972 Problem 1",
stmt=r"""Prove that from any set of ten distinct two-digit numbers, one can select two disjoint non-empty subsets with the
same sum.""",
hint=r"""Count the subsets and the possible values of their sums.""",
key=r"""There are more non-empty subsets (1023) than possible sums (at most 981), so two subsets have the same sum. Removing
their common elements makes them disjoint without changing the equality.""",
sol=r"""<p><b>Pigeonhole.</b> The set has $2^{10}-1=1023$ non-empty subsets. Each subset sum is at least $10$ and at most
$10\cdot99=990$, so there are at most $981$ possible sums. Hence two different non-empty subsets $X\ne Y$ have the same
sum.</p>
<p><b>Make them disjoint.</b> Let $X'=X\setminus Y$ and $Y'=Y\setminus X$. Removing the common elements from both subtracts
the same amount from each sum, so $X'$ and $Y'$ still have equal sums, and they are disjoint. Neither is empty: if
$X'=\varnothing$ then $X\subseteq Y$ with $X\ne Y$, so $Y$ has an extra positive element and a larger sum, a contradiction.
Similarly $Y'\ne\varnothing$. $\blacksquare$</p>"""))

Q.append(dict(id="3.4", tag="Erdős–Szekeres",
stmt=r"""Prove that any sequence of $mn+1$ distinct real numbers contains an increasing subsequence of length $m+1$ or a
decreasing subsequence of length $n+1$.""",
hint=r"""Label each term by the length of the longest increasing subsequence starting at it.""",
key=r"""Label each term with $L_i$, the length of the longest increasing subsequence starting at it. If no label exceeds $m$,
there are only $m$ labels for $mn+1$ terms, so $n+1$ terms share a label, and terms sharing a label must decrease.""",
sol=r"""<p>Let the sequence be $x_1,\dots,x_{mn+1}$, and let $L_i$ be the length of the longest increasing subsequence
starting at $x_i$. If some $L_i\ge m+1$ we are done. Otherwise every $L_i\in\{1,\dots,m\}$.</p>
<p><b>Pigeonhole.</b> $mn+1$ terms and $m$ labels, so some label is shared by at least $\lceil(mn+1)/m\rceil=n+1$ terms,
say $x_{i_1},\dots,x_{i_{n+1}}$ with $i_1\lt\dots\lt i_{n+1}$.</p>
<p><b>Same label $\Rightarrow$ decreasing.</b> Take $i\lt j$ with $L_i=L_j$. If $x_i\lt x_j$, then $x_i$ followed by a longest
increasing subsequence from $x_j$ is increasing of length $L_j+1$, so $L_i\ge L_j+1$, a contradiction. So $x_i\gt x_j$
(they are distinct). Hence $x_{i_1}\gt x_{i_2}\gt\dots\gt x_{i_{n+1}}$ is decreasing of length $n+1$. $\blacksquare$</p>
<p><b>Sharpness.</b> $mn$ terms are not enough. Take $n$ blocks, each an increasing run of $m$ numbers, with every block
entirely below the previous one, e.g. for $m=3,n=2$: $4,5,6,1,2,3$.</p>"""))

SECTION = dict(num=3, title="The pigeonhole principle",
               blurb="choosing the boxes: remainders, pairs, regions, subset sums, labels",
               intro="More pigeons than boxes: proving existence without finding the object.", teach=teach, questions=Q)
