# -*- coding: utf-8 -*-
import ROOT as r

r.gROOT.SetBatch(True)

path = "~vrbouza/www/Miscelánea/2019_07_11_ejsplots/2019_07_16_pruebaplots_shifts/"

res = r.TFile.Open('results.root')
c = r.TCanvas()
for plot in ['hPhiRes_{alg}_{cor}_Sec.12_P2','hPhiRes_P2_{alg}_{cor}','hPhiRes_{alg}_{cor}_MB2_P2','hPhiRes_{alg}_{cor}_Wh.0_P2','hTanPsiRes_P2_{alg}_{cor}','hTanPsiRes_{alg}_{cor}_Sec.12_P2','hTanPsiRes_{alg}_{cor}_MB2_P2','hTanPsiRes_{alg}_{cor}_Wh.0_P2','hTimeRes_{alg}_{cor}_Sec.12_P2','hTimeRes_{alg}_{cor}_MB2_P2','hTimeRes_{alg}_{cor}_Wh.0_P2','hTimeRes_P2_{alg}_{cor}','hxRes_{alg}_{cor}_Sec.12_P2','hxRes_{alg}_{cor}_MB2_P2','hxRes_{alg}_{cor}_Wh.0_P2','hxRes_P2_{alg}_{cor}']:
    for icor in ["Correlated", "Uncorrelated", "All"]:
        hb = res.Get(plot.format(alg = 'HB', cor = icor))
        am = res.Get(plot.format(alg = 'AM', cor = icor))
        am.SetLineColor(r.kRed)
        hb.SetStats(False)
        hb.GetYaxis().SetRangeUser(0, max([hb.GetMaximum(), am.GetMaximum()]) + max([hb.GetMaximum(), am.GetMaximum()]) * 0.1)

        hb.Draw()
        am.Draw('same')
        c.SetLogy()
        c.SaveAs(path + plot.format(alg = 'comparison', cor = icor) + '.png')
        c.SaveAs(path + plot.format(alg = 'comparison', cor = icor) + '.pdf')
c.Close()
del c
c = r.TCanvas()
for plot in ['PhiRes_{alg}_{cor}_Res_perChamb', 'PhiRes_{alg}_{cor}_Res_perSec', 'PhiRes_{alg}_{cor}_Res_perWheel', 'TanPsiRes_{alg}_{cor}_Res_perChamb', 'TanPsiRes_{alg}_{cor}_Res_perSec', 'TanPsiRes_{alg}_{cor}_Res_perWheel', 'TimeRes_{alg}_{cor}_Res_perChamb', 'TimeRes_{alg}_{cor}_Res_perSec', 'TimeRes_{alg}_{cor}_Res_perWheel', 'xRes_{alg}_{cor}_Res_perChamb', 'xRes_{alg}_{cor}_Res_perSec', 'xRes_{alg}_{cor}_Res_perWheel']:
    for icor in ["Correlated", "Uncorrelated", "All"]:
        hb = res.Get(plot.format(alg = 'HB', cor = icor))
        am = res.Get(plot.format(alg = 'AM', cor = icor))
        am.SetLineColor(r.kRed)
        hb.SetStats(False)
        hb.GetYaxis().SetRangeUser(0, max([hb.GetMaximum(), am.GetMaximum()]) + max([hb.GetMaximum(), am.GetMaximum()]) * 0.1)

        hb.Draw()
        am.Draw('same')
        c.SaveAs(path + plot.format(alg = 'comparison', cor = icor) + '.png')
        c.SaveAs(path + plot.format(alg = 'comparison', cor = icor) + '.pdf')
res.Close()
