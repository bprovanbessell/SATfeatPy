#Feature extraction pipeline
This will explain the basic structure and usage of the pipeline to extract features from cnf SAT problems.

First, the cnf undergoes pre-processing (see [pre-processing](pre-processing.md)). SatELite, tautology reduction, clause reduction, unit clause reduction.
Each of these processes _is_ available as an option. (Specify with input?).

Features of the cnf are then extracted. Problem size features, balance features, graph features... (see [features](features.md)).
Each of these feature sets is available as an option to compute.