from feature_computation import preprocessing, parse_cnf, active_features, base_features, local_search_probing, \
    graph_features_ansotegui, graph_features_manthey_alfonso, more_graph_features
from feature_computation.dpll import DPLLProbing
from sat_instance import write_to_file


class SATInstance:
    """
    Class to hold the methods for generating features from a cnf. This class handles the parsing of the cnf file into
    data structures necessary to the perform feature extraction. Then the various features can be generated, and are
    stored in the features dictionary.

    """

    def __init__(self, input_cnf, preprocess=True, verbose=False, preprocess_tmp=True):
        self.verbose = verbose

        self.path_to_cnf = input_cnf

        # satelite preprocessing
        # n.b. satelite only works on linux, mac no longer supports 32 bit binaries...

        if preprocess:
            if self.verbose:
                print("Preprocessing with SatELite")

            if preprocess_tmp:
                preprocessed_path = preprocessing.satelite_preprocess_tmp(self.path_to_cnf)
            else:
                preprocessed_path = preprocessing.satelite_preprocess(self.path_to_cnf)
            self.path_to_cnf = preprocessed_path

        # parse the cnf file
        if self.verbose:
            print("Parsing cnf file")
        self.clauses, self.c, self.v = parse_cnf.parse_cnf(self.path_to_cnf)

        # computed with active features
        # These change as they are processed with dpll probing algorithms
        self.num_active_vars = 0
        self.num_active_clauses = 0
        # states and lengths of the clauses
        self.clause_states = []
        self.clause_lengths = []
        # array of the length of the number of variables, containing the number of active clauses, and binary clauses that each variable contains
        self.num_active_clauses_with_var = []
        self.num_bin_clauses_with_var = []
        # stack of indexes of the clauses that have 1 literal
        self.unit_clauses = []

        # all of the clauses that contain a positive version of this variable
        self.clauses_with_positive_var = []
        self.clauses_with_negative_var = []
        # used for dpll operations, perhaps better to keep them in a dpll class...

        self.var_states = []

        self.features_dict = {}

        # necessary for unit propagation setup
        if self.verbose:
            print("Parsing active features")
        self.parse_active_features()

        # Do first round of unit prop to remove all unit clauses
        self.dpll_prober = DPLLProbing(self)
        if self.verbose:
            print("First round of unit propagation")
        self.dpll_prober.unit_prop(0, 0)

    def clauses_with_literal(self, literal):
        """
        Returns a list of clauses that contain the literal
        :param literal:
        :return:
        """
        if literal > 0:
            return self.clauses_with_positive_var[literal]
        else:
            return self.clauses_with_negative_var[abs(literal)]

    def parse_active_features(self):
        # self.num_active_vars, self.num_active_clauses, self.clause_states, self.clauses, self.num_bin_clauses_with_var, self.var_states =\
        active_features.get_active_features(self, self.clauses, self.c, self.v)

    def gen_basic_features(self):
        """
        Generates the basic features (Including but not limited to 1-33 from the satzilla paper).
        """
        if self.verbose:
            print("Generating basic features")

        base_features_dict = base_features.compute_base_features(self.clauses, self.c, self.v, self.num_active_vars,
                                                                 self.num_active_clauses)
        self.features_dict.update(base_features_dict)

    def gen_dpll_probing_features(self):
        """
        Generates the dpll probing features (34-40 from the satzilla paper).
        """
        if self.verbose:
            print("DPLL probing")

        self.dpll_prober.unit_propagation_probe(False)

        self.dpll_prober.search_space_probe()

        self.features_dict.update(self.dpll_prober.unit_props_log_nodes_dict)

    def gen_local_search_probing_features(self):
        """
        Generates the local search probing features (including but not limited to 41-48 from the satzilla paper).
        """
        # also doesnt seem to fully work on osx.
        if self.verbose:
            print("Local search probing with SAPS and GSAT")

        saps_res_dict, gsat_res_dict = local_search_probing.local_search_probe(self.path_to_cnf)

        self.features_dict.update(saps_res_dict)
        self.features_dict.update(gsat_res_dict)

    def gen_ansotegui_features(self):
        if self.verbose:
            print("Generating features from Ansotegui")

        alpha = graph_features_ansotegui.estimate_power_law_alpha(self.clauses, self.num_active_clauses,
                                                                  self.num_active_vars)

        vig = graph_features_ansotegui.create_vig(self.clauses, self.num_active_clauses, self.num_active_vars)
        cvig = graph_features_ansotegui.create_cvig(self.clauses, self.num_active_clauses, self.num_active_vars)

        modularity = graph_features_ansotegui.compute_modularity_q(vig)

        N_vig = graph_features_ansotegui.burning_by_node_degree(vig, self.num_active_vars)
        N_cvig = graph_features_ansotegui.burning_by_node_degree(cvig, self.num_active_vars + self.num_active_clauses)

        d_poly, d_exp = graph_features_ansotegui.linear_regression_fit(N_vig)
        db_poly, db_exp = graph_features_ansotegui.linear_regression_fit(N_cvig)

        ansotegui_features = {"vig_modularty": modularity,
                              "vig_d_poly": d_poly,
                              "cvig_db_poly": db_poly,
                              "variable_alpha": alpha
                              }

        self.features_dict.update(ansotegui_features)

    def gen_manthey_alfonso_graph_features(self):
        if self.verbose:
            print("Generating features from the paper of Manthey-Alfonso")

        v_nd_p, v_nd_n, c_nd_p, c_nd_n = graph_features_manthey_alfonso.create_vcg(self.clauses)

        all_stats = [graph_features_manthey_alfonso.get_graph_stats("v_nd_p_", v_nd_p),
                     graph_features_manthey_alfonso.get_graph_stats("v_nd_n_", v_nd_n),
                     graph_features_manthey_alfonso.get_graph_stats("c_nd_p_", c_nd_p),
                     graph_features_manthey_alfonso.get_graph_stats("c_nd_n_", c_nd_n)]

        nd, w = graph_features_manthey_alfonso.create_vg(self.clauses)
        all_stats.append(graph_features_manthey_alfonso.get_graph_stats("vg_al_", nd, w))

        nd, w = graph_features_manthey_alfonso.create_cg(self.clauses)
        cg_stats = graph_features_manthey_alfonso.get_graph_stats("cg_al_", nd, w)
        all_stats.append(cg_stats)

        nd, w = graph_features_manthey_alfonso.create_rg(self.clauses)
        rg_stats = graph_features_manthey_alfonso.get_graph_stats("rg_", nd, w)
        all_stats.append(rg_stats)

        _, nd, w = graph_features_manthey_alfonso.create_big(self.clauses)
        big_stats = graph_features_manthey_alfonso.get_graph_stats("big_", nd, w)
        all_stats.append(big_stats)

        andg, bandg, exog = graph_features_manthey_alfonso.create_exo_and_band(self.clauses)

        nd, w = graph_features_manthey_alfonso.get_degrees_weights(andg)
        and_stats = graph_features_manthey_alfonso.get_graph_stats("and_", nd, w)
        all_stats.append(and_stats)

        nd, w = graph_features_manthey_alfonso.get_degrees_weights(bandg)
        band_stats = graph_features_manthey_alfonso.get_graph_stats("band_", nd, w)
        all_stats.append(band_stats)

        nd, w = graph_features_manthey_alfonso.get_degrees_weights(exog)
        exo_stats = graph_features_manthey_alfonso.get_graph_stats("exo_", nd, w)
        all_stats.append(exo_stats)

        for stats_dict in all_stats:
            self.features_dict.update(stats_dict)

        rwh = more_graph_features.recursive_weight_heuristic(10, self.clauses, self.num_active_vars)
        self.features_dict.update(rwh)

    def write_results(self):
        write_to_file.write_features_to_json(self.features_dict)
