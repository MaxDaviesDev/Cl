from lib import *

def incidence():
    # 3 students x 4 clubs incidence table
    rows = ["Ann", "Ben", "Cat"]
    M = [[1, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 1]]
    h = '<table class="t"><tr><th></th>' + "".join("<th>club %d</th>" % (j + 1) for j in range(4)) + "<th>row total</th></tr>"
    for name, r in zip(rows, M):
        h += "<tr><th>%s</th>%s<td><b>%d</b></td></tr>" % (name, "".join("<td>%s</td>" % ("✓" if v else "") for v in r), sum(r))
    h += "<tr><th>column total</th>%s<td><b>%d</b></td></tr></table>" % ("".join("<td><b>%d</b></td>" % sum(M[i][j] for i in range(3)) for j in range(4)), sum(map(sum, M)))
    return h

teach = r"""
<p>Double counting means counting <i>one</i> collection of objects in <i>two</i> different ways. Both counts must give
the same number, and setting them equal gives an equation you couldn't easily have found otherwise. It proves identities,
gives answers, and, when one of the counts is only an estimate, proves inequalities.</p>

<h2>The idea in a table</h2>
<p>Suppose some students belong to some clubs. Make a table with a row for each student, a column for each club, and a
tick when that student is in that club. The total number of ticks can be found by adding up the <b>row totals</b> (each
student's number of clubs) or the <b>column totals</b> (each club's size). The two answers are equal.</p>
""" + incidence() + r"""
<p>Here $3+2+3 = 2+2+2+2 = 8$. That's the whole principle. The art is choosing what the ticks are: usually <b>pairs</b>
such as (person, club they're in), (vertex, edge at it), (pair of judges, contestant they agree on).</p>

""" + example(7, "finding an unknown",
r"""Each of 20 students belongs to exactly 3 clubs, and each club has exactly 12 members. How many clubs are there?""",
r"""<p>Count the pairs (student, club) with the student in the club.</p>
<p><b>By students:</b> $20\times3=60$. &nbsp;<b>By clubs:</b> if there are $c$ clubs, $12c$.</p>
<p>So $12c=60$ and $c=5$.</p>""") + r"""

""" + theorem("the handshake lemma",
r"""<p>In any graph (Section 9), the sum of the degrees equals twice the number of edges:
$$\sum_v\deg v = 2|E|.$$
<i>Proof.</i> Count pairs (vertex, edge at that vertex). By vertices: $\sum\deg v$. By edges: each edge has 2 ends, so $2|E|$.</p>
<p><b>Consequence.</b> The sum of the degrees is even. For instance, 9 people can't each know exactly 3 of the others: the
degrees would sum to 27, which is odd.</p>""") + r"""

<h2>Proving identities by double counting</h2>
<p>To prove $A=B$, find a set and show that $A$ counts it one way and $B$ counts it another way. This is often called a
<b>combinatorial proof</b>, or a committee argument.</p>

""" + example(7, "pairs sorted by their larger element",
r"""Prove that $1+2+\dots+(n-1)=\dbinom n2$.""",
r"""<p>Count the 2-element subsets of $\{1,\dots,n\}$. Directly, there are $\binom n2$.</p>
<p>Now sort them by their <b>larger element</b> $k$. If the larger element is $k$, the smaller can be any of $1,\dots,k-1$:
$k-1$ choices. So the number of pairs is $\sum_{k=2}^n(k-1)=1+2+\dots+(n-1)$. $\blacksquare$</p>
<p><b>Pattern.</b> One side counts the set directly. The other side splits it into cases (here by the largest element) and adds
them up. That's the most common shape of a combinatorial proof.</p>""") + r"""

<h2>Inequalities by double counting</h2>
<p>If one count is exact and the other is only <b>bounded</b>, you get an inequality instead of an equation.</p>

""" + example(7, "a bound from counting pairs",
r"""Ten students form committees. Each committee has exactly 4 members, and no two students serve together on more than
one committee. Prove there are at most 7 committees.""",
r"""<p>Count the pairs (pair of students, committee containing both).</p>
<p><b>By committees:</b> each committee contains $\binom42=6$ pairs of students, so the count is exactly $6c$.</p>
<p><b>By pairs of students:</b> there are $\binom{10}2=45$ pairs, and each is together in at most one committee, so the count is
at most $45$.</p>
<p>So $6c\le45$, giving $c\le7$. $\blacksquare$</p>
<p>(This only proves a bound. Whether 7 is actually achievable is a separate question; see Section 11.)</p>""") + r"""

""" + method("count the same thing two ways",
r"""<ul>
<li>Choose objects to count: usually pairs or triples such as (person, committee), (vertex, edge), (pair, set containing it).</li>
<li>Count them by summing over the first coordinate, then over the second.</li>
<li><b>Identities:</b> both counts are exact. <b>Inequalities:</b> one count is exact and the other is bounded,
often by the condition in the problem, or by an inequality such as AM–GM or Cauchy–Schwarz.</li>
<li>A useful fact for the bounding step: $\binom x2+\binom{b-x}2$ is smallest when $x$ is as close to $b/2$ as possible.</li>
</ul>""") + check([
r"""A graph has 10 vertices, each of degree 4. How many edges does it have?""",
r"""Prove $\binom nk\cdot k=n\binom{n-1}{k-1}$ by counting committees with a chair.""",
r"""In a group, every person has exactly 3 friends and there are 12 friendships. How many people are there?"""],
[r"""$20$""", r"""choose the committee then the chair, or the chair then the rest""", r"""$8$"""])

