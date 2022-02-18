# Differences in paper description of features and their implementation
There are a lot of differences between the description of the features in the SATzilla paper, and the actual implementation of them.
This documents and describes the differences.

Pre-processing is first done by SatELite (http://minisat.se/SatELite.html). Apparently outdated and obsolete, but will
be necessary to use to compare with versions of SATzilla.

For all features, pre-processing, and clause reduction is performed on the clauses, before and features are computed.

Ratio c/v, this is actually implemented as the inverse: v/c.
Ration of positive and negative literals in each clause. In the implementation, the "ratio" is actually more a measure 
of the balance between positive and negative literals in the clause, as opposed the the ratio. It is implemented as:
for each clause, the ratio of the clause is: 2 x | 0.5 X (pos/(pos + neg))|, where pos and neg represent the number of
positive and  negative literals in the clause respectively.

Satzilla code does not compute the variation co-efficient for positive and negative variable ratios, but instead uses std.

The ratio of binary clauses is the number of binary plus unary clauses over the total number of clauses.
Similarly with ternary clauses, the ratio is the number of unary plus binary plus ternary clauses over the total number of clauses.

For the statistics of number of variable occurrences in horn clauses, the statistics are calculated for normalized variable counts,
(each count is divided by the number of active clauses)

vcg clause degrees This is also normalised (each degree divided by the number of active variables) 
(but normalised values are not used for entropy)

In the paper this is done by just counting the literals per clause, but this is based on the assumption that
the clauses have been pre-processed.

vcg variable degrees -> number of clauses that contain the variable (similar as with clause degrees)

vg node degrees divided by number of active variables

# Features to improve/modify implemenation of
* Overall refactor of methods to make them more pythonic (optimise with list comprehension instead of loops, etc. Look into numba to provide a precompiled version )

# Notes on SATzilla implementation:
different options
- base is features 1-33 (+ a few other options)
- SP is survey propagation ->
- dia is diameter?
- cl (quartiles, min, max etc) (executing zchaff07)
- lp ??? lpslack
- unit: features 34-38 number of unit propagations (eg, variables reduced at certain depth)
- ls: (local search) executes ubcsat2006 (currently crashes) features 41-48 
- lobjois: features 39-40 search space size estimate (stochastic in nature, will have to use a certain level of freedom 
when checking results.) 


RISS (Alfonso) has multiple different descriptions of Graphs, and features calculated. Furthermore, RISS implementation
of the Graphs, is different to that as described in the papers. Our implementation of creating the Naive Encoded constraint graphs
(AND, BAND, EXO) follows pseudocode in [4], as opposed to implementation and description in [3]. We are open to clarification of graph description
and pseudocode.

It would be worth trying to improve accuracy of the RWH by strictly re-implementing from "Recursive weight heuristic for random k-sat"

TODO: fix ref
[4] Increasing the Robustness of SAT Solving with Machine Learning Techniques
[5] Recursive weight heuristic for random k-sat

