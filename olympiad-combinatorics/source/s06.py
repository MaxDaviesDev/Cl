from lib import *

# 5x5 minus centre, pinwheel of four 2x3 rectangles, each split into 3 dominoes
pin = [[None] * 5 for _ in range(5)]
k = 0
def put(cells):
    global k
    for r, c in cells: pin[r][c] = k
    k += 1
# top-left rows 0-1, cols 0-2: three vertical dominoes
for c in range(3): put([(0, c), (1, c)])
# top-right rows 0-2, cols 3-4: three horizontal dominoes
for r in range(3): put([(r, 3), (r, 4)])
# bottom-right rows 3-4, cols 2-4: vertical
for c in range(2, 5): put([(3, c), (4, c)])
# bottom-left rows 2-4, cols 0-1: horizontal
for r in range(2, 5): put([(r, 0), (r, 1)])

# tromino tiling of 8x8 minus (3,3), found by computer search and checked
TRO = [[0, 0, 0, 1, 1, 1, 2, 3],
       [4, 4, 4, 5, 5, 5, 2, 3],
       [6, 7, None, 8, 8, 8, 2, 3],
       [6, 7, 9, 9, 9, 10, 10, 10],
       [6, 7, 11, 11, 11, 12, 12, 12],
       [13, 13, 13, 14, 14, 14, 15, 16],
       [17, 17, 17, 18, 18, 18, 15, 16],
       [19, 19, 19, 20, 20, 20, 15, 16]]

def strip_colouring():
    txt = {(r, c): str((r + c) % 3) for r in range(4) for c in range(7)}
    fills = {(1, c): "#fbe3b4" for c in range(1, 4)}
    fills.update({(0, 5): "#cfe0f4", (1, 5): "#cfe0f4", (2, 5): "#cfe0f4"})
    return board(4, 7, cell=20, text=txt, fill=fills)

