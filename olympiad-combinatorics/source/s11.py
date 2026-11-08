from lib import *

teach = r"""
<p>“Find the largest (or smallest) possible…” problems are the most common type at BMO1, and the most commonly
half-solved. A complete answer always has <b>two independent parts</b>, and both need proof.</p>

""" + theorem("the two halves of every “find the max”",
r"""<p>To show the maximum is $M$:</p>
<ol>
<li><b>Bound:</b> prove that <i>every</i> valid configuration has size at most $M$.</li>
<li><b>Construction:</b> exhibit <i>one</i> valid configuration of size exactly $M$, and check it is valid.</li>
</ol>
<p>The bound alone doesn't show $M$ is reached; the construction alone doesn't show you can't do better. For a minimum,
swap the roles: prove every configuration has size at least $M$, and give one with exactly $M$.</p>""") + r"""

""" + example(11, "rooks: the simplest case",
r"""What is the largest number of rooks that can be placed on an $8\times8$ board so that no two attack each other (a rook attacks
along its row and column)?""",
r"""<p><b>Bound.</b> Two rooks in the same row attack each other, so each of the 8 rows contains at most one rook: at most 8.</p>
<p><b>Construction.</b> Put rooks on the main diagonal, squares $(1,1),(2,2),\dots,(8,8)$. They are in different rows and
different columns, so none attack each other.</p>
<p><b>Answer: 8.</b> Notice the shape of the bound: we <b>split the board into 8 pieces</b> (rows), each of which can hold at
most one rook. This “partition into pieces with at most one each” is pigeonhole in disguise, and it's the most common way to
prove a bound.</p>""") + r"""

""" + example(11, "no two consecutive",
r"""What is the largest subset of $\{1,2,\dots,20\}$ containing no two consecutive numbers?""",
r"""<p><b>Small cases first.</b> From $\{1,2,3,4\}$ the best is 2, e.g. $\{1,3\}$; from $\{1,\dots,6\}$, 3. It looks like half.</p>
<p><b>Bound.</b> Split $\{1,\dots,20\}$ into the 10 pairs $\{1,2\},\{3,4\},\dots,\{19,20\}$. Each pair is two consecutive numbers,
so a valid subset contains at most one from each pair: at most 10 elements.</p>
<p><b>Construction.</b> The odd numbers $\{1,3,5,\dots,19\}$: 10 numbers, any two differ by at least 2.</p>
<p><b>Answer: 10.</b></p>""") + r"""

""" + example(11, "a minimum problem",
r"""What is the smallest number of squares of an $8\times8$ board that must be marked so that every domino placed on the board
(covering two adjacent squares) covers at least one marked square?""",
r"""<p><b>Bound (at least 32).</b> The board can be tiled by 32 non-overlapping dominoes (e.g. 4 in each row). Each of these
dominoes must cover a marked square, and they don't overlap, so at least 32 squares are marked.</p>
<p><b>Construction (32 works).</b> Mark all 32 black squares of the chessboard colouring. Any domino covers one black and one
white square, so it covers a marked square.</p>
<p><b>Answer: 32.</b> For a minimum, the bound comes from finding many <i>disjoint</i> things that each need their own mark.</p>""") + r"""

<h2>Where do bounds and constructions come from?</h2>
<ul>
<li><b>Bounds:</b> pigeonhole (partition into parts that each contain at most one element); double counting (Section 7);
invariants and colourings; sometimes an averaging argument.</li>
<li><b>Constructions:</b> look at the small cases. The best examples for $n=2,3,4$ usually show a pattern (every other square,
all the odd numbers, the top half). Often the extremal configuration is very regular or symmetric.</li>
<li>The two halves guide each other. If you can't push a construction past $M$, ask <i>what's stopping you</i>: that obstacle
is the bound. If your bound proof has slack, a better construction may exist.</li>
</ul>

""" + trap(r"""<p>A solution that only gives an example, or only proves a bound, is incomplete. At BMO1, this typically scores 2–4 out
of 10. Label the two parts clearly (“Bound.”, “Construction.”) so the marker sees you've done both, and in the construction,
actually <b>verify</b> that your example satisfies the conditions.</p>""") + check([
r"""What is the largest number of bishops on a $4\times4$ board with no two attacking? (Try it.)""",
r"""What is the largest subset of $\{1,\dots,10\}$ with no two elements differing by exactly 5?""",
r"""Fewest squares to mark on a $4\times4$ board so every $1\times2$ domino covers a marked one?"""],
[r"""$6$ (in general $2n-2$)""", r"""$5$: pairs $\{k,k+5\}$; take $1,\dots,5$""", r"""$8$"""])

