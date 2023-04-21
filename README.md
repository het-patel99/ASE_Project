# Automated Software Engineering Project

## How to Run??

1. First Install requirement by pip3 install -r requirement.txt
2. go to src/ directory and then python3 main.py
3. To run all the files :
   - python3 testScript.py

After running the testScript.py the output will be stored in /etc/out/filename file is stored inside the etc/out/ directory

[REPORT LINK](https://github.com/het-patel99/ASE_Project/blob/main/report/ASE_Project_Report.pdf)

Here is the auto2.out file:
```
refreshing sway
Far [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
halves [100, 200, 300, 400, 500, 600, 700]
min_cluster [0.0, 0.2, 0.4, 0.6]
Max [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
P [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
rest [1, 2, 3, 4]
reuse [True, False]
new:  {'Far': 0.75, 'halves': 500, 'min_cluster': 0.2, 'Max': 11, 'P': 2.0, 'rest': 3, 'reuse': True}

         CityMPG+    HighwayMPG+    Weight-    Class-    Avg evals
-----  ----------  -------------  ---------  --------  -----------
all            21             28       3040      17.7            0
sway1        31.1           35.5     2125.8       8.8            5
xpln1        29.7           34.1     2223.2      10.3            5
sway2        31.6           37.2     2123.2       9.6         13.3
xpln2        29.7             34     2169.8         9            5
top          35.7           41.9       2045       8.6           93

             Best    Beat Sway?    Beat Xpln?
-----------  ------  ------------  ------------
CityMPG+     top     True          False
HighwayMPG+  top     True          False
Weight-      top     True          True
Class-       top     False         True

                CityMPG+    HighwayMPG+    Weight-    Class-
--------------  ----------  -------------  ---------  --------
all to all      =           =              =          =
all to sway1    ≠           ≠              ≠          ≠
all to sway2    ≠           ≠              ≠          ≠
sway1 to sway2  ≠           ≠              ≠          ≠
sway1 to xpln1  ≠           ≠              ≠          ≠
sway1 to xpln2  ≠           ≠              ≠          ≠
xpln1 to xpln2  ≠           ≠              ≠          ≠
sway1 to top    ≠           ≠              ≠          ≠
21.31user 0.11system 0:21.43elapsed 99%CPU (0avgtext+0avgdata 189516maxresident)k
0inputs+16outputs (0major+46029minor)pagefaults 0swaps
```
# Team Member (Group 18)

1. Het Patel (hpatel28)
2. Shaunak Patel (shpate25)
