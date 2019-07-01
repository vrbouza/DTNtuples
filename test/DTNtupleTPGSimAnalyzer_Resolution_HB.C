#include "DTNtupleTPGSimAnalyzer.h"

#include"TMath.h"

DTNtupleTPGSimAnalyzer::DTNtupleTPGSimAnalyzer(const TString & inFileName,
					       const TString & outFileName) :
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
  for (Long64_t jentry=0; jentry<nentries;jentry++) 
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

  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh. -2", "Wh. -1", "Wh. 0", "Wh. +1", "Wh. +2"};
  std::vector<std::string> secTags    = { "Sec. 1", "Sec. 2", "Sec. 3", "Sec. 4", "Sec. 5", "Sec. 6", "Sec. 7", "Sec. 8","Sec. 9","Sec. 10","Sec. 11","Sec. 12","Sec. 13","Sec. 14"};

  
  m_plots["DirRes_P2"] = new TH1F("hDirRes_P2",
				  "DirRes Seg-TP total distribution; |#Delta#phi| (rad); entries",
				  101,-14.5,14.5);

  m_plots["PosRes_P2"] = new TH1F("hPosRes_P2",
				  "PosRes Seg-TP total distribution; |#Delta#phi| (rad); entries",
				  101,-3.5,3.5);


  for (const auto & whTag : whTags){
    m_plots["DirRes_P2" + whTag] = new TH1F(("hDirRes_" + whTag +  "_P2").c_str(),
					    ("DirRes Seg-TP distribution for " + whTag +  "; |#Delta#phi| (rad); entries").c_str(),
					    101,-14.5,14.5);
    m_plots["PosRes_P2" + whTag] = new TH1F(("hPosRes_" + whTag +  "_P2").c_str(),
					    ("PosRes Seg-TP distribution for " + whTag +  "; |#Delta#phi| (rad); entries").c_str(),
					    101,-3.5,3.5);
  }
  
  for (const auto & secTag : secTags){
    m_plots["DirRes_P2" + secTag] = new TH1F(("hDirRes_" + secTag +  "_P2").c_str(),
					     ("DirRes Seg-TP distribution for " + secTag +  "; |#Delta#phi| (rad); entries").c_str(),
					     101,-14.5,14.5);
    m_plots["PosRes_P2" + secTag] = new TH1F(("hPosRes_" + secTag +  "_P2").c_str(),
					     ("PosRes Seg-TP distribution for " + secTag +  "; |#Delta#phi| (rad); entries").c_str(),
					     101,-3.5,3.5);
  }

  for (const auto & chambTag : chambTags){
    m_plots["DirRes_P2" + chambTag] = new TH1F(("hDirRes_" + chambTag +  "_P2").c_str(),
					       ("DirRes Seg-TP distribution for " + chambTag +  "; |#Delta#phi| (rad); entries").c_str(),
					       101,-14.5,14.5);
    m_plots["PosRes_P2" + chambTag] = new TH1F(("hPosRes_" + chambTag +  "_P2").c_str(),
					       ("PosRes Seg-TP distribution for " + chambTag +  "; |#Delta#phi| (rad); entries").c_str(),
					       101,-3.5,3.5);
  }
  
}

