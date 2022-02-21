import os


def local_search_probe(cnf_file, saps=True, gsat=True):
    """
    Perform the local search probing with SAPS and GSAT algorithms, via ubcsat.
    :param cnf_file:
    :param saps:
    :param gsat:
    :return:
    """
    # should be run from project root directory

    # Run from ubcsat directory
    # run on pre-processed file

    # -inst cnf_name
    # -alg saps
    # -noimprove 0.1n -> what is this 0.1n??
    # -r stats
    # outfile
    # "best[mean+cv],firstlmstep[mean+median+cv+q10+q90],bestavgimpr[mean+cv],firstlmratio[mean+cv],estacl"
    # -runs num_runs
    # -gtimeout time_limit -> gtimeout as opposed to timeout

    # file = "cnf_examples/basic.cnf"
    if not os.path.isdir("ubcsat/results/"):
        os.mkdir("results")

    args_list = []
    args_list.append("./ubcsat/ubcsat_linux")
    # add file instance to probe
    args_list.append("-inst")
    args_list.append(cnf_file)

    # stop running if we are not improving
    args_list.append("-noimprove")
    args_list.append("0.1n")

    # set up statistics used as features
    args_list.append("-r stats")
    temp_fn = os.popen("mktemp /tmp/sapsgsat-XXXX").read().strip("\n")
    # args_list.append("ubcsat/results/out.txt")
    args_list.append(temp_fn)
    args_list.append("best[mean+cv],firstlmstep[mean+median+cv+q10+q90],bestavgimpr[mean+cv],firstlmratio[mean+cv],estacl")
    # this file gets overwritten every time, probably useful to look into temporary files in the future

    # number of runs of each algorithm
    num_runs = "10000"

    args_list.append("-runs")
    args_list.append(num_runs)

    timelimit = "2"
    args_list.append("-gtimeout")
    args_list.append(timelimit)

    args_list.append("-r out null")
    saps_res_dict = {}
    gsat_res_dict = {}

    if saps:
        # run the saps algorithm
        args_list.append("-alg")
        args_list.append("saps")

        command = " ".join(args_list)
        # print(command)
        # run saps
        os.system(command)

        saps_res_dict = read_ubcsat_results(True, temp_fn)

    if gsat:
        args_list[-1] = "gsat"
        command = " ".join(args_list)
        # print(command)
        # run gsat
        os.system(command)
        gsat_res_dict = read_ubcsat_results(False, temp_fn)

    return saps_res_dict, gsat_res_dict


def read_ubcsat_results(saps, temp_fn):
    """
    Read the results of the ubcsat saps or gsat runs, and put them into a dictionary
    :param saps:
    :return:
    """
    if saps:
        prefix = "saps_"
    else:
        prefix = "gsat_"
    res_dict = {}
    with open(temp_fn) as f:
        for line in f:
            line.strip("\n")
            res = line.split(" = ")
            if len(res) > 1:
                # print(res)
                res_dict[prefix + res[0]] = float(res[1])

    assert(len(res_dict) == 12)
    return res_dict
