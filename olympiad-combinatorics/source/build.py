import importlib, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from front import FRONT

MODS = [m for m in ["s%02d" % i for i in range(12)] if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), m + ".py"))]
SECTIONS = [importlib.import_module(m).SECTION for m in MODS]

def qpage(q):
    return ('<div class="qpage">'
            '<div class="qhead"><span class="qnum">Question %s</span><span class="tag">%s</span></div>'
            '<div class="stmt">%s</div>'
            '<div class="hint"><b>Hint:</b> %s</div>'
            '</div>' % (q["id"], q["tag"], q["stmt"], q["hint"]))

def spage(q):
    ans = '<div class="answer"><b>Answer:</b> %s</div>' % q["answer"] if q.get("answer") else ""
    return ('<div class="spage">'
            '<div class="qhead"><span class="qnum">Solution %s</span><span class="tag">%s</span></div>'
            '<div class="stmt small">%s</div>'
            '<div class="key"><b>Key idea.</b> %s</div>'
            '<div class="sol">%s</div>%s'
            '</div>' % (q["id"], q["tag"], q["stmt"], q["key"], q["sol"], ans))

parts = [FRONT(SECTIONS)]
for s in SECTIONS:
    parts.append('<section class="teach" id="sec%d"><h1><span class="secnum">%d</span>%s</h1>'
                 '<div class="secintro">%s</div>%s</section>'
                 % (s["num"], s["num"], s["title"], s.get("intro", ""), s["teach"]))
    if s["questions"]:
        parts[-1] = parts[-1].replace("</section>", '<div class="box practise"><div class="boxhead">Now practise</div><div class="boxbody">'
            'Each question below has its own page with space to work and a hint printed upside down at the bottom. '
            'The full solution is on the following page.<div class="qlist">%s</div></div></div></section>'
            % "".join('<div><b>%s</b> &nbsp;<span class="tag">%s</span></div>' % (q["id"], q["tag"]) for q in s["questions"]))
    for q in s["questions"]:
        parts.append(qpage(q))
        parts.append(spage(q))

html = open(os.path.join(os.path.dirname(__file__), "template.html")).read().replace("%%BODY%%", "\n".join(parts))
open(os.path.join(os.path.dirname(__file__), "index.html"), "w").write(html)
print("ok", sum(len(s["questions"]) for s in SECTIONS), "questions")
