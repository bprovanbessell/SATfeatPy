
def local_search_probe(saps=True, gsat=True):
    # -inst cnf_name
    # -alg saps
    # -noimprove 0.1n -> what is this 0.1n??
    # -r stats
    # outfile
    # "best[mean+cv],firstlmstep[mean+median+cv+q10+q90],bestavgimpr[mean+cv],firstlmratio[mean+cv],estacl"
    # -runs num_runs
    # -gtimeout time_limit -> gtimeout as opposed to timeout

    file = "cnf_examples/basic.cnf"
    file_inst = "-inst " + file

    no_improve = " -noimprove " + "0.1n"

    stats = " -r stats out.txt"
    stats2 = " best[mean+cv],firstlmstep[mean+median+cv+q10+q90],bestavgimpr[mean+cv],firstlmratio[mean+cv],estacl"

    runs = " -runs 200"

    timelimit = 2
    gtimeout = " -gtimeout " + str(timelimit)

    if saps:
        alg = "saps"
        alg_inst = " -alg " + alg
        command = "./ubcsat " + file_inst + alg_inst + no_improve + stats + stats2 + runs

    if gsat:
        alg = "gsat"
        alg_inst = " -alg " + alg
        command = "./ubcsat " + file_inst + alg_inst + no_improve + stats + stats2 + runs

    print(command)



local_search_probe()