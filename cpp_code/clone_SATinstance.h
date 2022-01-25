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

    int unitPropProbe(bool haltOnAssignment, bool doComp);

    bool setVarAndProp(int var, bool val);
    // backtrack undoes one call of setVar *or* unitprop
    void backtrack();


    double array_entropy(double *array, int num, int vals, int maxval);
    int computeFeatures(bool doComp);


    int currentClause;
   inline int *firstClause();
   int *nextClause();

   // two lit iterators are provided so that two
   // clauses can be iterated over simultaneously

   int currentLit, currentLit2;
   int *currentClauseForLitIter, *currentClauseForLitIter2;
   inline int firstLitInClause(int *clause);
   inline int nextLitInClause();
   inline int firstLitInClause2(int *clause);
   inline int nextLitInClause2();

     int currentClauseWithVar;
   int currentVarForClauseIter;
   bool posClauses;
   inline int *firstClauseWithVar(int var, bool positive);
   int *nextClauseWithVar();




    SATinstance(const char* filename);
};

#endif