Q = []
Q.append(dict(id="11.1", tag="kings",
stmt=r"""What is the maximum number of kings that can be placed on an $8\times8$ chessboard so that no two attack each other? (A king
attacks the up to eight squares adjacent to it, including diagonally.)""",
hint=r"""Cut the board into $2\times2$ blocks.""",
key=r"""Any two squares of a $2\times2$ block are adjacent, so each block holds at most one king. That gives 16, and putting one king in
the same corner of every block achieves it.""",
sol=fig(board(8, 8, cell=17, dots=[(r, c) for r in range(0, 8, 2) for c in range(0, 8, 2)],
              thick=[(r, c, r + 2, c + 2) for r in range(0, 8, 2) for c in range(0, 8, 2)])) + r"""
<p><b>Bound.</b> Divide the board into 16 blocks of size $2\times2$. Any two squares in one block are adjacent (horizontally,
vertically or diagonally), so each block contains at most one king. Hence at most 16 kings.</p>
<p><b>Construction.</b> Place a king in the top-left square of every block, i.e. on all squares with odd row and odd column
numbers. Any two of these are at least 2 apart in row or in column, so none attack each other. That's 16 kings.</p>""",
answer=r"""$16$."""))

Q.append(dict(id="11.2", tag="no divisibility",
stmt=r"""What is the largest size of a subset of $\{1,2,\dots,2n\}$ in which no element divides another?""",
hint=r"""Question 3.1(b) gives the bound. For the construction, take the largest numbers.""",
key=r"""Bound: grouping by odd part gives $n$ classes, and each class holds at most one element. Construction: $\{n+1,\dots,2n\}$,
where the smallest multiple of any element is already too big.""",
sol=r"""<p><b>Bound.</b> Group the numbers by odd part: $x=2^km$, $m\in\{1,3,\dots,2n-1\}$, giving $n$ groups. Two numbers in the same
group differ by a power of 2, so one divides the other. So a valid subset has at most one element per group, at most $n$ in
total.</p>
<p><b>Construction.</b> $\{n+1,n+2,\dots,2n\}$ has $n$ elements. If $a\mid b$ with $a\lt b$ in this set, then
$b\ge2a\ge2n+2\gt2n$, which is impossible.</p>""",
answer=r"""$n$."""))

Q.append(dict(id="11.3", tag="residues",
stmt=r"""What is the largest size of a subset of $\{1,2,\dots,50\}$ in which no two distinct elements have a sum divisible by 7?""",
hint=r"""Sort the numbers by remainder mod 7. Which remainder classes can't both be used? How many elements of remainder 0 can there be?""",
key=r"""Two numbers sum to a multiple of 7 iff their remainders are $r$ and $7-r$, or both 0. So from each pair of classes
$\{1,6\},\{2,5\},\{3,4\}$ we use at most one whole class, and at most one multiple of 7.""",
sol=r"""<p><b>Class sizes.</b> Among $1,\dots,50$: remainder 1 occurs 8 times ($1,8,\dots,50$), and each of the remainders $0,2,3,4,5,6$
occurs 7 times.</p>
<p><b>Bound.</b> Let $S$ be valid. If $x,y\in S$ had remainders $r$ and $7-r$ ($r\in\{1,2,3\}$), then $7\mid x+y$. So for each
pair of classes $\{1,6\},\{2,5\},\{3,4\}$, $S$ meets only one class. Also $S$ contains at most one multiple of 7. Hence
$$|S|\le\max(8,7)+\max(7,7)+\max(7,7)+1=23.$$</p>
<p><b>Construction.</b> Take all numbers with remainder 1, 2 or 3, plus the number 7: $8+7+7+1=23$ elements. Remainders of
sums of two distinct elements lie in $\{1+1,1+2,\dots,3+3\}\cup\{0+1,0+2,0+3\}=\{2,3,4,5,6\}\cup\{1,2,3\}$, never 0. And there is
only one multiple of 7.</p>""",
answer=r"""$23$."""))

SECTION = dict(num=11, title="Extremal problems: bound + construction",
               blurb="prove nothing larger works, and give an example that achieves it",
               intro="Two halves, both required.", teach=teach, questions=Q)
