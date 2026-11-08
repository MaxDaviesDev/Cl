from lib import *

def ltromino_fig():
    # 8x8 board split into quarters, hole in top-left quarter, central tromino
    fill = {(1, 2): "#333"}
    for rc in [(3, 4), (4, 3), (4, 4)]:
        fill[rc] = "#f6c26b"
    return board(8, 8, cell=16, fill=fill, thick=[(0, 0, 4, 4), (0, 4, 4, 8), (4, 0, 8, 4), (4, 4, 8, 8)])

teach = r"""
<p>Many counting problems are hard to solve directly for size $n$, but easy to solve if you already know the answers for
smaller sizes. That's <b>recursion</b>. Its partner for proofs is <b>induction</b>: prove the result for small cases, then
show how each case follows from smaller ones.</p>

<h2>Recursion: look at the last step</h2>
<p>To find a recurrence, classify the objects of size $n$ by what happens at one end: is the element $n$ used? What does
the last column look like? What was the last move? Each class is usually a smaller copy of the original problem.</p>

""" + example(8, "the Tower of Hanoi",
r"""There are 3 pegs, and $n$ discs of different sizes on the first peg, largest at the bottom. A move takes the top disc
of one peg and puts it on another peg, never on a smaller disc. What is the smallest number of moves needed to move all
$n$ discs to the third peg?""",
r"""<p><b>Small cases.</b> $h_1=1$, $h_2=3$ (small disc aside, big disc across, small disc on top), $h_3=7$.</p>
<p><b>Look at the largest disc.</b> At the moment the largest disc moves, the other $n-1$ discs must all be on the remaining
peg (they can't be on top of it, nor on the peg it's moving to). Getting them there takes at least $h_{n-1}$ moves.
After the largest disc's move, they must all come back on top of it: at least $h_{n-1}$ more. So
$h_n\ge 2h_{n-1}+1$, and this is achievable by doing exactly that. So $h_n=2h_{n-1}+1$.</p>
<p><b>Solve it.</b> The values $1,3,7,15,\dots$ suggest $h_n=2^n-1$. Check by induction: $h_1=1=2^1-1$, and if
$h_{n-1}=2^{n-1}-1$ then $h_n=2(2^{n-1}-1)+1=2^n-1$. ✓</p>
<p><b>Tip.</b> A neat trick for this recurrence: $h_n+1=2(h_{n-1}+1)$, so $h_n+1$ doubles each time.</p>""") + r"""

<h2>Induction</h2>
<p>To prove a statement $P(n)$ for all $n\ge1$:</p>
<ol>
<li><b>Base case:</b> prove $P(1)$.</li>
<li><b>Inductive step:</b> assume $P(n-1)$ (the <i>inductive hypothesis</i>) and use it to prove $P(n)$.</li>
</ol>
<p>Then $P(1)$ holds, so $P(2)$ does, so $P(3)$ does, and so on. In combinatorics, the inductive step usually means:
<i>take an object of size $n$, find a smaller object inside it, and use the hypothesis on that.</i> Or, for constructions:
<i>build the size-$n$ object out of smaller ones.</i></p>

""" + theorem("strong induction",
r"""<p>Sometimes $P(n)$ follows not from $P(n-1)$ but from some earlier case. <b>Strong induction</b> lets you assume
$P(k)$ for <i>all</i> $k\lt n$. It's just as valid: if the statement ever failed, there'd be a smallest $n$ where it fails,
and all smaller cases would be true, which the step says is impossible.</p>""") + r"""

""" + example(8, "stamps",
r"""You have unlimited 4p and 5p stamps. Prove that every amount of $n\ge12$ pence can be made exactly.""",
r"""<p><b>Base cases.</b> $12=4+4+4$, $13=4+4+5$, $14=4+5+5$, $15=5+5+5$.</p>
<p><b>Step.</b> Let $n\ge16$ and assume every amount from 12 to $n-1$ can be made. Then $n-4\ge12$ can be made; add one
4p stamp. $\blacksquare$</p>
<p><b>Why four base cases?</b> The step reaches back 4, so it only works once $n-4\ge12$. The amounts $12,13,14,15$ have to be
checked by hand. (And 11 really can't be made, so “12” is the right starting point.)</p>""") + r"""

""" + trap(r"""<p>Check the base cases cover everything the step needs. If the step uses $P(n-1)$ and $P(n-2)$, you need
<b>two</b> base cases. Also make sure the step works for the <i>smallest</i> $n$ you apply it to: a famous fake proof
(“all horses are the same colour”) fails exactly because its step doesn't work from $n=1$ to $n=2$.</p>""") + r"""

""" + method("build the answer from smaller cases",
r"""<ul>
<li><b>Recursion:</b> classify the size-$n$ objects by what happens at the last element, and count each class using
smaller sizes. Then solve the recurrence or recognise it ($F_n$, $2^n$, $2^n-1$, …), and prove your formula by induction.</li>
<li><b>Induction for constructions:</b> split a size-$n$ object into smaller copies, and deal with the leftover piece.</li>
<li><b>Strong induction:</b> assume the result for all smaller cases, not just $n-1$.</li>
<li>Fibonacci: $F_1=F_2=1$, $F_{k+1}=F_k+F_{k-1}$, giving $1,1,2,3,5,8,13,21,\dots$</li>
</ul>""") + check([
r"""How many binary strings of length $n$ have no two consecutive 0s? Find a recurrence and the answer for $n=5$.""",
r"""$n$ points on a circle are joined by all chords. Into how many pieces is the circle's interior cut when $n=1,2,3,4,5$ (no three chords meeting at a point)? Don't trust the pattern!""",
r"""Prove by induction that $1+3+5+\dots+(2n-1)=n^2$."""],
[r"""$s_n=s_{n-1}+s_{n-2}$, $s_1=2,s_2=3$; $s_5=13$""", r"""$1,2,4,8,16$, but $n=6$ gives $31$, not $32$""",
 r"""step: $(n-1)^2+(2n-1)=n^2$"""])

