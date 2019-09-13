import ROOT as r
r.gROOT.ProcessLine(".x loadTPGSimAnalysis.C")
for pu in 'nopu,pu'.split(','):
    for age in 'age,noage'.split(','):
        for qual in ',nothreehits'.split(','):
            name = '%s_%s'%('nopu' if pu == 'nopu' else 'pu200', age)
            analysis = r.DTNtupleTPGSimAnalyzer("/pool/ciencias/userstorage/sscruz/DT_TDR_12sep/%s.root"%name,"results_eff_%s_%s%s.root"%(pu,age,qual),qual)
            analysis.Loop()
