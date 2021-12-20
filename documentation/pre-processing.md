# CNF Pre-processing implementation
The cnf undergoes pre-processing after the initial file has been parsed

### Tautology filtering
If a clause is a tautology, it is not used for computation, and is considered inactive. A clause is considered a tautology
if it contains 2 literals x and not x, for all x in the set of variables.

### Redundant literals.
Literals that occur twice are removed.

### Clause reduction