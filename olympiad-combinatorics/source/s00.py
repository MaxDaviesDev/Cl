from lib import *

teach = r"""
<p>Algebra and geometry problems usually announce their method: you see an inequality, you think AM–GM; you see a
cyclic quadrilateral, you chase angles. Combinatorics problems often don't. They are short, easy to understand,
and the difficulty lies entirely in finding the right way to look at them. This section is about how to find that
way. Come back to it after you've worked through the rest of the pack: it will make more sense then.</p>

<h2>Step 1. Play with small cases</h2>
<p>Before trying to prove anything, work out the answer for $n=1,2,3,4$ by hand, drawing pictures. This does three
things. It makes sure you understand the question (many errors come from misreading it). It gives you a
conjecture for the answer. And, most importantly, <i>the way you count the small cases often is the proof</i>. If you
notice yourself reasoning “the case $n=4$ is the case $n=3$ plus something”, that's a recursion (Section 8).</p>

""" + example(0, "small cases find the proof",
r"""In how many ways can a $2\times n$ strip be tiled with $1\times 2$ dominoes?""",
r"""<p><b>Small cases.</b> Draw them. $n=1$: one way (a single vertical domino). $n=2$: two ways (two vertical, or two horizontal).
$n=3$: three ways. $n=4$: five ways. The sequence $1,2,3,5$ looks like Fibonacci.</p>
<p><b>Turning the pattern into a proof.</b> While drawing $n=4$ you may notice that every tiling starts at the left end
in one of two ways: a single vertical domino, or two horizontal dominoes stacked on top of each other (one
horizontal domino on its own would leave a gap below it that only another horizontal domino can fill). In the first
case what's left is a $2\times(n-1)$ strip; in the second, a $2\times(n-2)$ strip. So if $t_n$ is the number of tilings,
$$t_n = t_{n-1} + t_{n-2},\qquad t_1 = 1,\ t_2 = 2,$$
which gives $1,2,3,5,8,13,\dots$, the Fibonacci numbers. The small cases didn't just suggest the answer: they showed
us <i>why</i> it's true.</p>""",
figrow(fig(tiling([[0,1,1],[0,2,2]], cell=18)), fig(tiling([[0,0,1],[2,2,1]], cell=18)), fig(tiling([[0,1,2],[0,1,2]], cell=18)))
+ '<div class="cap" style="text-align:center">The three tilings of a $2\\times 3$ strip.</div>') + r"""

<h2>Step 2. Recognise the type of question</h2>
<p>The wording of the question is the best clue to the method. Learn this table: it's the map for the whole pack.</p>
<table class="t">
<tr><th>The question says…</th><th>Try first</th><th>Section</th></tr>
<tr><td style="text-align:left">“How many…?”</td><td style="text-align:left">bijections, complements, inclusion–exclusion, recursion, double counting</td><td>1, 2, 7, 8</td></tr>
<tr><td style="text-align:left">“Prove that there exist…”</td><td style="text-align:left">pigeonhole, extremal principle</td><td>3, 5</td></tr>
<tr><td style="text-align:left">“Is it possible to reach / tile…?”</td><td style="text-align:left">invariants, colourings</td><td>4, 6</td></tr>
<tr><td style="text-align:left">“Show the process stops”</td><td style="text-align:left">monovariants</td><td>5</td></tr>
<tr><td style="text-align:left">“Who wins?”</td><td style="text-align:left">winning/losing positions, symmetry, strategy stealing</td><td>10</td></tr>
<tr><td style="text-align:left">“Find the maximum / minimum”</td><td style="text-align:left">bound <i>and</i> construction</td><td>11</td></tr>
<tr><td style="text-align:left">People, friendships, roads, matches</td><td style="text-align:left">draw a graph</td><td>9</td></tr>
</table>

<h2>Step 3. Reformulate</h2>
<p>Restate the problem in a cleaner language: a graph (people become dots, relationships become lines), a grid,
a sequence of 0s and 1s, a set of subsets. A good reformulation strips away the story and often makes the problem
obvious. For example, “a party where some pairs shake hands” is just a graph; “choose which of $n$ people come” is
a binary string of length $n$; “walk from one corner of a grid to the other” is a word made of R's and U's.</p>

<h2>Step 4. Know what a complete answer needs</h2>
<ul>
<li><b>“Find the number”</b>: a number, plus an argument that every object is counted exactly once.</li>
<li><b>“Is it possible?”</b>: if yes, an explicit construction; if no, a proof (usually an invariant or colouring).</li>
<li><b>“Find the maximum”</b>: a proof that nothing larger works <i>and</i> an example achieving it. Missing either half
loses most of the marks (Section 11).</li>
<li><b>“Who wins?”</b>: the winner, and their strategy, with a proof it works against <i>every</i> reply.</li>
</ul>

<h2>Step 5. Write it so a marker can follow it</h2>
<p>Combinatorics solutions are easy to get almost right. Name things: say exactly what you are counting, what the
pigeons and boxes are, what the invariant is and why each move preserves it. Short labelled paragraphs
(“Bound.”, “Construction.”, “Claim.”) make a solution easy to mark, which is good for you.</p>

""" + trap(r"""<p><b>Overcounting and undercounting</b> are the classic errors. Whenever you count, ask: <i>is each object counted
exactly once?</i> Test your method on a small case where you can list everything. When you divide by a symmetry
factor (“each arrangement was counted 6 times”), check that <i>every</i> arrangement really was counted that many
times.</p>""")

SECTION = dict(num=0, title="The toolkit: how to attack a problem",
               blurb="small cases, recognising the question type, reformulating, writing up",
               intro="Read this first, and again at the end.", teach=teach, questions=[])
