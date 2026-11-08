# Olympiad Combinatorics: Learn and Practise

`Olympiad_Combinatorics_Learn_and_Practise.pdf` is a rebuilt version of the BMO1 combinatorics method pack.
Each of the 11 sections now teaches the idea first (explanations, worked examples, why-it-works boxes,
common traps, a quick check), then gives the original 39 questions, each on its own page with an upside-down
hint and the full solution on the next page.

## Rebuilding

```
cd source
npm install katex@0.16.11 playwright
python3 build.py      # writes index.html
node render.js ../Olympiad_Combinatorics_Learn_and_Practise.pdf
```
