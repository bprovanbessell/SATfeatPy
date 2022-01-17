from enums import VarState, ClauseState
"""
First we need to compute the active variables and clauses
After pre-processing, active variable and clause computation is done
I'm not sure how redundant this is, possibly the SatELite pre-processing takes care of most of this...
Tautologies are removed,
"""


def get_active_features(clauses, c, v):
    # int *lits = new int[numVars+1];
    clause_states = [False] * c
    num_active_clauses_with_var = [0] * (v + 1)
    num_bin_clauses_with_var = [0] * (v + 1)

    num_active_clauses = c

    # These are used at some point...
    unit_clauses = []

    num_binary_clauses = 0
    num_ternary_clauses = 0

    # basically we want to remove literals if they appear twice
    # and remove the clause if it is a tautology (if variable both positive and negated appears in the clause)

    # sort the clauses. Make it a set, to remove duplicates, and iterate pairwaise,
    # check if variables are negations, and if so we have a tautology

    for clause_i in range(c):

        clause = clauses[clause_i]
        num_literals = len(clause)
        clause.sort(key=lambda x: abs(x))

        # mark and remove redundant literals
        # mark tautologies
        tautology = False
        for i in range(num_literals -1):
            j = i+1
            if clause[i] == -clause[j]:
                # we have a tautology
                tautology = True
                break
        # remove duplicates
        clause = list(set(clause))
        clauses[clause_i] = clause
        # print(clause)

        # Clause is sorted in terms of literals, and duplicates have been removed

        if not tautology:
            clause_states[clause_i] = True

            num_literals = len(clause)

            if num_literals == 1:
                unit_clauses.append(clause)
            if num_literals == 2:
                # for (int i=0; i < numLits; i++)
                #     numBinClausesWithVar[ABS(lits[i])] + +;
                for i in range(num_literals):
                    num_bin_clauses_with_var[abs(clause[i])] += 1
                num_binary_clauses += 1
            if num_literals == 3:
                num_ternary_clauses += 1

            for i in range(num_literals):

                num_active_clauses_with_var[abs(clause[i])] += 1

        else:
            # the clause was a tautology, so we can ignore it
            num_active_clauses -= 1

    # Now remove the redundant variables
    num_active_vars = v
    var_states = [VarState.UNASSIGNED] * (v+1)

    for i in range(1, v+1):
        if num_active_clauses_with_var[i] == 0:
            var_states[i] = VarState.IRRELEVANT
            num_active_vars -= 1
        else:
            # redundant
            var_states[i] = VarState.UNASSIGNED

    # here, a round of unit propagation is done to remove the unit clauses
    # TODO: add unit propagation code, and call it here

    return num_active_vars, num_active_clauses, clause_states, clauses, num_bin_clauses_with_var, var_states


