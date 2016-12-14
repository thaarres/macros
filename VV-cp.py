
from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
import array

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "12.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref
# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def get_palette(mode):
  palette = {}
  palette['gv'] = [] 
  colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
  colors = ['#ffbbcc','#de77ae','#762a83','#9970ab','#a6dba0','#7ac5cd','#003b6f']
  colors = ['#46211A','#693D3D','#BA5536','#A43820','#AEBD38','#598234','#90AFC5','#336B87','#2A3132']
  
  for c in colors:
    palette['gv'].append(c)
  return palette[mode] 
 
def get_canvas():
 canvas = TCanvas("c2","c2",50,50,W,H)
 canvas.SetFillColor(0)
 canvas.SetBorderMode(0)
 canvas.SetFrameFillStyle(0)
 canvas.SetFrameBorderMode(0)
 canvas.SetLeftMargin( L/W )
 canvas.SetRightMargin( R/W )
 canvas.SetTopMargin( T/H )
 canvas.SetBottomMargin( B/H )
 canvas.SetTickx(0)
 canvas.SetTicky(0)
 return canvas

def get_ratio(hdata,histsum):

   ratio = TH1F("ratio","ratio",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
     nbkg = histsum.GetBinContent(b)
     ndata = hdata.GetBinContent(b)
     if nbkg != 0 and ndata != 0:
       r = hdata.GetBinContent(b)/nbkg
       ratio.SetBinContent(b,r)
       err = r*TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b)/(ndata*ndata) + histsum.GetBinError(b)*histsum.GetBinError(b)/(nbkg*nbkg) )
       ratio.SetBinError(b,err)   
    
   ratio.SetLineColor(kBlack)
   ratio.SetMarkerColor(kBlack) 
   return ratio

    
def get_line(xmin,xmax,y,style):

   line = TLine(xmin,y,xmax,y)
   line.SetLineColor(kRed)
   line.SetLineStyle(style)
   line.SetLineWidth(2)
   return line
            
argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                              help="configuration")
parser.add_option("-R", "--ratio", dest="ratio", default=True, action="store_true",
                              help="do ratio plot")
parser.add_option("-s", "--save", dest="save", default=False, action="store_true",
                              help="save canvas")
parser.add_option("-b", "--batch", dest="noX", default=False, action="store_true",
                              help="Run in quiet batch mode")                              
parser.add_option("-t", "--time", dest="time", default=10, action="store", type="float",
                              help="time sleep")
parser.add_option("-l", "--log", dest="log", default=False, action="store_true",
                              help="Plot logY")			
	                                    			      			      			      
(opts, args) = parser.parse_args(argv)
print opts.config

config = ConfigParser.ConfigParser()
config.read(opts.config)

prefix = config.get('StackPlots','prefix')
files = eval(config.get('StackPlots','filelist'))
lumi = config.getfloat('StackPlots','lumi')
data = config.get('StackPlots','data')
signal = eval(config.get('StackPlots','signal'))
histos = eval(config.get('StackPlots','histos'))
bkgname = eval(config.get('StackPlots','bkg'))
signalname = eval(config.get('StackPlots','signalname'))
scalesignal = config.getfloat('StackPlots','scalesignal')
rebin = config.getint('StackPlots','rebin')
doratio = opts.ratio
log = opts.log


if opts.noX: gROOT.SetBatch(True)
print "------------------------------------"
print "Lumi = %.1f" %lumi
print "------------------------------------"
print "Input files directory: %s" %prefix
print "------------------------------------"
print "data file : %s" %data
print "signal file : %s" %signal
print "backgrounds : "
print files  
print "------------------------------------"
print "Histos : "
print histos

filelist = []

for f in files:
   filename = prefix + "/" + f
   filetmp = TFile.Open(filename,"READ") 
   htmp = TH1F(filetmp.Get(histos[0]))
   print htmp.Integral()
   filelist.append(filetmp)

filelistSIG = []      
if signal != "":
  for f in signal:
     filename = prefix + "/" + f
     print filename
     filetmp = TFile.Open(filename,"READ") 
     filelistSIG.append(filetmp)

if data != "":
   file_data = TFile.Open(prefix+"/"+data,"READ")

lineStyle = [1,2,3,9,1,2,1,1,1]
markerStyle = [20,22,33,46]