Q = []
Q.append(dict(id="8.1", tag="Fibonacci",
stmt=r"""Let $a_n$ be the number of subsets of $\{1,2,\dots,n\}$ (including the empty set) that contain no two consecutive
integers. Prove that $a_n=F_{n+2}$.""",
hint=r"""Split according to whether $n$ is in the subset.""",
key=r"""Either $n$ is not in the subset, leaving any valid subset of $\{1,\dots,n-1\}$; or $n$ is in it, so $n-1$ is not, leaving any
valid subset of $\{1,\dots,n-2\}$. That's the Fibonacci recurrence.""",
sol=r"""<p><b>Recurrence.</b> Take $n\ge3$ and split the valid subsets $S$ of $\{1,\dots,n\}$:</p>
<ul>
<li>$n\notin S$: then $S$ is any valid subset of $\{1,\dots,n-1\}$, giving $a_{n-1}$.</li>
<li>$n\in S$: then $n-1\notin S$, and $S\setminus\{n\}$ is any valid subset of $\{1,\dots,n-2\}$, giving $a_{n-2}$.</li>
</ul>
<p>So $a_n=a_{n-1}+a_{n-2}$.</p>
<p><b>Initial values.</b> $a_1=2$ ($\varnothing$, $\{1\}$) $=F_3$, and $a_2=3$ ($\varnothing$, $\{1\}$, $\{2\}$) $=F_4$.</p>
<p><b>Induction.</b> $a_n$ and $F_{n+2}$ satisfy the same recurrence with the same first two values, so they are equal for all
$n$. $\blacksquare$</p>"""))