teach = r"""
<p>Colouring is an invariant argument for <b>tiling and covering</b> problems. You colour the board in a clever way so that
every tile, wherever it is placed, covers the same number of squares of each colour. Then you compare with the colour
counts of the region you're trying to cover. If they don't match, no tiling exists.</p>

<h2>The chessboard colouring</h2>
<p>Colour the squares black and white like a chessboard: square $(i,j)$ (row $i$, column $j$) is black when $i+j$ is even.
Two squares that share a side have different colours. So a <b>domino</b> ($1\times2$ or $2\times1$), wherever it is
placed, covers exactly one black and one white square. Therefore:</p>
""" + theorem("the domino count",
r"""<p>If a region can be tiled by dominoes, it has <b>equally many</b> black and white squares. Equivalently: if the numbers are
different, the region can't be tiled.</p>""") + r"""

""" + example(6, "two boards with a square removed",
r"""(a) Can a $5\times5$ board with its <i>centre</i> square removed be tiled by dominoes?
<br>(b) What if instead we remove the square in row 1, column 2?""",
r"""<p><b>Count colours.</b> A $5\times5$ board has 13 squares with $i+j$ even (black, including all four corners) and 12 white.</p>
<p><b>(b) first.</b> The square $(1,2)$ has $i+j=3$, odd, so it's white. Removing it leaves 13 black and 11 white. Each domino
covers one of each, so 12 dominoes would cover 12 of each. Impossible: <b>no</b>.</p>
<p><b>(a)</b> The centre $(3,3)$ is black. Removing it leaves 12 black and 12 white. The colouring does <i>not</i> rule out a tiling
here, but it doesn't prove one exists either. For that we need to <b>construct</b> one, and the picture shows one: four
$2\times3$ rectangles arranged like a pinwheel, each made of 3 dominoes. So the answer is <b>yes</b>.</p>""",
figrow(fig(board(5, 5, cell=20, chess=True, cross=[(2, 2)]), "(a) centre removed"),
       fig(tiling(pin, cell=20), "a tiling of (a)"),
       fig(board(5, 5, cell=20, chess=True, cross=[(0, 1)]), "(b) a white square removed"))) + r"""

""" + trap(r"""<p>A colouring argument proves <b>impossibility</b> only. Matching colour counts never prove that a tiling exists: for
that you must give a tiling. (For example, a $2\times2$ board with two diagonally opposite squares removed has one
black and one white square left, but can't be covered by a domino.)</p>""") + r"""

<h2>Colourings for longer tiles</h2>
<p>For a $1\times k$ strip, use $k$ colours: colour square $(i,j)$ with $(i+j)\bmod k$. Along any row or column, the colours
cycle $0,1,\dots,k-1,0,1,\dots$, so any $k$ consecutive squares in a line contain <b>one of each colour</b>. Wherever a
$1\times k$ strip is placed, it covers one square of each colour.</p>
""" + fig(strip_colouring(), "The colouring $(i+j) \\bmod 3$: every $1\\times3$ strip, horizontal or vertical, covers one 0, one 1 and one 2.") + r"""

""" + example(6, "an unbalanced tile",
r"""Can a $6\times6$ board be tiled by T-tetrominoes (four squares in a T shape)?""",
r"""<p><b>Count.</b> The area is 36, so a tiling would use 9 T-tetrominoes. The board has 18 black and 18 white squares.</p>
<p><b>What one tile covers.</b> With the chessboard colouring, a T-tetromino covers its centre square and the three squares
next to it. The three neighbours all have the opposite colour to the centre. So each T covers either 3 black + 1 white, or
1 black + 3 white: it changes the difference “black minus white” by $+2$ or $-2$.</p>
<p><b>Parity.</b> With 9 tiles, black minus white is a sum of nine terms each $\pm2$. If $p$ tiles are $+2$, the sum is
$2p-2(9-p)=4p-18$, which is never 0 because $p$ would have to be $4.5$. But the board has black minus white $=0$.
So: <b>no</b>.</p>
<p><b>Lesson.</b> Even when tiles don't cover colours equally, the colouring still controls what's possible.</p>""") + r"""

""" + method("colour so each tile looks the same",
r"""<ul>
<li><b>Dominoes:</b> chessboard colouring.</li>
<li><b>$1\times k$ strips:</b> colour by $(i+j)\bmod k$, or by $i\bmod k$, so each strip covers one of each colour.</li>
<li><b>$1\times4$ strips:</b> also try colouring $2\times2$ <i>blocks</i> like a chessboard.</li>
<li>Count each colour on the board and compare with what the tiles can cover.</li>
<li>If two different colourings each give a condition, <b>combine</b> them.</li>
<li>To prove a tiling <b>exists</b>, draw one, often by building it from smaller tileable pieces or by induction.</li>
</ul>""") + check([
r"""Can a $3\times3$ board with one corner removed be tiled by dominoes?""",
r"""Can a $7\times7$ board with its centre square removed be tiled by $1\times2$ dominoes?""",
r"""How many black squares does a $7\times7$ chessboard-coloured board have, if the corners are black?"""],
[r"""Yes: one domino for the rest of row 1, one for the rest of column 1, two for the $2\times2$ block left""",
 r"""Yes: colours balance (centre is black) and a pinwheel of four $3\times4$ rectangles works""", r"""$25$"""])

Q = []
Q.append(dict(id="6.1", tag="dominoes",
stmt=r"""Two diagonally opposite corner squares are removed from an $8\times8$ chessboard. Can the remaining 62 squares be covered
by 31 dominoes ($1\times2$ rectangles)?""",
hint=r"""What colour are the removed squares?""",
key=r"""Every domino covers one black and one white square. Opposite corners have the same colour, so the colours are unbalanced.""",
sol=fig(board(8, 8, cell=17, chess=True, cross=[(0, 0), (7, 7)])) + r"""
<p>Colour the board as a chessboard. Opposite corners have the same colour (say white), since moving from one to the other
changes the row by 7 and the column by 7, so $i+j$ changes by 14. The remaining board has 32 black and 30 white squares.
Every domino covers two adjacent squares, one black and one white, so 31 dominoes cover exactly 31 of each. Since
$32\ne31$, this is impossible.</p>""",
answer=r"""No."""))

