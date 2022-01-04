#include "clone_SATinstance.h"

// #include <stdio.h>
// #include <math.h>
// #include <time.h>

// #include <sys/times.h>
// #include <limits.h>
// #include <stdlib.h>

// #include <set>
// #include <map>
// #include <algorithm>
#include <iostream>
#include <fstream>
// #include <sstream>
// #include <cstring>
// #include <vector>
// #include <cassert>
// #include "lp_solve_4.0/lpkit.h"
// #include "lp_solve_4.0/patchlevel.h"
// #include "stopwatch.h"

#define MAX(X,Y) ((X) > (Y) ? (X) : (Y))
#define MIN(X,Y) ((X) > (Y) ? (Y) : (X))
#define ABS(X) ((X) > 0 ? (X) : -(X))

#define positive(X) ((X) > 0)
#define negative(X) ((X) < 0)

#define RESERVED_VALUE (-512)


int main(int argc, char** argv) {
    
    char *filename;
    char outfile[512];      
    filename=argv[1];

    std::cout << "filename: ";
    std::cout << filename;
    std::cout << "\n";

    SATinstance* sat = new SATinstance(filename); 
	return 0;
}

SATinstance::SATinstance(const char* filename) {

    // what is normally in features
    ifstream infile(filename);
    if (!infile) {
        fprintf(stderr, "c Error: Could not read from input file %s.\n", filename);
        exit(1);
    }
    char chbuf;
    char strbuf[1024];
    infile.get(chbuf);
    while (chbuf != 'p') {
        infile.ignore(1000, '\n');
        infile.get(chbuf);
        if(!infile) {
            fprintf(stderr, "c ERROR: Premature EOF reached in %s\n", filename);
            exit(1);
        }
    }

    int origNumVars, origNumClauses;
    infile >> strbuf; // "cnf"
    infile >> origNumVars >> origNumClauses;


    printf("c Orignal number of varibales is %d, number of clauses is %d \n", origNumVars, origNumClauses);

    printf("c Input file is: %s. \n", filename);
    // up til here


    // if doComp -> what is this useless garbage?
    // ifstream infile(filename);
    // if (!infile){
    //     fprintf(stderr, "c Error: Could not read from input file %s.\n", filename);
    //     exit(1);    
    // }

    // inputFileName = (char *)filename;
    // char chbuf;
    // char strbuf[1024];
    // infile.get(chbuf);
    // while (chbuf != 'p') {
    //     //    infile.getline(strbuf, 100);
    //     infile.ignore(1000, '\n');
    //     infile.get(chbuf);
    //     if(!infile){
    //         fprintf(stderr, "c ERROR: Premature EOF reached in %s\n", filename);
    //         exit(1);
    //     }
    // }

    // infile >> strbuf; // "cnf"
    // if( strcmp(strbuf, "cnf")!=0 ){
    //     fprintf(stderr, "c Error: Can only understand cnf format!\n");
    //     exit(1);
    // }

    // infile >> numVars >> numClauses;
    numVars = origNumVars;
    numClauses = origNumClauses;

    clauses = new int*[numClauses];
    clauseStates = new clauseState[numClauses];
    clauseLengths = new int[numClauses];

    negClausesWithVar = new vector<int>[numVars+1];
    posClausesWithVar = new vector<int>[numVars+1];

    numActiveClausesWithVar = new int[numVars+1];
    numBinClausesWithVar = new int[numVars+1];

    for (int i=1; i<=numVars; i++) {
        numActiveClausesWithVar[i] = 0;
        numBinClausesWithVar[i] = 0;
    }

    int *lits = new int[numVars+1];

    // read stuff into data structure. 
    // take care of all data structure
    // clauseLengths,  unitClauses, numBinClausesWithVar
    // negClausesWithVar, posClausesWithVar, numActiveClausesWithVar
    for (int clauseNum=0; clauseNum<numClauses; clauseNum++) {

        int numLits = 0;  // not including 0 terminator
        if(!infile) {
            fprintf(stderr, "c ERROR: Premature EOF reached in %s\n", filename);
            exit(1);
        }

        infile >> lits[numLits];
        while (lits[numLits] != 0){  
            infile >> lits[++numLits];
        }

        /* test if some literals are redundant and sort the clause */
        bool tautology = false;
        for (int i=0; i<numLits-1; i++) {
            int tempLit = lits[i];
            for (int j=i+1; j<numLits; j++) {
	            if (ABS(tempLit) > ABS(lits[j])) {
                // this is sorting the literals	 
	            int temp = lits[j];
	            lits[j] = tempLit;
		        tempLit = temp;
	            } 
                else if (tempLit == lits[j]) {
	                lits[j--] = lits[--numLits];
	                printf("c literal %d is redundant in clause %d\n", tempLit, clauseNum);
	            } 
                else if (ABS(tempLit) == ABS(lits[j])) {
                    tautology = true;
                //	  printf("c Clause %d is tautological.\n", clauseNum);
                //	  break;
	            }
            }
            if (tautology) break;
            else lits[i] = tempLit;
        } 

        if (!tautology) {
            clauseLengths[clauseNum] = numLits;
            clauses[clauseNum] = new int[numLits+1];
            clauseStates[clauseNum] = ACTIVE;

        if (numLits == 1) {
            unitClauses.push(clauseNum);
        }
	
        else if (numLits == 2){
            for (int i=0; i<numLits; i++)
		    numBinClausesWithVar[ABS(lits[i])]++;
        }
	

	    for (int litNum = 0; litNum < numLits; litNum++) {
		    if (lits[litNum] < 0){
                negClausesWithVar[ABS(lits[litNum])].push_back(clauseNum);
            }
		    else{
                posClausesWithVar[lits[litNum]].push_back(clauseNum);
            }
            
	        numActiveClausesWithVar[ABS(lits[litNum])]++;
	        clauses[clauseNum][litNum] = lits[litNum];
	    }
        clauses[clauseNum][numLits] = 0;
        } else {
        clauseNum--;
        numClauses--;
        }

    }


    delete[] lits;
    numActiveClauses = numClauses;

    // remove some redandant variables
    // prepar data sturcuture: varStates
    varStates = new varState[numVars+1];
    numActiveVars = numVars;
    for (int i=1; i<=numVars; i++) {
        if (numActiveClausesWithVar[i]  == 0) {
            varStates[i] = IRRELEVANT;
            numActiveVars--;
        } else
        varStates[i] = UNASSIGNED;
    }

    // before doing anything first do a round of unit propogation to remove all the 
    // unit clasues
    int dummy1, dummy2;
    unitprop(dummy1, dummy2);

    // test_flag = new int[numVars+1];
    // indexCount = 0;    

    // if (seed == 0)
    // seed=(long)time(NULL);

    // srand(seed);
    printf ("c Number of variable is: %d, Number of clause is : %d \n", numActiveVars, numActiveClauses);
}

