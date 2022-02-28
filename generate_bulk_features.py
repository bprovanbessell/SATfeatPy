import time

import sat_instance.sat_instance
from sat_instance.sat_instance import SATInstance
import glob
import csv


def bulk_gen_features(path_to_cnfs="/projects/satdb/dataset_final/", results_csv="features.csv", file_type="*"):
    # for each file, we need to create a sat_instance for it
    # file_list = glob.glob(path_to_cnfs + "sat_4*.cnf")
    file_list = glob.glob(path_to_cnfs + file_type + ".cnf")
    dict_keys = ['c', 'v', 'clauses_vars_ratio', 'vars_clauses_ratio', 'vcg_var_mean', 'vcg_var_coeff', 'vcg_var_min',
     'vcg_var_max', 'vcg_var_entropy', 'vcg_clause_mean', 'vcg_clause_coeff', 'vcg_clause_min', 'vcg_clause_max',
     'vcg_clause_entropy', 'vg_mean', 'vg_coeff', 'vg_min', 'vg_max', 'pnc_ratio_mean', 'pnc_ratio_coeff',
     'pnc_ratio_min', 'pnc_ratio_max', 'pnc_ratio_entropy', 'pnv_ratio_mean', 'pnv_ratio_coeff', 'pnv_ratio_min',
     'pnv_ratio_max', 'pnv_ratio_entropy', 'pnv_ratio_stdev', 'binary_ratio', 'ternary_ratio', 'ternary+',
     'hc_fraction', 'hc_var_mean', 'hc_var_coeff', 'hc_var_min', 'hc_var_max', 'hc_var_entropy',
     'unit_props_at_depth_1', 'unit_props_at_depth_4', 'unit_props_at_depth_16', 'unit_props_at_depth_64',
     'unit_props_at_depth_256', 'mean_depth_to_contradiction_over_vars', 'estimate_log_number_nodes_over_vars',
     'saps_BestSolution_Mean', 'saps_BestSolution_CoeffVariance', 'saps_FirstLocalMinStep_Mean',
     'saps_FirstLocalMinStep_CoeffVariance', 'saps_FirstLocalMinStep_Median', 'saps_FirstLocalMinStep_Q.10',
     'saps_FirstLocalMinStep_Q.90', 'saps_BestAvgImprovement_Mean', 'saps_BestAvgImprovement_CoeffVariance',
     'saps_FirstLocalMinRatio_Mean', 'saps_FirstLocalMinRatio_CoeffVariance', 'saps_EstACL_Mean',
     'gsat_BestSolution_Mean', 'gsat_BestSolution_CoeffVariance', 'gsat_FirstLocalMinStep_Mean',
     'gsat_FirstLocalMinStep_CoeffVariance', 'gsat_FirstLocalMinStep_Median', 'gsat_FirstLocalMinStep_Q.10',
     'gsat_FirstLocalMinStep_Q.90', 'gsat_BestAvgImprovement_Mean', 'gsat_BestAvgImprovement_CoeffVariance',
     'gsat_FirstLocalMinRatio_Mean', 'gsat_FirstLocalMinRatio_CoeffVariance', 'gsat_EstACL_Mean',
                 'vig_modularty',
     'vig_d_poly', 'cvig_db_poly', 'variable_alpha', 'v_nd_p_node_min', 'v_nd_p_node_max', 'v_nd_p_node_mode',
     'v_nd_p_node_mean', 'v_nd_p_node_std', 'v_nd_p_node_zeros', 'v_nd_p_node_entropy', 'v_nd_p_node_q1',
     'v_nd_p_node_q2', 'v_nd_p_node_q3', 'v_nd_p_node_val_rate', 'v_nd_p_weights_min', 'v_nd_p_weights_max',
     'v_nd_p_weights_mode', 'v_nd_p_weights_mean', 'v_nd_p_weights_std', 'v_nd_p_weights_zeros',
     'v_nd_p_weights_entropy', 'v_nd_p_weights_q1', 'v_nd_p_weights_q2', 'v_nd_p_weights_q3', 'v_nd_p_weights_val_rate',
     'v_nd_n_node_min', 'v_nd_n_node_max', 'v_nd_n_node_mode', 'v_nd_n_node_mean', 'v_nd_n_node_std',
     'v_nd_n_node_zeros', 'v_nd_n_node_entropy', 'v_nd_n_node_q1', 'v_nd_n_node_q2', 'v_nd_n_node_q3',
     'v_nd_n_node_val_rate', 'v_nd_n_weights_min', 'v_nd_n_weights_max', 'v_nd_n_weights_mode', 'v_nd_n_weights_mean',
     'v_nd_n_weights_std', 'v_nd_n_weights_zeros', 'v_nd_n_weights_entropy', 'v_nd_n_weights_q1', 'v_nd_n_weights_q2',
     'v_nd_n_weights_q3', 'v_nd_n_weights_val_rate', 'c_nd_p_node_min', 'c_nd_p_node_max', 'c_nd_p_node_mode',
     'c_nd_p_node_mean', 'c_nd_p_node_std', 'c_nd_p_node_zeros', 'c_nd_p_node_entropy', 'c_nd_p_node_q1',
     'c_nd_p_node_q2', 'c_nd_p_node_q3', 'c_nd_p_node_val_rate', 'c_nd_p_weights_min', 'c_nd_p_weights_max',
     'c_nd_p_weights_mode', 'c_nd_p_weights_mean', 'c_nd_p_weights_std', 'c_nd_p_weights_zeros',
     'c_nd_p_weights_entropy', 'c_nd_p_weights_q1', 'c_nd_p_weights_q2', 'c_nd_p_weights_q3', 'c_nd_p_weights_val_rate',
     'c_nd_n_node_min', 'c_nd_n_node_max', 'c_nd_n_node_mode', 'c_nd_n_node_mean', 'c_nd_n_node_std',
     'c_nd_n_node_zeros', 'c_nd_n_node_entropy', 'c_nd_n_node_q1', 'c_nd_n_node_q2', 'c_nd_n_node_q3',
     'c_nd_n_node_val_rate', 'c_nd_n_weights_min', 'c_nd_n_weights_max', 'c_nd_n_weights_mode', 'c_nd_n_weights_mean',
     'c_nd_n_weights_std', 'c_nd_n_weights_zeros', 'c_nd_n_weights_entropy', 'c_nd_n_weights_q1', 'c_nd_n_weights_q2',
     'c_nd_n_weights_q3', 'c_nd_n_weights_val_rate', 'vg_al_node_min', 'vg_al_node_max', 'vg_al_node_mode',
     'vg_al_node_mean', 'vg_al_node_std', 'vg_al_node_zeros', 'vg_al_node_entropy', 'vg_al_node_q1', 'vg_al_node_q2',
     'vg_al_node_q3', 'vg_al_node_val_rate', 'vg_al_weights_min', 'vg_al_weights_max', 'vg_al_weights_mode',
     'vg_al_weights_mean', 'vg_al_weights_std', 'vg_al_weights_zeros', 'vg_al_weights_entropy', 'vg_al_weights_q1',
     'vg_al_weights_q2', 'vg_al_weights_q3', 'vg_al_weights_val_rate', 'cg_al_node_min', 'cg_al_node_max',
     'cg_al_node_mode', 'cg_al_node_mean', 'cg_al_node_std', 'cg_al_node_zeros', 'cg_al_node_entropy', 'cg_al_node_q1',
     'cg_al_node_q2', 'cg_al_node_q3', 'cg_al_node_val_rate', 'cg_al_weights_min', 'cg_al_weights_max',
     'cg_al_weights_mode', 'cg_al_weights_mean', 'cg_al_weights_std', 'cg_al_weights_zeros', 'cg_al_weights_entropy',
     'cg_al_weights_q1', 'cg_al_weights_q2', 'cg_al_weights_q3', 'cg_al_weights_val_rate', 'rg_node_min', 'rg_node_max',
     'rg_node_mode', 'rg_node_mean', 'rg_node_std', 'rg_node_zeros', 'rg_node_entropy', 'rg_node_q1', 'rg_node_q2',
     'rg_node_q3', 'rg_node_val_rate', 'rg_weights_min', 'rg_weights_max', 'rg_weights_mode', 'rg_weights_mean',
     'rg_weights_std', 'rg_weights_zeros', 'rg_weights_entropy', 'rg_weights_q1', 'rg_weights_q2', 'rg_weights_q3',
     'rg_weights_val_rate', 'big_node_min', 'big_node_max', 'big_node_mode', 'big_node_mean', 'big_node_std',
     'big_node_zeros', 'big_node_entropy', 'big_node_q1', 'big_node_q2', 'big_node_q3', 'big_node_val_rate',
     'big_weights_min', 'big_weights_max', 'big_weights_mode', 'big_weights_mean', 'big_weights_std',
     'big_weights_zeros', 'big_weights_entropy', 'big_weights_q1', 'big_weights_q2', 'big_weights_q3',
     'big_weights_val_rate', 'and_node_min', 'and_node_max', 'and_node_mode', 'and_node_mean', 'and_node_std',
     'and_node_zeros', 'and_node_entropy', 'and_node_q1', 'and_node_q2', 'and_node_q3', 'and_node_val_rate',
     'and_weights_min', 'and_weights_max', 'and_weights_mode', 'and_weights_mean', 'and_weights_std',
     'and_weights_zeros', 'and_weights_entropy', 'and_weights_q1', 'and_weights_q2', 'and_weights_q3',
     'and_weights_val_rate', 'band_node_min', 'band_node_max', 'band_node_mode', 'band_node_mean', 'band_node_std',
     'band_node_zeros', 'band_node_entropy', 'band_node_q1', 'band_node_q2', 'band_node_q3', 'band_node_val_rate',
     'band_weights_min', 'band_weights_max', 'band_weights_mode', 'band_weights_mean', 'band_weights_std',
     'band_weights_zeros', 'band_weights_entropy', 'band_weights_q1', 'band_weights_q2', 'band_weights_q3',
     'band_weights_val_rate', 'exo_node_min', 'exo_node_max', 'exo_node_mode', 'exo_node_mean', 'exo_node_std',
     'exo_node_zeros', 'exo_node_entropy', 'exo_node_q1', 'exo_node_q2', 'exo_node_q3', 'exo_node_val_rate',
     'exo_weights_min', 'exo_weights_max', 'exo_weights_mode', 'exo_weights_mean', 'exo_weights_std',
     'exo_weights_zeros', 'exo_weights_entropy', 'exo_weights_q1', 'exo_weights_q2', 'exo_weights_q3',
     'exo_weights_val_rate', 'rwh_0_mean', 'rwh_0_coeff', 'rwh_0_min', 'rwh_0_max', 'rwh_1_mean', 'rwh_1_coeff',
     'rwh_1_min', 'rwh_1_max', 'rwh_2_mean', 'rwh_2_coeff', 'rwh_2_min', 'rwh_2_max',
                 "file_name", "satzilla_base_t", "satzilla_probe_t", "ansotegui_t", "alfonso_t"]

    with open(results_csv, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=dict_keys)
        writer.writeheader()

        for i, file_name in enumerate(file_list):
            print(file_name)
            print("file ", i, " out of ", len(file_list))
            sat_inst = SATInstance(file_name, preprocess=True)
            if sat_inst.solved:
                continue

            t1 = time.time()
            sat_inst.gen_basic_features()
            t2 = time.time()
            sat_inst.gen_dpll_probing_features()
            # linux only
            sat_inst.gen_local_search_probing_features()
            t3 = time.time()
            sat_inst.gen_ansotegui_features()
            t4 = time.time()
            sat_inst.gen_manthey_alfonso_graph_features()
            t5 = time.time()

            sat_inst.features_dict["file_name"] = file_name
            sat_inst.features_dict["satzilla_base_t"] = (t2 - t1)
            sat_inst.features_dict["satzilla_probe_t"] = (t3 - t2)
            sat_inst.features_dict["ansotegui_t"] = (t4 - t3)
            sat_inst.features_dict["alfonso_t"] = (t5 - t4)
            writer.writerow(sat_inst.features_dict)

    f.close()


if __name__ == "__main__":
    # path_to_cnfs = "cnf_examples/"
    classes = ["clique_", "colour_", "cliquecoloring", "dominating", "matching", "op", "php", "subsetcard", "tiling", "tseitin"]
    binary = ["sat", "unsat"]
    path_to_cnfs = "/projects/satdb/dataset_final/"
    file_type = binary[0] + "*" + classes[0] + "*"
    results_csv = file_type + "_features.csv"

    bulk_gen_features(path_to_cnfs=path_to_cnfs, results_csv=results_csv, file_type=file_type)

    """
    sat clique
    sat color
    unsat clique
    unsat color
    sat/unsat cliquecoloring
    sat dominating
    --- unsat dominating 1 3
    sat matching
    unsat matching 1 4
    sat op/unsat 0 5
    sat/unsat php
    --- sat subsetcard 0 7
    unsat subsetcard
    sat tiling 0 8
    unsat tiling
    --- sat tsetin 0 9
    unsat tiling
    unsat tseitin
    
    random
    """
