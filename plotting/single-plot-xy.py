

#!/usr/bin/python
import ROOT
from ROOT import gDirectory,TColor,TGraph,gPad,TPad,TCut, gStyle, gROOT, gSystem, gInterpreter, TFile, TF1, TTree, TH2F, TH1F,TH3F,TLine, TCanvas,TChain, TVector3, TLegend, Math, TLatex
import numpy as np
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetPalette(61,0,0.9 )
TColor.InvertPalette()
import argparse

import os

def parse_args():
	parser = argparse.ArgumentParser(	prog='single-plot-xy.py',    description='Makes a canvas with 1 plot')           
	parser.add_argument('-var',   '--varshort',  default = "xy", choices=['xy'] )
	parser.add_argument('-level', '--cutlevel',  default = 4,      choices=[0,1,2,3,4], type=int )   
	parser.add_argument('-pol',   '--polarity',  default = -1,      choices=[-1,0,1],       type=int )
	parser.add_argument('-norm',  '--normalise', default = 0,      choices=[0,1],       type=int )
	parser.add_argument('-type',  '--tracktype', default = 'original',      choices=['original','new'] )
	parser.add_argument('-miss',  '--wcmissing',    default = 0,      choices=[0,2,3,4], type=int )
	parser.add_argument('-period',  '--period',  default = 234,      choices=[2,3,4,234], type=int)
	return parser.parse_args()




args = parse_args()
#print(args.varshort, args.cutlevel, args.polarity, args.normalise)
polarity = args.polarity
if polarity==0:
	s_polarity = "Negative "
elif polarity==1:
	s_polarity = "Positive "
else:
	s_polarity = "+/- "



period = args.period
fname = "trackana_p"+str(period)+"_bloat.root"


latex = ROOT.TLatex ()
latex.SetTextFont(43) # the 3 means size is in pixels
latex.SetTextSize(60) # pixels



f= TFile(fname)
f.cd("testbeamtrackana")
t= gDirectory.Get("trackTree")



cutQ = TCut("_pass_trigger && _pass_tof && _pass_deadtime && _pass_intimehit")
if(polarity==-1):
	cutP = TCut("")
else:
	cutP = TCut("_ev_polarity=="+str(polarity))
cutWCNP = TCut("_wcn_p>0")


# wcn [cm]
# WC1 at -45.5752,  0.05334, 159.101 cm, np.degrees(np.arctan(45.5752/159.101)) = 15.984599406050755 
wc1_center =  -455.752                                                                                                                             
# WC2 at -85.9993,  0.0889, 299.888 cm,  np.degrees(np.arctan(85.9993/299.888)) = 16.001376971077327
wc2_center =  -859.993                                                                                                                               
# WC3 at -135.285,  0.00762, 736.945 cm,   np.degrees(np.arctan(135.285/736.945)) = 10.402277649683464
wc3_center =  -1352.85                                                                                                                             
# WC4 at -135.387,  0.03048, 1014.33 cm, np.degrees(np.arctan(135.387/1014.33)) = 7.60257967471892
wc4_center =  -1353.87 

wcis = [1,2,3,4]
ext = 80
xlows = [wc1_center-ext, wc2_center-ext, wc3_center-ext, wc4_center-ext]
xhighs = [wc1_center+ext, wc2_center+ext,wc3_center+ext, wc4_center+ext]
ylow = -1*ext
yhigh = ext
nbinsx = 2*ext
nbinsy = 2*ext

for wci in wcis:

	print("Doing wci: ",wci)

	varx = "_wcn_x"+str(wci)
	xtitle=" hit x [mm]"
	vary = "_wcn_y"+str(wci)
	ytitle=" hit y [mm]"

	pngname="wcn_xy"+str(wci)+"_pol"+str(polarity)+"_period"+str(period)+"_miss"+str(args.wcmissing)+".png"

	base = TCut(cutP)#cutQ+cutP#+cutWCNP

	track4   = TCut("_wcn_missing==0")
	#track3   = TCut("_wcn_missing!=0")+base
	nowc4    = TCut("_wcn_missing==4")
	nowc2    = TCut("_wcn_missing==2")
	nowc3    = TCut("_wcn_missing==3")

	if(args.wcmissing==0):
		base +=track4 
	elif(args.wcmissing==2):
		base +=nowc2 
	elif(args.wcmissing==3):
		base +=nowc3 
	elif(args.wcmissing==4):
		base +=nowc4 


 

	# wc (nonsensical?)
	# x1 80,100
	# y1 -15,0
	# x2 40,60
	# y2 -15,0
	# x3 -10,10
	# y3 -15,0
	# x4 -10,10
	# y4 -15,0


	h1= TH2F("h1","h1",nbinsx, xlows[wci-1], xhighs[wci-1], nbinsy, ylow, yhigh)


	t.Draw(vary+':'+varx+'>>h1',base,'goff')


	c=TCanvas("c","",900,900)
	c.cd()

	pad = TPad("pad", "pad", 0,0,1,1) 
	pad.Draw()
	pad.cd()

	gPad.SetTopMargin(0.03)  
	gPad.SetRightMargin(0.03) 
	gPad.SetBottomMargin(0.03)
	gPad.SetLeftMargin(0.03)
	# give the leftermost pads a left margin
	gPad.SetLeftMargin(0.12)  

	# give the bottomost pads a bottom pargin
	gPad.SetBottomMargin(0.12)


	h1.GetXaxis().SetNdivisions(5)
	h1.GetYaxis().SetNdivisions(5)

	# bottomost plots get an x-axis
	h1.GetXaxis().SetTitle(xtitle)
	h1.GetYaxis().SetTitle(ytitle)

	h1.GetYaxis().SetLabelFont(43)
	h1.GetXaxis().SetLabelFont(43)

	h1.GetXaxis().SetLabelSize(54)
	h1.GetYaxis().SetLabelSize(54)


	h1.GetYaxis().SetTitleFont(43)
	h1.GetXaxis().SetTitleFont(43)

	h1.GetXaxis().SetTitleSize(54)
	h1.GetYaxis().SetTitleSize(54)

	h1.GetXaxis().SetTitleOffset(0.9)
	h1.GetYaxis().SetTitleOffset(0.9)

	h1.GetXaxis().CenterTitle()
	h1.GetYaxis().CenterTitle()

	h1.SetFillColor(1)

	h1.Draw("COL")

	latex.SetNDC()

	#latex.DrawLatex(0.7 ,0.85 , s_polarity)
	#latex.DrawLatex(0.7 ,0.9 , "Period "+str(period))
	latex.DrawLatex(0.7 ,0.9 , "WC "+str(wci))
	if (args.wcmissing>0):
		latex.DrawLatex(0.7 ,0.85 , "miss "+str(args.wcmissing))

	c.cd()


	c.Print(pngname)
	c.Close()


