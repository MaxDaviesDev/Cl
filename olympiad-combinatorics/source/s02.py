from lib import *

def venn():
    return ('<svg width="230" height="150" viewBox="0 0 230 150">'
            '<circle cx="85" cy="62" r="48" fill="#2563a8" fill-opacity="0.13" stroke="#2563a8" stroke-width="1.6"/>'
            '<circle cx="145" cy="62" r="48" fill="#c0392b" fill-opacity="0.13" stroke="#c0392b" stroke-width="1.6"/>'
            '<circle cx="115" cy="104" r="48" fill="#2f7a4a" fill-opacity="0.13" stroke="#2f7a4a" stroke-width="1.6"/>'
            '<text x="40" y="22" font-family="KaTeX_Main" font-style="italic" font-size="14">A</text>'
            '<text x="182" y="22" font-family="KaTeX_Main" font-style="italic" font-size="14">B</text>'
            '<text x="168" y="146" font-family="KaTeX_Main" font-style="italic" font-size="14">C</text>'
            '<g font-family="KaTeX_Main" font-size="11" text-anchor="middle">'
            '<text x="68" y="55">1</text><text x="162" y="55">1</text><text x="115" y="130">1</text>'
            '<text x="115" y="45">2</text><text x="90" y="98">2</text><text x="140" y="98">2</text>'
            '<text x="115" y="80">3</text></g></svg>')

