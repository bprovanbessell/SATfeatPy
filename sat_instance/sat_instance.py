from feature_computation import preprocessing, parse_cnf
class SATInstance:

    def __init__(self, input_cnf, preprocess=True):
        self.path_to_cnf = input_cnf

        # satelite preprocessing
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

    def clauses_with_literal(self, literal):
        if literal > 0:
            return self.clauses_with_positive_var[literal]
        else:
            return self.clauses_with_negative_var[abs(literal)]

    def parse_active_features(self):
        # self.num_active_vars, self.num_active_clauses, self.clause_states, self.clauses, self.num_bin_clauses_with_var, self.var_states =\
            active_features.get_active_features(self, self.clauses, self.c, self.v)