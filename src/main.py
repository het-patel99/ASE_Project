from tabulate import tabulate
from data import Data
from explain import Explain, select_rows
from sway import SwayOptimizer
from options import options
from stats import cliffs_delta, bootstrap
from data_analyse import help_string

def main():
    options.parse_cli_settings(help_string)
    if options["help"]:
        print(help_string)
    else:
        results = {"all": [], "sway": [], "xpln": [], "top": []}
        n_evals = {"all": 0, "sway": 0, "xpln": 0, "top": 0}

        comparisons = [
            [["all", "all"], None],
            [["all", "sway"], None],
            [["sway", "xpln"], None],
            [["sway", "top"], None]
        ]

        count = 0
        data = None

        while count < options["itrs"]:
            data = Data(options["file"])
            reuse=options["reuse"]
            rest=options["rest"]
            far=options["Far"]
            halves=options["halves"]
            i_min=options["min_cluster"]
            best, rest, evals_sway = SwayOptimizer(reuse = reuse,rest = rest,far = far, halves = halves,i_min = i_min).run(data)

            x = Explain(best, rest)
            rule, _ = x.xpln(data, best, rest)

            if rule != -1:
                selected_rows = select_rows(rule, data.rows)
                data1 = Data.clone(data, selected_rows)
                results['all'].append(data)
                results['sway'].append(best)
                results['xpln'].append(data1)
                top2, _ = data.betters(len(best.rows))
                top = Data.clone(data, top2)
                results['top'].append(top)
                n_evals["all"] += 0
                n_evals["sway"] += evals_sway
                n_evals["xpln"] += evals_sway
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
            result = {}
            for item in value:
                stats = item.stats()
                for k1, v1 in stats.items():
                    result[k1] = result.get(k1, 0) + v1
            for k2, v2 in result.items():
                result[k2] /= options["itrs"]
            stats_list = [key] + [result[y] for y in headers]
            stats_list.append(n_evals[key] / options["itrs"])
            table.append(stats_list)
        
        if options["color"]:
            for i, header in enumerate(headers):
                header_vals = [v[i + 1] for v in table]
                fun = max if header[-1] == "+" else min
                max_min_val = fun(header_vals)
                max_min_index = header_vals.index(max_min_val)
                table[max_min_index][i + 1] = f"\033[92m{table[max_min_index][i + 1]}\033[0m"

        print(tabulate(table, headers=headers + ["Avg evals"], numalign="right"))
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
