#include "clone_SATinstance.h"

// #include <stdio.h>
#include <math.h>
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

    printf("compute features");
    computeFeatures(true);

    // // ------------- pos neg entropy testing -----------------
    // double *pos_frac_per_var = new double [numVars+1];

    // int *pos_var = new int [numVars+1];
    // int *neg_var = new int [numVars+1];


    // for (int t=1; t <= numVars; t++) {

    //     if (varStates[t] != UNASSIGNED || var_array[t]==0){}
    //         pos_frac_per_var[t] = -900000;
    //         printf("shits messed up yo");
    //         continue;
    //     }

    //     pos_frac_per_var[t] = 2.0 * fabs(0.5 - (double)pos_var[t] / ((double)pos_var[t] + (double)neg_var[t]));

    // }

    // double res = 0;
}

int SATinstance::computeFeatures(bool doComp) {

//  testBackTrack();
//Stopwatch sw;
printf("c Initializing...");
//sw.Start();

//fprintf(stderr, "Computing features. Prefix %s endpref\n", featurePrefix);
// node degree stats for var-clause graph
int *var_array = new int[numVars+1];
int *var_graph = new int[numVars+1];
bool *var_graph_found = new bool[numVars+1];
double *var_graph_norm = new double[numVars+1];
int *horny_var = new int[numVars+1];
double *horny_var_norm = new double[numVars+1];
double *var_array_norm = new double[numVars+1];
int *clause_array = new int[numClauses];
double *clause_array_norm = new double[numClauses];
int *pos_in_clause = new int[numClauses];
int *neg_in_clause = new int[numClauses];
double *pos_frac_in_clause = new double[numClauses];
int *pos_var = new int [numVars+1];
int *neg_var = new int [numVars+1];
double *pos_frac_per_var = new double [numVars+1];
int unary=0, binary=0, trinary=0;
int horn_clauses = 0;
int t, tt;

// initialize
for (t=1; t<=numVars; t++) 
{
var_array[t] = 0;
pos_var[t] = 0;
neg_var[t] = 0;
horny_var[t] = 0;
var_array_norm[t] = RESERVED_VALUE;
pos_frac_per_var[t] = RESERVED_VALUE;
}

for (t=0;t<numClauses;t++)
{
clause_array[t] = (int)RESERVED_VALUE;
clause_array_norm[t] = RESERVED_VALUE;
pos_in_clause[t] = (int)RESERVED_VALUE;
neg_in_clause[t] = (int)RESERVED_VALUE;
pos_frac_in_clause[t] = RESERVED_VALUE;
}
// if (DEB)
// p("c Go through clauses...");
// writeFeature("nvarsOrig",(double)OrigNumVars);
// writeFeature("nclausesOrig",(double)OrigNumClauses);
// writeFeature("nvars",(double)numActiveVars);
// writeFeature("nclauses",(double)numActiveClauses);
// if ((double) numActiveVars ==0){
// writeFeature("reducedVars", RESERVED_VALUE);
// writeFeature("reducedClauses",RESERVED_VALUE);
// writeFeature("Pre-featuretime", preTime);
// writeFeature("vars-clauses-ratio",RESERVED_VALUE);
//  }
// else {
// writeFeature("reducedVars", ((double)OrigNumVars-(double)numActiveVars)/(double)numActiveVars);
// writeFeature("reducedClauses",((double)OrigNumClauses-(double)numActiveClauses)/(double)numActiveClauses);
// writeFeature("Pre-featuretime", preTime);
// writeFeature("vars-clauses-ratio",((double)numActiveVars)/(double)numActiveClauses);
// }

// go through all the clauses
// What we get from here is 
// clause_array : number of lierals
// pos_in_clause/neg_in_clause
// var_array: number of cluses contain this variable
// pos_var/neg_var
int *clause, lit;
t=0;
for (clause = firstClause(); clause != NULL; clause = nextClause()) 
{
// initialize 
clause_array[t] = 0;
pos_in_clause[t] = 0;
neg_in_clause[t] = 0;
	
for (lit = firstLitInClause(clause); lit != 0; lit = nextLitInClause()) 
	{
	clause_array[t]++;
	var_array[ABS(lit)]++;
	
	if (positive(lit)) 
	{
	pos_in_clause[t]++;
	pos_var[ABS(lit)]++;
	}
	else 
	{
	neg_in_clause[t]++;
	neg_var[ABS(lit)]++;
	}
	}
	
// may be this is a bad name for this. 
// basically, it compute the bias for the assignment     
// do we need say anything for cluase_array[t]=0
// this should not happened
if(clause_array[t]!=0)
	pos_frac_in_clause[t] = 2.0 * fabs(0.5 - (double) pos_in_clause[t] / ((double)pos_in_clause[t] + (double)neg_in_clause[t]));
else
	{
	pos_frac_in_clause[t]=RESERVED_VALUE;
	//	  fprintf(stderr, "L %d clause %d empty\n", featureLevel, t);
	}
	
// cardinality
switch(clause_array[t]) 
	{
	case 1: unary++; break;
	case 2: binary++; break;
	case 3: trinary++; break;
	}

// NOTE: isn't neg_in_clause <= 1 also horny? GMA
// this is really not make sense. by switching pos/neg, you can get different horn clause  
// horn clause
if (pos_in_clause[t] <= 1)
	{
	for (lit = firstLitInClause(clause); lit != 0; lit = nextLitInClause()) 
	horny_var[ABS(lit)]++;
	horn_clauses++;
	}        
// normalize
clause_array_norm[t] = (double) clause_array[t] / (double) numActiveVars;   
// increment clause index
t++;
}
//  fprintf(stderr, "Level %d: Went through %d clauses\n", featureLevel, t);

// positive ratio in clauses
// writeStats(pos_frac_in_clause,numClauses,"POSNEG-RATIO-CLAUSE");
std::cout << array_entropy(pos_frac_in_clause,numClauses,100,1);
// writeFeature("POSNEG-RATIO-CLAUSE-entropy",array_entropy(pos_frac_in_clause,numClauses,100,1));
// // clause side in the bipartite graph
// writeStats(clause_array_norm,numClauses,"VCG-CLAUSE");
// writeFeature("VCG-CLAUSE-entropy",array_entropy(clause_array,numClauses,numActiveVars+1));
// // cardinality of clauses
// if ((double) numActiveVars ==0){
// writeFeature("UNARY",RESERVED_VALUE);
// writeFeature("BINARY+",RESERVED_VALUE);
// writeFeature("TRINARY+",RESERVED_VALUE);
//  }
// else {
// writeFeature("UNARY",(double)unary/(double)numActiveClauses);
// writeFeature("BINARY+",(double)(unary+binary)/(double)numActiveClauses);
// writeFeature("TRINARY+",(double)(unary+binary+trinary)/(double)numActiveClauses);
// }


// writeFeature("Basic-featuretime", gSW.TotalLap()-myTime);
// myTime=gSW.TotalLap();

// if (DEB)
// p("c Go through variables...");

// Go through the variables
for (t=1; t <= numVars; t++) 
{
if (varStates[t] != UNASSIGNED || var_array[t]==0)  // do we still want the second part?
	{
	var_graph[t] = (int)RESERVED_VALUE;
	var_array_norm[t] = RESERVED_VALUE;
	var_graph_norm[t] = RESERVED_VALUE;
	horny_var[t] = (int)RESERVED_VALUE;
	horny_var_norm[t] = RESERVED_VALUE;
	var_array[t] = (int)RESERVED_VALUE;
	pos_var[t] = (int)RESERVED_VALUE;
	neg_var[t] = (int)RESERVED_VALUE;
	pos_frac_per_var[t] = RESERVED_VALUE;
	continue;
	}
	
for (tt=1; tt <= numVars; tt++)
	var_graph_found[tt] = false;
	
// now do the variable graph
for (clause = firstClauseWithVar(t,false); clause != NULL; clause = nextClauseWithVar())
	{
	//fprintf(stderr, "Var %d false: clause %xd\n", t, clause);            
	for (lit = firstLitInClause(clause); lit != 0; lit = nextLitInClause())
	var_graph_found[ABS(lit)] = true;     
	}
for (clause = firstClauseWithVar(t,true); clause != NULL; clause = nextClauseWithVar())
	{
	//fprintf(stderr, "Var %d truee: clause %xd\n", t, clause);
	for (lit = firstLitInClause(clause); lit != 0; lit = nextLitInClause())
	var_graph_found[ABS(lit)] = true;    
	}
	
var_graph[t] = - 1; // counting self
for (tt=1; tt<=numVars; tt++)
	if (var_graph_found[tt]) var_graph[t]++;
	
// calculate and normalize
pos_frac_per_var[t] = 2.0 * fabs(0.5 - (double)pos_var[t] / ((double)pos_var[t] + (double)neg_var[t]));
var_array_norm[t] = (double) var_array[t] / (double) numActiveClauses;
var_graph_norm[t] = (double) var_graph[t] / (double) numActiveClauses;
horny_var_norm[t] = (double) horny_var[t] / (double) numActiveClauses;
}

// variable side in the bipartite graph
// writeStats(var_array_norm+1, numActiveVars, "VCG-VAR");
// writeFeature("VCG-VAR-entropy",array_entropy(var_array+1,numActiveVars,numActiveClauses+1));

/* == DEBUG:  
fprintf(stderr, "c L %d: %lf %lf %lf %lf\n", featureLevel, array_min(clause_array_norm, NB_CLAUSE), array_max(clause_array_norm, NB_CLAUSE), mean(clause_array_norm, NB_CLAUSE), stdev(clause_array_norm, NB_CLAUSE, mean(clause_array_norm, NB_CLAUSE)));
for(t=0; t<NB_CLAUSE; t++)
{
fprintf(stderr, "c L %d clause[%d]:\t", featureLevel, t);
if(clause_array_norm[t]==RESERVED_VALUE) fprintf(stderr, "RESERVED\n");
else fprintf(stderr, "c %lf\n", clause_array_norm[t]);
}
*/


// // positive ratio in variables
// writeStatsSTDEV(pos_frac_per_var+1,numActiveVars,"POSNEG-RATIO-VAR");
// writeFeature("POSNEG-RATIO-VAR-entropy",array_entropy(pos_frac_per_var+1,numActiveVars,100,1));
// printf("POSNEG ratio var entropy: %d", array_entropy(pos_frac_per_var+1,numActiveVars,100,1));

double res = array_entropy(pos_frac_per_var+1,numActiveVars,100,1);

printf("posneg ratio var: ");

std::cout << res;

std::cout << array_entropy(pos_frac_per_var+1,numActiveVars,100,1);

// // horn clauses
// writeStats(horny_var_norm+1,numActiveVars,"HORNY-VAR");
// writeFeature("HORNY-VAR-entropy",array_entropy(horny_var+1,numActiveVars,numActiveClauses+1));
// if ((double) numActiveVars ==0)
// writeFeature("horn-clauses-fraction",RESERVED_VALUE);
// else
// writeFeature("horn-clauses-fraction",(double)horn_clauses / (double)numActiveClauses);

// // variable graph
// writeStats(var_graph_norm+1, numActiveVars, "VG");

// clean up after yourself, you pig!
delete[] var_array;
delete[] var_graph;
delete[] var_graph_norm;
delete[] horny_var;
delete[] horny_var_norm;
delete[] var_array_norm;
delete[] clause_array;
delete[] clause_array_norm;
delete[] pos_in_clause;
delete[] neg_in_clause;
delete[] pos_frac_in_clause;
delete[] pos_var;
delete[] neg_var;
delete[] pos_frac_per_var;
delete[] var_graph_found;


// writeFeature("KLB-featuretime", gSW.TotalLap()-myTime);
// myTime=gSW.TotalLap();
// if (DEB)
// p("c Clause graph...");
// clauseGraphFeatures(false);
// if (DEB)
// p("c Done with base features");


// return FEAT_OK;
return 15;
}


