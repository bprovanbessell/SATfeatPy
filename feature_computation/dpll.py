import random
import parse_cnf
from enums import VarState, ClauseState

verbose = True

# unit propagation

# define
num_vars_to_try = 10
num_probes = 5


# num_bin_clauses_with_var, int array containing the number of binary clauses with a certain variable (index),
# this should change as the propogation happens?


def unit_prop_probe(haltOnAssignment, doComp, active_vars, num_bin_clauses_with_var, var_states, v):
    if verbose:
        print("unit prop probe")

    if not doComp:
        next_probe_depth = 1
        for j in range(num_probes):
            next_probe_depth = next_probe_depth * 4
            print("vars-reduced-depth-" + next_probe_depth)
            # they also write the actual feature here? or just reserve the memory for it
            print("feature")

        print("time to calculate unit probing...")

    #     Note: depth is number of vars: manually set- not including unitprop
    current_depth = 0
    orig_num_active_vars = active_vars
    reached_bottom = False

    for probe_num in range(num_probes):
        # sets depth to 1, 4, 16, 64, 256

        # alternatively next_probe_depth = 4 ** probe_num
        next_probe_depth = 1
        for j in range(probe_num):
            next_probe_depth = next_probe_depth * 4

        # the actual searching
        while current_depth < next_probe_depth and not reached_bottom:
            # define the int arrays, values not yet initialised though... Contents undefined
            # int varsInMostBinClauses[NUM_VARS_TO_TRY];
            # int numBin[NUM_VARS_TO_TRY];

            vars_in_most_bin_clauses = [0] * num_vars_to_try
            num_bin = [0] * num_vars_to_try

            array_size = 0
            for var in range(1, v + 1):
                if var_states[var] != VarState.UNASSIGNED: continue

                if array_size < num_vars_to_try: array_size += 1

                j = 0
                while j < array_size - 1 and num_bin_clauses_with_var[var] < num_bin[j]:
                    j += 1

                # what is this actually doing...
                for k in range(array_size - 1, j, -1):
                    vars_in_most_bin_clauses[k] = vars_in_most_bin_clauses[k - 1]
                    num_bin[k] = num_bin[k - 1]

                vars_in_most_bin_clauses[j] = var
                num_bin[j] = num_bin_clauses_with_var[var]

            max_props_var = 0
            max_props_val = False

            # if there are no binary clauses, just take the first unassigned var
            if array_size == 0:
                max_props_var = 1
                while var_states[max_props_var] != VarState.UNASSIGNED and max_props_var < v:
                    max_props_var += 1

                max_props_val = True

            else:
                max_props = -1

                for var_num in range(array_size):
                    value = True
                    # do while
                    while True:
                        # do block
                        # for val = true and val = false??
                        if set_var_and_prop(vars_in_most_bin_clauses[var_num], val) and num_active_vars <= 0:

                            if haltOnAssignment:
                                output_assignment()
                                # DONE is just some number... still to be seen what this does in the satzilla code
                                return DONE

                        num_props = orig_num_active_vars - num_active_vars - current_depth

                        if(num_props > max_props):
                            max_props_var = vars_in_most_bin_clauses[var_num]
                            max_props_val = value

                        backtrack()

                        value = not value

                        if value == True:
                            break

            assert (maxPropsVar != 0);

            if (not setVarAndProp(maxPropsVar, maxPropsVal)):
                reached_bottom = True

            else if (numActiveClauses == 0):
                if (haltOnAssignment) :
                    outputAssignment()
                    # return DONE

            reachedBottom = True


            current_depth += 1


def set_var_and_prop(var, val, var_states, reduced_vars):
    """

    :param var: integer, the variable
    :param val: boolean, value that the variable should get set to
    :return:
    """

    num_clauses_reduced = 0
    num_vars_reduced = 1

    assert var_states[var] == VarState.UNASSIGNED

    # set the value of the variable
    if val:
        var_states[var] = VarState.TRUE_VAL
        literal = var
    else:
        var_states[var] = VarState.FALSE_VAL
        literal = -var

    # really these variables should be global
    # reduced_vars.append(var)
    # num_active_vars -= 1

    consistent = reduce_clauses(literal, num_clauses_reduced, num_vars_reduced)

    if consistent:
        consistent = unit_prop(num_clauses_reduced, num_vars_reduced)

    # stack to hold the number that have been reduced?...
    # num_reduced_clauses.append(num_clauses_reduced)
    # num_reduced_var.appned(num_vars_reduced)

    return consistent
    pass

