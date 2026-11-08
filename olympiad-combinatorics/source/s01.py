from lib import *

teach = r"""
<p>Counting is the foundation of everything else in this pack. The goal is never to list objects one by one: it's to
find a structure that lets you count them with a short calculation. Almost all counting arguments are built from
three ideas: <b>multiply</b> for independent choices, <b>add</b> for separate cases, and <b>match up</b> the objects with
something easier to count.</p>

<h2>The product rule and the sum rule</h2>
<p>If you make a sequence of choices, with $a_1$ options for the first, $a_2$ for the second (whatever you chose
first), and so on, the total number of outcomes is $a_1a_2a_3\cdots$. If the objects split into cases that don't
overlap, the total is the sum of the cases.</p>

""" + example(1, "product and sum rules",
r"""A password is 3 characters long. Each character is a lower-case letter (26 options) or a digit (10 options).
(a) How many passwords are there? (b) How many contain no letter repeated and no digit repeated?""",
r"""<p>(a) Each position has $36$ options, chosen independently: $36^3 = 46\,656$.</p>
<p>(b) Here the number of options for each position depends on what came before, so split into cases by the
<i>pattern</i> of types (L = letter, D = digit). These cases don't overlap, so we add them.</p>
<ul>
<li>LLL: $26\cdot 25\cdot 24 = 15\,600$.</li>
<li>Two letters, one digit: the digit's position can be chosen in $3$ ways, then $26\cdot25\cdot10$, giving $3\cdot 6500=19\,500$.</li>
<li>One letter, two digits: $3\cdot 26\cdot 10\cdot 9 = 7020$.</li>
<li>DDD: $10\cdot 9\cdot 8 = 720$.</li>
</ul>
<p>Total $15\,600+19\,500+7020+720 = 42\,840$. Notice the pattern: the <b>sum rule</b> splits into cases where the
<b>product rule</b> works cleanly.</p>""") + r"""

<h2>Arrangements and selections</h2>
<p>The number of ways to arrange $n$ different objects in a row is $n! = n(n-1)\cdots 2\cdot 1$ (product rule:
$n$ choices for the first place, $n-1$ for the second, …). The number of ways to choose an <i>ordered</i> list of
$k$ of them is $n(n-1)\cdots(n-k+1)$.</p>
<p>Often we want an <i>unordered</i> selection: a set of $k$ objects, where order doesn't matter. Each set of $k$ objects
appears $k!$ times among the ordered lists (once for each way of ordering it), so we divide:</p>
""" + theorem("binomial coefficients",
r"""<p>The number of $k$-element subsets of an $n$-element set is
$$\binom nk = \frac{n(n-1)\cdots(n-k+1)}{k!} = \frac{n!}{k!\,(n-k)!}.$$
For example, choosing 3 of 5 people: there are $5\cdot4\cdot3=60$ ordered lists, each group of three appears
$3!=6$ times, so $\binom53 = 10$.</p>
<p><b>Useful identities</b>, each with a one-line reason:</p>
<ul>
<li>$\binom nk=\binom n{n-k}$: choosing the $k$ who are in is the same as choosing the $n-k$ who are out.</li>
<li>$\binom nk=\binom{n-1}{k-1}+\binom{n-1}k$ (Pascal's rule): a $k$-subset either contains the element $n$
(then choose $k-1$ more from the other $n-1$) or it doesn't (choose all $k$ from the other $n-1$).</li>
<li>$\sum_k\binom nk=2^n$: both sides count all subsets of an $n$-set; on the right, each element is either in or out.</li>
</ul>""") + r"""

<h2>The bijection principle</h2>
<p>A <b>bijection</b> is a perfect matching between two sets: every object in the first set is paired with exactly one
object in the second, and vice versa. If such a matching exists, the two sets have the same size. This is the most
powerful idea in counting: <i>to count something hard, match it with something easy.</i></p>
<p>For example, subsets of $\{1,\dots,n\}$ match up with binary strings of length $n$: write a 1 in position $i$ if
$i$ is in the subset. The subset $\{1,3,4\}$ of $\{1,\dots,5\}$ becomes $10110$. There are $2^n$ strings, so $2^n$
subsets. To prove a map is a bijection, check you can go <b>both ways</b>: every object gives a valid partner, and
from the partner you can recover the object uniquely.</p>

""" + example(1, "a bijection that removes a restriction",
r"""How many ways are there to choose 3 numbers from $\{1,2,\dots,10\}$ so that no two of them are consecutive?""",
r"""<p><b>The idea.</b> The restriction “no two consecutive” is awkward. Let's find a matching with something
unrestricted. Write the chosen numbers as $a&lt;b&lt;c$. “Not consecutive” means $b\ge a+2$ and $c\ge b+2$. If we
squeeze the gaps by sending
$$(a,b,c)\ \longmapsto\ (a,\ b-1,\ c-2),$$
the new numbers satisfy $a &lt; b-1 &lt; c-2$ (strictly increasing, but now they're allowed to be consecutive), and
they lie in $\{1,\dots,8\}$.</p>
<p><b>Check it's a bijection.</b> Going back: given any $x&lt;y&lt;z$ in $\{1,\dots,8\}$, the triple $(x, y+1, z+2)$ has
gaps at least 2 and lies in $\{1,\dots,10\}$. The two maps undo each other. So the number we want is the number
of 3-subsets of an 8-set: $\binom83 = 56$.</p>
<p><b>Sanity check on a small case.</b> Choose 2 non-consecutive numbers from $\{1,2,3,4\}$: the same argument gives
$\binom32=3$, and indeed the options are $\{1,3\},\{1,4\},\{2,4\}$. In general the answer is $\binom{n-k+1}{k}$.</p>""") + r"""

<h2>Stars and bars</h2>
<p>How many ways can you share out 7 identical sweets between 3 children (some children may get none)? Draw the 7
sweets as stars in a row and use 2 bars to split the row into 3 blocks: the first child gets the stars before the
first bar, the second those between the bars, the third those after the second bar.</p>
<div class="fig"><span class="mono" style="font-size:13pt">★★ | ★★★★ | ★</span> &nbsp;&nbsp; means &nbsp;&nbsp; $(2,4,1)$
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="mono" style="font-size:13pt">| ★★★★★ | ★★</span> &nbsp;&nbsp; means &nbsp;&nbsp; $(0,5,2)$</div>
<p>Every row of 7 stars and 2 bars gives a sharing, and every sharing gives exactly one row. A row is 9 symbols, and
it's determined by which 2 of the 9 positions hold bars: $\binom92 = 36$ ways.</p>
""" + theorem("stars and bars",
r"""<p>The number of solutions of $x_1+x_2+\dots+x_k=n$ in <b>non-negative</b> integers is $\displaystyle\binom{n+k-1}{k-1}$
(rows of $n$ stars and $k-1$ bars).</p>
<p>The number of solutions in <b>positive</b> integers is $\displaystyle\binom{n-1}{k-1}$: give each $x_i$ one star first,
then share out the remaining $n-k$ freely; equivalently, choose $k-1$ of the $n-1$ gaps between $n$ stars in a row.</p>""") + r"""
""" + trap(r"""<p>Stars and bars is for <b>identical</b> objects going into <b>different</b> boxes. If the objects are
different (7 different sweets to 3 children), each sweet independently picks a child: $3^7$ ways. Always ask: are
the objects identical? Are the boxes?</p>""") + r"""

<h2>Lattice paths</h2>
<p>A path on the grid from $(0,0)$ to $(m,n)$ using unit steps right (R) and up (U) is the same as a word with $m$ R's
and $n$ U's. For instance, the path in the picture is $\mathrm{RRURU}$. The word is fixed once you choose which $m$ of
the $m+n$ positions are R's, so there are $\binom{m+n}{m}$ paths.</p>
""" + fig(lattice(3, 2, "RRURU"), "The path RRURU from $(0,0)$ to $(3,2)$. There are $\\binom52=10$ such paths.") + r"""

<h2>Complementary counting</h2>
<p>When the condition says “at least one”, it's usually easier to count the objects with <i>none</i> and subtract
from the total.</p>
""" + example(1, "complements beat cases",
r"""How many 3-letter strings (using the 26 letters, repeats allowed) contain at least one A?""",
r"""<p><b>The tempting wrong method.</b> “Put an A in one of 3 places, fill the other two freely: $3\cdot26^2=2028$.”
This overcounts: the string AAB is counted twice (once with the A chosen in position 1, once with position 2), and
AAA three times.</p>
<p><b>Right method.</b> Total strings: $26^3=17\,576$. Strings with no A: $25^3=15\,625$. So the answer is
$17\,576-15\,625=1951$.</p>""") + r"""
""" + method("which counting tool?",
r"""<ul>
<li>Choices made one after another → <b>product rule</b>; separate cases → <b>sum rule</b>.</li>
<li>Order doesn't matter → divide by the number of orderings, or use $\binom nk$ directly.</li>
<li>Awkward condition → find a <b>bijection</b> to something without it.</li>
<li>Identical objects into distinct boxes → <b>stars and bars</b>.</li>
<li>“At least one” → <b>complement</b>.</li>
<li>Proving an identity → show both sides count the same set in two ways (<b>committee argument</b>; see also Section 7).</li>
</ul>""") + check([
r"""How many ways can 10 identical coins be shared among 4 people so that everyone gets at least one?""",
r"""How many paths of R and U steps go from $(0,0)$ to $(5,3)$?""",
r"""How many 5-digit numbers have at least one digit equal to 7?"""],
[r"""$\binom93=84$""", r"""$\binom83=56$""", r"""$90\,000-8\cdot9^4=37\,512$"""])

