import sys
from sat_instance.sat_instance import SATInstance

if __name__ == "__main__":
    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # linux test setup
    try:
        cnf_path = sys.argv[1]

    except IndexError as E:
        print("no cnf path specified, using basic example")
        cnf_path = "cnf_examples/basic.cnf"

    if sys.platform == "darwin":
        # osx
        cnf_path = "cnf_examples/sat_4color_200_1126_10020_preprocessed.cnf"
        cnf_path = "cnf_examples/count_10_4.cnf"
        satinstance = SATInstance(cnf_path, preprocess=False)

    else:
        satinstance = SATInstance(cnf_path, preprocess=True)

    satinstance.gen_basic_features()

    satinstance.gen_dpll_probing_features()

    # N.b. ubcsat binary currently only runs on linux
    satinstance.gen_local_search_probing_features()

    satinstance.gen_ansotegui_features()

    satinstance.gen_manthey_alfonso_graph_features()

    print(satinstance.features_dict)

    # satinstance.write_results()
