#Feature extraction implementation
This file documents the features that can be extracted by this software, and gives a brief explanation of each feature.

### Size features
1. Number of clauses: denoted c
2. Number of variables: denoted v
3. Ratio: c/v

### Variable-Clause Graph features
#### A variable-clause graph (VCG) is a bipartite graph with a node for each variable, a node for each clause,
#### and an edge between them whenever a variable occurs in a clause
4-8. Variable nodes degree statistics: mean, coefficient of variation, min, max and entropy.
9-13. Clause nodes degree statistics: mean, coefficient of variation, min, max and entropy.
_The degree of a node is the number of edges incident (connected) to that node._

### Variable Graph features
#### A variable graph (VG) has a node for each variable, and an edge between variables that occur together in at least one clause
14-17. Nodes degree statistics: mean , coefficient of variation, min and max.

###Balance features
18-20. Ratio of positive and negative literals in each clause: mean, variation coefficient and entropy (see extra notes). 
_For each clause, the ratio is the number of positive literals/number of negative literals.
These ratios are then aggregated, and statistics on them output._

26-27. Fraction of binary and ternary clauses: Fraction of clauses that have 2 literals over total number of clauses,
fraction of clauses with 3 literals, over total number of clauses

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
- NetworkX - for graph creation and statistics
- cnfgen - for creating part of the testbed