double SATinstance::array_entropy(double *array, int num, int vals, int maxval)
{
int *p = new int[vals+1];
double entropy = 0.0,pval;
int t,res=0;
int idx;

// initialize
for (t=0;t<=vals;t++) p[t] = 0;

// make the distribution
for (t=0;t<num;t++) 
{

	// how would this value possibly be a reserved value??
if (array[t] == (double)RESERVED_VALUE) {res++; continue;}
idx = (int) floor(array[t] / ((double)maxval/(double)vals));
//      if (idx > maxval) idx = maxval;
if ( idx > vals ) idx = vals;
if ( idx < 0 ) idx = 0;
p[idx]++;
}

// find the entropy
for (t=0; t<=vals; t++)
{
if (p[t]) 
	{
	pval = double(p[t])/double(num-res);
	entropy += pval * log(pval);
	}
}
	
delete[] p;

return -1.0 * entropy;
}


bool SATinstance::unitprop(int &numClausesReduced, int &numVarsReduced) {

bool consistent = true;

// printf("units length: %d \n", unitClauses.size());

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

// for (int i=0; i<(int)clausesWithLit(-lit).size(); i++) {
//     int clause = clausesWithLit(-lit)[i];
//     printf("%d, ", clause);
// }
// "remove" vars from inconsistent clauses
for (int i=0; i<(int)clausesWithLit(-lit).size(); i++) {
int clause = clausesWithLit(-lit)[i];
if (clauseStates[clause] == ACTIVE) {
reducedClauses.push(clause);
numClausesReduced++;

clauseLengths[clause]--;
if (clauseLengths[clause] == 2){
    for (int i=0; clauses[clause][i] != 0; i++)
	numBinClausesWithVar[ABS(clauses[clause][i])]++;
}
	
	else if (clauseLengths[clause] == 1) {
		for (int i=0; clauses[clause][i] != 0; i++)
		numBinClausesWithVar[ABS(clauses[clause][i])]--;
        // printf("%d is unit clause", clause);
		unitClauses.push(clause);

} else if (clauseLengths[clause] == 0)
	return false;
}
}

// printf("consisten clause");
// for (int i=0; i<(int)clausesWithLit(lit).size(); i++) {
// int clause = clausesWithLit(lit)[i];
//     printf("%d", clause);
// }
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

// printf("variable to set %d\n", var);
// printf("active vars %d\n", numActiveVars);

assert(varStates[var] == UNASSIGNED);
varStates[var] = val ? TRUE_VAL : FALSE_VAL;
reducedVars.push(var);
numActiveVars--;

int lit = val ? var : -var;
bool consistent = reduceClauses(lit, numClausesReduced, numVarsReduced);
// printf("reduce c, v, con %d %d %d\n", numClausesReduced, numVarsReduced, consistent);


if (consistent)
consistent = unitprop(numClausesReduced, numVarsReduced);

// printf("consistent %d\n", consistent);
// printf("clauses reduced, vars reduced %d %d\n", numClausesReduced, numVarsReduced);

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


int *SATinstance::firstClause() {
currentClause = 0;
return nextClause();
}

int *SATinstance::nextClause() {
while (currentClause < numClauses && clauseStates[currentClause] != ACTIVE)
currentClause++;

return currentClause >= numClauses ? NULL : clauses[currentClause++];
}

int SATinstance::firstLitInClause(int *clause) {
currentClauseForLitIter = clause;
currentLit = 0;
return nextLitInClause();
}

int SATinstance::nextLitInClause() {
while (currentClauseForLitIter[currentLit] != 0 &&
	varStates[ABS(currentClauseForLitIter[currentLit])] != UNASSIGNED)
currentLit++;

if (currentClauseForLitIter[currentLit] == 0)
return 0;
else
return currentClauseForLitIter[currentLit++];
}

int *SATinstance::firstClauseWithVar(int var, bool ispos) {
currentClauseWithVar = 0;
currentVarForClauseIter = var;
posClauses = ispos;
return nextClauseWithVar();
}

int *SATinstance::nextClauseWithVar() {
if (posClauses) {
while (currentClauseWithVar < (int)posClausesWithVar[currentVarForClauseIter].size() &&
	clauseStates[posClausesWithVar[currentVarForClauseIter][currentClauseWithVar]] != ACTIVE)
currentClauseWithVar++;
if (currentClauseWithVar == (int)posClausesWithVar[currentVarForClauseIter].size())
return NULL;
else	    
return clauses[posClausesWithVar[currentVarForClauseIter][currentClauseWithVar++]];
} 
else {
while (currentClauseWithVar < (int)negClausesWithVar[currentVarForClauseIter].size() &&
	clauseStates[negClausesWithVar[currentVarForClauseIter][currentClauseWithVar]] != ACTIVE)
currentClauseWithVar++;
if (currentClauseWithVar == (int)negClausesWithVar[currentVarForClauseIter].size() )
return NULL;
else	    
return clauses[negClausesWithVar[currentVarForClauseIter][currentClauseWithVar++]];
}
}