def reduce_clauses(literal, num_clauses_reduced, num_vars_reduced, clauses_with_literal, clause_states, reduced_clauses):
    # we are trying to assign this literal value to true (in all clauses that contain it)

    # "remove" vars from inconsistent clauses

    # check which clauses contain the negative of this literal, and remove that negative literal from them
    for i in range(len(clauses_with_literal[-literal])):
        clause_num = clauses_with_literal(-literal)[i]
        if clause_states[clause_num] == ClauseState.ACTIVE:
            reduced_clauses.push(clause_num)
            num_clauses_reduced += 1

            # could be quite important
            # clause_lengths[clause_num] -=1

            if len(clauses[clause_num] == 2):
                # seems a bit funky, depends on how the clauses are stored still, maybe the literals are set to 0 if they are "removed"??
                # for (int i=0; clauses[clause][i] != 0; i++)

                for i in range(2):
                    num_bin_clauses_with_var[abs(clauses(clause_num)[i])] += 1
            elif len(clauses[clause_num] == 1):
                # for (int i=0; clauses[clause][i] != 0; i++)
                # still not sure how they store the clauses exactly
                for i in range(1):
                    num_bin_clauses_with_var[abs(clauses(clause_num)[i])] -= 1

            elif len(clauses[clause_num] == 0):
                # inconsistent, the last literal in the clause has been removed, and it has to be satisfied, as opposed to being removed
                return False

    # satisfy the consistent clauses
    for i in range(len(clauses_with_literal[literal])):
        clause_num = clauses_with_literal[i]
        if clause_states[clause_num] == ClauseState.ACTIVE:

            clause_states[clause_num] = ClauseState.PASSIVE
            reduced_clauses.append(clause_num)
            num_active_clauses -=1

            j=0
            other_var_in_clause = abs(clauses[clause_num][j])
            while other_var_in_clause != 0:
                num_active_clauses_with_var[other_var_in_clause] -= 1

                # if clause_lengths[clause_num] == 2:
                if(len(clauses[clause_num]) == 2):
                    num_bin_clauses_with_var[other_var_in_clause] -= 1

                # is the variable now irrelevant (active, but existing in no clauses
                if num_active_clauses_with_var[other_var_in_clause] == 0 and var_states[other_var_in_clause] == VarState.UNASSIGNED:
                    var_states[other_var_in_clause] = VarState.IRRELEVANT
                    reduced_vars.append(other_var_in_clause)
                    num_active_vars -=1
                    num_vars_reduced -=1

                j+=1
                other_var_in_clause = abs(clauses[clause_num][j])

            num_clauses_reduced +=1
    
    return True

    pass

def unit_prop(num_clauses_reduced, num_vars_reduced,
              unit_clauses, clause_states, var_states, clauses):

    consistent = True

    # for each unit clause
    while (not len(unit_clauses) == 0) and consistent:
        # get the next unit clause
        clause_number = unit_clauses.pop()

        # skip inactive clauses
        if clause_states[clause_number] != ClauseState.ACTIVE: continue


        lit_num = 0
        # seems a bit weird to check this, as this clause should only have 1 literal in it (Unit clause??)
        while (var_states[abs(clauses[clause_number][lit_num])] != VarState.UNASSIGNED):
            lit_num += 1

        # this is literally being checked here
        assert len(clauses[clause_number]) ==1

        # get the literal literal (excuse the pun)
        literal = clauses[clause_number][lit_num]

        if literal > 0:
            var_states[abs(literal)] = VarState.TRUE_VAL
        else:
            var_states[abs(literal)] = VarState.FALSE_VAL

        reduced_vars.append(abs(lit))
        num_active_vars -=1
        num_vars_reduced +=1

        # now reduce the clauses with that literal value
        consistent = consistent and reduce_clauses(literal, num_clauses_reduced, num_vars_reduced)

    return consistent
    pass


def output_assignment():
    pass

def backtrack():
    pass

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
    cnf_path = "../cnf_examples/basic.cnf"

    clauses, c, v = parse_cnf.parse_cnf(cnf_path)
    solution = backtracking(clauses, [])
    if solution:
        solution += [x for x in range(1, v + 1) if x not in solution and -x not in solution]
        solution.sort(key=lambda x: abs(x))
        print('SATISFIABLE')
        print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('UNSATISFIABLE')

    solution = backtracking(clauses, [])
