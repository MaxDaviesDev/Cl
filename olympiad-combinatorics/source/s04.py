from lib import *

teach = r"""
<p>Many problems describe a <b>process</b>: a board of numbers, a set of coins, a robot that moves, and a rule for what
one move does. Then they ask whether some target can ever be reached. If the answer is “no”, you can't try every
sequence of moves: there are infinitely many. Instead, you find a quantity that the moves <i>cannot change</i>.</p>

""" + theorem("the invariant principle",
r"""<p>An <b>invariant</b> is a quantity that every move leaves unchanged. If an invariant has one value at the start and
a different value at the target, then the target can never be reached, whatever moves are made.</p>""") + r"""

""" + example(4, "parity of a count",
r"""Seven coins lie on a table, all heads up. A move is to turn over exactly two coins. Can you reach a position with all
seven coins tails up?""",
r"""<p><b>What does one move do?</b> Turning over two coins changes the number of heads by $-2$ (two heads become tails),
$+2$ (two tails become heads) or $0$ (one of each).</p>
<p><b>Invariant.</b> In every case the number of heads changes by an even number, so its <b>parity</b> never changes.</p>
<p><b>Compare.</b> At the start there are 7 heads (odd). The target has 0 heads (even). So the target is unreachable.</p>""") + r"""

""" + example(4, "a colouring invariant",
r"""A knight starts on a corner of a chessboard. Can it return to the same square after exactly 25 moves?""",
r"""<p>Every knight move goes 2 squares one way and 1 the other, so $i+j$ (row plus column) changes by $\pm1$ or $\pm3$, an odd
number. So each move changes the colour of the knight's square. After 25 moves (odd) the knight is on the opposite colour
from where it started, so it can't be on the starting square. <b>No.</b></p>
<p>Here the invariant is “colour of the square, compared with the parity of the number of moves made”.</p>""") + r"""

<h2>How to find an invariant</h2>
<p>Write down exactly what <i>one move</i> does to the configuration. Then try natural quantities: the sum, the number of
odd entries, the sum mod $k$, the sum of squares, the product. Test each against your description of a move. Often
nothing is quite invariant, but a <b>combination</b> is: two quantities that change by the same amount have an invariant
difference.</p>

""" + example(4, "combining two quantities",
r"""The numbers $1,2,\dots,20$ are written on a board. A move is to erase two numbers $a,b$ and write $a+b-1$. What number
remains after 19 moves?""",
r"""<p><b>What one move does.</b> The sum $S$ of the numbers goes down by exactly 1, and the count $c$ of numbers goes down by
exactly 1.</p>
<p><b>Invariant.</b> So $S-c$ never changes. At the start, $S-c=210-20=190$.</p>
<p><b>At the end.</b> One number $z$ remains, so $S-c=z-1$. Hence $z-1=190$, and the final number is always
$\mathbf{191}$, whatever order the moves are made in.</p>""") + r"""

""" + why("a proof by invariant is airtight",
r"""<p>Suppose $Q$ is invariant. After any number of moves $Q$ still has its starting value, by induction on the number of
moves (each move keeps it the same). So every reachable configuration has that value of $Q$. A configuration with a
different value of $Q$ is never reachable. There's no need to think about clever sequences of moves at all.</p>""") + r"""

""" + method("find what doesn't change",
r"""<ul>
<li>Write down precisely what one move does.</li>
<li>Try: <b>parity</b> of a sum or count; a sum or difference <b>mod $k$</b>; a <b>sum of squares</b>; a <b>product</b>; a
<b>colouring</b> count (Section 6).</li>
<li>If a quantity changes in a controlled way, look for a combination (a difference, a ratio) that doesn't.</li>
<li>Try your candidate on small examples before writing the proof.</li>
</ul>""") + trap(r"""<p>An invariant proves <b>impossibility</b>. It does not, on its own, prove that a target with the right value is
reachable; that needs an explicit sequence of moves. If the question is “can we reach X?” and the invariant agrees at the
start and at X, you have proved nothing yet.</p>""") + check([
r"""The numbers $1,2,\dots,9$ are on a board. A move: replace two numbers by their sum. Can 50 ever appear as the last number?""",
r"""Each cell of a $3\times3$ grid holds $0$. A move: add 1 to two cells that share a side. Can all nine cells end up equal to 1?""",
r"""A move replaces a pair $(a,b)$ by $(a+2b,\ b)$. Starting from $(1,2)$, can you reach $(4,2)$?"""],
[r"""No: the sum $45$ is invariant""", r"""No: each move adds 2 to the total, which stays even, but 9 is odd""",
 r"""No: $a$ stays odd (it changes by $2b$)"""])

