import random
from feature_computation.enums import VarState, ClauseState
# from feature_computation.features import Features

class DPLLProbing:
    """
    So the values(states) of the variables are stored in varStates
    The clauses themselves are not changed (I assume for storage reasons)

    So assignments of the variables are stored in varstate, if they are true, false, etc,
     and then clauses are iterated through and checked if they are unassigned, so that is the next unit clause

     lengths of clauses kept track of in clause_lengths


     First check is for unit clauses -> if there are unit clauses
     Within these clauses, the unassigned variable is found
     This variable is set to the value of the literal (positive or negative)
     and the clauses that contain this variable are reduced

     reduction
     first remove all of the instances of the negative variable...
     so reduce the size of clauses with this variable,
     if the new size is 0, then we have a problem (inconsistent)

     Then satisfy the consistent clauses (clauses that contain that literal)

    """

    def __init__(self, feats, verbose = True):
        self.feats = feats
        self.verbose = verbose
        self.num_vars_to_try = 10
        self.num_probes = 5

        # two stacks
        self.num_reduced_clauses = []
        self.num_reduced_vars = []

        # stack of variables that have been reduced
        self.reduced_vars = []
        self.reduced_clauses = []


# unit propagation

# num_bin_clauses_with_var, int array containing the number of binary clauses with a certain variable (index),
# this should change as the propogation happens

    def unit_prop_probe(self, haltOnAssignment, doComp):
        """
        Method to calculate the dpll probing features

        :param haltOnAssignment:
        :param doComp:
        :param active_vars:
        :param num_bin_clauses_with_var:
        :param var_states:
        :param v:
        :return:
        """
        if self.verbose:
            print("unit prop probe")

        if not doComp:
            next_probe_depth = 1
            for j in range(self.num_probes):
                next_probe_depth = next_probe_depth * 4
                print("vars-reduced-depth-", next_probe_depth)
                # they also write the actual feature here? or just reserve the memory for it
                print("feature")

            print("time to calculate unit probing...")

        # the depths are manually set, multiples of 4 each time
        current_depth = 0
        orig_num_active_vars = self.feats.num_active_vars
        reached_bottom = False

        for probe_num in range(self.num_probes):
            # sets depth to 1, 4, 16, 64, 256

            # alternatively next_probe_depth = 4 ** probe_num
            next_probe_depth = 1
            for j in range(probe_num):
                next_probe_depth = next_probe_depth * 4

            if self.verbose:
                print("searching depth: ", next_probe_depth)
            # the actual searching
            while current_depth < next_probe_depth and not reached_bottom:
                print("c depth", current_depth)
                # define the int arrays, values not yet initialised though... Contents undefined
                # int varsInMostBinClauses[NUM_VARS_TO_TRY];
                # int numBin[NUM_VARS_TO_TRY];

                vars_in_most_bin_clauses = [0] * self.num_vars_to_try
                num_bin = [0] * self.num_vars_to_try

                array_size = 0
                for var in range(1, self.feats.v + 1):
                    # if the variable is not unassigned, skip it (it already has a value (true, false) or it is irrelevant
                    if self.feats.var_states[var] != VarState.UNASSIGNED: continue

                    if array_size < self.num_vars_to_try: array_size += 1

                    j = 0
                    while j < array_size - 1 and self.feats.num_bin_clauses_with_var[var] < num_bin[j]:
                        j += 1

                    # what is this actually doing... somehow sorting and keeping track of the top 10 vars that occur in the most binary clauses??
                    for k in range(array_size - 1, j, -1):
                        vars_in_most_bin_clauses[k] = vars_in_most_bin_clauses[k - 1]
                        num_bin[k] = num_bin[k - 1]

                    vars_in_most_bin_clauses[j] = var
                    num_bin[j] = self.feats.num_bin_clauses_with_var[var]

                max_props_var = 0
                max_props_val = False

                # if there are no binary clauses, just take the first unassigned var
                if array_size == 0:
                    max_props_var = 1
                    while self.feats.var_states[max_props_var] != VarState.UNASSIGNED and max_props_var < self.feats.v:
                        max_props_var += 1

                    max_props_val = True

                else:
                    max_props = -1

                    for var_num in range(array_size):

                        # should be simplified, basically you try to set the variable to true, and to false
                        value = True
                        # do while
                        while True:
                            # do block
                            # for value = True and value = False
                            # print("vars in bin clauses", vars_in_most_bin_clauses)

                            # print("before")
                            con = self.set_var_and_prop(vars_in_most_bin_clauses[var_num], value)
                            # print("con", con)
                            # print("active vars", self.feats.num_active_vars)
                            if con and self.feats.num_active_vars <= 0:

                                if haltOnAssignment:
                                    print("solved")
                                    print(self.feats.num_active_clauses)
                                    print(self.feats.num_active_vars)
                                    # output_assignment()
                                    # DONE is just some number... still to be seen what this does in the satzilla code
                                    return

                            num_props = orig_num_active_vars - self.feats.num_active_vars - current_depth

                            if num_props > max_props:
                                max_props_var = vars_in_most_bin_clauses[var_num]
                                max_props_val = value

                            self.backtrack()

                            value = not value

                            if value:
                                break

                assert (max_props_var != 0)

                if not self.set_var_and_prop(max_props_var, max_props_val):
                    reached_bottom = True

                elif (self.feats.num_active_clauses == 0):
                    print("no more active variables, solved")
                    if (haltOnAssignment):
                        print("assignment solved")
                        print(self.feats.num_active_clauses)
                        print(self.feats.num_active_vars)
                        # outputAssignment()
                        return

                    reached_bottom = True

                current_depth += 1

            print("vars reduced depth ", next_probe_depth)
            print((orig_num_active_vars - self.feats.num_active_vars - current_depth)/self.feats.v)

        while(self.feats.num_active_vars != orig_num_active_vars):
            self.backtrack()

        # writefeature

    def set_var_and_prop(self, var, value):
        """

        :param var: integer, the variable
        :param value: boolean, value that the variable should get set to
        :return:
        """
        # these need to be passed by reference, instead of passed by assignment
        num_clauses_reduced = 0
        num_vars_reduced = 1

        # print("Variable to set:", var, self.feats.var_states[var])
        # print("active vars", self.feats.num_active_vars)
        # can only set an unassigned variable to a value
        assert self.feats.var_states[var] == VarState.UNASSIGNED

        # set the value of the variable
        if value:
            self.feats.var_states[var] = VarState.TRUE_VAL
            literal = var
        else:
            self.feats.var_states[var] = VarState.FALSE_VAL
            literal = -var

        self.reduced_vars.append(var)
        self.feats.num_active_vars -= 1

        consistent, num_clauses_reduced, num_vars_reduced = self.reduce_clauses(literal, num_clauses_reduced, num_vars_reduced)
        # print("reduce c, v, con", num_clauses_reduced, num_vars_reduced, consistent)

        if consistent:
            consistent, num_clauses_reduced, num_vars_reduced = self.unit_prop(num_clauses_reduced, num_vars_reduced)
        # print("num clauses reduced", num_clauses_reduced)
        # print("num clauses reduced", num_clauses_reduced)

        # print("consistent 1: ", consistent)
        # differing here... check unit prop
        # print("clauses reduced, vars_reduced", num_clauses_reduced, num_vars_reduced)
        # stack to hold the number that have been reduced, used in backtracking
        self.num_reduced_clauses.append(num_clauses_reduced)
        self.num_reduced_vars.append(num_vars_reduced)

        return consistent

    def reduce_clauses(self, orig_literal, num_clauses_reduced, num_vars_reduced):
        # we are trying to assign this literal value to true (in all clauses that contain it)

        # "remove" vars from inconsistent clauses

        # check which clauses contain the negative of this literal, and remove that negative literal from them
        # clauses_with_literal = self.feats.clauses_with_literal(-literal)
        # print(self.feats.clauses_with_literal(-orig_literal))
        for clause_num in self.feats.clauses_with_literal(-orig_literal):
            # iterate through all of the clauses that contain this literal
            # clause_num = self.feats.clauses_with_literal(-literal)[i]
            # if it is active
            if self.feats.clause_states[clause_num] == ClauseState.ACTIVE:
                self.reduced_clauses.append(clause_num)
                num_clauses_reduced += 1

                # could be quite important
                # decrease the size (this length actually represents the number of yet to be assigned variables within that clause)
                self.feats.clause_lengths[clause_num] -= 1

                if self.feats.clause_lengths[clause_num] == 2:
                    # 0 marked as the end of the clause
                    # for (int i=0; clauses[clause][i] != 0; i++)

                    # iterate through the clause
                    # for j in range(len(self.feats.clauses[clause_num])):
                    for literal in self.feats.clauses[clause_num]:
                        # still a bit strange, does this not mark duplicates??
                        # self.feats.num_bin_clauses_with_var[abs(self.feats.clauses[clause_num][j])] += 1
                        self.feats.num_bin_clauses_with_var[abs(literal)] += 1

                elif self.feats.clause_lengths[clause_num] == 1:
                    # for (int i=0; clauses[clause][i] != 0; i++)
                    # clauses themselves are never actually edited, just the values in varstates, clausestates, clauselengths etc.
                    # for j in range(len(self.feats.clauses[clause_num])):
                    for literal in self.feats.clauses[clause_num]:
                        self.feats.num_bin_clauses_with_var[abs(literal)] -= 1

                    # now a unit clause
                    # print(clause_num, "is unit clause")
                    self.feats.unit_clauses.append(clause_num)

                elif self.feats.clause_lengths[clause_num] == 0:
                    # inconsistent, the last literal in the clause has been removed, and it has to be satisfied, as opposed to being removed
                    return False, num_clauses_reduced, num_vars_reduced

        # satisfy the consistent clauses
        # print("consisten clause", self.feats.clauses_with_literal(orig_literal))
        for i in range(len(self.feats.clauses_with_literal(orig_literal))):
            clause_num = self.feats.clauses_with_literal(orig_literal)[i]
            if self.feats.clause_states[clause_num] == ClauseState.ACTIVE:
                # print("pacify ", clause_num)

                self.feats.clause_states[clause_num] = ClauseState.PASSIVE
                self.reduced_clauses.append(clause_num)
                self.feats.num_active_clauses -= 1

                # Seems to be iterating through the clause again
                # j=0
                # int otherVarInClause = ABS(clauses[clause][j]);
                # while other_var_in_clause != 0:
                for j in range(len(self.feats.clauses[clause_num])):
                    curr_var = abs(self.feats.clauses[clause_num][j])
                    self.feats.num_active_clauses_with_var[curr_var] -= 1

                    if self.feats.clause_lengths[clause_num] == 2:
                        self.feats.num_bin_clauses_with_var[curr_var] -= 1

                    # is the variable now irrelevant (active, but existing in no clauses)
                    if self.feats.num_active_clauses_with_var[curr_var] == 0 and self.feats.var_states[curr_var] == VarState.UNASSIGNED:
                        self.feats.var_states[curr_var] = VarState.IRRELEVANT
                        self.reduced_vars.append(curr_var)
                        self.feats.num_active_vars -=1
                        num_vars_reduced +=1

                num_clauses_reduced += 1

        return True, num_clauses_reduced, num_vars_reduced

    def unit_prop(self, num_clauses_reduced, num_vars_reduced):
        """
        Propagates the unit clauses
        :param num_clauses_reduced:
        :param num_vars_reduced:
        :return:
        """

        consistent = True

        # for each unit clause (if there are unit clauses)
        while (len(self.feats.unit_clauses) > 0) and consistent:
            # get the next unit clause
            clause_number = self.feats.unit_clauses.pop()

            # skip inactive clauses
            # print("cstate", self.feats.clause_states[clause_number])
            if self.feats.clause_states[clause_number] != ClauseState.ACTIVE: continue
            # print("unit clause number", clause_number)

            lit_num = 0

            # while the current literal is not unassigned
            # get the next possible unassigned literal
            while (self.feats.var_states[abs(self.feats.clauses[clause_number][lit_num])] != VarState.UNASSIGNED):
                lit_num += 1

            assert self.feats.clause_lengths[clause_number] == 1

            # get the literal literal (excuse the pun)
            literal = self.feats.clauses[clause_number][lit_num]

            if literal > 0:
                self.feats.var_states[abs(literal)] = VarState.TRUE_VAL
            else:
                self.feats.var_states[abs(literal)] = VarState.FALSE_VAL

            self.reduced_vars.append(abs(literal))
            self.feats.num_active_vars -= 1
            num_vars_reduced += 1

            # now reduce the clauses with that literal value
            r_consistent, num_clauses_reduced, num_vars_reduced = self.reduce_clauses(literal, num_clauses_reduced, num_vars_reduced)
            # consistent = consistent and self.reduce_clauses(literal, num_clauses_reduced, num_vars_reduced)
            consistent = consistent and r_consistent

        return consistent, num_clauses_reduced, num_vars_reduced

    def output_assignment(self):
        pass

    def backtrack(self):
        """
        Should undo one call of setVar or unitprop
        :return:
        """
        # print("backtrack")

        num_vars_reduced = self.num_reduced_vars.pop()

        # for all the vars that were reduced, unassign them
        for i in range(num_vars_reduced):
            var = self.reduced_vars.pop()
            self.feats.var_states[var] = VarState.UNASSIGNED
            self.feats.num_active_vars += 1

        # for all of the clauses that were reduced
        num_clauses_reduced = self.num_reduced_clauses.pop()
        for i in range(num_clauses_reduced):
            clause_num = self.reduced_clauses.pop()

            # re activate the clause
            if self.feats.clause_states[clause_num] != ClauseState.ACTIVE:
                self.feats.num_active_clauses += 1
                self.feats.clause_states[clause_num] = ClauseState.ACTIVE

                if self.feats.clause_lengths[clause_num] == 2:
                    for j in range(len(self.feats.clauses[clause_num])):
                        literal = self.feats.clauses[clause_num][j]
                        self.feats.num_active_clauses_with_var[abs(literal)] += 1
                        self.feats.num_bin_clauses_with_var[abs(literal)] += 1
                else:
                    for j in range(len(self.feats.clauses[clause_num])):
                        literal = self.feats.clauses[clause_num][j]
                        self.feats.num_active_clauses_with_var[abs(literal)] += 1

            else:
                self.feats.clause_lengths[clause_num] += 1

                if self.feats.clause_lengths[clause_num] == 2:
                    for j in range(len(self.feats.clauses[clause_num])):
                        literal = self.feats.clauses[clause_num][j]
                        self.feats.num_bin_clauses_with_var[abs(literal)] += 1

                elif self.feats.clause_lengths[clause_num] == 3:
                    for j in range(len(self.feats.clauses[clause_num])):
                        literal = self.feats.clauses[clause_num][j]
                        self.feats.num_bin_clauses_with_var[abs(literal)] -= 1

        # empty out unit clauses
        self.feats.unit_clauses = []

