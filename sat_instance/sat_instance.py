from feature_computation import preprocessing, parse_cnf, active_features, base_features, local_search_probing
from feature_computation.dpll import DPLLProbing



class SATInstance:

    def __init__(self, input_cnf, preprocess=True):
        self.path_to_cnf = input_cnf

        # satelite preprocessing
        # n.b. satelite only works on linux, mac no longer supports 32 bit binaries...

        if preprocess:
            preprocessed_path = preprocessing.satelite_preprocess(self.path_to_cnf)
            self.path_to_cnf = preprocessed_path

        # parse the cnf file
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
        self.parse_active_features()

        # Do first round of unit prop to remove all unit clauses
        self.dpll_prober = DPLLProbing(self)
        self.dpll_prober.unit_prop(0, 0)

    def clauses_with_literal(self, literal):
        if literal > 0:
            return self.clauses_with_positive_var[literal]
        else:
            return self.clauses_with_negative_var[abs(literal)]

    def parse_active_features(self):
        # self.num_active_vars, self.num_active_clauses, self.clause_states, self.clauses, self.num_bin_clauses_with_var, self.var_states =\
        active_features.get_active_features(self, self.clauses, self.c, self.v)

    def gen_basic_features(self):

        base_features_dict = base_features.compute_base_features(self.clauses, self.c, self.v, self.num_active_vars,
                                                                 self.num_active_clauses)
        self.features_dict.update(base_features_dict)

    def gen_dpll_probing_features(self):

        self.dpll_prober.unit_propagation_probe(False, True)

        self.dpll_prober.search_space_probe()

        self.features_dict.update(self.dpll_prober.unit_props_log_nodes_dict)

    def gen_local_search_probing_features(self):

        saps_res_dict, gsat_res_dict = local_search_probing.local_search_probe(self.path_to_cnf)

        self.features_dict.update(saps_res_dict)
        self.features_dict.update(gsat_res_dict)

