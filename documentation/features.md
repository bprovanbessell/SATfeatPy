#Feature extraction implementation
This file documents the features that can be extracted by this software, and gives a brief explanation of each feature.

N.B. numbers refer to the feature number within [1].
### Size features
1. Number of clauses: denoted c
2. Number of variables: denoted v
3. Ratio: c/v

### Variable-Clause Graph features
**A variable-clause graph (VCG) is a bipartite graph with a node for each variable, a node for each clause, 
and an edge between them whenever a variable occurs in a clause **

4-8. Variable nodes degree statistics: mean, coefficient of variation, min, max and entropy.
9-13. Clause nodes degree statistics: mean, coefficient of variation, min, max and entropy.
_The degree of a node is the number of edges incident (connected) to that node._

### Variable Graph features
**A variable graph (VG) has a node for each variable, and an edge between variables that occur together in at least one clause**

14-17. Nodes degree statistics: mean , coefficient of variation, min and max.

###Balance features
18-20. Ratio of positive and negative literals in each clause: mean, variation coefficient and entropy (see extra notes). 
_For each clause, the ratio is the number of positive literals/number of negative literals.
These ratios are then aggregated, and statistics on them output._
n.b. The _ratio_ is not actually a ratio, but a measure of the offset/bias between the positive and negative values:
2 * abs(0.5 - pos/(pos + neg))  
21-25. Ratio of positive and negative occurrences of each variable: mean, coefficient of variation, min, max and entropy.  
26-27. Fraction of binary and ternary clauses: Fraction of clauses that have 2 literals over total number of clauses,
fraction of clauses with 2 or 3 literals, over total number of clauses.


### Proximity to Horn Formula
**A clause is a Horn clause if it contains at most one positive literal**  
28 Fraction of Horn clauses.  
29-33. Number of occurrences in a Horn clause for each variable: mean, co-efficient of variation, minimum, maximum, entropy.
The number of times a variable appears in all horn clauses.

### DPLL Probing Features
**DPLL (Davis-Putnam-Logemann-Loveland) algorithm is a backtracking algorithm for solving CNF SAT problems.**  
34-38. Number of unit propagations: computed at depths 1, 4, 16, 64 and 256.  
39-40. Search space size estimate: mean depth to contradiction, estimate of the log of number of nodes.

### Local Search Probing Features
**The SAPS and GSAT algorithms for solving SAT problems are run up to 10000 times, 
(or as many times within a 2 second time limit) on the cnf. Various statistics over the runs are calculated**  
41-44. Number of steps to the best local minimum in a run: mean, median, 10th and 90th percentiles for SAPS and GSAT.  
45 . Average improvement to best in a run: mean improvement to best solution for SAPS and GSAT.
46-47. Fraction of improvement due to first local minimum: mean for SAPS and GSAT.
48 . Coefficient of variation of the number of unsatisfied clauses in each local minimum.

### Features from Structure features for SAT instances classification (Ansotegui)
4 structure features
- d: fractal dimension for VIG (_vig_d_poly_)
- d_b: fractal dimension for CVIG (_cvig_db_poly_)
- alpha_v: powerlaw exponent (_variable_alpha_)
- Q: modularity (for VIG) (_vig_modularity_)

A variable incidence graph (VIG): Set of vertexes is the set of boolean variables - weights assigned to edges as follows
W(x, y) = sum (1/(c choose 2)) where x and y are an element of c (c is the clause I am assuming)

Clause variable incidence graph (CVIG): set of vertexes is set of variables and clauses, weight function:
w(x, c) = 1/|c| if x elem c
0 otherwise.
(signs of literals not considered)

Scale free structure - power law distribution. Estimation computed by method of Maximum likelihood
Modularity(Q) of VIG (louvain method) of the best partition.
Fractal dimensions of VIC and CVIG - computed by interpolating log N(r) vs log r, as N(r) ~ r^-d.
N(r) is the estimate of the minimum number of circles with radius r that cover the graph.
Estimated using the Burning by node degree algorithm.

Please refer to [2] for a more theoretical description of the features.

See [GraphFeatSat](https://www.ugr.es/~jgiraldez/) and [code](https://www.ugr.es/~jgiraldez/download/graph_features_sat_v_2_2.tar.gz) for original implementation.

###Extra Notes on aggregation and statistical references
- Coefficient of variation (variation coefficient in paper): 
The coefficient of variation represents the ratio of the standard deviation to the mean
- Entropy: Shannon entropy (https://en.wikipedia.org/wiki/Entropy_(information_theory)). A distribution of the array is
made, from which the entropy is calculated

### Features from New CNF Features and Formula Classification (Alfonso)
- Three new features
Features
- Bunch of new graphs with weights
- Binary Implication graph
- Naive encoded restraints
- Recursive weight heuristic

New graphs
- CV (clause variable) CV+ and CV- (for positive and negative literals) (degrees)
- Variable graph (now with weights 2^-k) (without considering polarity) (degrees, weights) 
- Clause graph (weights the size of the intersection of the clauses) (degrees, weights)
- Resolution graph (Connects clauses when they produce a non-tautological resolvant) (degrees, weights)
(clauses as vertices, edge between clauses iff | C_i intersection (not C_j) | = 1) (there is one literal in clause i that also appears as negated in clause j),
with weights 2 ^ -(|C_i union C_j| -2) (degrees, weights)

For the literal graph (what graph exactly?), the sequence deg +- = max(deg_cv+(i), deg_cv-(i))/deg_cv+(i) + deg_cv-(i) (represents major polarity of each clause)

Binary Implication graph
Simple graph of a formula, contains all literals as vertices (V = lits(F)), all edges in the graph correspond to the
binary clauses in the current formula E = {(a, b), (not b, not a) | {not a, b} elem F}. Sequence with the degree of each node is used.

Sequences from said graphs are taken and stats calculated, with additional statistics such as quantiles, 0 weight occurrences and the number times in which the modal value occurs.

Naive encoded Constraints
Add undirected AND gates, Blocked AND gates, and Exactly One AND gates (psuedocode in paper)

Recursive Weight Heuristic
The heuristic provides a score for each literal x that represents the tendency whether x is present in a model of the formula F.
This is computed for 3 iterations.

Please refer to [3] for a more detailed and theoretical description of the features.

## Basic notes on SAT problems
Positive/negative literal is a respective instance of a variable.
Clause is a disjunction of literal(s)
CNF (Conjunctive Normal Form): Conjunction (and) of disjunction (or) of literals.

- cnfgen - for creating part of the testbed
