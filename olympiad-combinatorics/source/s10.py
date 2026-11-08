from lib import *

def pn_table(moves, N):
    win = []
    for n in range(N):
        win.append(any(n - m >= 0 and not win[n - m] for m in moves))
    h = '<table class="t"><tr><th>$n$</th>' + "".join("<td>%d</td>" % n for n in range(N)) + "</tr><tr><th>type</th>"
    h += "".join('<td class="P">P</td>' if not w else "<td>N</td>" for w in win) + "</tr></table>"
    return h

def coins_circle():
    import math
    n = 10
    out = ['<svg width="290" height="120" viewBox="0 0 290 120">']
    for i in range(n):
        a = math.radians(-90 + 360 * i / n)
        x, y = 60 + 45 * math.cos(a), 60 + 45 * math.sin(a)
        taken = i in (0,)
        out.append('<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="#1f2933" stroke-width="1.4"/>' % (x, y, "#fff" if taken else "#f6c26b"))
    out.append('<text x="125" y="64" font-size="18">→</text>')
    # line of 9 with middle one removed
    for i in range(9):
        x = 155 + i * 15
        removed = i == 4
        out.append('<circle cx="%d" cy="60" r="6.5" fill="%s" stroke="#1f2933" stroke-width="1.3"/>' % (x, "#fff" if removed else ("#f6c26b" if i < 4 else "#9cc3ea")))
    out.append('<text x="200" y="95" font-size="10" font-family="Inter" text-anchor="middle" fill="#5f6b77">two equal rows of 4: now copy</text>')
    out.append('</svg>')
    return "".join(out)

teach = r"""
<p>Game problems ask: in a two-player game with given rules, who wins with perfect play, and how? An answer needs a
<b>strategy</b> for the winner and a proof that it works <i>whatever the opponent does</i>. Three methods cover almost
every olympiad game.</p>
<p>Throughout, the games are finite (they always end), have no draws, and both players see everything. For such games one
of the two players always has a winning strategy; the question is which.</p>

<h2>Method 1: winning and losing positions</h2>
<p>Call a position <b>P</b> (a <b>P</b>revious-player win: the player <i>to move</i> loses) or <b>N</b> (a <b>N</b>ext-player
win: the player to move wins). The rules:</p>
""" + theorem("P and N positions",
r"""<ul>
<li>A position where the player to move has <b>no moves</b> (and so has lost) is P.</li>
<li>A position is <b>N</b> if <b>some</b> move leads to a P position (move there, and your opponent is stuck in a losing position).</li>
<li>A position is <b>P</b> if <b>every</b> move leads to an N position (whatever you do, your opponent is now winning).</li>
</ul>
<p>The winning strategy is simple: <b>always move to a P position.</b></p>""") + r"""

""" + example(10, "a subtraction game by table",
r"""A pile has $n$ stones. Players alternately remove 1, 3 or 4 stones. Whoever takes the last stone wins. For which $n$ does
the second player win?""",
r"""<p><b>Build the table from 0 upwards.</b> $n=0$: no move, so P. $n=1$: can move to 0 (P), so N. $n=2$: the only move is to 1
(N), so P. $n=3$: move to 0, N. $n=4$: move to 0, N. $n=5$: can reach 4 or 2, and 2 is P, so N. $n=6$: can reach 5, 3, 2; 2
is P, so N. $n=7$: reaches 6, 4, 3, all N, so P. Continuing:</p>
""" + pn_table((1, 3, 4), 17) + r"""
<p><b>Guess.</b> The P positions are $n\equiv0$ or $2\pmod 7$.</p>
<p><b>Prove.</b> We check the two rules. (1) From a P position ($n\equiv0,2$) every move goes to an N position: removing
$1,3,4$ from $n\equiv0$ gives $6,4,3$, and from $n\equiv2$ gives $1,6,5\pmod 7$; none is 0 or 2. (2) From every other
position some move goes to P: from $1$, remove 1 (to 0); from $3$, remove 1 (to 2) or 3; from $4$, remove 4 (to 0); from $5$,
remove 3 (to 2); from $6$, remove 4 (to 2). So the second player wins exactly when $n\equiv0$ or $2\pmod7$.</p>""") + r"""

""" + trap(r"""<p>A pattern in a table is only a guess. The proof is checking the two rules (every move from P goes to N; some move
from N goes to P) for <b>all</b> positions, usually using the pattern's form (here, residues mod 7).</p>""") + r"""

<h2>Method 2: symmetry (copy the opponent)</h2>
<p>If you can reach a <b>symmetric</b> position, you can then answer each opponent move with its mirror image. The opponent
always moves first in each symmetric pair, so if they can move, so can you, and you never run out of moves first. The one
thing to check: <b>the mirror move is always legal</b>.</p>

""" + example(10, "coins in a circle",
r"""$n\ge3$ coins are arranged in a circle. Players alternately take either one coin, or two coins that are next to each other.
Whoever takes the last coin wins. Who wins?""",
r"""<p><b>The second player wins.</b> After the first player's move, the remaining coins form a single row (the circle has been
broken). If that row has at most 2 coins, take them all and win. Otherwise take 1 or 2 coins from the <b>exact middle</b>
of the row (1 if the row has odd length, 2 if even), leaving two equal rows. From now on, whatever the first player takes
from one row, take the same coins from the matching position in the other row.</p>
<p><b>Legality.</b> After each of the second player's moves, the position is two identical copies. The first player's move
affects only one copy (coins taken together are adjacent, so they're in the same row), and the matching coins in the other copy
are still there, and still adjacent. So the second player can always move, and therefore the first player is the one who
eventually can't.</p>""",
fig(coins_circle(), "After the first player takes one coin, the second takes the middle one.")) + r"""

<h2>Method 3: strategy stealing</h2>
<p>Sometimes you can prove the first player wins without knowing how. Suppose, for contradiction, that the second player has a
winning strategy. If the first player can make some move that “does no harm” (a move that could just as well have been part
of any later position), the first player can make it and then pretend to be the second player, following the second
player's strategy. That would make <i>both</i> players winners: a contradiction. Question 10.3 is the classic example.</p>
""" + method("three standard strategies",
r"""<ul>
<li><b>P/N positions:</b> compute small cases, guess the pattern, then prove: from P every move goes to N, and from N some
move goes to P.</li>
<li><b>Symmetry:</b> make the position symmetric (often using the centre or the middle), then copy. Check the copied move is always legal.</li>
<li><b>Strategy stealing:</b> if an extra move can never hurt, the first player wins (but we may not know how).</li>
<li>Always state <b>who</b> wins and <b>describe the strategy</b>; then prove it works against every reply.</li>
</ul>""") + check([
r"""Players alternately remove 1 or 2 stones from a pile; whoever takes the last stone wins. Which $n$ are P positions?""",
r"""Same game, but whoever takes the last stone <i>loses</i>. Which $n\ge1$ are P positions?""",
r"""In the 1, 3, 4 game above, who wins with $n=100$?"""],
[r"""multiples of 3""", r"""$n\equiv1\pmod3$""", r"""$100\equiv2\pmod 7$: the second player"""])

