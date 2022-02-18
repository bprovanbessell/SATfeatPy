# CNF Pre-processing implementation

First, the cnf is pre-processed by SatELite (http://minisat.se/SatELite.html).

The cnf undergoes further pre-processing after the initial file has been parsed (as implemented in SATzilla):

### Tautology filtering
If a clause is a tautology, it is not used for computation, and is considered inactive. A clause is considered a tautology
if it contains 2 literals x and not x, for all x in the set of variables.

### Redundant literals.
Literals that occur twice are removed.

### Clause reduction
Unit clauses are removed by running a single round of unit propagation on the formula.