#Feature extraction implemented

### Size features
1. Number of clauses: denoted c
2. Number of variables: denoted v
3. Ratio: c/v

###Balance features
18-20. Ratio of positive and negative literals in each clause: mean, variation coefficient and entropy (see extra notes). 
_For each clause, the ratio is the number of positive literals/number of negative literals.
These ratios are then aggregated, and statistics on them output._

### Proximity to Horn Formula
#### A clause is a Horn clause if it contains at most one positive literal
28. Fraction of Horn clauses

###Extra Notes on aggregation and statistical references
- Coefficient of variation (variation coefficient in paper): 
The coefficient of variation represents the ratio of the standard deviation to the mean
- Entropy: ?

## Basic notes on SAT problems
Positive/negative literal is a respective instance of a variable.
Clause is a disjunction of literal(s)
CNF (Conjunctive Normal Form): Conjunction (and) of disjunction (or) of literals.

##Useful libraries/notes
- networkX
- cnfgen
- python-nnf