import sat_instance.sat_instance
from sat_instance.sat_instance import SATInstance
import glob
import csv


def bulk_gen_features(path_to_cnfs="/projects/satdb/dataset_final/", results_csv="features.csv"):
    # for each file, we need to create a sat_instance for it
    # file_list = glob.glob(path_to_cnfs + "sat_4*.cnf")
    file_list = glob.glob(path_to_cnfs + "*.cnf")
    dict_keys = ['c', 'v', 'clauses_vars_ratio', 'vars_clauses_ratio', 'vcg_var_mean', 'vcg_var_coeff', 'vcg_var_min',
               'vcg_var_max', 'vcg_var_entropy', 'vcg_clause_mean', 'vcg_clause_coeff', 'vcg_clause_min',
               'vcg_clause_max', 'vcg_clause_entropy', 'vg_mean', 'vg_coeff', 'vg_min', 'vg_max', 'pnc_ratio_mean',
               'pnc_ratio_coeff', 'pnc_ratio_min', 'pnc_ratio_max', 'pnc_ratio_entropy', 'pnv_ratio_mean',
               'pnv_ratio_coeff', 'pnv_ratio_min', 'pnv_ratio_max', 'pnv_ratio_entropy', 'pnv_ratio_stdev',
               'binary_ratio', 'ternary_ratio', 'ternary+', 'hc_fraction', 'hc_var_mean', 'hc_var_coeff', 'hc_var_min',
               'hc_var_max', 'hc_var_entropy', 'unit_props_at_depth_1', 'unit_props_at_depth_4',
               'unit_props_at_depth_16', 'unit_props_at_depth_64', 'unit_props_at_depth_256',
               'mean_depth_to_contradiction_over_vars', 'estimate_log_number_nodes_over_vars', 'vig_modularty',
               'vig_d_poly', 'cvig_db_poly', 'variable_alpha']

    with open(results_csv, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=dict_keys)
        writer.writeheader()

        for i, file_name in enumerate(file_list):
            print(file_name)
            print("File ", i, "of ", len(file_list))
            sat_inst = SATInstance(file_name, preprocess=False)

            sat_inst.gen_basic_features()
            sat_inst.gen_dpll_probing_features()
            # linux only
            # sat_inst.gen_local_search_probing_features()
            sat_inst.gen_ansotegui_features()
            # sat_inst.gen_manthey_alfonso_graph_features()

            writer.writerow(sat_inst.features_dict)

    f.close()


if __name__ == "__main__":
    path_to_cnfs = "cnf_examples/"

    bulk_gen_features(path_to_cnfs)
