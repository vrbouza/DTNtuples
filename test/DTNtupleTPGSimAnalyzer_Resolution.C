#include "DTNtupleTPGSimAnalyzer.h"
#include "TVector2.h"
#include "TF1.h"

DTNtupleTPGSimAnalyzer::DTNtupleTPGSimAnalyzer(const TString & inFileName,
                                               const TString & outFileName):
  m_outFile(outFileName,"RECREATE"), DTNtupleBaseAnalyzer(inFileName)
{

  m_minMuPt = 20;

  m_maxMuSegDPhi = 0.2;
  m_maxMuSegDEta = 0.3;

  m_minSegHits = 4;

  m_maxSegTrigDPhi = 0.1;
  m_maxMuTrigDPhi  = 0.2;

}



DTNtupleTPGSimAnalyzer::~DTNtupleTPGSimAnalyzer()
{

}



void DTNtupleTPGSimAnalyzer::Loop()
{

  book();

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntries();

  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
    {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEvent(jentry);   nbytes += nb;

      if(jentry % 100 == 0)
  std::cout << "[DTNtupleTPGSimAnalyzer::Loop] processed : "
      << jentry << " entries\r" << std::flush;

      fill();

    }

  std::cout << std::endl;

  endJob();
}



void DTNtupleTPGSimAnalyzer::book()
{
  m_outFile.cd();

  std::vector<std::string> algoTag   = {"_AM","_HB" };
  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh.-2", "Wh.-1", "Wh.0", "Wh.+1", "Wh.+2"};
  std::vector<std::string> secTags   = { "Sec.1", "Sec.2", "Sec.3", "Sec.4", "Sec.5", "Sec.6", "Sec.7", "Sec.8","Sec.9","Sec.10","Sec.11","Sec.12","Sec.13","Sec.14"};

  for (const auto & algo : algoTag)
  {
    Double_t limtanpsi   = 0.1; Double_t limphi   = 0.005; Double_t limtime  = 5;   Double_t limx   = 0.2;
    UShort_t nbinstanpsi = 200; UShort_t nbinsphi = 150;   UShort_t nbinstime = 11; UShort_t nbinsx = 101;
    m_plots["TanPsiRes_P2" + algo] = new TH1F(("hTanPsiRes_P2"+ algo).c_str() ,
            "TanPsiRes Seg-TP total distribution; #Delta tan(#psi) (adim.); entries",
            nbinstanpsi,-limtanpsi,+limtanpsi);
    m_plots["PhiRes_P2" + algo] = new TH1F(("hPhiRes_P2"+ algo).c_str(),
            "PhiRes Seg-TP total distribution; #Delta#phi (rad); entries",
            nbinsphi,-limphi,+limphi);
    m_plots["TimeRes_P2" + algo] = new TH1S(("hTimeRes_P2"+ algo).c_str(),
            "TimeRes Seg-TP total distribution; #Delta BX (adim.); entries",
            nbinstime,-limtime,+limtime);
    m_plots["xRes_P2" + algo] = new TH1F(("hxRes_P2"+ algo).c_str(),
            "xRes Seg-TP total distribution; #Delta x (cm); entries",
            nbinsx,-limx,+limx);

    for (const auto & whTag : whTags)
    {
      m_plots["TanPsiRes_P2" + algo + whTag] = new TH1F(("hTanPsiRes" + algo +"_" + whTag +  "_P2").c_str(),
                ("TanPsiRes Seg-TP distribution for " + whTag +  "; #Delta tan(#psi) (adim.); entries").c_str(),
                nbinstanpsi,-limtanpsi,+limtanpsi);
      m_plots["PhiRes_P2" + algo + whTag] = new TH1F(("hPhiRes" + algo  +"_" + whTag +  "_P2").c_str(),
                ("PhiRes Seg-TP distribution for " + whTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinsphi,-limphi,+limphi);
      m_plots["TimeRes_P2" + algo + whTag] = new TH1S(("hTimeRes" + algo  +"_" + whTag +  "_P2").c_str(),
                ("TimeRes Seg-TP distribution for " + whTag +  "; #Delta BX (adim.); entries").c_str(),
                nbinstime,-limtime,+limtime);
      m_plots["xRes_P2" + algo + whTag] = new TH1F(("hxRes" + algo  +"_" + whTag +  "_P2").c_str(),
                ("xRes Seg-TP distribution for " + whTag +  "; #Delta x (cm); entries").c_str(),
                nbinsx,-limx,+limx);
    }

    for (const auto & secTag : secTags)
    {
      m_plots["TanPsiRes_P2" + algo + secTag] = new TH1F(("hTanPsiRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("TanPsiRes Seg-TP distribution for " + secTag +  "; #Delta tan(#psi) (adim.); entries").c_str(),
                nbinstanpsi,-limtanpsi,+limtanpsi);
      m_plots["PhiRes_P2" + algo + secTag] = new TH1F(("hPhiRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("PhiRes Seg-TP distribution for " + secTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinsphi,-limphi,+limphi);
      m_plots["TimeRes_P2" + algo + secTag] = new TH1S(("hTimeRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("TimeRes Seg-TP distribution for " + secTag +  "; #Delta BX (adim.); entries").c_str(),
                nbinstime,-limtime,+limtime);
      m_plots["xRes_P2" + algo + secTag] = new TH1F(("hxRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("xRes Seg-TP distribution for " + secTag +  "; #Delta x (cm); entries").c_str(),
                nbinsx,-limx,+limx);
    }

    for (const auto & chambTag : chambTags)
    {
      m_plots["TanPsiRes_P2" + algo + chambTag] = new TH1F(("hTanPsiRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("TanPsiRes Seg-TP distribution for " + chambTag +  "; #Delta tan(#psi) (adim.); entries").c_str(),
            nbinstanpsi,-limtanpsi,+limtanpsi);
      m_plots["PhiRes_P2" + algo + chambTag] = new TH1F(("hPhiRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("PhiRes Seg-TP distribution for " + chambTag +  "; #Delta#phi (rad); entries").c_str(),
            nbinsphi,-limphi,+limphi);
      m_plots["TimeRes_P2" + algo + chambTag] = new TH1S(("hTimeRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("TimeRes Seg-TP distribution for " + chambTag +  "; #Delta BX (adim.); entries").c_str(),
            nbinstime,-limtime,+limtime);
      m_plots["xRes_P2" + algo + chambTag] = new TH1F(("hxRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("xRes Seg-TP distribution for " + chambTag +  "; #Delta x (cm); entries").c_str(),
            nbinsx,-limx,+limx);
    }
  }
}



void DTNtupleTPGSimAnalyzer::fill()
{
  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh.-2", "Wh.-1", "Wh.0", "Wh.+1", "Wh.+2"};
  std::vector<std::string> secTags   = { "Sec.1", "Sec.2", "Sec.3", "Sec.4", "Sec.5", "Sec.6", "Sec.7", "Sec.8","Sec.9","Sec.10","Sec.11","Sec.12","Sec.13","Sec.14"};

  for (std::size_t iGenPart = 0; iGenPart < gen_nGenParts; ++iGenPart)
  {
    if (std::abs(gen_pdgId->at(iGenPart)) != 13 || gen_pt->at(iGenPart) < m_minMuPt) continue;

    // CB this should not be a vector ...
    std::vector<std::size_t> bestSegIndex = { 999, 999, 999, 999 };
    std::vector<Int_t> bestSegNHits       = { 0, 0, 0, 0 };


    for (std::size_t iSeg = 0; iSeg < seg_nSegments; ++iSeg)
    {
      Int_t segSt    = seg_station->at(iSeg);
      Int_t segNHits = seg_phi_nHits->at(iSeg);

      Double_t muSegDPhi = std::abs(acos(cos(gen_phi->at(iGenPart) - seg_posGlb_phi->at(iSeg))));
      Double_t muSegDEta = std::abs(gen_eta->at(iGenPart) - seg_posGlb_eta->at(iSeg));

      if (muSegDPhi < m_maxMuSegDPhi &&
          muSegDEta < m_maxMuSegDEta &&
          segNHits >= m_minSegHits &&
          segNHits >= bestSegNHits.at(segSt - 1))
      {
        bestSegNHits[segSt - 1] = segNHits;
        bestSegIndex[segSt - 1] = iSeg;
      }
    }


    // ==================== VARIABLES FOR THE HOUGH TRANSFORM BASED ALGORITHM
    for (const auto & iSeg : bestSegIndex)
    {
      if (iSeg == 999) continue;

      Int_t segWh  = seg_wheel->at(iSeg);
      Int_t segSec = seg_sector->at(iSeg);
      Int_t segSt  = seg_station->at(iSeg);

      std::string chambTag = chambTags.at(segSt - 1);
      std::string whTag    = whTags.at(segWh+2);
      std::string secTag   = secTags.at(segSec-1);

      int bestTPHB = -1;
      Double_t bestSegTrigHBDPhi = 1000;
      Double_t bestHBDPhi = 0;
      for (std::size_t iTrigHB = 0; iTrigHB < ph2TpgPhiEmuHb_nTrigs; ++iTrigHB)
      {
        Int_t trigHBWh  = ph2TpgPhiEmuHb_wheel->at(iTrigHB);
        Int_t trigHBSec = ph2TpgPhiEmuHb_sector->at(iTrigHB);
        Int_t trigHBSt  = ph2TpgPhiEmuHb_station->at(iTrigHB);
        Int_t trigHBBX  = ph2TpgPhiEmuHb_BX->at(iTrigHB);

        if (segWh  == trigHBWh && segSec == trigHBSec &&  segSt  == trigHBSt)
        {
          Double_t trigGlbPhi    = trigPhiInRad(ph2TpgPhiEmuHb_phi->at(iTrigHB),trigHBSec);
          Double_t finalHBDPhi   = seg_posGlb_phi->at(iSeg) - trigGlbPhi;
          Double_t segTrigHBDPhi = abs(acos(cos(finalHBDPhi)));
//           if (segTrigHBDPhi < m_maxSegTrigDPhi && trigHBBX == 20 &&  bestSegTrigHBDPhi > segTrigHBDPhi)
          if (segTrigHBDPhi < m_maxSegTrigDPhi && bestSegTrigHBDPhi > segTrigHBDPhi)
          {
            bestTPHB          = iTrigHB;
            bestSegTrigHBDPhi = segTrigHBDPhi;
            bestHBDPhi        = TVector2::Phi_mpi_pi(finalHBDPhi);
          }
        }
      }

      if (bestTPHB > -1)
      {
        // TanPsi
        Double_t segLocalHBDtanpsi = (seg_dirLoc_x->at(iSeg) / seg_dirLoc_z->at(iSeg)) - TMath::TwoPi() * ph2TpgPhiEmuHb_dirLoc_phi->at(bestTPHB) / 360;
        m_plots["TanPsiRes_P2_HB"]           ->Fill( segLocalHBDtanpsi );
        m_plots["TanPsiRes_P2_HB" + whTag]   ->Fill( segLocalHBDtanpsi );
        m_plots["TanPsiRes_P2_HB" + secTag]  ->Fill( segLocalHBDtanpsi );
        m_plots["TanPsiRes_P2_HB" + chambTag]->Fill( segLocalHBDtanpsi );

        // Phi
        m_plots["PhiRes_P2_HB"]           ->Fill( bestHBDPhi );
        m_plots["PhiRes_P2_HB" + whTag]   ->Fill( bestHBDPhi );
        m_plots["PhiRes_P2_HB" + secTag]  ->Fill( bestHBDPhi );
        m_plots["PhiRes_P2_HB" + chambTag]->Fill( bestHBDPhi );

        // Time
        if (seg_phi_t0->at(iSeg) > -500)
        {
          Short_t segLocalHBDtime = ((Short_t) (seg_phi_t0->at(iSeg) / 10 )) - (ph2TpgPhiEmuHb_BX->at(bestTPHB) - 20);

          m_plots["TimeRes_P2_HB"]           ->Fill( segLocalHBDtime );
          m_plots["TimeRes_P2_HB" + whTag]   ->Fill( segLocalHBDtime );
          m_plots["TimeRes_P2_HB" + secTag]  ->Fill( segLocalHBDtime );
          m_plots["TimeRes_P2_HB" + chambTag]->Fill( segLocalHBDtime );
        }

        // x
        Double_t segLocalHBDx = 0;
        if ((ph2TpgPhiEmuHb_quality->at(bestTPHB) == 6) || (ph2TpgPhiEmuHb_quality->at(bestTPHB) == 8) || (ph2TpgPhiEmuHb_quality->at(bestTPHB) == 9))
        {
          segLocalHBDx = seg_posLoc_x_midPlane->at(iSeg) - ph2TpgPhiEmuHb_posLoc_x->at(bestTPHB);
        }
        else if (ph2TpgPhiEmuHb_superLayer->at(bestTPHB) == 1) segLocalHBDx = seg_posLoc_x_SL1->at(iSeg) - ph2TpgPhiEmuHb_posLoc_x->at(bestTPHB);
        else                                                   segLocalHBDx = seg_posLoc_x_SL3->at(iSeg) - ph2TpgPhiEmuHb_posLoc_x->at(bestTPHB);
        m_plots["xRes_P2_HB"]           ->Fill( segLocalHBDx );
        m_plots["xRes_P2_HB" + whTag]   ->Fill( segLocalHBDx );
        m_plots["xRes_P2_HB" + secTag]  ->Fill( segLocalHBDx );
        m_plots["xRes_P2_HB" + chambTag]->Fill( segLocalHBDx );
      }


      // ==================== VARIABLES FOR THE ANALYTICAL METHOD ALGORITHM
      int bestTPAM = -1;
      Double_t bestSegTrigAMDPhi = 1000;
      Double_t bestAMDPhi = 0;
      for (std::size_t iTrigAM = 0; iTrigAM < ph2TpgPhiEmuAm_nTrigs; ++iTrigAM)
      {
        Int_t trigAMWh  = ph2TpgPhiEmuAm_wheel->at(iTrigAM);
        Int_t trigAMSec = ph2TpgPhiEmuAm_sector->at(iTrigAM);
        Int_t trigAMSt  = ph2TpgPhiEmuAm_station->at(iTrigAM);
        Int_t trigAMBX  = ph2TpgPhiEmuAm_BX->at(iTrigAM);

        if (segWh  == trigAMWh && segSec == trigAMSec &&  segSt  == trigAMSt)
        {
          Double_t trigGlbPhi    = trigPhiInRad(ph2TpgPhiEmuAm_phi->at(iTrigAM),trigAMSec);
          Double_t finalAMDPhi   = seg_posGlb_phi->at(iSeg) - trigGlbPhi;
          Double_t segTrigAMDPhi = abs(acos(cos(finalAMDPhi)));

//           if ((segTrigAMDPhi < m_maxSegTrigDPhi) && (trigAMBX == 0) && (bestSegTrigAMDPhi > segTrigAMDPhi))
          if ((segTrigAMDPhi < m_maxSegTrigDPhi) && (bestSegTrigAMDPhi > segTrigAMDPhi))
          {
            bestTPAM          = iTrigAM;
            bestSegTrigAMDPhi = segTrigAMDPhi;
            bestAMDPhi        = TVector2::Phi_mpi_pi(finalAMDPhi);
          }
        }
      }

      if (bestTPAM > -1)
      {
        // TanPsi
        Double_t segLocalAMDtanpsi = (seg_dirLoc_x->at(iSeg) / seg_dirLoc_z->at(iSeg)) - TMath::TwoPi() * ph2TpgPhiEmuAm_dirLoc_phi->at(bestTPAM) / 360;
        m_plots["TanPsiRes_P2_AM"]           ->Fill( segLocalAMDtanpsi );
        m_plots["TanPsiRes_P2_AM" + whTag]   ->Fill( segLocalAMDtanpsi );
        m_plots["TanPsiRes_P2_AM" + secTag]  ->Fill( segLocalAMDtanpsi );
        m_plots["TanPsiRes_P2_AM" + chambTag]->Fill( segLocalAMDtanpsi );

        // Phi
        m_plots["PhiRes_P2_AM"]           ->Fill( bestAMDPhi );
        m_plots["PhiRes_P2_AM" + whTag]   ->Fill( bestAMDPhi );
        m_plots["PhiRes_P2_AM" + secTag]  ->Fill( bestAMDPhi );
        m_plots["PhiRes_P2_AM" + chambTag]->Fill( bestAMDPhi );

        // Time
        if (seg_phi_t0->at(iSeg) > -500)
        {
          Short_t segLocalAMDtime = ((Short_t) (seg_phi_t0->at(iSeg) / 10 )) - ph2TpgPhiEmuAm_BX->at(bestTPAM);

          // Time
          m_plots["TimeRes_P2_AM"]           ->Fill( segLocalAMDtime );
          m_plots["TimeRes_P2_AM" + whTag]   ->Fill( segLocalAMDtime );
          m_plots["TimeRes_P2_AM" + secTag]  ->Fill( segLocalAMDtime );
          m_plots["TimeRes_P2_AM" + chambTag]->Fill( segLocalAMDtime );
        }

        // x
        Double_t segLocalAMDx = 0;
        if ((ph2TpgPhiEmuAm_quality->at(bestTPAM) == 6) || (ph2TpgPhiEmuAm_quality->at(bestTPAM) == 8) || (ph2TpgPhiEmuAm_quality->at(bestTPAM) == 9))
        {
          segLocalAMDx = seg_posLoc_x_midPlane->at(iSeg) - ph2TpgPhiEmuAm_posLoc_x->at(bestTPAM);
        }
        else if (ph2TpgPhiEmuAm_superLayer->at(bestTPAM) == 1) segLocalAMDx = seg_posLoc_x_SL1->at(iSeg) - ph2TpgPhiEmuAm_posLoc_x->at(bestTPAM);
        else                                                   segLocalAMDx = seg_posLoc_x_SL3->at(iSeg) - ph2TpgPhiEmuAm_posLoc_x->at(bestTPAM);
        m_plots["xRes_P2_AM"]           ->Fill( segLocalAMDx );
        m_plots["xRes_P2_AM" + whTag]   ->Fill( segLocalAMDx );
        m_plots["xRes_P2_AM" + secTag]  ->Fill( segLocalAMDx );
        m_plots["xRes_P2_AM" + chambTag]->Fill( segLocalAMDx );
      }
    }
  }
}



TH1F* DTNtupleTPGSimAnalyzer::makeHistoPer( std::string mag, std::string suffix, vector<std::string> tags, std::string algo)
{
  TH1F* ret = new TH1F((mag + "_" + algo + suffix).c_str(),"",
            tags.size(), -0.5,-0.5+tags.size());
  for (unsigned int i = 0; i < tags.size(); ++i){
    ret->GetXaxis()->SetBinLabel(i+1, tags[i].c_str());

    if (m_plots[mag + "_P2_" + algo + tags[i]]->Integral()) {

      if      (mag == "PhiRes")    m_plots[mag + "_P2_" + algo + tags[i]]->Fit("gaus","SQ", "", -0.0005, 0.0005);
      else if (mag == "TanPsiRes") m_plots[mag + "_P2_" + algo + tags[i]]->Fit("gaus","SQ", "", -0.01, 0.01);
      else                         m_plots[mag + "_P2_" + algo + tags[i]]->Fit("gaus","SQ");

      ret->SetBinContent(i+1, m_plots[mag + "_P2_" + algo + tags[i]]->GetFunction("gaus")->GetParameter(2));
    }
  }
  return ret;
}



void DTNtupleTPGSimAnalyzer::endJob()
{
  // make the fits
  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh.-2", "Wh.-1", "Wh.0", "Wh.+1", "Wh.+2"};
  std::vector<std::string> secTags   = { "Sec.1", "Sec.2", "Sec.3", "Sec.4", "Sec.5", "Sec.6", "Sec.7", "Sec.8","Sec.9","Sec.10","Sec.11","Sec.12","Sec.13","Sec.14"};
  std::vector<std::string> magnitudes = { "TimeRes", "PhiRes", "TanPsiRes", "xRes"};
  std::vector<std::string> algotag    = { "AM", "HB" };
  for (const auto & mag : magnitudes)
  {
    for (const auto & algo : algotag)
    {
      m_plots[mag + "_" + algo + "_Res_perChamb"] = makeHistoPer( mag, "_Res_perChamb", chambTags, algo);
      m_plots[mag + "_" + algo + "_Res_perWheel"] = makeHistoPer( mag, "_Res_perWheel", whTags   , algo);
      m_plots[mag + "_" + algo + "_Res_perSec"]   = makeHistoPer( mag, "_Res_perSec"  , secTags  , algo);
    }
  }


  m_outFile.cd();

  m_outFile.Write();
  m_outFile.Close();
}



Double_t DTNtupleTPGSimAnalyzer::trigPhiInRad(Double_t trigPhi, Int_t sector)
{
  return trigPhi / 65536. * 0.8 + TMath::Pi() / 6 * (sector - 1);
}
