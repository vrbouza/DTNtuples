#include "TROOT.h"

void loadTPGSimAnalysis()
{
  gROOT->ProcessLine(".L DTNtupleBaseAnalyzer.C++");
  gROOT->ProcessLine(".L DTNtupleTPGSimAnalyzer_Efficiency.C++");
}
