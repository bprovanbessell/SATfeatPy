# SAT-features

Python library to extract features from SAT problems. Re-production of SATzilla feature extractor.

Features implemented:
1-33. of Satzilla paper (see [features](documentation/features.md)).

Current command line usage, from project root directory.
This will print a dictionary of the features. Abbreviations can be found in (see [features](documentation/features.md)). [TO DO].
```
python features.py path/to/cnf_file.cnf
```

N.b. current implementation reliant on SatELite binaries, which only work on linux systems.

**Dependencies**
- NetworkX:  ```pip install networkx```
- community ```pip install python-louvain```
- powerlaw ```pip install powerlaw```
- sklearn ```pip install scikit-learn```

**Important references**
- Xu, Lin, et al. "SATzilla: portfolio-based algorithm selection for SAT." Journal of Artificial Intelligence Research (2008): 565-606.
