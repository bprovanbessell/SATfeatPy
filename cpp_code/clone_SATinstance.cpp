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

    printf("unit prop");
    unitPropProbe(false, true);
}

bool SATinstance::unitprop(int &numClausesReduced, int &numVarsReduced) {

bool consistent = true;

// printf("unit clauses empty: %d \n", unitClauses.empty());

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

// printf ("c Number of variables reduced is: %d, Number of clauses reduced is : %d \n", numVarsReduced, numClausesReduced);
return true;
}


inline vector<int> &SATinstance::clausesWithLit(int lit) {
if (positive(lit))
return posClausesWithVar[lit];
else
return negClausesWithVar[-lit];
}


bool SATinstance::setVarAndProp(int var, bool val) {
int numClausesReduced = 0;
int numVarsReduced = 1;

printf("variable to set %d\n", var);
printf("active vars %d\n", numActiveVars);

assert(varStates[var] == UNASSIGNED);
varStates[var] = val ? TRUE_VAL : FALSE_VAL;
reducedVars.push(var);
numActiveVars--;

int lit = val ? var : -var;
bool consistent = reduceClauses(lit, numClausesReduced, numVarsReduced);
printf("reduce c, v, con %d %d %d\n", numClausesReduced, numVarsReduced, consistent);


if (consistent)
consistent = unitprop(numClausesReduced, numVarsReduced);

printf("consistent %d\n", consistent);
printf("clauses reduced, vars reduced %d %d\n", numClausesReduced, numVarsReduced);

numReducedClauses.push(numClausesReduced);
numReducedVars.push(numVarsReduced);

return consistent;
}


void SATinstance::backtrack() {
    printf("backtrack\n");
int numVarsReduced = numReducedVars.top();
numReducedVars.pop();
for (int i=0; i<numVarsReduced; i++) {
int var = reducedVars.top();
reducedVars.pop();
varStates[var] = UNASSIGNED;
numActiveVars++;
}

int numClausesReduced = numReducedClauses.top();
numReducedClauses.pop();
for (int i=0; i<numClausesReduced; i++) {
int clause = reducedClauses.top();
reducedClauses.pop();

if (clauseStates[clause] != ACTIVE) {
numActiveClauses++;
clauseStates[clause] = ACTIVE;

if (clauseLengths[clause] == 2)
	for (int j=0; clauses[clause][j] != 0; j++) {
	numActiveClausesWithVar[ABS(clauses[clause][j])]++;
	numBinClausesWithVar[ABS(clauses[clause][j])]++;
	}
else
	for (int j=0; clauses[clause][j] != 0; j++)
	numActiveClausesWithVar[ABS(clauses[clause][j])]++;
} else {
clauseLengths[clause]++;
if (clauseLengths[clause] == 2)
	for (int j=0; clauses[clause][j] != 0; j++)
	numBinClausesWithVar[ABS(clauses[clause][j])]++;

else if (clauseLengths[clause] == 3)
	for (int j=0; clauses[clause][j] != 0; j++)
	numBinClausesWithVar[ABS(clauses[clause][j])]--;
}
}

while (!unitClauses.empty())
unitClauses.pop();
}



#define NUM_VARS_TO_TRY 10
#define NUM_PROBES 5

int SATinstance::unitPropProbe(bool haltOnAssignment, bool doComp) {


//testBackTrack();
printf("unit prop probe \n");
if(!doComp)
{

int nextProbeDepth = 1;
for (int j=0; j<NUM_PROBES; j++){
nextProbeDepth *= 4;
char featNameStr[100];
sprintf(featNameStr, "vars-reduced-depth-%d", nextProbeDepth/4);
printf(featNameStr);
}
// writeFeature("unit-featuretime", RESERVED_VALUE);
return 0;
}

// NOTE: depth is number of vars manually set- not including unitprop.
int currentDepth = 0;
int origNumActiveVars = numActiveVars;
bool reachedBottom = false;

for (int probeNum=0; probeNum<NUM_PROBES; probeNum++) {
// this sets depth to 1, 4, 16, 64, 256
int nextProbeDepth = 1;
for (int j=0; j<probeNum; j++){
nextProbeDepth *= 4;
}

while (currentDepth < nextProbeDepth && !reachedBottom) {
    printf("cdepth %d\n", currentDepth);
int varsInMostBinClauses[NUM_VARS_TO_TRY];
int numBin[NUM_VARS_TO_TRY];

int arraySize = 0;
for (int var=1; var<=numVars; var++) {
		if (varStates[var] != UNASSIGNED) continue;
	if (arraySize < NUM_VARS_TO_TRY) arraySize++;

	int j=0;
		while (j < arraySize-1 && numBinClausesWithVar[var] < numBin[j]) j++;
		//hereeeeee
		for (int k=arraySize-1; k>j; k--) {
		varsInMostBinClauses[k] = varsInMostBinClauses[k-1];
		numBin[k] = numBin[k-1];
		}
	varsInMostBinClauses[j] = var;
	numBin[j] = numBinClausesWithVar[var];
}

int maxPropsVar = 0;
bool maxPropsVal;

// if there are no binary clauses, just take the first unassigned var
if (arraySize == 0) {
	maxPropsVar = 1;
	while (varStates[maxPropsVar] != UNASSIGNED && maxPropsVar < numVars) maxPropsVar++;
	maxPropsVal = true;
} 
else {
	int maxProps = -1;

	for (int varNum = 0; varNum < arraySize; varNum++) {
	bool val = true;
	do {  // for val = true and val = false
		
	if (setVarAndProp(varsInMostBinClauses[varNum], val) &&
		numActiveVars <= 0) {
	if (haltOnAssignment) {
		printf("we done here");
		return 12;
	}
	}

	int numProps = origNumActiveVars - numActiveVars - currentDepth;

	if (numProps > maxProps) {
	maxPropsVar = varsInMostBinClauses[varNum];
	maxPropsVal = val;
	}

	backtrack();

	val = !val;
	} while (val == false);

	}
}
// hereish

assert (maxPropsVar != 0);

if (!setVarAndProp(maxPropsVar, maxPropsVal)){
    	reachedBottom = true;
        printf("make that shit true\n");
        char str[100];
        sprintf(str, "vars-reduced%d", currentDepth);
        printf(str);
        // printf("depth %d\n", currentDepth);
}

else if (numActiveClauses == 0) {
	if (haltOnAssignment) {
	printf("done here aswell");
	return 12;
	}
	reachedBottom = true;
}

currentDepth++;

}
// hereish now

char featNameStr[100];
sprintf(featNameStr, "vars-reduced-depth-%d", nextProbeDepth);

printf(featNameStr);
double res = (double)(origNumActiveVars - numActiveVars - currentDepth)/numVars;
std::cout << res;
// writeFeature(featNameStr, (double)(origNumActiveVars - numActiveVars - currentDepth)/numVars);
}

while (numActiveVars != origNumActiveVars)
backtrack();
// writeFeature("unit-featuretime", gSW.TotalLap()-myTime);
// myTime=gSW.TotalLap();
return 13;
}



