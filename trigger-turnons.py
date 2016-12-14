from ROOT import *
import time
import math
from array import *
import CMS_lumi, tdrstyle
from optparse import OptionParser


tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "12.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
# gROOT.SetBatch(True)

parser = OptionParser()
parser.add_option("-s", "--save", dest="save", default=False, action="store_true",
                              help="save canvas")
parser.add_option("-b", "--batch", dest="noX", default=False, action="store_true",
                              help="Run in quiet batch mode")                              
parser.add_option("-t", "--time", dest="time", default=2, action="store", type="float",
                              help="time sleep")		                                    			      			      			      

(opts, args) = parser.parse_args()

if opts.noX: gROOT.SetBatch(True)

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4
def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#de77ae','#a6dba0','#4393c3','#4393c3']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
def sigmoid(x,p):
    max_eff = 1.
    return max_eff/(1+math.exp(-p[1]*(x[0]-p[0])))
    # return max_eff/(p[1]+math.exp(-p[0]*x[0]))
    return sigmoid
    # k == 1/sigma*Ethres, x0 = EThreshold

def getLegend():
  l = TLegend(0.4304361,0.263552,0.708124,0.4624967)
  l.SetTextSize(0.033)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  return l

def getPave():
  addInfo = TPaveText(0.5604027,0.846131,0.8288591,0.9419643,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.030)
  addInfo.SetTextAlign(12)
  return addInfo

def getCanvas():
  c = TCanvas("c","TriggerEff",800,800)
  c.GetWindowHeight()
  c.GetWindowWidth()
  c.SetTitle("")
  c.SetGridx()
  c.SetGridy()
  return c

def formatGraph(c,mg,label,bin1,bin2):
  mg.SetMinimum(0.)
  mg.SetMaximum(1.2)
  mg.GetXaxis().SetTitleSize(0.06)
  mg.GetXaxis().SetTitleOffset(0.95)
  mg.GetXaxis().SetLabelSize(0.05)
  mg.GetYaxis().SetTitleSize(0.06)
  mg.GetYaxis().SetLabelSize(0.05)
  mg.GetXaxis().SetTitle(label)
  mg.GetYaxis().SetTitle("Efficiency")
  mg.GetXaxis().SetRangeUser(bin1,bin2)
  mg.GetYaxis().SetNdivisions(408)
  CMS_lumi.CMS_lumi(c, iPeriod, iPos)
  c.Update()

def setEffStyle(eff,color,marker):
  eff.SetMarkerStyle(marker)
  eff.SetMarkerSize(1.1)
  eff.SetMarkerColor(color)
  eff.SetLineColor( color)
  
def doFit(eff,l,histtmp,end):
  fit_x3 = TF1("fit_x3", sigmoid, 0., 2000., 2)
  fit_x3.SetParameters(1.0,0.01)
  start = histtmp.GetBinCenter(histtmp.FindFirstBinAbove(0.75))
  print "Starting point = %s" %start
  eff.Fit(fit_x3, "+","",start,end)
  fit = eff.GetFunction("fit_x3")
  mass = fit.GetX(0.9900, start, end, 1.E-10, 100, False)
  print "99 percent efficient at mass:"
  print mass
  print "######"
  l.AddEntry(eff, "%s:" %(histtmp.GetTitle()), "lep" )
  l.AddEntry(0, ">99 %%: M_{jj} > %.0f GeV" %(mass), "" )
  return fit
    


outpath="plots_ichepjson/trigger/"
file = TFile.Open('/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/ExoDiBosonAnalysis.SingleMuon_trigger.root', 'READ')   
palette = get_palette('gv')
col = TColor()
markerStyles = [20,22,26]

colorcodes = [18,17,16,15,11,20,23,29,30,32]
pal = array('i', colorcodes)
gStyle.SetPalette(10,pal)

