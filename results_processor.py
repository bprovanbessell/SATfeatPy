def get_sat_unsat_results(results_txt):

    fn_res = []
    with open(results_txt, 'r') as res_file:

        for i, line in enumerate(res_file):
            print(line)
            if i in [0, 1, 2, 53]:
                continue

            splitted = line.split()
            file_name = splitted[0]
            result = splitted[2]

            fn_res.append((file_name, result))

    return fn_res

# test this
def get_sat_unsat_2007_results(results_txt='phase_1.txt'):
    fn_res = {}
    with open(results_txt, 'r') as res_file:
        for i, line in enumerate(res_file):
            if i in [0, 1]:
                continue

            splitted = line.split()
            # print(splitted)
            file_name = splitted[0]
            result = splitted[2]

            if result == "SAT":
                fn_res[file_name] = result
            if result == "UNSAT":
                if fn_res.get(file_name, None) is not None:
                    fn_res[file_name] = result

    return fn_res


if __name__ == "__main__":

    # res = get_sat_unsat_results("2006_instances/SAT-Race_TS_1/Solver2005-results.txt")
    res = get_sat_unsat_2007_results("2007/phase1.txt")
    print(res)
    print(len(res))