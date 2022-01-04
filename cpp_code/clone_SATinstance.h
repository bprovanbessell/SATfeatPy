#ifndef _SAT_INSTANCE_H
#define _SAT_INSTANCE_H

#include <stdio.h>

#include <map>
#include <set>
#include <string>
#include <stack>
#include <vector>
using namespace std;

class SATinstance{

    public:
    typedef enum {TRUE_VAL, FALSE_VAL, UNASSIGNED, IRRELEVANT} varState;
    typedef enum {ACTIVE, PASSIVE} clauseState;
    char* inputFileName;
    int numVars, numClauses;
    int **clauses;

    vector<int> *negClausesWithVar;
    vector<int> *posClausesWithVar;


    /* These change as tree is explored. */
    varState *varStates;
    clauseState *clauseStates;
    int numActiveVars, numActiveClauses;

    int *numActiveClausesWithVar;
    int *numBinClausesWithVar;
    int *clauseLengths;

    stack<int> unitClauses;

    stack<int> reducedClauses;
    stack<int> numReducedClauses;

    stack<int> reducedVars;
    stack<int> numReducedVars;

    bool unitprop(int &numClausesReduced, int &numVarsReduced);
    bool reduceClauses(int lit, int &numClausesReduced, int &numVarsReduced);
    inline vector<int> & clausesWithLit(int lit);




    SATinstance(const char* filename);
};

#endif