dataevents  = 0  

palette = get_palette('gv')
col = TColor()
for h in histos:
   if h.find("Mjj") != -1: log = True
  
   rebin = config.getint('StackPlots','rebin')
  
   if h.find("Mjj") != -1 : 
     rebin = 200
   if h.find("nVertices") != -1:
      rebin = 2
   if h.find("MET") != -1:
      rebin = 5
   if h.find("Pt") != -1:  
     rebin = 4
    
   sysunc = []
   statunc = []
   
   l = TLegend(0.515383,0.4644522,0.7538201,0.8869464,"","NDC")
   # l.SetNColumns(2)
   l.SetTextSize(0.038)
   l.SetLineColor(0)
   l.SetShadowColor(0)
   l.SetLineStyle(1)
   l.SetLineWidth(1)
   l.SetFillColor(0)
   l.SetFillStyle(0)
   l.SetMargin(0.35)
   l.SetTextAlign(12)
             
   if data != "":  
      h_data = TH1F(file_data.Get(h)) 
      h_data.Rebin(rebin)   
      h_data.SetLineColor(kBlack)
      h_data.SetLineColor(kBlack);
      h_data.SetMarkerColor(kBlack);
      h_data.SetMarkerStyle(20);
      h_data.SetMarkerSize(1.);
      dataevents = h_data.Integral()
      l.AddEntry(h_data,"CMS Data","Ple")
   
   if signal != "":
      histolistSIG = []   
      fits = []
      i = 0
      for f in xrange(0,len(filelistSIG)):
        print filelistSIG[f].GetName()
        print h
        histolistSIG.append(TH1F(filelistSIG[f].Get(h))) 
        i+=1
      i = 0
      for h_signal in histolistSIG:   
        print h_signal.GetName()
        graphColor = col.GetColor(palette[i])
        h_signal.SetLineColor(graphColor)
        h_signal.SetLineWidth(2)
        h_signal.SetLineStyle(lineStyle[i])
        h_signal.Scale(dataevents/h_signal.Integral())
        h_signal.Scale(scalesignal)
        if h.find("afterTau21") != -1 : h_signal.Scale(0.18)
        h_signal.Rebin(rebin)
        l.AddEntry(h_signal,signalname[i],"l")
        i+=1
        fittmp = TGraph(h_signal)
        fits.append(fittmp)
  
     
   histolist = []   
   for f in xrange(0,len(filelist)):
     histolist.append(TH1F(filelist[f].Get(h)))

   for j in range(0,len(histolist)):
     histolist[j].Scale(lumi)
     print lumi
     histolist[j].SetName("hist%i"%j) 
     histolist[j].Rebin(rebin) 
     histolist[j].SetLineColor( col.GetColor(palette[j+6]))
     histolist[j].SetMarkerColor( col.GetColor(palette[j+6]))
     histolist[j].SetMarkerStyle( markerStyle[j])
     histolist[j].SetLineWidth(2)
     histolist[j].SetLineStyle(lineStyle[j])
     l.AddEntry(histolist[j],bkgname[j],"lp") 
     if data != "":
        print "MC   = %i" %histolist[j].Integral()
        print "DATA = %i" %h_data.Integral()
        diff = h_data.Integral()-histolist[j].Integral()
        sf = h_data.Integral()/histolist[j].Integral()
        histolist[j].Scale(sf)
        error = sf*math.sqrt( (1./h_data.Integral()) + (1./histolist[j].Integral()) )    
        print "DATA/MC scalefactor = %f +- %f" %(sf,error)

   xMin  = histolist[0].GetXaxis().GetXmin()
   xMax  = histolist[0].GetXaxis().GetXmax()
   nBins = histolist[0].GetXaxis().GetNbins()	
   xAxisTitle = histolist[0].GetXaxis().GetTitle().replace("[GeV]","(GeV)")    
   yTitle = "Events / %.2f" %((xMax-xMin)/nBins)

   if xAxisTitle.find("GeV") != -1:
      yTitle+=" GeV"
   elif xAxisTitle.find("rad") != -1:
      yTitle+=" rad"
   elif xAxisTitle.find("cm") != -1:
      yTitle+=" cm"

   canv = get_canvas()
   canv.SetTickx()
   canv.SetTicky()  
   canv.GetWindowHeight()
   canv.GetWindowWidth()
   canv.Divide(1,2,0,0,0)
   canv.cd(1)
   
   p11_1 = canv.GetPad(1)
   p11_1.SetPad(0.01,0.26,0.99,0.98)
   # p11_1.SetRightMargin(0.05)
   # p11_1.SetTopMargin(0.05)
   p11_1.SetBottomMargin(0.025)
   # p11_1.SetFillColor(0)
   # p11_1.SetBorderMode(0)
   # p11_1.SetFrameFillStyle(0)
   # p11_1.SetFrameBorderMode(0)
   
   p11_1.SetFillColor(0)
   p11_1.SetBorderMode(0)
   p11_1.SetFrameFillStyle(0)
   p11_1.SetFrameBorderMode(0)
   p11_1.SetLeftMargin( L/W )
   p11_1.SetRightMargin( R/W )
   p11_1.SetTopMargin( T/H )
   # p11_1.SetBottomMargin( B/H )
   
   addInfo = TPaveText(0.6986976,0.3236208,0.9512358,0.4620241,"NDC")
   if not h.find("PrunedMass_afterTau21") != -1 and (h.find("chf") != -1 or h.find("Tau21") != -1 or h.find("tau2tau1") != -1 or h.find("tau3tau1") != -1  or h.find("tau3tau2") !=-1 or h.find("DeltaEta") != -1): addInfo = TPaveText(0.17051072,0.3897145,0.2576454,0.5281177,"NDC")
  
   # addInfo.AddText("AK8CHSPF jets")
   if h.find("punzi") != -1 or h.find("afterPUPPISoftdropMass") != -1  or h.find("afterPrunedMass") !=-1 : addInfo.AddText("65 GeV < M_{G} #leq 105 GeV")
   if files[0].find("pt1000") != -1: addInfo.AddText("|#eta| < 2.5, p_{T} > 1 TeV")
   else : addInfo.AddText("|#eta| < 2.5, p_{T} > 200 GeV")
   if h.find("afterTau21") != -1: addInfo.AddText("#tau_{21} #leq 40")
   addInfo.AddText("M_{jj} > 1020 GeV, |#Delta#eta_{jj}| < 1.3")
   addInfo.SetFillColor(0)
   addInfo.SetLineColor(0)
   addInfo.SetFillStyle(0)
   addInfo.SetBorderSize(0)
   addInfo.SetTextFont(42)
   addInfo.SetTextSize(0.040)
   addInfo.SetTextAlign(12)
   
   if h.find("SoftdropMass") != -1 :
     xAxisTitle = "PUPPI + softdrop mass (GeV)"
   if h.find("afterPUPPISoftdropMass") != -1 :
     xAxisTitle = "PUPPI #tau_{21}"
   if h.find("Tau21_afterPrunedMass") != -1 :
     xAxisTitle = "#tau_{21}"  
   if h.find("puppi_tau2tau1") != -1 :
       xAxisTitle = "PUPPI #tau_{21}"
   if h.find("nVertices") != -1 :
     xAxisTitle = "Number of PVs"    
   if h.find("Pt_jet1") != -1 :
     xAxisTitle = "Leading jet p_{T} (GeV)"
   if h.find("Pt_jet2") != -1 :
     xAxisTitle = "Second leading jet p_{T} (GeV)"   
    
   ymax = histolist[0].GetMaximum()*2.0     
   if log:
     p11_1.SetLogy()
     ymax = h_data.GetMaximum()*360000. 
     if h.find("emf") != -1 or h.find("chargedEmEnergyFraction") != -1: 
       ymax = h_data.GetMaximum()*690000. 
       print "YES!!! " ,h
   else:
     ymax = histolist[0].GetMaximum()*2.0 
   if h.find("SoftdropMass") != -1 : ymax = histolist[0].GetMaximum()*1.1   
   if h.find("PuppiSoftdropMass_afterTau21") != -1 : ymax = histolist[0].GetMaximum()*2.1   
   if h.find("PUPPITau21") != -1 or h.find("puppi_tau2tau1") != -1 : ymax = histolist[0].GetMaximum()*2.2   
   if h.find("Phi") != -1 or h.find("Eta") != -1 : ymax = histolist[0].GetMaximum()*2.7  
   if h.find("chf") != -1 : ymax = histolist[0].GetMaximum()*2.0  
   print ymax
   print ymax
   print ymax
   print ymax
   vFrame = p11_1.DrawFrame(histolist[0].GetXaxis().GetXmin(),0.005,histolist[0].GetXaxis().GetXmax(),ymax)  
   if log: vFrame = p11_1.DrawFrame(histolist[0].GetXaxis().GetXmin(),0.2,histolist[0].GetXaxis().GetXmax(),ymax) 
   if h.find("Mjj") != -1 : vFrame = p11_1.DrawFrame(1000,0.2,histolist[0].GetXaxis().GetXmax(),ymax) 
   vFrame.SetTitle("")
   vFrame.SetXTitle(xAxisTitle)
   vFrame.SetYTitle(yTitle)
   vFrame.GetYaxis().SetTitleSize(0.06)
   vFrame.GetYaxis().SetTitleOffset(1.0)

   for hist in histolist:
     hist.Draw("HISTsame") 
   if signal != "":
     for h_signal in histolistSIG:
       h_signal.Draw("HISTsame")
     # for h_signal in fits:
 #       h_signal.Draw("Csame")
     if data != "":
       h_data.Draw("samePE")

   l.Draw("same")
  
   
   addInfo.Draw("same")
   p11_1.RedrawAxis()
   p11_1.Update()
   p11_1.GetFrame().Draw()
   CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
   canv.Update()
   
   if doratio:

      canv.cd(2)
      p11_2 = canv.GetPad(2)
      p11_2.SetPad(0.01,0.02,0.99,0.27)
      p11_2.SetBottomMargin(0.35)
