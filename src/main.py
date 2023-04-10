import sys
import getopt
from tests import *

# Define default values for options
the = {
    "seed": 937162211,
    "dump": False,
    "halves": "",
    "reuse": True,
    "go": "data",
    "help": False,
    "file": "../etc/data/auto93.csv",
    "min": "min",
    "rest": 4
}
ENV = {}
b4 = {}

# Cache old option names so that later we can find any rogue options
for k, v in ENV.items():
    b4[k] = v

# Define short and long options
short_options = "hg"
long_options = []

def help():
    # Print help message
    print("""
    script.lua: an example script with help text and a test suite
    (c)2022, Tim Menzies <timm@ieee.org>, BSD-2
    USAGE:   script.lua  [OPTIONS] [-g ACTION]
    OPTIONS:
    -d, --dump    On crash, dump stack   = false
    -f, --file    Name of file           = ../etc/data/auto93.csv
    -g, --go      Start-up action        = data
    -h, --help    Show help              = false
    -p, --p       Distance coefficient   = 2
    -s, --seed    Random number seed     = 937162211
    ACTIONS:
    -g  the     Show settings
    -g  rand    Generate, reset, regenerate same
    -g  sym     Check syms
    -g  num     Check nums
    """)


def run_tests():
    # Execute the test cases and count the number of passing and failing test cases
    passing_count = 1
    failing_count = 0
    test_suite = [test_nums, test_sym, test_the, test_half, test_csv, test_data, test_clone, test_cliffs, test_tree, test_dist, test_sway, test_bins, test_explain]
    for test in test_suite:
        if test():
            passing_count += 1
        else:
            failing_count += 1
    print("Test Cases Passing: ", passing_count)

def main():
    try:
        # Parse command line arguments
        arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ('-h', '--help'):
                help()
            if current_argument in ("-g", '--go'):
                run_tests()
                
    except getopt.error as err:
        print(str(err))

if __name__ == "__main__":
    main()