"""
The features as described in the SATzilla paper are different to those in the code.
First we need to compute the active variables and clauses
"""


def get_active_features(clauses, c, v):
    # int *lits = new int[numVars+1];
    lits = []

    for clause_num, clause in enumerate(clauses):
        num_literals = len(clause)

        # test if some literals are redundant and sort the clause
        tautology = False

        for i in range(num_literals - 1):
            temp_literal = clause[i]

            for j in range(i + 1, num_literals):
                # this is sorting the literals in the clause

                if abs(temp_literal) > abs(clause[j]):
                    temp = clause[j]
                    clause[j] = temp_literal
                    temp_literal = temp

                elif temp_literal == clause[j]:
                    # lits[j - -] = lits[--numLits];
                    # printf("c literal %d is redundant in clause %d\n", tempLit, clauseNum);
                    pass
                elif abs(temp_literal) == abs(clause[j]):
                    tautology = True

            if tautology:
                break
            else:
                clause[i] = temp_literal

        if not tautology:
            clause_states[clause_num] = ACTIVE