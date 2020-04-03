#include "TROOT.h"

void loadTPGSimAnalysis_eff()
{
  gROOT->ProcessLine(".L DTNtupleBaseAnalyzer.C++");
  gROOT->ProcessLine(".L DTNtupleTPGSimAnalyzer_Efficiency.C++");
}
