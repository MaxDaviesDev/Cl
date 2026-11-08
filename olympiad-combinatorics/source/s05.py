from lib import *

def crossing():
    # two crossing segments R1B1, R2B2 and the uncrossed swap
    return ('<svg width="300" height="120" viewBox="0 0 300 120" font-family="KaTeX_Main" font-size="12">'
            '<g transform="translate(10,10)">'
            '<line x1="10" y1="10" x2="110" y2="90" stroke="#1f2933" stroke-width="1.8"/>'
            '<line x1="10" y1="90" x2="110" y2="10" stroke="#1f2933" stroke-width="1.8"/>'
            '<circle cx="10" cy="10" r="4.5" fill="#c0392b"/><circle cx="10" cy="90" r="4.5" fill="#c0392b"/>'
            '<circle cx="110" cy="90" r="4.5" fill="#2563a8"/><circle cx="110" cy="10" r="4.5" fill="#2563a8"/>'
            '<text x="-6" y="8" font-style="italic">R₁</text><text x="-6" y="102" font-style="italic">R₂</text>'
            '<text x="116" y="102" font-style="italic">B₁</text><text x="116" y="8" font-style="italic">B₂</text>'
            '<text x="66" y="54" font-style="italic">X</text></g>'
            '<text x="150" y="64" font-size="18">→</text>'
            '<g transform="translate(170,10)">'
            '<line x1="10" y1="10" x2="110" y2="10" stroke="#1f2933" stroke-width="1.8"/>'
            '<line x1="10" y1="90" x2="110" y2="90" stroke="#1f2933" stroke-width="1.8"/>'
            '<circle cx="10" cy="10" r="4.5" fill="#c0392b"/><circle cx="10" cy="90" r="4.5" fill="#c0392b"/>'
            '<circle cx="110" cy="90" r="4.5" fill="#2563a8"/><circle cx="110" cy="10" r="4.5" fill="#2563a8"/>'
            '</g></svg>')

