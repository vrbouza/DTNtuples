#include "DTNtupleTPGSimAnalyzer.h"


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
    Double_t limdir   = 0.15; Double_t limpos   = 0.005; Double_t limtime  = 5;
    UShort_t nbinsdir = 101;  UShort_t nbinspos = 101;   UShort_t nbinstim = 11;
    m_plots["DirRes_P2" + algo] = new TH1F(("hDirRes_P2"+ algo).c_str() ,
            "DirRes Seg-TP total distribution; #Delta#phi (rad); entries",
            nbinsdir,-limdir,+limdir);
    m_plots["PosRes_P2" + algo] = new TH1F(("hPosRes_P2"+ algo).c_str(),
            "PosRes Seg-TP total distribution; #Delta#phi (rad); entries",
            nbinspos,-limpos,+limpos);
    m_plots["TimRes_P2" + algo] = new TH1S(("hTimRes_P2"+ algo).c_str(),
            "TimRes Seg-TP total distribution; #Delta t (ns); entries",
            nbinstim,-limtime,+limtime);

    for (const auto & whTag : whTags)
    {
      m_plots["DirRes_P2" + algo + whTag] = new TH1F(("hDirRes" + algo +"_" + whTag +  "_P2").c_str(),
                ("DirRes Seg-TP distribution for " + whTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinsdir,-limdir,+limdir);
      m_plots["PosRes_P2" + algo + whTag] = new TH1F(("hPosRes" + algo  +"_" + whTag +  "_P2").c_str(),
                ("PosRes Seg-TP distribution for " + whTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinspos,-limpos,+limpos);
      m_plots["TimRes_P2" + algo + whTag] = new TH1S(("hTimRes" + algo  +"_" + whTag +  "_P2").c_str(),
                ("TimRes Seg-TP distribution for " + whTag +  "; #Delta t (ns); entries").c_str(),
                nbinstim,-limtime,+limtime);
    }

    for (const auto & secTag : secTags)
    {
      m_plots["DirRes_P2" + algo + secTag] = new TH1F(("hDirRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("DirRes Seg-TP distribution for " + secTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinsdir,-limdir,+limdir);
      m_plots["PosRes_P2" + algo + secTag] = new TH1F(("hPosRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("PosRes Seg-TP distribution for " + secTag +  "; #Delta#phi (rad); entries").c_str(),
                nbinspos,-limpos,+limpos);
      m_plots["TimRes_P2" + algo + secTag] = new TH1S(("hTimRes" + algo  +"_" + secTag +  "_P2").c_str(),
                ("TimRes Seg-TP distribution for " + secTag +  "; #Delta t (ns); entries").c_str(),
                nbinstim,-limtime,+limtime);
    }

    for (const auto & chambTag : chambTags)
    {
      m_plots["DirRes_P2" + algo + chambTag] = new TH1F(("hDirRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("DirRes Seg-TP distribution for " + chambTag +  "; #Delta#phi (rad); entries").c_str(),
            nbinsdir,-limdir,+limdir);
      m_plots["PosRes_P2" + algo + chambTag] = new TH1F(("hPosRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("PosRes Seg-TP distribution for " + chambTag +  "; #Delta#phi (rad); entries").c_str(),
            nbinspos,-limpos,+limpos);
      m_plots["TimRes_P2" + algo + chambTag] = new TH1S(("hTimRes" + algo  +"_" + chambTag +  "_P2").c_str(),
            ("TimRes Seg-TP distribution for " + chambTag +  "; #Delta t (ns); entries").c_str(),
            nbinstim,-limtime,+limtime);
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
          if (segTrigHBDPhi < m_maxSegTrigDPhi &&  bestSegTrigHBDPhi > segTrigHBDPhi)
          {
            bestTPHB          = iTrigHB;
            bestSegTrigHBDPhi = segTrigHBDPhi;
            bestHBDPhi        = finalHBDPhi + ((finalHBDPhi > TMath::Pi()) ? -2*TMath::Pi() : 0) +  ((finalHBDPhi < -TMath::Pi()) ? 2*TMath::Pi() : 0);
	  } 
        }
      }

      if (bestTPHB > -1)
      {
        // Slope
        Double_t segLocalHBDPhi = TMath::ATan ( ( seg_dirLoc_x->at(iSeg) / seg_dirLoc_z->at(iSeg)) ) - 2*TMath::Pi()* ph2TpgPhiEmuHb_dirLoc_phi->at(bestTPHB) /360;
        m_plots["DirRes_P2_HB"]           ->Fill( segLocalHBDPhi );
        m_plots["DirRes_P2_HB" + whTag]   ->Fill( segLocalHBDPhi );
        m_plots["DirRes_P2_HB" + secTag]  ->Fill( segLocalHBDPhi );
        m_plots["DirRes_P2_HB" + chambTag]->Fill( segLocalHBDPhi );

        // DPhi
        m_plots["PosRes_P2_HB"]           ->Fill( bestHBDPhi );
        m_plots["PosRes_P2_HB" + whTag]   ->Fill( bestHBDPhi );
        m_plots["PosRes_P2_HB" + secTag]  ->Fill( bestHBDPhi );
        m_plots["PosRes_P2_HB" + chambTag]->Fill( bestHBDPhi );

        // Time
        if (seg_phi_t0->at(iSeg) > -500)
        {
          Short_t segLocalHBDtime = ((Short_t) (seg_phi_t0->at(iSeg) / 10 )) - (ph2TpgPhiEmuHb_BX->at(bestTPHB) - 20);

          m_plots["TimRes_P2_HB"]           ->Fill( segLocalHBDtime );
          m_plots["TimRes_P2_HB" + whTag]   ->Fill( segLocalHBDtime );
          m_plots["TimRes_P2_HB" + secTag]  ->Fill( segLocalHBDtime );
          m_plots["TimRes_P2_HB" + chambTag]->Fill( segLocalHBDtime );
        }
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
            bestAMDPhi        = finalAMDPhi  + ((finalAMDPhi > TMath::Pi()) ? -2*TMath::Pi() : 0) +  ((finalAMDPhi < -TMath::Pi()) ? 2*TMath::Pi() : 0);
          }
        }
      }

      if (bestTPAM > -1)
      {
        // Slope
        Double_t segLocalAMDPhi  = TMath::ATan ( ( seg_dirLoc_x->at(iSeg) / seg_dirLoc_z->at(iSeg)) ) - TMath::TwoPi() * ph2TpgPhiEmuAm_dirLoc_phi->at(bestTPAM) / 360;
        m_plots["DirRes_P2_AM"]           ->Fill( segLocalAMDPhi );
        m_plots["DirRes_P2_AM" + whTag]   ->Fill( segLocalAMDPhi );
        m_plots["DirRes_P2_AM" + secTag]  ->Fill( segLocalAMDPhi );
        m_plots["DirRes_P2_AM" + chambTag]->Fill( segLocalAMDPhi );

        // DPhi
        m_plots["PosRes_P2_AM"]           ->Fill( bestAMDPhi );
        m_plots["PosRes_P2_AM" + whTag]   ->Fill( bestAMDPhi );
        m_plots["PosRes_P2_AM" + secTag]  ->Fill( bestAMDPhi );
        m_plots["PosRes_P2_AM" + chambTag]->Fill( bestAMDPhi );

        // Time
        if (seg_phi_t0->at(iSeg) > -500)
        {
          Short_t segLocalAMDtime = ((Short_t) (seg_phi_t0->at(iSeg) / 10 )) - ph2TpgPhiEmuAm_BX->at(bestTPAM);

          // Time
          m_plots["TimRes_P2_AM"]           ->Fill( segLocalAMDtime );
          m_plots["TimRes_P2_AM" + whTag]   ->Fill( segLocalAMDtime );
          m_plots["TimRes_P2_AM" + secTag]  ->Fill( segLocalAMDtime );
          m_plots["TimRes_P2_AM" + chambTag]->Fill( segLocalAMDtime );
        }
      }
    }
  }
}



void DTNtupleTPGSimAnalyzer::endJob()
{

  m_outFile.cd();

  m_outFile.Write();
  m_outFile.Close();

}



Double_t DTNtupleTPGSimAnalyzer::trigPhiInRad(Double_t trigPhi, Int_t sector)
{
  return trigPhi / 65536. * 0.8 + TMath::Pi() / 6 * (sector - 1);
}
