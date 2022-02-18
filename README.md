# SAT-features

Python library to extract features from SAT problems. Re-production of SATzilla feature extractor.

Features implemented:
1-48. of Satzilla paper (see [features](documentation/features.md)).

Fractal dimension of CVIG and VIG, modularity of VIG, and alpha (powerlaw fit of variable occurrences) from Structure Features for SAT instances classification.

Current command line usage, from project root directory.
This will print a dictionary of the features. Abbreviations can be found in (see [features](documentation/features.md)). [TO DO].
```
python features.py path/to/cnf_file.cnf
```

N.b. current implementation reliant on SatELite binaries, which only work on linux systems.

**Dependencies**
- Python 3.8
- NetworkX:  ```pip install networkx```
- community ```pip install python-louvain```
- powerlaw ```pip install powerlaw```
- sklearn ```pip install scikit-learn```
- scipy ```pip install scipy```

A binary for ubcsat is included in the ubcsat folder, however you may have to compile and add this yourself for full functionality.
Please clone and compile [ubcsat](https://github.com/dtompkins/ubcsat/tree/beta), and put the resulting binary in the ubcsat folder, if the current binary does not work. We found the beta branch to be stable.

## How to use this package
Download dependencies
Clone this repository within your project.
You can call the feature generation from the command line by invoking the generate features python file
```python generate_features.py```
You can specify the features to generate from within this file or via command line 
TODO: add command line specification for file, different groups of features.

- From command line:

- Within python applications:
The sat_instance class contains all methods necessary to generate the variety of features.

**Important references**
- Xu, Lin, et al. "SATzilla: portfolio-based algorithm selection for SAT". Journal of Artificial Intelligence Research (2008): 565-606.
- Ansotegui, Giraldez-Cru, et al. "Structure features for SAT instances classification". Journal of Applied Logic (2017): 23:27–39.