teach = r"""
<p>Two closely related ideas. The <b>extremal principle</b>: look at the biggest, smallest, longest or “best” object, and
use the fact that it is extreme. The <b>monovariant</b>: to show a process stops, find a quantity that always moves in
one direction and can't do so for ever.</p>

<h2>The extremal principle</h2>
<p>If you are asked to prove that something exists, or that a configuration has some property, consider an
<i>extreme</i> one: the player with the most wins, the longest path, the arrangement with the smallest total. Being
extreme gives you extra information for free, and it's often exactly the information you need.</p>

""" + example(5, "the player with the most wins",
r"""In a tournament every pair of players plays once, and there are no draws. Prove that there is a player $X$ such that
every other player either lost to $X$, or lost to someone who lost to $X$.""",
r"""<p><b>Pick the extreme object.</b> Let $X$ be a player with the most wins (there are finitely many players, so this
exists).</p>
<p><b>Use it.</b> Suppose some player $Y$ did <i>not</i> lose to $X$, and did not lose to anyone who lost to $X$. Then
$Y$ beat $X$, and $Y$ also beat every player that $X$ beat (since $Y$ didn't lose to any of them). So $Y$ has at least all
of $X$'s wins, plus the win against $X$: more wins than $X$. That contradicts the choice of $X$. $\blacksquare$</p>
<p><b>Lesson.</b> We never had to <i>find</i> $X$ by searching. Choosing the extreme object and arguing by contradiction
did all the work.</p>""") + r"""

""" + example(5, "a longest path",
r"""In a finite graph, every vertex has degree at least 2. Prove that the graph contains a cycle.""",
r"""<p>Take a <b>longest path</b> $v_0v_1\dots v_\ell$ (paths don't repeat vertices; there are finitely many, so a longest one
exists). The end $v_0$ has at least 2 neighbours, so it has a neighbour $w\ne v_1$. If $w$ were not on the path,
$wv_0v_1\dots v_\ell$ would be a longer path. So $w=v_i$ for some $i\ge2$, and $v_0v_1\dots v_iv_0$ is a cycle.
$\blacksquare$</p>""") + r"""

""" + trap(r"""<p>Make sure the extreme object <b>exists</b>. Any finite set has a largest and smallest element, and any non-empty
set of positive integers has a smallest element. But an infinite set of real numbers may have none: $\{1,\tfrac12,\tfrac13,\dots\}$
has no smallest element. Say in your write-up why the extreme object exists.</p>""") + r"""

<h2>Monovariants</h2>
<p>A <b>monovariant</b> is a quantity that changes in only one direction: every move strictly increases it (or strictly
decreases it). If, in addition, it can take only finitely many values (or it's a non-negative integer that strictly
decreases), then the process <b>must stop</b>.</p>

""" + example(5, "swapping out-of-order neighbours",
r"""A row of $n$ different numbers is given. A move: find two <i>adjacent</i> numbers in the wrong order (bigger on the
left) and swap them. Prove that whatever moves are chosen, the process stops, and that it ends with the numbers in
increasing order.""",
r"""<p><b>Monovariant.</b> Let $I$ be the number of <b>inversions</b>: pairs (not necessarily adjacent) in which the larger
number is to the left of the smaller. Swapping an adjacent out-of-order pair fixes that pair and doesn't change the
relative order of any other pair. So every move decreases $I$ by exactly 1.</p>
<p><b>It stops.</b> $I$ is a non-negative integer, at most $\binom n2$ at the start, so there can be at most $\binom n2$
moves.</p>
<p><b>Where it stops.</b> The process stops only when no adjacent pair is out of order, which means the row is
increasing. $\blacksquare$</p>""") + r"""

""" + why("monovariants force termination",
r"""<p>A strictly decreasing sequence of non-negative integers $Q_0\gt Q_1\gt Q_2\gt\cdots$ has at most $Q_0+1$ terms. More
generally, a quantity that strictly increases at each step can't repeat a value, so if it can take only finitely many
values, there are only finitely many steps.</p>""") + r"""

<h2>The two ideas together</h2>
<p>Very often a single proof can be written either way. “Take the configuration that minimises $Q$. If it weren't good,
a move would decrease $Q$, contradiction” is the extremal form. “Keep making moves that decrease $Q$; this stops, and
when it stops the configuration is good” is the monovariant form. Use whichever reads more cleanly.</p>

""" + method("extremal and monovariant",
r"""<ul>
<li>To prove existence: consider the <b>largest/smallest/longest</b> object, or the configuration <b>minimising</b> a cleverly
chosen total, and show that if it failed you could make something even more extreme.</li>
<li>To prove a process ends: find a quantity that changes <b>strictly in one direction</b> and has <b>finitely many
values</b> (or is a non-negative integer).</li>
<li>Good candidates: a total sum; a number of “bad pairs”; a total length; the number of inversions.</li>
</ul>""") + check([
r"""Why does every finite set of points in the plane have two points at maximal distance?""",
r"""Each of $n$ coins is heads or tails. A move: pick a head that has a tail immediately to its right, and turn both over. Why must this stop?""",
r"""Prove that $\sqrt2$ is irrational using the extremal principle."""],
[r"""finitely many pairs, so one has the largest distance""",
 r"""read H as 1, T as 0; each move replaces 10 by 01, and the binary number decreases""",
 r"""if $\sqrt2=p/q$ with $q$ minimal, then $\sqrt2=(2q-p)/(p-q)$ with $0\lt p-q\lt q$"""])

Q = []
Q.append(dict(id="5.1", tag="extremal",
stmt=r"""Every point of the integer grid $\mathbb Z^2$ is labelled with a positive integer. Each label equals the average of the
labels of its four neighbours. Prove that all labels are equal.""",
hint=r"""Positive integers have a minimum. What happens at a point where the minimum is attained?""",
key=r"""Positive integers have a smallest value $m$. At a point labelled $m$, the four neighbours average to $m$ but are each
at least $m$, so all four equal $m$. This spreads to every point.""",
sol=r"""<p>The labels are positive integers, so there is a smallest label $m$, attained at some point $P$. (This is where
integrality matters: for positive reals the minimum might not exist.)</p>
<p>At any point $X$ with label $m$, the four neighbours have labels $\ge m$ and average exactly $m$. If any neighbour were
$\gt m$, the average would exceed $m$. So all four neighbours have label $m$.</p>
<p>Starting from $P$ and moving one step at a time, every lattice point can be reached, so by induction on the number of
steps, every point has label $m$. $\blacksquare$</p>"""))

