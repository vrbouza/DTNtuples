# -*- coding: utf-8 -*-
import ROOT as r

r.gROOT.SetBatch(True)

res = r.TFile.Open('results.root')
c = r.TCanvas()
for plot in ['hPhiRes_%s_Sec.12_P2','hPhiRes_P2_%s','hPhiRes_%s_MB2_P2','hPhiRes_%s_Wh.0_P2','hTanPsiRes_P2_%s','hTanPsiRes_%s_Sec.12_P2','hTanPsiRes_%s_MB2_P2','hTanPsiRes_%s_Wh.0_P2','hTimeRes_%s_Sec.12_P2','hTimeRes_%s_MB2_P2','hTimeRes_%s_Wh.0_P2','hTimeRes_P2_%s','hxRes_%s_Sec.12_P2','hxRes_%s_MB2_P2','hxRes_%s_Wh.0_P2','hxRes_P2_%s']:
    hb = res.Get(plot%'HB')
    am = res.Get(plot%'AM')
    am.SetLineColor(r.kRed)
    
    hb.Draw()
    am.Draw('same')
    c.SetLogy()
    c.SaveAs("~vrbouza/www/Miscelánea/2019_07_11_ejsplots/" + plot%'comparison' + '.png')
    c.SaveAs("~vrbouza/www/Miscelánea/2019_07_11_ejsplots/" + plot%'comparison' + '.pdf')
c.Close()
del c
c = r.TCanvas()
for plot in ['PhiRes_%s_Res_perChamb', 'PhiRes_%s_Res_perSec', 'PhiRes_%s_Res_perWheel', 'TanPsiRes_%s_Res_perChamb', 'TanPsiRes_%s_Res_perSec', 'TanPsiRes_%s_Res_perWheel', 'TimeRes_%s_Res_perChamb', 'TimeRes_%s_Res_perSec', 'TimeRes_%s_Res_perWheel', 'xRes_%s_Res_perChamb', 'xRes_%s_Res_perSec', 'xRes_%s_Res_perWheel']:
    hb = res.Get(plot%'HB')
    am = res.Get(plot%'AM')
    am.SetLineColor(r.kRed)

    hb.GetYaxis().SetRangeUser(0, max([hb.GetMaximum(), am.GetMaximum()]) + max([hb.GetMaximum(), am.GetMaximum()]) * 0.1)
    hb.Draw()
    am.Draw('same')
    c.SaveAs("~vrbouza/www/Miscelánea/2019_07_11_ejsplots/" + plot%'comparison' + '.png')
    c.SaveAs("~vrbouza/www/Miscelánea/2019_07_11_ejsplots/" + plot%'comparison' + '.pdf')
res.Close()