bool SATinstance::unitprop(int &numClausesReduced, int &numVarsReduced) {

bool consistent = true;

printf("unit clauses empty: %d \n", unitClauses.empty());

while (!unitClauses.empty() && consistent) {
int clauseNum = unitClauses.top();
unitClauses.pop();

if (clauseStates[clauseNum] != ACTIVE) continue;

int litNum = 0;
while (varStates[ABS(clauses[clauseNum][litNum])] != UNASSIGNED) {
litNum++;
}

// assertions are our friends!
assert (clauseLengths[clauseNum] == 1);

int lit = clauses[clauseNum][litNum];

varStates[ABS(lit)] = positive(lit) ? TRUE_VAL : FALSE_VAL;
reducedVars.push(ABS(lit));
numActiveVars--;
numVarsReduced++;

consistent &= reduceClauses(lit, numClausesReduced, numVarsReduced);
}

return consistent;
}


bool SATinstance::reduceClauses(int lit, int &numClausesReduced, int &numVarsReduced) {

// "remove" vars from inconsistent clauses
for (int i=0; i<(int)clausesWithLit(-lit).size(); i++) {
int clause = clausesWithLit(-lit)[i];
if (clauseStates[clause] == ACTIVE) {
reducedClauses.push(clause);
numClausesReduced++;

clauseLengths[clause]--;
if (clauseLengths[clause] == 2)
	for (int i=0; clauses[clause][i] != 0; i++)
	numBinClausesWithVar[ABS(clauses[clause][i])]++;
	else if (clauseLengths[clause] == 1) {
		for (int i=0; clauses[clause][i] != 0; i++)
		numBinClausesWithVar[ABS(clauses[clause][i])]--;
		unitClauses.push(clause);

} else if (clauseLengths[clause] == 0)
	return false;
}
}

// satisfy consistent clauses
for (int i=0; i<(int)clausesWithLit(lit).size(); i++) {
int clause = clausesWithLit(lit)[i];
if (clauseStates[clause] == ACTIVE) {
	
clauseStates[clause] = PASSIVE;
reducedClauses.push(clause);
numActiveClauses--;

int j=0;
int otherVarInClause = ABS(clauses[clause][j]);
while (otherVarInClause != 0) {
	numActiveClausesWithVar[otherVarInClause]--;
	if (clauseLengths[clause] == 2)
		numBinClausesWithVar[otherVarInClause]--;

	// is the var now irrelevant (active, but existing in no clauses)?
	if (numActiveClausesWithVar[otherVarInClause] == 0 &&
	varStates[otherVarInClause] == UNASSIGNED) {
	varStates[otherVarInClause] = IRRELEVANT;
	reducedVars.push(otherVarInClause);
	numActiveVars--;
	
	numVarsReduced++;
	}

	j++;
	otherVarInClause = ABS(clauses[clause][j]);
}
numClausesReduced++;
}
}

printf ("c Number of variables reduced is: %d, Number of clauses reduced is : %d \n", numVarsReduced, numClausesReduced);
return true;
}


inline vector<int> &SATinstance::clausesWithLit(int lit) {
if (positive(lit))
return posClausesWithVar[lit];
else
return negClausesWithVar[-lit];
}