# #-------------------------Pt vs SD-------------------------------#
#
# histoname = 'PtvsMSD_num'
#
# rbin = 2
# bin1 = 200
# bin2 = 850
# label = 'p_{T} (GeV)'
# addInfo1 = "p_{T} > 200 GeV, |#eta| < 2.5"
# addInfo2 = 'NUM = PF360TrimMass30'
# addInfo3 = 'DEN = PF320'
# hnum = TH2F(file.Get('PtvsMSD_num')) #PtvsMPR_den
# hden = TH2F(file.Get('PtvsMSD_den')) #PtvsMPR_den
# hden.GetXaxis().SetRangeUser(bin1,bin2)
# l=getLegend()
# hnum.Divide(hden)
#
# c = getCanvas()
# hnum.Draw("COLZ")
#
# turnon = hnum.FindFirstBinAbove(0.9999,2)
# print turnon
# print turnon
# turnon = hnum.FindFirstBinAbove(0.9999,1)
# print turnon
# print turnon
# turnon = hnum.FindFirstBinAbove(0.9999)
# print turnon
# print turnon
# formatGraph(c,hnum,label,bin1,bin2)
# hnum.GetYaxis().SetTitle("PUPPI softdrop mass (GeV)")
# hnum.GetYaxis().SetRangeUser(0.,150.)
# hnum.GetYaxis().SetNdivisions(308)
# addInfo = getPave()
# addInfo.AddText(addInfo1)
# addInfo.AddText(addInfo2)
# addInfo.AddText(addInfo3)
# addInfo.Draw()
# hnum.SetMaximum(1.0)
# c.Update()
#
# if opts.save:
#   canvasname ="%striggereff-2DsdmassVSpt.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, hden, hnum

# #-------------------------HT vs SD-------------------------------#
# histonames = ['HT800_vsSD']
#
# rbin = 2
# bin1 = 0
# bin2 = 210
# label = 'PUPPI softdrop mass (GeV)'
# addInfo1 = "p_{T} > 200 GeV, |#eta| < 2.5"
# addInfo2 = ''
# hden = TH1F(file.Get('PFHT650_vsSD'))
# hden.GetXaxis().SetRangeUser(bin1,bin2)
# hden.Rebin(rbin)
# l=getLegend()
#
# i=0
# mg =  TMultiGraph()
# for h in histonames:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp.Rebin(rbin)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,100)
#   mg.Add(eff)
#   l.AddEntry(0,"","")
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   l.AddEntry(0,"","")
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.SetMinimum(0.90)
# mg.SetMaximum(1.10)
# addInfo = getPave()
# addInfo.AddText(addInfo1)
# addInfo.AddText(addInfo2)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereff-HTvssdmass.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, addInfo, hden, histtmp
#
# #-------------------------vs SD-------------------------------#
# histonames = ['PFJet360_Trim_SD']
#
# rbin = 2
# bin1 = 0
# bin2 = 210
# label = 'PUPPI softdrop mass (GeV)'
# addInfo1 = "p_{T} > 200 GeV, |#eta| < 2.5"
# addInfo2 = ''
# hden = TH1F(file.Get('PFJet320_SD'))
# hden.GetXaxis().SetRangeUser(bin1,bin2)
# hden.Rebin(rbin)
# l=getLegend()
#
# i=0
# mg =  TMultiGraph()
# for h in histonames:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp.Rebin(rbin)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,100)
#   mg.Add(eff)
#   l.AddEntry(0,"","")
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   l.AddEntry(0,"","")
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# addInfo = getPave()
# addInfo.AddText(addInfo1)
# addInfo.AddText(addInfo2)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereff-sdmass.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, addInfo, hden, histtmp
#
# # #-------------------------vs PRUNED-------------------------------#
# label = 'Pruned mass (GeV)'
# histonames = ['PFJet360_Trim_P']
# hden = TH1F(file.Get('PFJet320_P'))
# hden.GetXaxis().SetRangeUser(bin1,bin2)
# hden.Rebin(rbin)
# i=0
# l=getLegend()
# mg =  TMultiGraph()
# for h in histonames:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp.Rebin(rbin)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,100)
#   mg.Add(eff)
#   l.AddEntry(0,"","")
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   l.AddEntry(0,"","")
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# addInfo = getPave()
# addInfo.AddText(addInfo1)
# addInfo.AddText(addInfo2)
# addInfo.Draw()
# c.Update()
#
# if opts.save:
#   canvasname ="%striggereff-prunedmass.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, addInfo, hden, histtmp


# #-------------------------vs Mjj, No V-tag-------------------------------#
label = 'Dijet invariant mass (GeV)'
addInfo1 = "No V-tag"
addInfo2 = ''

bins1 = range (700,1100,20)
bins2 = range (1100,1300,50)
bins3 = range (1300,2100,100)
bins = []
bins = bins1
bins += bins2
bins += bins3
# bins = [650.,675., 720., 800.,850., 900.,950.,975., 1000.,1025.,1050.,1075.,1100.,1150., 1200.,1300.,1400.,1500,1600., 2000.]
runArray = array('d',bins)
binnum = len(bins)-1