teach = r"""
<p>Complementary counting (Section 1) handles one bad property: count everything, subtract the bad. Inclusion–exclusion
handles <i>several</i> bad properties at once. The difficulty is that the bad sets overlap, and the formula is the
systematic way to correct for that.</p>

<h2>Two sets</h2>
<p>In a class of 30, 18 play football, 15 play tennis and 8 play both. How many play at least one? Adding $18+15=33$
counts the 8 who play both <i>twice</i>, so subtract them once: $33-8=25$. Then $30-25=5$ play neither.</p>
$$|A\cup B| = |A| + |B| - |A\cap B|.$$

<h2>Three sets</h2>
<p>For three sets, start with $|A|+|B|+|C|$. The numbers in the picture show how many times each region has been
counted so far: regions in two sets are counted twice, the centre three times.</p>
""" + fig(venn(), "How often each region is counted by $|A|+|B|+|C|$.") + r"""
<p>Subtracting $|A\cap B|+|B\cap C|+|C\cap A|$ fixes the double regions (now counted once) but takes the centre down
from 3 to $3-3=0$. So we add $|A\cap B\cap C|$ back:</p>
$$|A\cup B\cup C| = |A|+|B|+|C| - |A\cap B| - |B\cap C| - |C\cap A| + |A\cap B\cap C|.$$
""" + theorem("inclusion–exclusion",
r"""<p>For finite sets $A_1,\dots,A_m$ inside a set of $N$ objects,
$$|A_1\cup\dots\cup A_m| = \sum_i|A_i| - \sum_{i\lt j}|A_i\cap A_j| + \sum_{i\lt j\lt k}|A_i\cap A_j\cap A_k| - \cdots$$
and so the number of objects in <b>none</b> of the sets is
$$N - \sum_i|A_i| + \sum_{i\lt j}|A_i\cap A_j| - \sum_{i\lt j\lt k}|A_i\cap A_j\cap A_k| + \cdots$$
In words: add the singles, subtract the pairs, add the triples, subtract the quadruples, …</p>""") + why("each element is counted exactly once",
r"""<p>Take an element lying in exactly $t\ge1$ of the sets. It is counted $\binom t1$ times among the singles, $\binom t2$
times among the pairs, and so on, so in total
$$\binom t1-\binom t2+\binom t3-\cdots = 1-(1-1)^t = 1$$
time, using the binomial theorem. An element in none of the sets is counted 0 times. Check with $t=3$: $3-3+1=1$. ✓</p>""") + r"""

""" + example(2, "divisibility",
r"""How many of the numbers $1,2,\dots,100$ are divisible by 2 or by 3? How many by neither?""",
r"""<p>Let $A$ be the multiples of 2 and $B$ the multiples of 3. Then $|A|=50$ and $|B|=\lfloor100/3\rfloor=33$. A
number is in both exactly when it's a multiple of 6, so $|A\cap B|=\lfloor100/6\rfloor=16$. Hence
$|A\cup B|=50+33-16=67$, and $100-67=33$ numbers are divisible by neither.</p>""") + r"""

""" + example(2, "stars and bars with an upper limit",
r"""How many solutions does $x_1+x_2+x_3=10$ have in integers with $0\le x_i\le 4$?""",
r"""<p><b>Set-up.</b> Without the upper limit, stars and bars gives $\binom{12}{2}=66$ solutions. The bad property $A_i$
is “$x_i\ge5$”. We want the solutions in none of $A_1,A_2,A_3$.</p>
<p><b>Singles.</b> Solutions with $x_1\ge5$: put $x_1=5+y_1$, then $y_1+x_2+x_3=5$ with all variables $\ge0$, which has
$\binom72=21$ solutions. By symmetry $|A_i|=21$ for each $i$.</p>
<p><b>Pairs.</b> $x_1\ge5$ and $x_2\ge5$ forces $x_1=x_2=5$, $x_3=0$: one solution. So $|A_i\cap A_j|=1$.</p>
<p><b>Triples.</b> All three $\ge5$ would sum to at least 15: impossible, so $0$.</p>
<p><b>Answer.</b> $66-3\cdot21+3\cdot1-0=6$.</p>
<p><b>Check by listing.</b> With each part at most 4 and total 10, the parts are $\{4,4,2\}$ or $\{4,3,3\}$ in some order:
$3+3=6$ solutions. ✓</p>""") + r"""

""" + method("how to set it up",
r"""<ol>
<li>Decide what the <b>bad properties</b> are, so that the objects you want are those with <i>none</i> of them.</li>
<li>Check that the <b>intersections</b> are easy to count: “has bad properties $i$ and $j$” should be a clean condition.</li>
<li>Look for <b>symmetry</b>: if any $j$ of the $m$ properties are satisfied by $N_j$ objects, regardless of which $j$, then the
answer is
$$\sum_{j=0}^m(-1)^j\binom mj N_j,$$
because there are $\binom mj$ ways to choose which $j$ properties.</li>
</ol>
Typical uses: divisibility by several primes, onto functions, derangements (no object in its own place), and upper
limits in stars and bars.""") + trap(r"""<p>Don't stop after the pairs. With three or more sets you must keep going (add triples, subtract quadruples, …)
until the intersections are empty. Also make sure an intersection is computed correctly: “multiple of 4 and of 6” means
multiple of $12$, not of $24$ (use the lcm).</p>""") + check([
r"""How many integers from 1 to 60 are divisible by 3 or 5?""",
r"""How many ways can 4 people swap hats so that nobody gets their own hat back?""",
r"""How many solutions does $x_1+x_2+x_3=7$ have with $0\le x_i\le3$?"""],
[r"""$20+12-4=28$""", r"""$D_4=9$""", r"""$\binom92-3\binom52=36-30=6$"""])

