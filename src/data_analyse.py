import os
import pandas as pd
from data import Data
from num import Num
from options import options
from stats import cliffs_delta, bootstrap
from tabulate import tabulate

# Define command-line options
help_string = """
project: multi-objective
semi-supervised explanation system:
(c) Group 18
  
USAGE: python3 main.py [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins        initial number of bins           = 16
  -c  --cliff       cliff's delta threshold          = .147
  -d  --D           different is over sd*d           = .35
  -F  --Far         distance to distant              = .95
  -h  --help        show help                        = false
  -H  --halves      search space for clustering      = 512
  -I  --min_cluster size of smallest cluster         = .5
  -M  --Max         numbers                          = 512
  -p  --P           dist coefficient                 = 2
  -R  --rest        how many of rest to sample       = 10
  -r  --reuse       child splits reuse a parent pole = true
  -x  --bootstrap   number of samples to bootstrap   = 512    
  -o  --ci          confidence interval              = 0.05
  -f  --file        file to generate table of        = ../etc/data/auto2.csv
  -n  --itrs        number of iterations to run      = 20
  -w  --color       output with color                = true
  -s  --sway2       refresh the sway2 parameters     = true
"""
options.parse_cli_settings(help_string)