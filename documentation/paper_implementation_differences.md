# Differences in paper description of features and their implementation
There are a lot of differences between the description of the features in the SATzilla paper, and the actual implementation of them.
This documents and describes the differences.

For all features, pre-processing, and clause reduction is performed on the clauses, before and features are computed.


Ratio c/v, this is actually implemented as the inverse: v/c.
Ration of positive and negative literals in each clause. In the implementation, the "ratio" is actually more a measure 
of the balance between positive and negative literals in the clause, as opposed the the ratio. It is implemented as:
for each clause, the ratio of the clause is: 2 x | 0.5 X (pos/(pos + neg))|, where pos and neg represent the number of
positive and  negative literals in the clause respectively.