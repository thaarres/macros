
from optparse import OptionParser
import os,commands, os.path
import sys
from ROOT import *
import math
import time
from array import *
# import CMS_lumi, tdrstyle
import copy
# ---------------------------------------------------------------------------------------------------------------------------
def write(fname, histolist):
    """Write the new histogram to disk"""
    base = fname
    outfname = "/shome/thaarres/EXOVVAnalysisRunII/LimitCode/CMSSW_7_1_5/src/DijetCombineLimitCode/input/" + base + ".root"
    # outfname = base + ".root"
    print "Saving file %s " %outfname
    fout = TFile(outfname,"RECREATE")
    for h in histolist:
      h.Write()
    fout.Close()
# ---------------------------------------------------------------------------------------------------------------------------
argv = sys.argv
parser = OptionParser()   
parser.add_option("-L", "--lumi", dest="lumi", default=12900,
                              help="Set lumi")                                                                                                                                                                                            			      			      			      			      
(opts, args) = parser.parse_args(argv)  

path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/"
rebin = 1
    
# ---------------------------------------------------------------------------------------------------------------------------  

# cmd = "rm /shome/thaarres/EXOVVAnalysisRunII/CMSSW_7_1_5/src/DijetCombineLimitCode/input/*.root"
# print cmd
# os.system(cmd)


gROOT.SetBatch(kTRUE)
      