Q = []
Q.append(dict(id="1.1", tag="stars &amp; bars",
stmt=r"""Find the number of solutions of $x_1+x_2+x_3+x_4=20$
<br>(a) in non-negative integers; &nbsp;&nbsp; (b) in positive integers.""",
hint=r"""(a) Stars and bars directly. (b) Substitute $y_i = x_i - 1$.""",
key=r"""(a) is stars and bars with $n=20$, $k=4$. (b) reduces to (a) by subtracting 1 from each variable, which is a
bijection between the two solution sets.""",
sol=r"""<p><b>(a)</b> Each solution corresponds to a row of 20 stars and 3 bars, with $x_i$ the number of stars in the $i$-th
block. Conversely, each such row gives a solution. Choosing the positions of the 3 bars among 23 positions:
$$\binom{23}{3} = \frac{23\cdot22\cdot21}{6} = 1771.$$</p>
<p><b>(b)</b> The map $y_i=x_i-1$ is a bijection from positive solutions of $x_1+\dots+x_4=20$ to non-negative
solutions of $y_1+\dots+y_4=16$ (it can be undone by $x_i=y_i+1$). By stars and bars there are
$\binom{19}{3}=\frac{19\cdot18\cdot17}{6}=969$ of these.</p>""",
answer=r"""(a) $1771$; (b) $969$. In general, $\binom{n+k-1}{k-1}$ and $\binom{n-1}{k-1}$."""))

