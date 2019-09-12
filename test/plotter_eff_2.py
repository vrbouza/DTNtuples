# -*- coding: utf-8 -*-
import ROOT as r
from copy import deepcopy
import CMS_lumi
r.gROOT.SetBatch(True)

path = "~sscruz/www/DT_TDR/2019_12_09_plots_eff_shiftsoff_qualities/"
plotscaffold = "hEff_{st}_{al}_{ty}"
savescaffold = "hEff_{pu}"
chambTag = ["MB1", "MB2", "MB3", "MB4"]


def makeresplot(hlist, aged, algo, pued = False, typ=""):
    print "Obtaining intermediate plot for algo", algo, "which is", aged, "aged and considering", pued, "pile-up"
    res = r.TFile.Open("results_eff_" + ((not pued) * "no") + "pu_" + (not aged) * "no" + "age" + typ  +".root")
    hmatched = [res.Get(plotscaffold.format(al = algo, st = chambTag[ich], ty = "matched")) for ich in range(4)]
    htotal   = [res.Get(plotscaffold.format(al = algo, st = chambTag[ich], ty = "total")) for ich in range(4)]

    resplot = r.TH1F("hEff_{al}_{ag}_{pu}{typ}".format(typ=typ,al = algo, ag = (not aged) * "no" + "age", pu = ((not pued) * "no") + "pu"), "", 20, -0.5, 19.5)

    ibin = 1
    for ich in range(4):
        for iwh in range(1, 6):
            resplot.SetBinContent(ibin, hmatched[ich].GetBinContent(iwh) / htotal[ich].GetBinContent(iwh))
            ibin += 1

    hlist.append(deepcopy(resplot))
    res.Close(); del hmatched, htotal, res, resplot
    return


lowlimityaxis  = 0.4
highlimityaxis = 1
markersize     = 1
yaxistitle     = "Efficiency (adim.)"
yaxistitleoffset= 1.5
xaxistitle     = "Wheel"
legxlow        = 0.3075 + 2 * 0.1975
legylow        = 0.7
legxhigh       = 0.9
legyhigh       = 0.9

markertypedir  = {}
markertypedir["AM_age"] = 20
markertypedir["AM_noage"] = 20
markertypedir["AM_agenothreehits"] = 34
markertypedir["AM_noagenothreehits"] = 34

markercolordir  = {}
markercolordir["AM_age"]   = r.kRed
markercolordir["AM_noage"] = r.kBlue
markercolordir["AM_agenothreehits"]   = r.kRed 
markercolordir["AM_noagenothreehits"] = r.kBlue


def combineresplots(hlist, pued = False):
    print "Combining list of plots that has", pued, "pile-up"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()
    leg = r.TLegend(legxlow, legylow, legxhigh, legyhigh)
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    hlist[0].GetYaxis().SetRangeUser(lowlimityaxis, highlimityaxis)
    hlist[0].GetYaxis().SetTitleOffset(yaxistitleoffset)
    hlist[0].GetYaxis().SetTitle(yaxistitle)
    hlist[0].GetXaxis().SetTitle(xaxistitle)
    hlist[0].GetXaxis().SetNdivisions(120)
    ilabel = 1
    for ich in range(4):
        for iwh in range(-2, 3):
            hlist[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1

    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerSize(markersize)
        hlist[iplot].SetMarkerStyle(markertypedir[hlist[iplot].GetName().replace("_nopu","").replace("_pu","").replace("hEff_","")])
        hlist[iplot].SetMarkerColor(markercolordir[hlist[iplot].GetName().replace("_nopu","").replace("_pu","").replace("hEff_","")])
        leg.AddEntry(hlist[iplot], hlist[iplot].GetName().replace("_nopu","").replace("_pu","").replace("hEff_",""), "P")
        hlist[iplot].Draw("P0" + (iplot != 0) * "same")

    leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.20, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    #cmslat = r.TLatex()
    #cmslat.SetTextSize(0.03);
    #cmslat.DrawLatexNDC(0.11, 0.91, "#scale[1.5]{CMS}");
    #cmslat.Draw("same");

    CMS_lumi.lumi_13TeV = ""
    CMS_lumi.extraText  = 'Simulation'
    CMS_lumi.cmsTextSize= 0.5
    CMS_lumi.lumi_sqrtS = ''
    CMS_lumi.CMS_lumi(r.gPad, 0, 0, 0.07)


    #c.SetLogy()
    c.SaveAs(path + savescaffold.format(pu = (not pued) * "no" + "pu") + ".png")
    c.SaveAs(path + savescaffold.format(pu = (not pued) * "no" + "pu") + ".pdf")
    c.SaveAs(path + savescaffold.format(pu = (not pued) * "no" + "pu") + ".root")
    c.Close(); del c
    return


print "\nBeginning plotting\n"
listofplots     = []
puedlistofplots = []

makeresplot(puedlistofplots, False, "AM", True , '')
makeresplot(puedlistofplots, True,  "AM", True , '')
makeresplot(listofplots, False, "AM", False, '')
makeresplot(listofplots, True,  "AM", False, '')
makeresplot(puedlistofplots, False, "AM", True , 'nothreehits')
makeresplot(puedlistofplots, True,  "AM", True , 'nothreehits')
makeresplot(listofplots, False, "AM", False, 'nothreehits')
makeresplot(listofplots, True,  "AM", False, 'nothreehits')


print "\nCombining and saving\n"
combineresplots(listofplots)
combineresplots(puedlistofplots, True)
