"""
The features as described in the SATzilla paper are different to those in the code.
First we need to compute the active variables and clauses
"""


def get_active_features(clauses, c, v):
    # int *lits = new int[numVars+1];
    lits = []
    clause_states = [False] * c
    num_active_clauses_with_var = [0] * v

    # These are used at some point...
    unit_clauses = []

    num_binary_clauses = 0
    num_ternary_clauses = 0

    # basically we want to remove literals if they appear twice
    # and remove the clause if it is a tautology (if variable both positive and negated appears in the clause)

    # sort the clauses. Make it a set, to remove duplicates, and iterate pairwaise,
    # check if variables are negations, and if so we have a tautology

    for clause_i in range(c):

        clause = clauses[i]
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

        if not tautology:
            clause_states[clause_i] = True

            num_literals = len(clause)

            if num_literals == 1:
                unit_clauses.append(clause)
            if num_literals == 2:
                # for (int i=0; i < numLits; i++)
                #     numBinClausesWithVar[ABS(lits[i])] + +;
                num_binary_clauses += 1
            if num_literals == 3:
                num_ternary_clauses += 1

            for i in range(num_literals):
                # if (lits[litNum] < 0)
                #     negClausesWithVar[ABS(lits[litNum])].push_back(clauseNum);
                #     else
                #     posClausesWithVar[lits[litNum]].push_back(clauseNum);
                num_active_clauses_with_var[abs(clause[i])] += 1


    # for clause_num, clause in enumerate(clauses):
    #     num_literals = len(clause)
    #
    #     # test if some literals are redundant and sort the clause
    #     tautology = False
    #
    #     for i in range(num_literals - 1):
    #         temp_literal = clause[i]
    #
    #         for j in range(i + 1, num_literals):
    #             # this is sorting the literals in the clause
    #
    #             if abs(temp_literal) > abs(clause[j]):
    #                 temp = clause[j]
    #                 clause[j] = temp_literal
    #                 temp_literal = temp
    #
    #             elif temp_literal == clause[j]:
    #                 newj = j - 1
    #                 num_literals -=1
    #
    #                 clause[newj] = clause[num_literals]
    #
    #                 # lits[j --] = lits[--numLits];
    #                 # printf("c literal %d is redundant in clause %d\n", tempLit, clauseNum);
    #                 # redundant literal, should be skipped
    #                 pass
    #             elif abs(temp_literal) == abs(clause[j]):
    #                 # tautology means it is always true
    #                 tautology = True
    #
    #         if tautology:
    #             break
    #         else:
    #             clause[i] = temp_literal
    #
    #     if not tautology:
    #         clause_states[clause_num] = True