Q = []
Q.append(dict(id="10.1", tag="P-positions",
stmt=r"""There are $n$ stones in a pile. Two players alternately remove 1, 2 or 3 stones. The player who takes the last stone wins.
For which $n$ does the first player have a winning strategy?""",
hint=r"""Compute who wins for $n=0,1,\dots,8$.""",
key=r"""Small cases suggest the losing positions are the multiples of 4. Prove it: from a multiple of 4 every move leaves a
non-multiple, and from a non-multiple you can always move to a multiple of 4.""",
sol=pn_table((1, 2, 3), 13) + r"""
<p><b>Claim:</b> the player to move loses if and only if $4\mid n$.</p>
<ul>
<li>$n=0$: the player to move has no stones to take, because the opponent took the last one, so they have lost.</li>
<li>From $n\equiv0\pmod4$, $n\gt0$: removing 1, 2, 3 leaves $n-1,n-2,n-3$, none divisible by 4.</li>
<li>From $n\not\equiv0$: remove $r=n\bmod4\in\{1,2,3\}$ stones, leaving a multiple of 4.</li>
</ul>
<p>So a player facing a non-multiple of 4 can always hand the opponent a multiple of 4, and the opponent can never return one.
The pile shrinks, so eventually the opponent faces 0 and has lost.</p>""",
answer=r"""The first player wins if and only if $n$ is not a multiple of 4."""))