Q.append(dict(id="8.2", tag="regions",
stmt=r"""$n$ lines are drawn in the plane, no two parallel and no three through a point. Into how many regions do they divide the
plane?""",
hint=r"""When you add the $n$-th line, how many pieces is it cut into by the others, and what does each piece do?""",
key=r"""The new line meets the $n-1$ old lines at $n-1$ distinct points, so it is cut into $n$ pieces. Each piece splits one
existing region in two.""",
sol=r"""<p>Let $R_n$ be the number of regions; $R_0=1$. Add the $n$-th line to a configuration of $n-1$ lines. It is not parallel to
any of them, so it meets each exactly once, and these $n-1$ points are distinct (no three lines concurrent). They cut the new
line into $n$ pieces (two rays and $n-2$ segments). Each piece lies inside one old region and divides it into two. So
$$R_n=R_{n-1}+n\quad\Longrightarrow\quad R_n=1+(1+2+\dots+n)=1+\frac{n(n+1)}2.$$
Check: $R_1=2$, $R_2=4$, $R_3=7$. ✓</p>""",
answer=r"""$\dfrac{n^2+n+2}{2}$ regions."""))

Q.append(dict(id="8.3", tag="inductive construction",
stmt=r"""Prove that for every $n\ge1$, a $2^n\times2^n$ board with any one square removed can be tiled by L-shaped trominoes
(three squares forming an L).""",
hint=r"""Split the board into four $2^{n-1}\times2^{n-1}$ quarters. One has the hole; place one tromino in the centre to create a
hole in each of the others.""",
key=r"""Induction on $n$. Split into four quarters; the removed square is in one of them. One L-tromino at the centre covers one
corner square of each of the other three quarters, so each quarter now has exactly one missing square, and induction applies.""",
sol=fig(ltromino_fig(), "Hole (black) in one quarter; the central tromino (orange) makes a “hole” in each other quarter.") + r"""
<p><b>Base case $n=1$.</b> A $2\times2$ board minus one square is exactly an L-tromino.</p>
<p><b>Inductive step.</b> Assume the result for $2^{n-1}\times2^{n-1}$ boards. Split the $2^n\times2^n$ board into four
$2^{n-1}\times2^{n-1}$ quarters. The removed square lies in exactly one quarter. Place one L-tromino on the three squares at
the centre of the board that belong to the other three quarters; they form an L. Now each quarter is a
$2^{n-1}\times2^{n-1}$ board with exactly one square missing or covered, and by the inductive hypothesis each can be tiled.
Together with the central tromino, this tiles the board. $\blacksquare$</p>"""))

Q.append(dict(id="8.4", tag="strong induction",
stmt=r"""Using the Fibonacci numbers $1,2,3,5,8,13,\dots$ (each at most once), prove that every positive integer can be written as
a sum of distinct Fibonacci numbers, no two of which are consecutive in this list. (Zeckendorf's theorem, existence part.)""",
hint=r"""Greedy: subtract the largest Fibonacci number $\le n$. Show the remainder is less than the previous Fibonacci number.""",
key=r"""Greedy plus strong induction. If $f_k\le n\lt f_{k+1}$, then $n-f_k\lt f_{k+1}-f_k=f_{k-1}$, so the representation of
$n-f_k$ uses only terms up to $f_{k-2}$, which are not adjacent to $f_k$.""",
sol=r"""<p>Write the list as $f_1=1$, $f_2=2$, and $f_{k+1}=f_k+f_{k-1}$. We use strong induction on $n$. For $n=1$: $1=f_1$.</p>
<p>Let $n\ge2$ and assume the claim for all smaller positive integers. Let $f_k$ be the largest list term $\le n$, so
$f_k\le n\lt f_{k+1}$. If $n=f_k$, we're done. Otherwise $m=n-f_k$ satisfies $1\le m\lt f_{k+1}-f_k=f_{k-1}$.</p>
<p>By the hypothesis, $m$ is a sum of distinct non-consecutive terms, each $\le m\lt f_{k-1}$, so each is at most $f_{k-2}$.
Adding $f_k$ gives a representation of $n$: all terms are distinct, and $f_k$ is not consecutive to any of them (the largest
is at most $f_{k-2}$). $\blacksquare$</p>
<p><b>Example.</b> $100=89+11=89+8+3$.</p>"""))

SECTION = dict(num=8, title="Recursion and induction",
               blurb="build the answer for $n$ from smaller cases; base case plus step",
               intro="Solve size $n$ using the answers for smaller sizes.", teach=teach, questions=Q)