hden = TH1F(file.Get('PFHT650_noTag'))
hden = hden.Rebin(binnum,"hden",runArray)

histonames1 = ['HT800_noTag','HT650_MJJ900_noTag','HT_noTag']
histonames2 = ['PFJet360_Trim_noTag', 'HT700_Trim_noTag','Substructure_noTag']
histonames3 = ['ALL_noTag','HT_noTag','Substructure_noTag']

addInfo = getPave()
addInfo.AddText(addInfo1)
addInfo.AddText(addInfo2)


bin1 = 600
bin2 = 2200
# #-------HT based-------
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames1:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-HT_noTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp
#
# #-------SUBSTRUCTURE based-------
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames2:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250.)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
# time.sleep(opts.time)
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-SUBST_noTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp

#-------ALL-------
l=getLegend()
i=0
mg =  TMultiGraph()
for h in histonames3:
  histtmp = TH1F(file.Get(h))
  histtmp.GetXaxis().SetRangeUser(bin1,bin2)
  name = 'hnew%i'%i
  histtmp = histtmp.Rebin(binnum,name,runArray)
  eff =  TGraphAsymmErrors()
  eff.Divide(histtmp,hden)
  histtmp.Divide(hden)
  setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i]) 
  myfit = doFit(eff,l,histtmp,1250.)
  mg.Add(eff)
  # l.AddEntry(eff, histtmp.GetTitle(), "lep" )
  i += 1

c = getCanvas()
mg.Draw("AP")
l.Draw("same")

formatGraph(c,mg,label,bin1,bin2)
mg.GetXaxis().SetNdivisions(404)
addInfo.Draw()
c.Update()
if opts.save:
  canvasname ="%striggereffMjj-ALL_noTag.pdf"%outpath
  print "saving to Canvas  %s" %canvasname
  c.Print(canvasname,"pdf")
  c.Print(canvasname.replace(".pdf",".root"),"root")
time.sleep(opts.time) 
del c, l, mg, hden, histtmp






# #-------------------------vs Mjj, Single V-tag-------------------------------#
label = 'Dijet invariant mass (GeV)'
addInfo1 = "Single V-tag"
addInfo2 = '65 GeV < M_{P} < 105 GeV'

bins1 = range (700,1100,20)
bins2 = range (1100,1300,50)
bins3 = range (1300,2100,100)
bins = []
bins = bins1
bins += bins2
bins += bins3
# bins = [650.,675., 720., 800.,850., 900.,950.,975., 1000.,1025.,1050.,1075.,1100.,1150., 1200.,1300.,1400.,1500,1600., 2000.]
runArray = array('d',bins)
binnum = len(bins)-1

hden = TH1F(file.Get('PFHT650'))
hden = hden.Rebin(binnum,"hden",runArray)

histonames1 = ['HT800','HT650_MJJ900','HT']
histonames2 = ['PFJet360_Trim', 'HT700_Trim','Substructure']
histonames3 = ['ALL','HT','Substructure']

addInfo = getPave()
addInfo.AddText(addInfo1)
addInfo.AddText(addInfo2)

# #-------HT based-------
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames1:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-HT_SingleTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp
#
# #-------SUBSTRUCTURE based-------
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames2:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250.)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
# time.sleep(opts.time)
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-SUBST_SingleTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp

#-------ALL-------
l=getLegend()
i=0
mg =  TMultiGraph()
for h in histonames3:
  histtmp = TH1F(file.Get(h))
  histtmp.GetXaxis().SetRangeUser(bin1,bin2)
  name = 'hnew%i'%i
  histtmp = histtmp.Rebin(binnum,name,runArray)
  eff =  TGraphAsymmErrors()
  eff.Divide(histtmp,hden)
  histtmp.Divide(hden)
  setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i]) 
  myfit = doFit(eff,l,histtmp,1250.)
  mg.Add(eff)
  # l.AddEntry(eff, histtmp.GetTitle(), "lep" )
  i += 1

c = getCanvas()
mg.Draw("AP")
l.Draw("same")

formatGraph(c,mg,label,bin1,bin2)
mg.GetXaxis().SetNdivisions(404)
addInfo.Draw()
c.Update()
if opts.save:
  canvasname ="%striggereffMjj-ALL_SingleTag.pdf"%outpath
  print "saving to Canvas  %s" %canvasname
  c.Print(canvasname,"pdf")
  c.Print(canvasname.replace(".pdf",".root"),"root")