Q.append(dict(id="10.2", tag="symmetry",
stmt=r"""Two players take turns placing identical circular coins on a circular table. Coins must lie entirely on the table and must
not overlap. The player who cannot move loses. Who wins?""",
hint=r"""The first player can use the centre of the table.""",
key=r"""The first player puts a coin exactly in the centre, then answers every move with its reflection through the centre. The
position stays symmetric, so the reflected move is always legal.""",
sol=r"""<p><b>Strategy for the first player.</b> First, place a coin with its centre at the table's centre $O$. Afterwards,
whenever the second player places a coin $C$, place $C'$, the reflection of $C$ through $O$.</p>
<p><b>Legality.</b> After each of the first player's moves, the arrangement is symmetric about $O$. Suppose the second player
has just legally placed $C$ (radius $r$).</p>
<ul>
<li>$C'$ is on the table, since the table is symmetric about $O$.</li>
<li>$C'$ doesn't overlap $C$: $C$ doesn't overlap the central coin, so the centre of $C$ is at distance at least $2r$ from $O$.
Then the centres of $C$ and $C'$ are at distance at least $4r$.</li>
<li>$C'$ doesn't overlap any earlier coin $D$: otherwise $C$ would overlap $D'$, which is also on the table by symmetry. That
would make $C$ illegal.</li>
</ul>
<p>So the first player can always move. The game ends (only finitely many coins fit), so it is the second player who
eventually cannot move.</p>""",
answer=r"""The first player wins."""))

Q.append(dict(id="10.3", tag="strategy stealing: Chomp",
stmt=r"""A chocolate bar is an $m\times n$ grid of squares ($mn\gt1$); the top-left square is poisoned. Players alternately choose a
remaining square and eat it together with all squares below it and to its right. Whoever eats the poisoned square loses. Prove
that the first player has a winning strategy.""",
hint=r"""Suppose the second player has a winning strategy. What if the first player starts by eating only the bottom-right square?""",
key=r"""If the second player could win, they'd have a winning reply to “eat the bottom-right square”. But that reply removes the
bottom-right square anyway, so the first player could have played it as their first move, and stolen the win.""",
sol=r"""<p>The game is finite with no draws, so one player has a winning strategy. Suppose it is the second player.</p>
<p>Let the first player eat only the bottom-right square $s$ (allowed since $mn\gt1$, so $s$ is not the poisoned square). The
second player's strategy gives a reply, eating some square $x$, after which the second player (now “the player who just
moved”) wins with correct play.</p>
<p>Eating $x$ removes every square below and to the right of $x$, and $s$ is one of these. So the position after “$s$ then $x$”
is the same as after just “$x$”. Hence the first player could have eaten $x$ on move one, reaching that same winning position as
the player who just moved, and would then win by following the second player's strategy. This contradicts the assumption that
the second player has a winning strategy. So the first player does. $\blacksquare$</p>"""))

Q.append(dict(id="10.4", tag="Nim",
stmt=r"""There are several piles of stones, of sizes $h_1,\dots,h_k$. Players alternately choose a pile and remove any positive
number of stones from it. Whoever takes the last stone wins. Prove that the player to move loses exactly when
$h_1\oplus h_2\oplus\dots\oplus h_k=0$, where $\oplus$ is binary XOR (add in binary without carrying).""",
hint=r"""Two facts are needed. From XOR 0, every move gives XOR $\ne0$. From XOR $s\ne0$, look at the highest binary digit of $s$ and
find a pile that has a 1 there.""",
key=r"""Positions with XOR 0 are the losing ones. Changing one pile always changes the XOR, so from 0 you must leave non-zero. From
non-zero $s$, choose a pile $h$ with a 1 in the top bit of $s$ and reduce it to $h\oplus s\lt h$, which makes the XOR 0.""",
sol=r"""<p>Let $s=h_1\oplus\dots\oplus h_k$. (Example: piles $3,5,6$ give $011\oplus101\oplus110=000$, a losing position for the player
to move.)</p>
<p><b>From $s=0$, every move gives $s\ne0$.</b> A move changes one pile $h_i$ to $h_i'\ne h_i$. The new XOR is
$s\oplus h_i\oplus h_i'=h_i\oplus h_i'\ne0$.</p>
<p><b>From $s\ne0$, some move gives $s=0$.</b> Let $2^d$ be the highest power of 2 in the binary expansion of $s$. Since the
$2^d$ digit of $s$ is 1, an odd number of piles have a 1 in that digit; pick one, $h_i$. Let $h_i'=h_i\oplus s$. In binary,
$h_i'$ agrees with $h_i$ above digit $d$, and has 0 where $h_i$ has 1 at digit $d$. So $h_i'\lt h_i$, and the move “reduce pile
$i$ to $h_i'$” is legal. The new XOR is $s\oplus h_i\oplus h_i'=s\oplus s=0$.</p>
<p><b>Conclusion.</b> The final position (no stones) has XOR 0, and the player to move there has lost. A player facing $s\ne0$
can always hand over $s=0$, and the opponent can never hand back $s=0$. Every move removes stones, so the game ends, with the
player facing $s=0$ losing. $\blacksquare$</p>"""))

SECTION = dict(num=10, title="Games",
               blurb="winning and losing positions, symmetry, strategy stealing, Nim",
               intro="Who wins, and how?", teach=teach, questions=Q)
