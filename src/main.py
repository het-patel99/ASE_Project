from tabulate import tabulate
from data import Data
from explain import Explain, select_rows
from sway import SwayOptimizer
from decisiontreeOptimizer import DtreeOptimizer
from sway2 import sway2hpOptimizer
from options import options
from statistics import mean
from stats import cliffs_delta, bootstrap

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
  -f  --file        file to generate table of        = ../etc/data/auto93.csv
  -n  --itrs        number of iterations to run      = 20
  -w  --color       output with color                = true
  -s  --sway2       refresh the sway2 parameters     = true
"""

def main():
    options.parse_cli_settings(help_string)
    if options["help"]:
        print(help_string)
    else:
        results = {"all": [], "sway1": [], "xpln1": [], "sway2": [], "xpln2": [], "top": []}
        n_evals = {"all": 0, "sway1": 0, "xpln1": 0, "sway2": 0, "xpln2": 0, "top": 0}

        comparisons = [
            [["all", "all"], None],
            [["all", "sway1"], None],
            [["all", "sway2"], None],
            [["sway1", "sway2"], None],
            [["sway1", "xpln1"], None],
            [["sway1", "xpln2"], None],
            [["xpln1", "xpln2"], None],
            [["sway1", "top"], None]
        ]
        ranks = {"all": 0, "sway1": 0, "sway2": 0, "xpln1": 0, "xpln2": 0, "top": 0}
        count = 0
        data = Data(options["file"])

        sway2 = sway2hpOptimizer(
                    reuse=options["reuse"],
                    far=options["Far"],
                    halves=options["halves"],
                    rest=options["rest"],
                    i_min=options["min_cluster"],
                    file=options["file"],
                    sway2=options["sway2"],
                    p=options["P"]
                )
        sway1 = SwayOptimizer(
                reuse=options["reuse"],
                far=options["Far"],
                halves=options["halves"],
                rest=options["rest"],
                i_min=options["min_cluster"],
                p=options["P"]
            )
        
        # all_ordered = data.betters()
        # for idx, row in enumerate(all_ordered):
        #     row.rank = 1 + (idx/len(data.rows))*99

        while count < options["itrs"]:
            
            best, rest, evals_sway = sway1.run(data)

            x = Explain(best, rest)
            rule, _ = x.xpln(data, best, rest)

            if rule != -1:
                best_xpln2, _, _ = DtreeOptimizer(best=best, rest=rest).run(data)
                xpln2 = Data.clone(data,best_xpln2)
                selected_rows = select_rows(rule, data.rows)
                data1 = Data.clone(data, selected_rows)
                best2, _, evals_sway2 = sway2.run(data)
                top2, _ = data.betters(len(best.rows))
                top = Data.clone(data, top2)
                results['all'].append(data)
                results['sway1'].append(best)
                results['xpln1'].append(data1)
                results['xpln2'].append(xpln2)
                results['top'].append(top)
                results['sway2'].append(best2)

                ranks['all'] += (mean([r.rank for r in data.rows]))
                ranks['sway1'] += (mean([r.rank for r in best.rows]))
                ranks['xpln1'] +=(mean([r.rank for r in data1.rows]))
                ranks['xpln2']+=(mean([r.rank for r in xpln2.rows]))
                ranks['sway2']+=(mean([r.rank for r in best2.rows]))
                ranks['top']+=(mean([r.rank for r in top.rows]))

                # accumulate the number of evals
                # for all: 0 evaluations 
                n_evals["all"] += 0
                n_evals["sway1"] += evals_sway
                n_evals["sway2"] += evals_sway2

                # xpln uses the same number of evals since it just uses the data from
                # sway to generate rules, no extra evals needed
                n_evals["xpln1"] += evals_sway
                n_evals["xpln2"] += evals_sway
                n_evals["top"] += len(data.rows)


                for i in range(len(comparisons)):
                    [base, diff], result = comparisons[i]
                    if result is None:
                        comparisons[i][1] = ["=" for _ in range(len(data.cols.y))]
                    for k in range(len(data.cols.y)):
                        if comparisons[i][1][k] == "=":
                            base_y, diff_y = results[base][count].cols.y[k], results[diff][count].cols.y[k]
                            equals = bootstrap(base_y.has(), diff_y.has()) and cliffs_delta(base_y.has(), diff_y.has())

                            if not equals:
                                if i == 0:
                                    print("WARNING: all to all {} {} {}".format(i, k, "false"))
                                    print(f"FAILED: all to all {results[base][count].cols.y[k].txt}")

                                comparisons[i][1][k] = "≠"

                count += 1

        headers = [y.txt for y in data.cols.y]
        table = []

        for key, value in results.items():
            stats = get_result(value)
            stats_list = [stats[y] for y in headers]
            stats_list += [n_evals[key] / options["itrs"]]
            # stats_list += [ranks[key] / options["itrs"]]
            stats_list = [round(n, 1) for n in stats_list]
            table.append([key] + stats_list)
        
        maxes = []
        h = [v[0] for v in table]
        for i in range(len(headers)):
            header_vals = [v[i+1] for v in table]
            fun = max if headers[i][-1] == "+" else min
            vals = [table[h.index("sway1")][i+1],table[h.index("sway2")][i+1]]
            vals_x = [table[h.index("xpln1")][i+1],table[h.index("xpln2")][i+1]]
            maxes.append([headers[i],
                          table[header_vals.index(fun(header_vals))][0],
                           vals.index(fun(vals)) == 1,
                           vals_x.index(fun(vals_x)) == 1])
            
        if options["color"]:
            for i, header in enumerate(headers):
                header_vals = [v[i + 1] for v in table]
                fun = max if header[-1] == "+" else min
                max_min_val = fun(header_vals)
                max_min_index = header_vals.index(max_min_val)
                table[max_min_index][i + 1] = f"\033[92m{table[max_min_index][i + 1]}\033[0m"

        print(tabulate(table, headers=headers + ["Avg evals"], numalign="right"))
        print()
     
        m_headers = ["Best", "Beat Sway?", "Beat Xpln?"]
        print(tabulate(maxes, headers=m_headers,numalign="right"))
        print()
        table = []
        for [base, diff], result in comparisons:
            table.append([f"{base} to {diff}"] + result)

        print(tabulate(table, headers=headers, numalign="right"))

def get_result(data_array):
    result = {}
    num_itrs = options["itrs"]
    for item in data_array:
        stats = item.stats()
        for k, v in stats.items():
            result[k] = result.get(k, 0) + v
    for k, v in result.items():
        result[k] /= num_itrs
    return result

main()
