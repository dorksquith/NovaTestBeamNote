#!/usr/bin/python
import ROOT
from ROOT import TColor, gDirectory,TGraph,gPad,TPad,TCut, gStyle, gROOT, gSystem, gInterpreter, TFile, TF1, TTree, TH2F, TH1F,TH3F,TLine, TCanvas,TChain, TVector3, TLegend, Math, TLatex
import numpy as np
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetOptTitle(0)
gStyle.SetPalette(61,0,0.9 )
TColor.InvertPalette()
from Vars import SetupVar
from Cuts import *

import argparse

import os

def parse_args():
	parser = argparse.ArgumentParser(	prog='2d-plot-style.py',    description='Makes a canvas with 1 plot')           
	parser.add_argument('-varx',         '--varxshort',    default = "mass"    )
	parser.add_argument('-vary',         '--varyshort',    default = "p"      )
	parser.add_argument('-level',        '--cutlevel',     default = 0,      choices=[0,1,2,3,4], type=int )   
	parser.add_argument('-pol',          '--polarity',     default = -1,     choices=[0,1,-1],    type=int )
	parser.add_argument('-period',       '--period',       default = 234,      choices=[2,3,4,234], type=int)
	parser.add_argument('-plane',        '--plane',        default = 0,                           type=int)
	parser.add_argument('-part',         '--particle',     default = "all",  choices=["all","proton","pimu","kaon","ckov","other"] )
	parser.add_argument('-pbp',          '--planebyplane', default = 0,      choices=[0,1],       type=int)
	parser.add_argument('-mom',          '--momentum',     default = 0,                           type=float )
	parser.add_argument('-cp',           '--cp',           default = 1,      choices=[0,1],       type=int )
	parser.add_argument('-miss',         '--wcmissing',    default = 0,      choices=[0,2,3,4],   type=int )
	return parser.parse_args()

args = parse_args()


def main():

	# input file
	fname = "trackan11_p234.root"
	f= TFile(fname)
	f.cd("testbeamtrackana")
	t= gDirectory.Get("trackTree")


	base, prefix, suffix, s_period, s_particle, s_momentum, s_polarity, s_quality = SetupCuts(args)
		
	# switch for which variables to plot
	varxshort = args.varxshort
	varyshort = args.varyshort

	if varxshort=="hits" and varyshort=="hits":
		xvars=['hitz','hitpe','hitgev','hitdr','hitdx','hitdy']
		#xvars=['avgdr','avgpe']
		yvars=xvars
	else:
		xvars = [varxshort]
		yvars = [varyshort]

	for ivar in range(len(xvars)):
		for jvar in range(len(yvars)):

			if xvars[ivar] == yvars[jvar]:
				continue

			# output figure name
			#pngname = partshort+'_'+periodshort+'_'+xvars[ivar]+'_'+yvars[jvar]+"_"+qualshort+"_"+polshort+"_"+momshort+"_"+cpshort+".png"
			pngname = prefix+xvars[ivar]+'_'+yvars[jvar]+suffix

			# ----------------------------------------------------------------#
			# DO STUFF
			# ----------------------------------------------------------------#
			varx, xtitle, nxbins, xlow, xhigh = SetupVar(xvars[ivar],args.particle,args.momentum)
			vary, ytitle, nybins, ylow, yhigh = SetupVar(yvars[jvar],args.particle,args.momentum)

			h1= TH2F("h1","h1",nxbins, xlow, xhigh, nybins, ylow, yhigh)

			t.Draw(vary+':'+varx+'>>h1',base,'goff')


			c=TCanvas("c","",900,900)
			c.cd()

			pad = TPad("pad", "pad", 0,0,1,1) 
			pad.Draw()
			pad.cd()

			gPad.SetGrid(0,0)
			gPad.SetTopMargin(0.06)  
			gPad.SetRightMargin(0.15) 
			gPad.SetLeftMargin(0.16)  
			gPad.SetBottomMargin(0.12)


			h1.GetXaxis().SetNdivisions(5)
			h1.GetYaxis().SetNdivisions(5)

			h1.GetXaxis().SetTitle(xtitle)
			h1.GetYaxis().SetTitle(ytitle)

			h1.GetYaxis().SetLabelFont(43)
			h1.GetXaxis().SetLabelFont(43)

			h1.GetXaxis().SetLabelSize(34)
			h1.GetYaxis().SetLabelSize(34)

			h1.GetYaxis().SetTitleFont(43)
			h1.GetXaxis().SetTitleFont(43)

			h1.GetXaxis().SetTitleSize(54)
			h1.GetYaxis().SetTitleSize(54)

			h1.GetXaxis().SetTitleOffset(0.9)
			h1.GetYaxis().SetTitleOffset(1.2)

			h1.GetXaxis().CenterTitle()
			h1.GetYaxis().CenterTitle()

			h1.SetFillColor(1)

			h1.SetContour(99)

			h1.GetYaxis().SetMaxDigits(3)
			h1.GetXaxis().SetMaxDigits(3)

			h1.Draw("COLZ")


			gPad.Update()
			gPad.Modified()
			c.Update()

			# plot labels
			latex = ROOT.TLatex ()
			latex.SetTextFont(43) # the 3 means size is in pixels
			latex.SetTextSize(34) # pixels
			#latex.SetNDC()
			#latex.DrawLatex(0.6 ,0.8 , s_particle)


			# position the legend and labels
			nxbins = h1.GetXaxis().GetNbins()
			nxbins55 = int(0.55*float(nxbins))
			text_x_pos = h1.GetXaxis().GetBinCenter(nxbins55 )
			text_y_pos = 0.9*yhigh

			
			# period and particle
			if(s_particle!="all"):
				latex.DrawText(text_x_pos ,text_y_pos*1.05 , "Period "+s_period +" ("+s_particle+")")
			else:
				latex.DrawText(text_x_pos ,text_y_pos*1.05 , "Period "+s_period)
			# polarity
			latex.DrawText(text_x_pos ,text_y_pos*0.97 , s_polarity)
			# momentum
			latex.DrawText(text_x_pos ,text_y_pos*0.89 , s_momentum)
			# quality
			latex.DrawText(text_x_pos ,text_y_pos*0.81 ,s_quality)


			for xbin in range(1,h1.GetNbinsX()+1):
				x = h1.GetXaxis().GetBinLowEdge(xbin) 
				l2 = TLine(x,ylow,x,yhigh)
				#l2.SetLineColor(628)
				l2.SetLineWidth(1)
				l2.SetLineStyle(1)
				#l2.DrawClone()

			gPad.Update()
			gPad.Modified()
			c.Update()

			c.cd()

			c.Print(pngname)
			c.Close()


if __name__ == "__main__":
    main()
