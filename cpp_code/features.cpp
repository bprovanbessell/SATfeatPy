#include "clone_SATinstance.h"
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <string.h>
// #include "global.h"
using namespace std;

int main(int argc, char** argv) {

    // DEB, verbose of some kind?
    bool DEB = true;

    // if(argc < 2){
    //     cerr << "Usage: features {  [-all] | [-base] |[-sp] [-Dia] [-Cl] [-unit] [-ls] [-lobjois] } infile [outfile]" << endl;
    //     return 1;
    // }

    char *filename;
    char outfile[512];      
    filename=argv[1];

    std::cout << "filename: ";
    std::cout << filename;
    std::cout << "\n";
    
   
//     sprintf(outfile, "%s", "/tmp");
//     strcat(outfile, "/outputXXXXXX");
//     mkstemp(outfile);
   
// //   gTimeOut = getTimeOut();
// //   BuildSolvers("123456", outfile);
// //   gSW.Start();

//   // before doing anything, count number of variables and clauses
//     ifstream infile(filename);
//     if (!infile) {
//         fprintf(stderr, "c Error: Could not read from input file %s.\n", filename);
//         exit(1);
//     }
//     char chbuf;
//     char strbuf[1024];
//     infile.get(chbuf);
//     while (chbuf != 'p') {
//         infile.ignore(1000, '\n');
//         infile.get(chbuf);
//         if(!infile) {
//             fprintf(stderr, "c ERROR: Premature EOF reached in %s\n", filename);
//             exit(1);
//         }
//     }

//     int origNumVars, origNumClauses;
//     infile >> strbuf; // "cnf"
//     infile >> origNumVars >> origNumClauses;

//     if (DEB) printf("c Orignal number of varibales is %d, number of clauses is %d \n", origNumVars, origNumClauses);

//     if (DEB) printf("c run SatELite as pre-processor ... \n");
//     int returnVal;
//     if (DEB) printf("c Input file is: %s. Output file is %s\n", filename, outfile);
    // returnVal = SolverSatelite -> execute(filename, 1200);
//   if (r eturnVal==10 || returnVal==20) {
// if (DEB)
//       printf("c This instance is solved by pre-processor with %d!\n", returnVal);
//       doComp=false;
//       }

//   SolverSatelite->cleanup();
    SATinstance* sat = new SATinstance(filename); 
    // SATinstance* sat = new SATinstance(outfile); 
    
    return 0;
}