Q = []
Q.append(dict(id="4.1", tag="parity",
stmt=r"""The numbers $1,2,\dots,10$ are written on a board. A move: erase two numbers $a,b$ and write $|a-b|$. After nine moves
one number remains. Prove that it is odd.""",
hint=r"""How does the parity of the sum of all numbers on the board change?""",
key=r"""$a+b$ and $|a-b|$ have the same parity, so the parity of the total sum never changes.""",
sol=r"""<p>Let $S$ be the sum of the numbers on the board. A move replaces $a+b$ by $|a-b|$ in $S$. Since
$a+b-|a-b|=2\min(a,b)$ is even, the parity of $S$ is unchanged. Initially $S=1+\dots+10=55$, which is odd. At the end $S$
is the single remaining number, so it is odd. $\blacksquare$</p>"""))

Q.append(dict(id="4.2", tag="mod 3",
stmt=r"""An island has 13 red, 15 green and 17 blue chameleons. When two chameleons of different colours meet, both change to
the third colour. Can all the chameleons eventually be the same colour?""",
hint=r"""Look at the differences of the counts, mod 3.""",
key=r"""Each meeting changes the counts by $(-1,-1,+2)$ in some order. Every pairwise difference then changes by $0$ or
$\pm3$, so the differences mod 3 are invariant.""",
sol=r"""<p>Let the counts be $(r,g,b)$. A meeting of red and green gives $(r-1,g-1,b+2)$. Then $r-g$ is unchanged, and $g-b$
and $r-b$ change by $-3$. The other two kinds of meeting are similar. So every difference $r-g$, $g-b$, $r-b$ is invariant
mod 3.</p>
<p>Initially $r-g=-2\equiv1$, $g-b=-2\equiv1$, $r-b=-4\equiv2\pmod3$. None is 0.</p>
<p>If all 45 chameleons were one colour, two of the counts would be 0, and their difference would be $0\equiv0\pmod 3$.
Contradiction.</p>""",
answer=r"""No."""))

Q.append(dict(id="4.3", tag="sum of squares",
stmt=r"""A pair of real numbers $(a,b)$ may be replaced by $\left(\dfrac{a+b}{\sqrt2},\ \dfrac{a-b}{\sqrt2}\right)$. Starting from
$(3,4)$, can we reach $(4,6)$?""",
hint=r"""Compute $a^2+b^2$ before and after a move.""",
key=r"""The move is a rotation followed by a reflection, which preserves distance from the origin, so $a^2+b^2$ is
invariant.""",
sol=r"""<p>$$\left(\frac{a+b}{\sqrt2}\right)^2+\left(\frac{a-b}{\sqrt2}\right)^2=\frac{(a^2+2ab+b^2)+(a^2-2ab+b^2)}{2}=a^2+b^2.$$
So $a^2+b^2$ is invariant. It equals $9+16=25$ at the start and $16+36=52$ at the target.</p>""",
answer=r"""No."""))

Q.append(dict(id="4.4", tag="product invariant",
stmt=r"""The numbers $1,2,\dots,n$ are written on a board. A move: erase two numbers $a,b$ and write $a+b+ab$. Find the number
that remains at the end, and show it doesn't depend on the order of the moves.""",
hint=r"""$a+b+ab=(1+a)(1+b)-1$.""",
key=r"""$a+b+ab+1=(1+a)(1+b)$. So the product of $(1+x)$ over all numbers $x$ on the board is unchanged by every move.""",
sol=r"""<p>Let $P=\prod(1+x)$, over all numbers $x$ on the board. A move removes the factors $(1+a)(1+b)$ and adds the factor
$1+(a+b+ab)=(1+a)(1+b)$. So $P$ is invariant. Initially $P=2\cdot3\cdots(n+1)=(n+1)!$. At the end, with one number $z$
left, $P=1+z$. So $z=(n+1)!-1$, whatever the order of moves.</p>""",
answer=r"""$(n+1)!-1$."""))

SECTION = dict(num=4, title="Invariants",
               blurb="parity, sums mod $k$, sums of squares, products: what a move can't change",
               intro="To show a target is unreachable, find something the moves can't change.", teach=teach, questions=Q)