""" Python implementation of dpll, could be useful in shrinking the satzilla code"""
def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def bcp(formula, unit):
    """
    If the unit is in the clause, it is fine, as it can be satisfied
    If a negative unit is in there, then remove it from the clause, as this will not be satisfied

    :param formula: formula (cnf still left to solve)
    :param unit:
    :return:
    """
    modified = []
    for clause in formula:
        # this clause is satisfied, so we don't need to search anywhere in it anymore
        if unit in clause: continue
        if -unit in clause:
            c = [x for x in clause if x != -unit]
            # clause is unsatisfiable
            if len(c) == 0: return -1
            modified.append(c)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []
    for literal, num in counter.items():
        if -literal not in counter:
            pures.append(literal)
    for pure in pures:
        formula = bcp(formula, pure)
    assignment += pures
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def variable_selection(formula):
    counter = get_counter(formula)
    return random.choice([x for x in counter.keys()])


def backtracking(formula, assignment):
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)

    assignment = assignment + pure_assignment + unit_assignment
    if formula == -1:
        return []
    if not formula:
        return assignment

    # randomly choose a variable to set
    variable = variable_selection(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])
    return solution


if __name__ == "__main__":
    # test out the algo here
    # cnf_path = "../cnf_examples/basic.cnf"
    #
    # # clauses, c, v = parse_cnf.parse_cnf(cnf_path)
    # solution = backtracking(clauses, [])
    # if solution:
    #     solution += [x for x in range(1, v + 1) if x not in solution and -x not in solution]
    #     solution.sort(key=lambda x: abs(x))
    #     print('SATISFIABLE')
    #     print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    # else:
    #     print('UNSATISFIABLE')
    #
    # solution = backtracking(clauses, [])
    pass
