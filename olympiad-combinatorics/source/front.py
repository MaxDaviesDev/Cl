def FRONT(sections):
    rows = []
    for s in sections:
        qs = s["questions"]
        qtxt = ("Questions %s–%s" % (qs[0]["id"], qs[-1]["id"])) if qs else "read first"
        rows.append('<tr><td class="n">%d</td><td><b>%s</b><br><span class="d">%s</span></td><td class="q">%s</td></tr>'
                    % (s["num"], s["title"], s["blurb"], qtxt))
    return r"""
<div class="cover">
  <div class="title">Olympiad Combinatorics</div>
  <div class="sub">Learn it, then practise it: a method pack for BMO1</div>
  <div class="meta">11 techniques &nbsp;·&nbsp; explanations and worked examples &nbsp;·&nbsp; 39 questions with full solutions</div>
</div>

<div class="front">
<h1>How to use this pack</h1>
<p>Combinatorics at olympiad level is less about knowing formulas and more about recognising which <i>idea</i> a problem
needs. This pack is built to teach those ideas from scratch, then make you use them.</p>
<p>Every section has two halves.</p>
<ol>
<li><b>Learn.</b> The idea is explained in plain language, with the reasoning behind every fact. Then come
<span style="color:#2f7a4a"><b>worked examples</b></span>, solved step by step with commentary on <i>why</i> each step is
taken, not just what it is. Coloured boxes mark the
<span style="color:#8a5a0b"><b>key facts</b></span>, the <span style="color:#2d5aa0"><b>method</b></span> (when to reach for it and how),
<span style="color:#6b4fa0"><b>why it works</b></span>, and the <span style="color:#a83232"><b>common traps</b></span>. Each Learn part ends
with a short <span style="color:#1d7480"><b>quick check</b></span>; the answers are printed upside down.</li>
<li><b>Practise.</b> The questions. Each has its own page with room to work and a hint printed upside down at the
bottom. Only turn it round when you've been stuck for a while. The model solution is on the next page, opening
with the <i>key idea</i> in one or two sentences.</li>
</ol>
<p><b>How to study a section.</b> Read the Learn part with a pencil. Before you read the solution to a worked example,
cover it and try it yourself for a few minutes. Then attempt the questions under exam conditions. When you check a
solution, ask: <i>what was the one idea, and what in the problem should have pointed me to it?</i> Write that down.
That sentence is what you'll remember in the exam.</p>
<p><b>The single most useful habit:</b> before anything else, try small cases ($n = 1, 2, 3, 4$) and look for the pattern.</p>
<p>Questions marked with a competition (IMO 1972, IMO 1998) are past olympiad problems. The rest are classics that every
olympiad student is expected to know.</p>

<h2>Contents</h2>
<table class="toc">""" + "".join(rows) + """</table>
</div>
"""