time.sleep(opts.time) 
del c, l, mg, hden, histtmp



# #-------------------------vs Mjj, Double V-tag-------------------------------#
label = 'Dijet invariant mass (GeV)'
addInfo1 = "Double V-tag"
addInfo2 = '65 GeV < M_{P} < 105 GeV'

bins1 = range (700,1100,40)
bins2 = range (1100,1300,60)
bins3 = range (1300,2100,120)
bins = []
bins = bins1
bins += bins2
bins += bins3
# bins = [650.,675., 720., 800.,850., 900.,950.,975., 1000.,1025.,1050.,1075.,1100.,1150., 1200.,1300.,1400.,1500,1600., 2000.]
runArray = array('d',bins)
binnum = len(bins)-1

hden = TH1F(file.Get('PFHT650_VV'))
hden = hden.Rebin(binnum,"hden",runArray)

histonames1 = ['HT800_VV','HT650_MJJ900_VV','HT_VV']
histonames2 = ['PFJet360_Trim_VV', 'HT700_Trim_VV','Substructure_VV']
histonames3 = ['ALL_VV','HT_VV','Substructure_VV']

addInfo = getPave()
addInfo.AddText(addInfo1)
addInfo.AddText(addInfo2)

# #-------HT based-------
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames1:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250.)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)

# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-HT_DoubleTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
#   c.Print(canvasname.replace(".pdf",".root"),"root")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp
#
# #-------SUBSTRUCTURE based-------
# hden = TH1F(file.Get('PFHT650_VV'))
# hden = hden.Rebin(binnum,"hden",runArray)
# l=getLegend()
# i=0
# mg =  TMultiGraph()
# for h in histonames2:
#   histtmp = TH1F(file.Get(h))
#   histtmp.GetXaxis().SetRangeUser(bin1,bin2)
#   name = 'hnew%i'%i
#   histtmp = histtmp.Rebin(binnum,name,runArray)
#   eff =  TGraphAsymmErrors()
#   eff.Divide(histtmp,hden)
#   histtmp.Divide(hden)
#   setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i])
#   # myfit = doFit(eff,l,histtmp,1250.)
#   mg.Add(eff)
#   l.AddEntry(eff, histtmp.GetTitle(), "lep" )
#   i += 1
#
# c = getCanvas()
# mg.Draw("AP")
# l.Draw("same")
#
# formatGraph(c,mg,label,bin1,bin2)
# mg.GetXaxis().SetNdivisions(404)
# addInfo.Draw()
# c.Update()
# if opts.save:
#   canvasname ="%striggereffMjj-SUBST_DoubleTag.pdf"%outpath
#   print "saving to Canvas  %s" %canvasname
#   c.Print(canvasname,"pdf")
# time.sleep(opts.time)
# del c, l, mg, hden, histtmp

#-------ALL-------
hden = TH1F(file.Get('PFHT650_VV'))
hden = hden.Rebin(binnum,"hden",runArray)
l=getLegend()
i=0
mg =  TMultiGraph()
for h in histonames3:
  histtmp = TH1F(file.Get(h))
  histtmp.GetXaxis().SetRangeUser(bin1,bin2)
  name = 'hnew%i'%i
  histtmp = histtmp.Rebin(binnum,name,runArray)
  eff =  TGraphAsymmErrors()
  eff.Divide(histtmp,hden)
  histtmp.Divide(hden)
  setEffStyle(eff,col.GetColor(palette[i]),markerStyles[i]) 
  myfit = doFit(eff,l,histtmp,1250.)
  mg.Add(eff)
  # l.AddEntry(eff, histtmp.GetTitle(), "lep" )
  i += 1

c = getCanvas()
mg.Draw("AP")
l.Draw("same")

formatGraph(c,mg,label,bin1,bin2)
mg.GetXaxis().SetNdivisions(404)
addInfo.Draw()
c.Update()
if opts.save:
  canvasname ="%striggereffMjj-ALL_DoubleTag.pdf"%outpath
  print "saving to Canvas  %s" %canvasname
  c.Print(canvasname,"pdf")
  c.Print(canvasname.replace(".pdf",".root"),"root")
time.sleep(opts.time) 
del c, l, mg, hden, histtmp