#       p11_2.SetRightMargin(0.05)
      p11_2.SetFillColor(0)
      p11_2.SetBorderMode(0)
      p11_2.SetFrameFillStyle(0)
      p11_2.SetFrameBorderMode(0)
      p11_2.SetLeftMargin( L/W )
      p11_2.SetRightMargin( R/W )
      # p11_2.SetTopMargin( T/H )
      # p11_2.SetBottomMargin( B/H )

      p11_2.SetGridx()
      p11_2.SetGridy()
   
   if doratio:
      vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(), 0.1, p11_1.GetUxmax(), 1.9)
      if h.find("Mjj") != -1 : vFrame2 = p11_2.DrawFrame(1000, 0.1, p11_1.GetUxmax(), 1.9)
      vFrame2.SetTitle("")
      vFrame2.SetXTitle(xAxisTitle)
     
      vFrame2.SetYTitle("#frac{Data}{MC}")
      vFrame2.GetYaxis().SetTitleSize(0.15)
      vFrame2.GetYaxis().SetTitleOffset(0.350)
      vFrame2.GetYaxis().SetLabelSize(0.09)

      vFrame2.GetXaxis().SetTitleSize(0.18)
      vFrame2.GetXaxis().SetTitleOffset(0.90)
      vFrame2.GetXaxis().SetLabelSize(0.12)
      vFrame2.GetXaxis().SetNdivisions(605)
      vFrame2.GetYaxis().SetNdivisions(504)
      vFrame2.GetYaxis().CenterTitle()
      
      pulls =[]
      j = -1
      for hsum in histolist:
        j += 1
        rh = get_ratio(h_data,hsum)
        rh.SetName(hsum.GetName())
        rh.SetMarkerColor( col.GetColor(palette[j+6]))
        rh.SetMarkerStyle( markerStyle[j])
        pulls.append(rh)
      for pull in pulls:  
        pull.Draw("same")
      li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),1,1)
      if h.find("Mjj") != -1 :li = get_line(1000,h_data.GetXaxis().GetXmax(),1,1)
      li.Draw("same")
      p11_2.RedrawAxis()

   canv.Update()
 
   p11_1.cd()
   p11_1.Update()
   p11_1.RedrawAxis()
   frame = p11_1.GetFrame()
   frame.Draw()   
   canv.cd()
   canv.Update()

   
   if opts.save: 
      canvasname = "/mnt/t3nfs01/data01/shome/thaarres/Notes/notes/AN-16-235/trunk/figures/controlplots/qcdcp_"+h+".pdf"
      canv.Print(canvasname,"pdf")
      canv.Print(canvasname.replace(".pdf",".root"),"root")
   time.sleep(opts.time) 