Q.append(dict(id="6.2", tag="$1\\times4$ strips",
stmt=r"""Can a $10\times10$ board be tiled with $1\times4$ rectangles?""",
hint=r"""Divide the board into $2\times2$ blocks and colour the blocks like a chessboard.""",
key=r"""With $2\times2$ blocks coloured alternately, every $1\times4$ strip covers exactly 2 black and 2 white cells. The
$10\times10$ board has $5\times5$ blocks, an odd number, so the colours are unbalanced.""",
sol=fig(board(10, 10, cell=14, fill={(r, c): SHADE for r in range(10) for c in range(10) if (r // 2 + c // 2) % 2 == 0})) + r"""
<p>Number rows and columns 0 to 9, and colour cell $(i,j)$ black if $\lfloor i/2\rfloor+\lfloor j/2\rfloor$ is even. This
colours the $2\times2$ blocks like a chessboard.</p>
<p><b>Each strip covers 2 + 2.</b> A horizontal strip covers 4 consecutive columns $j,\dots,j+3$ in one row. The values
$\lfloor j/2\rfloor$ along it are two consecutive integers, each appearing twice, so it covers 2 black and 2 white cells.
Vertical strips are the same.</p>
<p><b>Count.</b> There are $5\times5=25$ blocks: 13 black and 12 white. So the board has 52 black and 48 white cells. A
tiling by 25 strips would cover 50 of each, so it is impossible.</p>""",
answer=r"""No."""))

Q.append(dict(id="6.3", tag="two colourings",
stmt=r"""An $8\times8$ board is covered by 21 straight trominoes ($1\times3$ rectangles) and one single square. Which squares can the
single square occupy? (Number rows and columns 1 to 8.)""",
hint=r"""Colour cell $(i,j)$ with $(i+j)\bmod3$. Then use a second colouring, $(i-j)\bmod 3$.""",
key=r"""Under the colouring $(i+j)\bmod3$, each tromino covers one cell of each colour. The board has 22 cells of colour 0 and
21 of each other, so the single square has colour 0. The colouring $(i-j)\bmod3$ gives the same condition. Together these
force $i,j\in\{3,6\}$.""",
sol=r"""<p><b>Colouring 1.</b> Colour $(i,j)$ with $(i+j)\bmod3$. A tromino covers three consecutive cells in a row or column, so
$i+j$ takes three consecutive values, one in each class mod 3. Hence the 21 trominoes cover exactly 21 cells of each colour.
Counting the board directly gives 22 cells of colour 0 and 21 each of colours 1 and 2. So the single square has
$i+j\equiv0\pmod3$.</p>
<p><b>Colouring 2.</b> By the same argument with $(i-j)\bmod3$, which also has counts 22, 21, 21 with colour 0 the large one,
the single square has $i-j\equiv0\pmod3$.</p>
<p><b>Combine.</b> Adding gives $2i\equiv0$, so $i\equiv0\pmod 3$, and then $j\equiv0\pmod3$. So $i,j\in\{3,6\}$: the square is one
of $(3,3),(3,6),(6,3),(6,6)$.</p>
<p><b>All four are possible.</b> Here is a tiling with the single square at $(3,3)$. The other three positions follow by
reflecting the board.</p>""" + figrow(
fig(board(8, 8, cell=17, text={(r, c): str((r + c + 2) % 3) for r in range(8) for c in range(8)}, label_axes=True), "$(i+j)\\bmod 3$"),
fig(tiling(TRO, cell=19), "single square at $(3,3)$")),
answer=r"""Exactly the four squares $(3,3)$, $(3,6)$, $(6,3)$, $(6,6)$."""))

SECTION = dict(num=6, title="Colouring and tiling",
               blurb="colour the board so every tile covers the same colours, then count",
               intro="Invariants for tiling problems.", teach=teach, questions=Q)