Q = []
Q.append(dict(id="2.1", tag="divisibility",
stmt=r"""How many integers from 1 to 1000 are divisible by none of 2, 3, 5?""",
hint=r"""Let $A_p$ be the multiples of $p$. The multiples of both 2 and 3 are the multiples of 6, and
$|A_d| = \lfloor 1000/d\rfloor$.""",
key=r"""Let the bad sets be $A_2,A_3,A_5$ (multiples of each). Their intersections are multiples of $6,10,15,30$, which are
easy to count.""",
sol=r"""<p>Write $A_d$ for the multiples of $d$ in $\{1,\dots,1000\}$, so $|A_d|=\lfloor1000/d\rfloor$. Since $2,3,5$ are
coprime, $A_2\cap A_3=A_6$, and so on. We have
$$|A_2|=500,\ |A_3|=333,\ |A_5|=200,\quad |A_6|=166,\ |A_{10}|=100,\ |A_{15}|=66,\quad |A_{30}|=33.$$
By inclusion–exclusion,
$$|A_2\cup A_3\cup A_5|=(500+333+200)-(166+100+66)+33=734.$$
So the number divisible by none of them is $1000-734=266$.</p>""",
answer=r"""$266$."""))

Q.append(dict(id="2.2", tag="surjections",
stmt=r"""How many functions from $\{1,2,3,4,5\}$ to $\{a,b,c\}$ are <i>onto</i>, i.e. take every one of the values $a$, $b$, $c$?""",
hint=r"""Bad property $B_x$: “the value $x$ is never taken”.""",
key=r"""A function fails to be onto exactly when it misses some value. Counting functions that miss a given set of values is
easy: they map into the remaining values.""",
sol=r"""<p>There are $3^5=243$ functions in total. Let $B_x$ be the set of functions that never take the value $x$.</p>
<ul>
<li>$|B_x|=2^5=32$ (each input goes to one of the other two values).</li>
<li>$|B_x\cap B_y|=1^5=1$ (everything goes to the third value).</li>
<li>$|B_a\cap B_b\cap B_c|=0$.</li>
</ul>
<p>So $|B_a\cup B_b\cup B_c|=3\cdot32-3\cdot1+0=93$, and the number of onto functions is $243-93=150$.</p>""",
answer=r"""$150$. In general, the number of onto maps from an $n$-set to a $k$-set is $\sum_{j=0}^k(-1)^j\binom kj(k-j)^n$."""))

Q.append(dict(id="2.3", tag="derangements",
stmt=r"""$n$ letters are put into $n$ addressed envelopes, one in each. In how many ways can this be done so that no letter
is in its correct envelope? Evaluate your formula for $n=4$.""",
hint=r"""Bad property $B_i$: letter $i$ is in envelope $i$. How many arrangements fix a given set of $k$ letters?""",
key=r"""A derangement avoids all $n$ bad properties “letter $i$ is correct”. Fixing any particular $k$ letters leaves
$(n-k)!$ arrangements of the rest, so inclusion–exclusion gives a clean alternating sum.""",
sol=r"""<p>Arrangements are permutations of $\{1,\dots,n\}$. Let $B_i$ be the set of permutations with $i$ in position $i$.
For any $k$ indices, the permutations fixing all of them number $(n-k)!$ (arrange the other $n-k$ letters freely), and there
are $\binom nk$ ways to choose the indices. By inclusion–exclusion (the symmetric form), the number $D_n$ of
permutations in none of the $B_i$ is
$$D_n=\sum_{k=0}^n(-1)^k\binom nk(n-k)!=n!\sum_{k=0}^n\frac{(-1)^k}{k!}.$$
For $n=4$: $D_4=24\left(1-1+\tfrac12-\tfrac16+\tfrac1{24}\right)=12-4+1=9$.</p>
<p><b>Remarks.</b> $D_n/n!\to 1/e$, so about $37\%$ of arrangements are derangements. The recurrence
$D_n=(n-1)(D_{n-1}+D_{n-2})$ is also worth knowing; it can be proved by looking at where letter $n$ goes.</p>""",
answer=r"""$D_n=n!\left(1-\frac1{1!}+\frac1{2!}-\dots+\frac{(-1)^n}{n!}\right)$; $\;D_4=9$."""))

SECTION = dict(num=2, title="Inclusion–exclusion",
               blurb="correcting for overlaps: add singles, subtract pairs, add triples, …",
               intro="Counting objects that avoid several bad properties at once.", teach=teach, questions=Q)
