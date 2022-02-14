#Feature extraction pipeline
This will explain the basic structure and usage of the pipeline to extract features from cnf SAT problems.

First, the cnf undergoes pre-processing (see [pre-processing](pre-processing.md)). SatELite, tautology reduction, clause reduction, unit clause reduction.
Each of these processes _is_ available as an option. (Specify with input?).

Features of the cnf are then extracted. Problem size features, balance features, graph features... (see [features](features.md)).
Each of these feature sets is available as an option to compute.

These features can be output through standard output, or saved to a file. Alternatively, you can access the features 
directly from the satinstance object (they are stored as the dictionary _features_dict_).