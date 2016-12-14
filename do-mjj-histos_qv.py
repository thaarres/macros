
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
    if not fullpath.find("JetHT_qV.root")!=-1:
      continue
    print "Working on  file %s" %fullpath
    if fullpath.find("QCD")!=-1:
      lumi = opts.lumi
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      name += "_" + name1.split("_")[1]
      name += "_SR"
      if fullpath.find("_qV")!=-1: 
        name = "QCD_qV"
    elif fullpath.find("DATA")!=-1:
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      if fullpath.find("_qV")!=-1: 
        name+= "_qV"
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

  
    qVHP = TH1F('DijetMassHighPuriqV','DijetMassHighPuriqV',8000,0,8000)
    qWHP = TH1F('DijetMassHighPuriqW','DijetMassHighPuriqW',8000,0,8000)
    qZHP = TH1F('DijetMassHighPuriqZ','DijetMassHighPuriqZ',8000,0,8000)
    qVLP = TH1F('DijetMassLowPuriqV','DijetMassLowPuriqV'  ,8000,0,8000)
    qWLP = TH1F('DijetMassLowPuriqW','DijetMassLowPuriqW'  ,8000,0,8000)
    qZLP = TH1F('DijetMassLowPuriqZ','DijetMassLowPuriqZ'  ,8000,0,8000)
    # VVNP = TH1F('DijetMassNoPuriVV','DijetMassNoPuriVV',7000,0,7000)
