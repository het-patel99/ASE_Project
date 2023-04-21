# Automated Software Engineering Project

[![DOI](https://zenodo.org/badge/596268879.svg)](https://zenodo.org/badge/latestdoi/596268879)
![GitHub](https://img.shields.io/github/license/het-patel99/ASE_Project)
![GitHub issues](https://img.shields.io/github/issues/het-patel99/ASE_Project)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/het-patel99/ASE_Project)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/het-patel99/ASE_Project/unit_test.yml)
![github workflow](https://github.com/het-patel99/ASE_Project/actions/workflows/unit_test.yml/badge.svg)

s# How to Run??s

1. First Install requirement by pip3 install -r requirement.txt
2. go to src/ directory and then python3 main.py
3. To run all the files :
   - cd ..
   - python3 testScript.py

After running the testScript.py the output will be stored in /etc/out/filename file is stored inside the etc/out/ directory

Here is the SSM.out file:
refreshing sway
Far [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
halves [100, 200, 300, 400, 500, 600, 700]
min_cluster [0.0, 0.2, 0.4, 0.6]
Max [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
P [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
rest [1, 2, 3, 4]
reuse [True, False]
new: {'Far': 0.95, 'halves': 400, 'min_cluster': 0.6, 'Max': 16, 'P': 1.2, 'rest': 2, 'reuse': True}

         NUMBERITERATIONS-    TIMETOSOLUTION-    Avg evals

---

all 6 133.5 0
sway1 5 115.8 10
xpln1 5.3 119.1 10
sway2 5.5 113.9 23.1
xpln2 5 115.8 10
top 4 60 239360

                   Best    Beat Sway?    Beat Xpln?

---

NUMBERITERATIONS- top False True
TIMETOSOLUTION- top True True

                NUMBERITERATIONS-    TIMETOSOLUTION-

---

all to all = =
all to sway1 ≠ ≠
all to sway2 ≠ ≠
sway1 to sway2 ≠ ≠
sway1 to xpln1 ≠ ≠
sway1 to xpln2 ≠ ≠
xpln1 to xpln2 ≠ ≠
sway1 to top ≠ ≠
1260.86user 1.85system 21:02.86elapsed 99%CPU (0avgtext+0avgdata 1141556maxresident)k
0inputs+16outputs (0major+1221519minor)pagefaults 0swaps

# Team Member (Group 18)

1. Het Patel (hpatel28)
2. Shaunak Patel (shpate25)