Q = []
Q.append(dict(id="7.1", tag="handshakes",
stmt=r"""At a party, some pairs of people shake hands. Prove that the number of people who shake an odd number of hands is even.""",
hint=r"""Add up the numbers of handshakes of all people. How many times is each handshake counted?""",
key=r"""Summing each person's handshake count counts every handshake twice, so the total is even. An even total can't have an odd
number of odd terms.""",
sol=r"""<p>Let person $i$ shake $d_i$ hands and let $E$ be the number of handshakes. Count pairs (person, handshake they took part in).
Summing over people gives $\sum d_i$. Summing over handshakes gives $2E$, since each handshake involves two people. So
$\sum d_i=2E$ is even.</p>
<p>Split the sum into even $d_i$ and odd $d_i$. The even ones sum to an even number, so the odd ones must too. A sum of odd
numbers is even only if there is an even number of them. $\blacksquare$</p>"""))

Q.append(dict(id="7.2", tag="committee with a chair",
stmt=r"""Prove that $$\sum_{k=0}^n k\binom nk=n\,2^{n-1}.$$""",
hint=r"""Count committees (of any size) with a chair, chosen from $n$ people.""",
key=r"""Count pairs (committee, chair of that committee). Choosing the committee first gives the left side; choosing the chair
first gives the right side.""",
sol=r"""<p>Count the pairs $(C,p)$ where $C$ is a subset of the $n$ people and $p\in C$ is its chair.</p>
<p><b>Committee first.</b> For each $k$ there are $\binom nk$ committees of size $k$, each with $k$ choices of chair. Total
$\sum_kk\binom nk$.</p>
<p><b>Chair first.</b> Choose the chair in $n$ ways, then any subset of the other $n-1$ people to complete the committee:
$2^{n-1}$ ways. Total $n2^{n-1}$.</p>
<p>The two counts are equal. $\blacksquare$</p>"""))

Q.append(dict(id="7.3", tag="IMO 1998 Problem 2",
stmt=r"""In a competition there are $a$ contestants and $b$ judges, where $b\ge3$ is odd. Each judge rates each contestant as
“pass” or “fail”. Suppose $k$ is a number such that any two judges agree on at most $k$ contestants. Prove that
$$\frac ka\ge\frac{b-1}{2b}.$$""",
hint=r"""Count triples (contestant, unordered pair of judges who agree on that contestant). Bound the count from above using $k$,
and from below by looking at each contestant.""",
key=r"""Count $N$, the number of (pair of judges, contestant) with the pair agreeing. Per pair of judges, $N\le k\binom b2$. Per
contestant, if $x$ judges pass them there are $\binom x2+\binom{b-x}2\ge\frac{(b-1)^2}4$ agreeing pairs. Compare.""",
sol=r"""<p>Let $N$ be the number of triples $(\{J,J'\},C)$ with $J\ne J'$ judges who give contestant $C$ the same rating.</p>
<p><b>Upper bound.</b> Each of the $\binom b2$ pairs of judges agrees on at most $k$ contestants, so
$N\le k\binom b2=\dfrac{kb(b-1)}2$.</p>
<p><b>Lower bound.</b> Fix a contestant, passed by $x$ judges and failed by $b-x$. The agreeing pairs number
$$\binom x2+\binom{b-x}2=x^2-bx+\frac{b^2-b}2=\left(x-\frac b2\right)^2+\frac{b^2-2b}4.$$
Since $b$ is odd and $x$ is an integer, $\left|x-\frac b2\right|\ge\frac12$, so this is at least
$\frac14+\frac{b^2-2b}4=\frac{(b-1)^2}4$. Summing over contestants: $N\ge\dfrac{a(b-1)^2}4$.</p>
<p><b>Combine.</b> $\dfrac{kb(b-1)}2\ge\dfrac{a(b-1)^2}4$. Dividing by $\dfrac{ab(b-1)}2\gt0$: $\dfrac ka\ge\dfrac{b-1}{2b}$. $\blacksquare$</p>"""))

SECTION = dict(num=7, title="Double counting",
               blurb="count one set in two ways: identities, the handshake lemma, inequalities",
               intro="Count the same thing twice and compare.", teach=teach, questions=Q)