#     WWNP = TH1F('DijetMassNoPuriWW','DijetMassNoPuriWW',7000,0,7000)
#     WZNP = TH1F('DijetMassNoPuriWZ','DijetMassNoPuriWZ',7000,0,7000)
#     ZZNP = TH1F('DijetMassNoPuriZZ','DijetMassNoPuriZZ',7000,0,7000)
#     qVNP = TH1F('DijetMassNoPuriqV','DijetMassNoPuriqV',7000,0,7000)
#     qWNP = TH1F('DijetMassNoPuriqW','DijetMassNoPuriqW',7000,0,7000)
#     qZNP = TH1F('DijetMassNoPuriqZ','DijetMassNoPuriqZ',7000,0,7000)
    
    histolist.append(qVHP)
    histolist.append(qWHP)
    histolist.append(qZHP)
    histolist.append(qVLP)
    histolist.append(qWLP)
    histolist.append(qZLP)
    # histolist.append(qVNP)
    # histolist.append(qWNP)
    # histolist.append(qZNP)
    

    for event in intree:
  
      if ( event.MVV < 990.): continue
      if ( (65. <= event.jet_puppi_softdrop_jet2 <= 105. and event.jet_puppi_tau2tau1_jet2 <= 0.40) or (65. <= event.jet_puppi_softdrop_jet1 <= 105. and event.jet_puppi_tau2tau1_jet1 <= 0.40)):
           qVHP.Fill(event.MVV,event.weight) #qVHP
      if ( (65. <= event.jet_puppi_softdrop_jet2 <= 105. and 0.40 <event.jet_puppi_tau2tau1_jet2 <= 0.75) or (65. <= event.jet_puppi_softdrop_jet1 <= 105. and 0.40 <event.jet_puppi_tau2tau1_jet1 <= 0.75)):
           qVLP.Fill(event.MVV,event.weight) #qVLP

      if ( (85. < event.jet_puppi_softdrop_jet2 <= 105. and event.jet_puppi_tau2tau1_jet2 <= 0.40) or (85. < event.jet_puppi_softdrop_jet1 <= 105. and event.jet_puppi_tau2tau1_jet1 <= 0.40)):
           qZHP.Fill(event.MVV,event.weight) #qZHP
           # if event.MVV > 4400: #Print out some paramteters for event dispays!!
 #             print "qZHP:"
 #             print "MVV = " ,event.MVV
 #             print "Event = " ,event.event
 #             print "Run   = " ,event.run
 #             print "LS   = " ,event.lumi
 #             print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
 #             print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
 #             print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
 #             print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
 #             print "pT jet1  = " ,event.jet_pt_jet1
 #             print "pT jet2  = " ,event.jet_pt_jet2
 #             print "eta jet1  = " ,event.jet_eta_jet1
 #             print "eta jet2  = " ,event.jet_eta_jet2
 #             print "phi jet1  = " ,event.jet_phi_jet1
 #             print "phi jet2  = " ,event.jet_phi_jet2
 #             print "nPV  = " ,event.nPV
 #             print ""


      if ( (85. < event.jet_puppi_softdrop_jet2 <= 105. and 0.40 <event.jet_puppi_tau2tau1_jet2 <= 0.75) or (85. < event.jet_puppi_softdrop_jet1 <= 105. and 0.40 <event.jet_puppi_tau2tau1_jet1 <= 0.75)):
           qZLP.Fill(event.MVV,event.weight) #qZLP
           # if event.MVV > 5900:
           #   print "qZLP:"
           #   print "MVV = " ,event.MVV
           #   print "Event = " ,event.event
           #   print "Run   = " ,event.run
           #   print "LS   = " ,event.lumi
           #   print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
           #   print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
           #   print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
           #   print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
           #   print "pT jet1  = " ,event.jet_pt_jet1
           #   print "pT jet2  = " ,event.jet_pt_jet2
           #   print "eta jet1  = " ,event.jet_eta_jet1
           #   print "eta jet2  = " ,event.jet_eta_jet2
           #   print "phi jet1  = " ,event.jet_phi_jet1
           #   print "phi jet2  = " ,event.jet_phi_jet2
           #   print "nPV  = " ,event.nPV
           #   print ""

      if ( (65. <= event.jet_puppi_softdrop_jet2 <= 85. and event.jet_puppi_tau2tau1_jet2 <= 0.40) or (65. <= event.jet_puppi_softdrop_jet1 <= 85. and event.jet_puppi_tau2tau1_jet1 <= 0.40)):
           qWHP.Fill(event.MVV,event.weight) #qWHP
           # if event.MVV > 5700:
           #   print "qWHP:"
           #   print "MVV = " ,event.MVV
           #   print "Event = " ,event.event
           #   print "Run   = " ,event.run
           #   print "LS   = " ,event.lumi
           #   print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
           #   print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
           #   print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
           #   print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
           #   print "pT jet1  = " ,event.jet_pt_jet1
           #   print "pT jet2  = " ,event.jet_pt_jet2
           #   print "eta jet1  = " ,event.jet_eta_jet1
           #   print "eta jet2  = " ,event.jet_eta_jet2
           #   print "phi jet1  = " ,event.jet_phi_jet1
           #   print "phi jet2  = " ,event.jet_phi_jet2
           #   print "nPV  = " ,event.nPV
           #   print ""

      if ( (65. <= event.jet_puppi_softdrop_jet2 <= 85. and 0.40 <event.jet_puppi_tau2tau1_jet2 <= 0.75) or (65. <= event.jet_puppi_softdrop_jet1 <= 85. and 0.40 <event.jet_puppi_tau2tau1_jet1 <= 0.75)):
           qWLP.Fill(event.MVV,event.weight) #qWLP
           # if event.MVV > 5500:
           #   print "qWLP:"
           #   print "MVV = " ,event.MVV
           #   print "Event = " ,event.event
           #   print "Run   = " ,event.run
           #   print "LS   = " ,event.lumi
           #   print "jet_puppi_softdrop_jet1 = " ,event.jet_puppi_softdrop_jet1
           #   print "jet_puppi_softdrop_jet2 = " ,event.jet_puppi_softdrop_jet2
           #   print "Tau21 jet1  = " ,event.jet_puppi_tau2tau1_jet1
           #   print "Tau21 jet2  = " ,event.jet_puppi_tau2tau1_jet2
           #   print "pT jet1  = " ,event.jet_pt_jet1
           #   print "pT jet2  = " ,event.jet_pt_jet2
           #   print "eta jet1  = " ,event.jet_eta_jet1
           #   print "eta jet2  = " ,event.jet_eta_jet2
           #   print "phi jet1  = " ,event.jet_phi_jet1
           #   print "phi jet2  = " ,event.jet_phi_jet2
           #   print "nPV  = " ,event.nPV
           #   print ""
           #   print "jet1_rcn       = " ,event.jet1_rcn
           #   print "jet1_cm        = " ,event.jet1_cm
           #   print "jet1_nm        = " ,event.jet1_nm
           #   print "jet1_muf       = " ,event.jet1_muf
           #   print "jet1_phf       = " ,event.jet1_phf
           #   print "jet1_emf       = " ,event.jet1_emf
           #   print "jet1_nhf       = " ,event.jet1_nhf
           #   print "jet1_chf       = " ,event.jet1_chf
           #   print "jet1_che       = " ,event.jet1_che
           #   print "jet1_ne        = " ,event.jet1_ne
           #   print "jet1_hf_hf     = " ,event.jet1_hf_hf
           #   print "jet1_hf_emf    = " ,event.jet1_hf_emf
           #   print "jet1_hof       = " ,event.jet1_hof
           #   print "jet1_chm       = " ,event.jet1_chm
           #   print "jet1_neHadMult = " ,event.jet1_neHadMult
           #   print "jet1_phoMult   = " ,event.jet1_phoMult
           #   print "jet1_nemf      = " ,event.jet1_nemf
           #   print "jet1_cemf      = " ,event.jet1_cemf
           #   print "jet1_charge    = " ,event.jet1_charge
           #   print "jet1_area      = " ,event.jet1_area
           #   print "jet2_rcn       = " ,event.jet2_rcn
           #   print "jet2_cm        = " ,event.jet2_cm
           #   print "jet2_nm        = " ,event.jet2_nm
           #   print "jet2_muf       = " ,event.jet2_muf
           #   print "jet2_phf       = " ,event.jet2_phf
           #   print "jet2_emf       = " ,event.jet2_emf
           #   print "jet2_nhf       = " ,event.jet2_nhf
           #   print "jet2_chf       = " ,event.jet2_chf
           #   print "jet2_che       = " ,event.jet2_che
           #   print "jet2_ne        = " ,event.jet2_ne
           #   print "jet2_hf_hf     = " ,event.jet2_hf_hf
           #   print "jet2_hf_emf    = " ,event.jet2_hf_emf
           #   print "jet2_hof       = " ,event.jet2_hof
           #   print "jet2_chm       = " ,event.jet2_chm
           #   print "jet2_neHadMult = " ,event.jet2_neHadMult
           #   print "jet2_phoMult   = " ,event.jet2_phoMult
           #   print "jet2_nemf      = " ,event.jet2_nemf
           #   print "jet2_cemf      = " ,event.jet2_cemf
           #   print "jet2_charge    = " ,event.jet2_charge
           #   print "jet2_area      = " ,event.jet2_area
           #   print ""


             
             

    for h in histolist:
      print "Scaling histogram to %f pb"%lumi
      print "Saving histogram %s" %h.GetName()
      h.Scale(lumi)
    name = "qV900"
    write(name,histolist)
    filetmp.Close()
    del intree
    del histolist