Q.append(dict(id="1.2", tag="lattice paths",
stmt=r"""A path from $(0,0)$ to $(4,4)$ consists of unit steps, each either right or up. How many such paths do
<i>not</i> pass through the point $(2,2)$?""",
hint=r"""Count all paths, then subtract those through $(2,2)$, which split into two independent halves.""",
key=r"""Complementary counting. A path through $(2,2)$ is a path to $(2,2)$ followed by a path from $(2,2)$, so those
paths are counted by the product rule.""",
sol=r"""<p><b>All paths.</b> A path is a word of 4 R's and 4 U's, and every such word gives a path. So there are
$\binom84=70$.</p>
<p><b>Paths through $(2,2)$.</b> Such a path is a path $(0,0)\to(2,2)$ followed by a path $(2,2)\to(4,4)$, chosen
independently, and every such pair gives a path through $(2,2)$. So there are $\binom42\cdot\binom42=6\cdot6=36$.</p>
<p><b>Answer.</b> $70-36=34$.</p>""" + fig(lattice(4, 4, "RRUURURU", mark=(2, 2)), "A path through $(2,2)$: the part before and the part after are chosen independently."),
answer=r"""$34$."""))

Q.append(dict(id="1.3", tag="committee argument",
stmt=r"""Prove that for every $n\ge0$,
$$\binom n0^2+\binom n1^2+\dots+\binom nn^2=\binom{2n}{n}.$$""",
hint=r"""Count committees of size $n$ chosen from $n$ boys and $n$ girls. Split by the number of boys.""",
key=r"""Both sides count the $n$-element subsets of a set of $2n$ people. The left side sorts them by how many come from
the first half.""",
sol=r"""<p>Take $n$ boys and $n$ girls. The number of ways to choose $n$ people is $\binom{2n}{n}$.</p>
<p>Now count by the number $k$ of boys chosen ($0\le k\le n$). Choose the $k$ boys in $\binom nk$ ways, and the
$n-k$ girls in $\binom n{n-k}=\binom nk$ ways. So there are $\binom nk^2$ committees with exactly $k$ boys. Every
committee has exactly one value of $k$, so summing over $k$ counts each committee exactly once:
$$\sum_{k=0}^n\binom nk^2=\binom{2n}n.\qquad\blacksquare$$</p>"""))

Q.append(dict(id="1.4", tag="complementary counting",
stmt=r"""How many four-digit numbers (from 1000 to 9999) have at least one digit appearing more than once?""",
hint=r"""“At least one repeat” is the complement of “all digits different”.""",
key=r"""Counting “at least one repeat” directly needs many cases. Its complement, “all four digits distinct”, is a
single product-rule count.""",
sol=r"""<p><b>Total.</b> There are $9999-1000+1=9000$ four-digit numbers.</p>
<p><b>All digits distinct.</b> The first digit has 9 choices (not 0). The second has 9 (any digit except the first,
now including 0), the third 8, the fourth 7. So there are $9\cdot9\cdot8\cdot7=4536$.</p>
<p><b>Answer.</b> $9000-4536=4464$.</p>""",
answer=r"""$4464$."""))

SECTION = dict(num=1, title="Counting: bijections and stars &amp; bars",
               blurb="product and sum rules, binomial coefficients, bijections, stars and bars, complements",
               intro="Multiply, add, or match up with something easier.", teach=teach, questions=Q)