void DTNtupleTPGSimAnalyzer::fill()
{
  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh. -2", "Wh. -1", "Wh. 0", "Wh. +1", "Wh. +2"};
  std::vector<std::string> secTags    = { "Sec. 1", "Sec. 2", "Sec. 3", "Sec. 4", "Sec. 5", "Sec. 6", "Sec. 7", "Sec. 8","Sec. 9","Sec. 10","Sec. 11","Sec. 12","Sec. 13","Sec. 14"};

  for (std::size_t iGenPart = 0; iGenPart < gen_nGenParts; ++iGenPart)
    {
      if (std::abs(gen_pdgId->at(iGenPart)) != 13 ||
	  gen_pt->at(iGenPart) < m_minMuPt)
	continue;

      // CB this should not be a vector ...

      std::vector<std::size_t> bestSegIndex = { 999, 999, 999, 999 };
      std::vector<Int_t> bestSegNHits = { 0, 0, 0, 0 };


      for (std::size_t iSeg = 0; iSeg < seg_nSegments; ++iSeg)
	{
	  Int_t segSt  = seg_station->at(iSeg);	  
	  Int_t segNHits = seg_phi_nHits->at(iSeg);

	  Double_t muSegDPhi = std::abs(acos(cos(gen_phi->at(iGenPart) - seg_posGlb_phi->at(iSeg))));
	  Double_t muSegDEta = std::abs(gen_eta->at(iGenPart) - seg_posGlb_eta->at(iSeg));
	  
	  if ( muSegDPhi < m_maxMuSegDPhi && 
	       muSegDEta < m_maxMuSegDEta && 
	       segNHits >= m_minSegHits &&
	       segNHits >= bestSegNHits.at(segSt - 1))
	    {
	      bestSegNHits[segSt - 1] = segNHits;
	      bestSegIndex[segSt - 1] = iSeg;
	      
	    }
	  
	}

      for (const auto & iSeg : bestSegIndex)
	{
	  if (iSeg == 999)
	    continue;
	  

	  Int_t segWh  = seg_wheel->at(iSeg);
	  Int_t segSec = seg_sector->at(iSeg);
	  Int_t segSt  = seg_station->at(iSeg);

	  std::string chambTag = chambTags.at(segSt - 1);
	  std::string whTag    = whTags.at(segWh+2);
	  std::string secTag   = secTags.at(segSec-1);
	  
	  int bestTP = -1; 
	  Double_t bestSegTrigHBDPhi = 1000;
	  for (std::size_t iTrigHB = 0; iTrigHB < ph2TpgPhiEmuHb_nTrigs; ++iTrigHB){
	    
	    Int_t trigHBWh  = ph2TpgPhiEmuHb_wheel->at(iTrigHB);
	    Int_t trigHBSec = ph2TpgPhiEmuHb_sector->at(iTrigHB);
	    Int_t trigHBSt  = ph2TpgPhiEmuHb_station->at(iTrigHB);
	    Int_t trigHBBX  = ph2TpgPhiEmuHb_BX->at(iTrigHB);
	    
	    if (segWh  == trigHBWh && segSec == trigHBSec &&  segSt  == trigHBSt){
	      Double_t trigGlbPhi = trigPhiInRad(ph2TpgPhiEmuHb_phi->at(iTrigHB),trigHBSec);
	      Double_t segTrigHBDPhi = std::abs(acos(cos(seg_posGlb_phi->at(iSeg) - trigGlbPhi)));
	      if (segTrigHBDPhi < m_maxSegTrigDPhi && trigHBBX==20 &&  bestSegTrigHBDPhi > segTrigHBDPhi){
		bestTP = iTrigHB;
		bestSegTrigHBDPhi = segTrigHBDPhi;
	      }
	    }
	  }



	  if (bestTP > -1){
	    Double_t segLocalHBDPhi = TMath::ATan ( ( seg_dirLoc_x->at(iSeg) / seg_dirLoc_z->at(iSeg)) ) - 2*TMath::Pi()* ph2TpgPhiEmuHb_dirLoc_phi->at(bestTP) /360; 
	    m_plots["DirRes_P2"]->Fill( segLocalHBDPhi );
	    m_plots["DirRes_P2" + whTag]   ->Fill( segLocalHBDPhi );
	    m_plots["DirRes_P2" + secTag]  ->Fill( segLocalHBDPhi );
	    m_plots["DirRes_P2" + chambTag]->Fill( segLocalHBDPhi );

	    m_plots["PosRes_P2"]           ->Fill( bestSegTrigHBDPhi );
	    m_plots["PosRes_P2" + whTag]   ->Fill( bestSegTrigHBDPhi );
	    m_plots["PosRes_P2" + secTag]  ->Fill( bestSegTrigHBDPhi );
	    m_plots["PosRes_P2" + chambTag]->Fill( bestSegTrigHBDPhi );
	    
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