Q.append(dict(id="5.2", tag="monovariant",
stmt=r"""Real numbers are written in an $m\times n$ table. A move: change the sign of every entry in one row, or in one column.
Prove that by a sequence of moves you can make every row sum and every column sum non-negative.""",
hint=r"""Do the obvious greedy move. Show the total sum of the table strictly increases.""",
key=r"""Flip any line with a negative sum. That increases the total sum of the table strictly, and the total can take only
finitely many values, so the process stops, at a table with no negative line.""",
sol=r"""<p><b>Procedure.</b> While some row or column has negative sum $-s\lt0$, flip it.</p>
<p><b>Monovariant.</b> Flipping a line with sum $-s$ changes that line's sum to $+s$ and leaves all other entries alone. So
the total sum $T$ of the table increases by $2s\gt0$.</p>
<p><b>Termination.</b> Each entry is always $\pm$ its original value, so there are at most $2^{mn}$ possible tables and $T$
takes finitely many values. A strictly increasing sequence of values from a finite set must stop, so after finitely many
moves no line has negative sum. $\blacksquare$</p>"""))

Q.append(dict(id="5.3", tag="extremal configuration",
stmt=r"""In a parliament, each member has at most three enemies (enmity is mutual). Prove that the parliament can be split into
two houses so that every member has at most one enemy in their own house.""",
hint=r"""Among all splits, take one with the fewest pairs of enemies in the same house.""",
key=r"""Take a split minimising the number $N$ of “enemy pairs in the same house”. If someone had $\ge2$ enemies in their
house, moving them across would reduce $N$.""",
sol=r"""<p>There are finitely many splits, so choose one minimising $N$, the number of pairs of enemies sitting in the same
house.</p>
<p>Suppose some member $X$ has at least 2 enemies in their own house. $X$ has at most 3 enemies altogether, so at most 1 in
the other house. Move $X$ to the other house. The enemy pairs involving $X$ inside a house go from at least 2 to at most 1,
and no other pair is affected. So $N$ strictly decreases, contradicting minimality.</p>
<p>Hence in the minimising split everyone has at most one enemy in their own house. $\blacksquare$</p>"""))

Q.append(dict(id="5.4", tag="minimal total length",
stmt=r"""$n$ red and $n$ blue points are given in the plane, no three collinear. Prove that they can be joined in $n$ red–blue
pairs by segments no two of which cross.""",
hint=r"""Among all pairings, take the one with minimal total length. What would happen if two segments crossed?""",
key=r"""The pairing with smallest total length has no crossings. If $R_1B_1$ and $R_2B_2$ crossed, swapping partners would be
strictly shorter, by the triangle inequality.""",
sol=r"""<p>There are $n!$ red–blue pairings, so one has minimal total length. Suppose in it the segments $R_1B_1$ and $R_2B_2$
cross at a point $X$. Replace them by $R_1B_2$ and $R_2B_1$.</p>""" + fig(crossing()) + r"""
<p>By the triangle inequality,
$$R_1B_2+R_2B_1\lt(R_1X+XB_2)+(R_2X+XB_1)=R_1B_1+R_2B_2.$$
The inequalities are strict because $R_1,X,B_2$ are not collinear. If they were, $B_2$ would lie on line $R_1X$, which is
line $R_1B_1$, putting three points on a line. Similarly for $R_2,X,B_1$. So the new pairing is shorter, a contradiction.
Hence the minimal pairing has no crossings. $\blacksquare$</p>"""))

SECTION = dict(num=5, title="The extremal principle and monovariants",
               blurb="look at the biggest or smallest; find a quantity that only goes one way",
               intro="Extreme objects give free information; one-way quantities force processes to stop.", teach=teach, questions=Q)