i =0
histolist = []
for root, _, files in os.walk(path):
  for f in files:
    fullpath = os.path.join(root, f)
    if not fullpath.find("JetHT_VV.root")!=-1:
      continue
    print "Working on  file %s" %fullpath
    if fullpath.find("QCD")!=-1:
      lumi = opts.lumi
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      name += "_" + name1.split("_")[1]
      name += "_SR"
      if fullpath.find("_VV")!=-1: 
        name = "QCD_VV"
    elif fullpath.find("DATA")!=-1:
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      if fullpath.find("_VV")!=-1: 
        name+= "_VV"
      if fullpath.find("SB")!=-1:
        name1 = fullpath.split(".")[1]
        name = name1.split("_")[0]
        name+= "_SB"  
      lumi = 1.
    else:
      name = fullpath.split(".")[1]+'.'+fullpath.split(".")[2]
      name = name.split(".")[0]
      lumi = 1.
    print "Will save to filename %s" %name
    filetmp = TFile.Open(fullpath,"READ") 
    intree = filetmp.Get("tree")
    print "Using lumi = %s" %lumi
    
    histolist=[]

    VVHP = TH1F('DijetMassHighPuriVV','DijetMassHighPuriVV',7000,0,7000)
    WWHP = TH1F('DijetMassHighPuriWW','DijetMassHighPuriWW',7000,0,7000)
    WZHP = TH1F('DijetMassHighPuriWZ','DijetMassHighPuriWZ',7000,0,7000)
    ZZHP = TH1F('DijetMassHighPuriZZ','DijetMassHighPuriZZ',7000,0,7000)
    VVLP = TH1F('DijetMassLowPuriVV','DijetMassLowPuriVV',7000,0,7000)
    WWLP = TH1F('DijetMassLowPuriWW','DijetMassLowPuriWW',7000,0,7000)
    WZLP = TH1F('DijetMassLowPuriWZ','DijetMassLowPuriWZ',7000,0,7000)
    ZZLP = TH1F('DijetMassLowPuriZZ','DijetMassLowPuriZZ',7000,0,7000)
    
    # VVNP = TH1F('DijetMassNoPuriVV','DijetMassNoPuriVV',7000,0,7000)
    # WWNP = TH1F('DijetMassNoPuriWW','DijetMassNoPuriWW',7000,0,7000)
    # WZNP = TH1F('DijetMassNoPuriWZ','DijetMassNoPuriWZ',7000,0,7000)
    # ZZNP = TH1F('DijetMassNoPuriZZ','DijetMassNoPuriZZ',7000,0,7000)

    
    # histolist.append(VVHP)
    histolist.append(WWHP)
    histolist.append(WZHP)
    histolist.append(ZZHP)
    # # histolist.append(VVLP)
    histolist.append(WWLP)
    histolist.append(WZLP)
    histolist.append(ZZLP)
    # histolist.append(VVNP)
    # histolist.append(WWNP)
    # histolist.append(WZNP)
    # histolist.append(ZZNP)
  
    

    for event in intree:
  
      if ( event.MVV < 955.): continue

      if event.jet_puppi_tau2tau1_jet2 <= 0.40 and event.jet_puppi_tau2tau1_jet1 <= 0.40 :
        if (65. <= event.jet_puppi_softdrop_jet1 <= 85. and 65. <= event.jet_puppi_softdrop_jet2 <= 85.) :
           WWHP.Fill(event.MVV,event.weight) #WWHP
      #      if event.MVV > 2500: #Get some parameters for event displays
      #        print "WWHP:"
      #        print "MVV = " ,event.MVV
      #        print "Event = " ,event.event
      #        print "Run   = " ,event.run
      #        print "LS   = " ,event.lumi
      #        print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #        print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #        print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #        print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #        print "pT jet1  = " ,event.jet_pt_jet1
      #        print "pT jet2  = " ,event.jet_pt_jet2
      #        print "eta jet1  = " ,event.jet_eta_jet1
      #        print "eta jet2  = " ,event.jet_eta_jet2
      #        print "phi jet1  = " ,event.jet_phi_jet1
      #        print "phi jet2  = " ,event.jet_phi_jet2
      #        print ""
      #        print "jet1_rcn       = " ,event.jet1_rcn
      #        print "jet1_cm        = " ,event.jet1_cm
      #        print "jet1_nm        = " ,event.jet1_nm
      #        print "jet1_muf       = " ,event.jet1_muf
      #        print "jet1_phf       = " ,event.jet1_phf
      #        print "jet1_emf       = " ,event.jet1_emf
      #        print "jet1_nhf       = " ,event.jet1_nhf
      #        print "jet1_chf       = " ,event.jet1_chf
      #        print "jet1_che       = " ,event.jet1_che
      #        print "jet1_ne        = " ,event.jet1_ne
      #        print "jet1_hf_hf     = " ,event.jet1_hf_hf
      #        print "jet1_hf_emf    = " ,event.jet1_hf_emf
      #        print "jet1_hof       = " ,event.jet1_hof
      #        print "jet1_chm       = " ,event.jet1_chm
      #        print "jet1_neHadMult = " ,event.jet1_neHadMult
      #        print "jet1_phoMult   = " ,event.jet1_phoMult
      #        print "jet1_nemf      = " ,event.jet1_nemf
      #        print "jet1_cemf      = " ,event.jet1_cemf
      #        print "jet1_charge    = " ,event.jet1_charge
      #        print "jet1_area      = " ,event.jet1_area
      #        print "jet2_rcn       = " ,event.jet2_rcn
      #        print "jet2_cm        = " ,event.jet2_cm
      #        print "jet2_nm        = " ,event.jet2_nm
      #        print "jet2_muf       = " ,event.jet2_muf
      #        print "jet2_phf       = " ,event.jet2_phf
      #        print "jet2_emf       = " ,event.jet2_emf
      #        print "jet2_nhf       = " ,event.jet2_nhf
      #        print "jet2_chf       = " ,event.jet2_chf
      #        print "jet2_che       = " ,event.jet2_che
      #        print "jet2_ne        = " ,event.jet2_ne
      #        print "jet2_hf_hf     = " ,event.jet2_hf_hf
      #        print "jet2_hf_emf    = " ,event.jet2_hf_emf
      #        print "jet2_hof       = " ,event.jet2_hof
      #        print "jet2_chm       = " ,event.jet2_chm
      #        print "jet2_neHadMult = " ,event.jet2_neHadMult
      #        print "jet2_phoMult   = " ,event.jet2_phoMult
      #        print "jet2_nemf      = " ,event.jet2_nemf
      #        print "jet2_cemf      = " ,event.jet2_cemf
      #        print "jet2_charge    = " ,event.jet2_charge
      #        print "jet2_area      = " ,event.jet2_area
      #        print ""
      #
        if (85. < event.jet_puppi_softdrop_jet1 <= 105. and 85. < event.jet_puppi_softdrop_jet2 < 105.) :
           ZZHP.Fill(event.MVV,event.weight) #ZZHP
      #      if event.MVV > 2500:
      #        print "ZZHP:"
      #        print "MVV = " ,event.MVV
      #        print "Event = " ,event.event
      #        print "Run   = " ,event.run
      #        print "LS   = " ,event.lumi
      #        print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #        print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #        print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #        print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #        print "pT jet1  = " ,event.jet_pt_jet1
      #        print "pT jet2  = " ,event.jet_pt_jet2
      #        print "eta jet1  = " ,event.jet_eta_jet1
      #        print "eta jet2  = " ,event.jet_eta_jet2
      #        print "phi jet1  = " ,event.jet_phi_jet1
      #        print "phi jet2  = " ,event.jet_phi_jet2
      #        print ""
      #
        if ( (85 < event.jet_puppi_softdrop_jet1 <= 105. and 65. <= event.jet_puppi_softdrop_jet2 <= 85.) or (85 < event.jet_puppi_softdrop_jet2 <= 105. and 65. <= event.jet_puppi_softdrop_jet1 <= 85.) ) :
           WZHP.Fill(event.MVV,event.weight) #WZHP
      #      if event.MVV > 2500:
      #        print "WZHP:"
      #        print "MVV = " ,event.MVV
      #        print "Event = " ,event.event
      #        print "Run   = " ,event.run
      #        print "LS   = " ,event.lumi
      #        print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #        print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #        print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #        print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #        print "pT jet1  = " ,event.jet_pt_jet1
      #        print "pT jet2  = " ,event.jet_pt_jet2
      #        print "eta jet1  = " ,event.jet_eta_jet1
      #        print "eta jet2  = " ,event.jet_eta_jet2
      #        print "phi jet1  = " ,event.jet_phi_jet1
      #        print "phi jet2  = " ,event.jet_phi_jet2
      #        print ""
      #        print "jet1_rcn       = " ,event.jet1_rcn
      #        print "jet1_cm        = " ,event.jet1_cm
      #        print "jet1_nm        = " ,event.jet1_nm
      #        print "jet1_muf       = " ,event.jet1_muf
      #        print "jet1_phf       = " ,event.jet1_phf
      #        print "jet1_emf       = " ,event.jet1_emf
      #        print "jet1_nhf       = " ,event.jet1_nhf
      #        print "jet1_chf       = " ,event.jet1_chf
      #        print "jet1_che       = " ,event.jet1_che
      #        print "jet1_ne        = " ,event.jet1_ne
      #        print "jet1_hf_hf     = " ,event.jet1_hf_hf
      #        print "jet1_hf_emf    = " ,event.jet1_hf_emf
      #        print "jet1_hof       = " ,event.jet1_hof
      #        print "jet1_chm       = " ,event.jet1_chm
      #        print "jet1_neHadMult = " ,event.jet1_neHadMult
      #        print "jet1_phoMult   = " ,event.jet1_phoMult
      #        print "jet1_nemf      = " ,event.jet1_nemf
      #        print "jet1_cemf      = " ,event.jet1_cemf
      #        print "jet1_charge    = " ,event.jet1_charge
      #        print "jet1_area      = " ,event.jet1_area
      #        print "jet2_rcn       = " ,event.jet2_rcn
      #        print "jet2_cm        = " ,event.jet2_cm
      #        print "jet2_nm        = " ,event.jet2_nm
      #        print "jet2_muf       = " ,event.jet2_muf
      #        print "jet2_phf       = " ,event.jet2_phf
      #        print "jet2_emf       = " ,event.jet2_emf
      #        print "jet2_nhf       = " ,event.jet2_nhf
      #        print "jet2_chf       = " ,event.jet2_chf
      #        print "jet2_che       = " ,event.jet2_che
      #        print "jet2_ne        = " ,event.jet2_ne
      #        print "jet2_hf_hf     = " ,event.jet2_hf_hf
      #        print "jet2_hf_emf    = " ,event.jet2_hf_emf
      #        print "jet2_hof       = " ,event.jet2_hof
      #        print "jet2_chm       = " ,event.jet2_chm
      #        print "jet2_neHadMult = " ,event.jet2_neHadMult
      #        print "jet2_phoMult   = " ,event.jet2_phoMult
      #        print "jet2_nemf      = " ,event.jet2_nemf
      #        print "jet2_cemf      = " ,event.jet2_cemf
      #        print "jet2_charge    = " ,event.jet2_charge
      #        print "jet2_area      = " ,event.jet2_area
      #        print ""
      #
      if (event.jet_puppi_tau2tau1_jet2 <= 0.40 and 0.40 < event.jet_puppi_tau2tau1_jet1 <= 0.75) or (event.jet_puppi_tau2tau1_jet1 <= 0.40 and 0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75) :
        if (65 <= event.jet_puppi_softdrop_jet1 <= 85. and 65 <= event.jet_puppi_softdrop_jet2 < 85.) :
           WWLP.Fill(event.MVV,event.weight) #WWLP
      #      if event.MVV > 3500:
      #        print "WWLP:"
      #        print "MVV = " ,event.MVV
      #        print "Event = " ,event.event
      #        print "Run   = " ,event.run
      #        print "LS   = " ,event.lumi
      #        print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #        print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #        print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #        print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #        print "pT jet1  = " ,event.jet_pt_jet1
      #        print "pT jet2  = " ,event.jet_pt_jet2
      #        print "eta jet1  = " ,event.jet_eta_jet1
      #        print "eta jet2  = " ,event.jet_eta_jet2
      #        print "phi jet1  = " ,event.jet_phi_jet1
      #        print "phi jet2  = " ,event.jet_phi_jet2
      #        print ""
      #
        if (85 < event.jet_puppi_softdrop_jet1 <= 105. and 85. < event.jet_puppi_softdrop_jet2 <= 105.) :
          ZZLP.Fill(event.MVV,event.weight) #ZZLP
      #     if event.MVV > 2600:
      #       print "ZZLP:"
      #       print "MVV = " ,event.MVV
      #       print "Event = " ,event.event
      #       print "Run   = " ,event.run
      #       print "LS   = " ,event.lumi
      #       print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #       print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #       print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #       print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #       print "pT jet1  = " ,event.jet_pt_jet1
      #       print "pT jet2  = " ,event.jet_pt_jet2
      #       print "eta jet1  = " ,event.jet_eta_jet1
      #       print "eta jet2  = " ,event.jet_eta_jet2
      #       print "phi jet1  = " ,event.jet_phi_jet1
      #       print "phi jet2  = " ,event.jet_phi_jet2
      #       print ""
      #
        if ( (85 < event.jet_puppi_softdrop_jet1 <= 105. and 65. <= event.jet_puppi_softdrop_jet2 < 85.) or (85 < event.jet_puppi_softdrop_jet2 <= 105. and 65. <= event.jet_puppi_softdrop_jet1 < 85.) ) :
           WZLP.Fill(event.MVV,event.weight) #WZLP
      #      if event.MVV > 3500:
      #        print "WZLP:"
      #        print "MVV = " ,event.MVV
      #        print "Event = " ,event.event
      #        print "Run   = " ,event.run
      #        print "LS   = " ,event.lumi
      #        print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
      #        print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
      #        print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
      #        print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
      #        print "pT jet1  = " ,event.jet_pt_jet1
      #        print "pT jet2  = " ,event.jet_pt_jet2
      #        print "eta jet1  = " ,event.jet_eta_jet1
      #        print "eta jet2  = " ,event.jet_eta_jet2
      #        print "phi jet1  = " ,event.jet_phi_jet1
      #        print "phi jet2  = " ,event.jet_phi_jet2
      #        print ""
     
 

    for h in histolist:
      print "Scaling histogram to %f pb"%lumi
      print "Saving histogram %s" %h.GetName()
      h.Scale(lumi)
    name = "qV900"
    write(name,histolist)
    filetmp.Close()
    del intree
    del histolist

