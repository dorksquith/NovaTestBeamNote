# Make 4 columns by 3 rows where column is current [500, 750, 1000, 1250] and row is period [2,3,4]
# Want the y-axis to be consistent throughout
# fuck the axis title

#!/usr/bin/python
import ROOT
from ROOT import gDirectory,TGraph,gPad,TPad,TCut, gStyle, gROOT, gSystem, gInterpreter, TFile, TF1, TTree, TH2F, TH1F,TH3F,TLine, TCanvas,TChain, TVector3, TLegend, Math, TLatex
import numpy as np
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

from Vars import SetupVar
from Cuts import *

import argparse

import os

def parse_args():
	parser = argparse.ArgumentParser(	prog='single-plot.py',    description='Makes a canvas with 1 plot')           
	parser.add_argument('-period', '--period',  default = "234",      choices=["234","34","2","3","4"] ) 
	parser.add_argument('-var',   '--varshort',  default = "mass", choices=['beta','mass',
		'p','magdist','ykink','residual', 'pp',
		'x','y','mex','mey','mez','theta','phi','dix','diy','diz','ddx','ddy','ddz',
		'x1','x2','x3','x4','y1','y2','y3','y4',
		'intensity','run',
		'width','avgpe','avgdr','n','totpe','gev','frac','len','dedx','nhits',
		'detx','ke','last','hitdr','hitpe','hitdx','hitdy','mcke','mcp',
		'miss','amps'
		] )
	parser.add_argument('-var2',   '--var2short',  default = "mcke" )
	parser.add_argument('-level', '--cutlevel',  default = 3,      choices=[0,1,2,3,4], type=int )   
	parser.add_argument('-pol',   '--polarity',  default = -1,      choices=[-1,0,1],       type=int )
	parser.add_argument('-norm',  '--normalise', default = 0,      choices=[0,1],       type=int )
	
	parser.add_argument('-t3',    '--t3',        default = 0,      choices=[0,1],       type=int )
	parser.add_argument('-4p',    '--do_4p',     default = 0,      choices=[0,1],       type=int )
	parser.add_argument('-old',   '--old',       default = 0,      choices=[0,1],       type=int )
	parser.add_argument('-part',  '--particle',  default = "all",  choices=["all","proton","pimu","kaon","ckov"] )
	
	parser.add_argument('-betacut','--betacut',  default = 0,      choices=[-1,0,1], type=int )
	parser.add_argument('-mom',    '--momentum', default = 0,      type=float )
	#parser.add_argument('-cur',    '--current',  default = 0,      type=float )
	parser.add_argument('-cp',     '--cp',       default = 1,      choices=[0,1], type=int )
	parser.add_argument('-plane',  '--plane',    default = 0,      type=int )
	parser.add_argument('-lastplane',  '--lastplane',    default = -1,      type=int )
	parser.add_argument('-fit',  '--do_fit',    default = 0,      type=int )
	parser.add_argument('-miss',         '--wcmissing',    default = -1,      choices=[0,1,2,3,4],   type=int )
	#parser.add_argument('-fls',          '--flshits',    default = -1,      choices=[-1,0],   type=int )
	parser.add_argument('-mc',           '--mc',    default = 0,      choices=[0,1],   type=int )
	parser.add_argument('-datamc',       '--datamc',    default = 0,      choices=[0,1],   type=int )
	#parser.add_argument('-amps',         '--amps',       default = 0,      choices=[0,500,750,1000,1250],   type=int )
	parser.add_argument('-amps',         '--amps',       default = 0,      choices=[0,1234,1000,991,987,750,740,500,495,493,485],   type=int )
	parser.add_argument('-magdist',      '--magdist',    default = 0,      type=int )
	
	return parser.parse_args()


args = parse_args()
def main():

	
	
	# input file
	#fname = "trackan11_p234.root"
	#fname = "offset012345.root" #mc
	#ismc = 1
	fname="newprod_period234_v1.root"
	#fname="newprod_period4_v1.root"
	#fname = "data_p4_new.root"
	ismc=0

	period="234"
	f= TFile(fname)
	f.cd("testbeamtrackana")
	t= gDirectory.Get("trackTree")



	# configure the plot settings
	alf = 0.1 # percentage opacity for fill
	lw  = 5    # line width

	varshort = args.varshort
	xvars=[varshort]


	base, prefix, suffix, s_period, s_particle, s_momentum, s_polarity, s_quality, s_amps, s_magdist = SetupCuts(args)




	# switch for normalisation
	norm = bool(args.normalise)
	if(norm==False):
		normshort = "stats"
	else:
		normshort = "shape"

	# switch for including 3 point track distributions
	do_t3 = bool(args.t3)

	# switch for including new 4point only
	do_4p = bool(args.do_4p)	

	# switch for including original tracking
	do_old = bool(args.old)

	# switch for fitting a gaussian to the histogram
	do_fit = bool(args.do_fit)

	# switch for doing data and mc on same plot
	do_datamc = bool(args.datamc)

	if do_datamc:
		fnamemc = "sim_p4.root"
		fmc= TFile(fnamemc)
		fmc.cd("testbeamtrackana")
		tmc= gDirectory.Get("trackTree")
		var2short = args.var2short
		x2vars=[var2short]
		print("var2short: ",var2short)

	# switch for selecting lastplane (for proton ke plot)
	lastplane= args.lastplane
	s_lastplane =str(lastplane)
	if(lastplane>0):
		lastplane_cut = "_hit_lastplane=="+str(lastplane)
		base+=TCut(lastplane_cut)
		lpcut=TCut(lastplane_cut)
		lpshort="LP"+s_lastplane+"_"
		prefix+=lpshort
	else:
		lastplane_cut = ""
		lpshort=""

	mc_cuts = TCut(lastplane_cut)+TCut("_part_dproc>1")

	for ivar in range(len(xvars)):
	
		pngname = "newprod_"+prefix+xvars[ivar]+suffix

		
		var1, vartitle, nbins, xlow, xhigh = SetupVar(xvars[ivar],args.particle,args.momentum,args.amps)
		
		if do_datamc:
			var2, vartitle, nbins, xlow, xhigh = SetupVar(x2vars[ivar],args.particle,args.momentum,args.amps)
		else:
			var2 = var1

		
		
		ytitle =""

		latex = ROOT.TLatex ()
		latex.SetTextFont(43) # the 3 means size is in pixels
		latex.SetTextSize(34) # pixels


		c=TCanvas("c","",1100,900)
		c.cd()

		original_track_cut = TCut("_pass_wctrack")

		track4   = TCut("_wcn_missing==0")+base
		nowc4    = TCut("_wcn_missing==4")+base
		nowc2    = TCut("_wcn_missing==2")+base
		nowc3    = TCut("_wcn_missing==3")+base
		nowc1    = TCut("_wcn_missing==1")+base
		missUS   = TCut("_wcn_missing==1 || _wcn_missing==2")+base
		missDS   = TCut("_wcn_missing==3 || _wcn_missing==4")+base

		amax=1
		mean=0
		# --------------------------------------------------------#
		# draw into memory without actually drawing (goff option)
		# --------------------------------------------------------#

		# start with the new * point tracks, as we will always draw them.
		h1= TH1F("h1","h1",nbins,xlow,xhigh)
		t.Draw(var1+'>>h1',base,'goff')
		if norm and h1.Integral()>0:
			h1.Scale(1./h1.Integral(),"nosw2")
		amax = h1.GetMaximum()
		mean = h1.GetMean()
		print("mean: ",mean)
		print("rms: ",h1.GetRMS())
		print("integral: ",h1.Integral())
		#print("MaximumBin: ", h1.GetMaximumBin())
		xpeak = h1.GetXaxis().GetBinCenter(h1.GetMaximumBin())
		#print("xpeak: ",xpeak)

		# add the uncorrected momentum if we are plotting momentum and not plotting 3tracks (too busy)
		#if(varshort=='p' and do_t3==False):
		if(do_datamc):
			h1b= TH1F("h1b","h1b",nbins,xlow,xhigh)		
			tmc.Draw(var2+'>>h1b',mc_cuts,'goff')
			print("mc integral: ",h1b.Integral())
			if norm and h1b.Integral()>0:
				h1b.Scale(1./h1b.Integral(),"nosw2")		
			amax = max(h1.GetMaximum(), h1b.GetMaximum())

		# add the uncorrected momentum if we are plotting momentum and not plotting 3tracks (too busy)
		#if(varshort=='p' and do_t3==False):
		if(do_4p):
			h1b= TH1F("h1b","h1b",nbins,xlow,xhigh)		
			t.Draw(var2+'>>h1b',track4,'goff')
			if norm and h1b.Integral()>0:
				h1b.Scale(1./h1b.Integral(),"nosw2")
			amax = max(h1.GetMaximum(), h1b.GetMaximum())

		# original tracking
		if (do_old):
			h2= TH1F("h2","h2",nbins,xlow,xhigh)
			t.Draw(var1+'>>h2',base+original_track_cut,'goff')
			if norm and h2.Integral()>0:
				h2.Scale(1./h2.Integral(),"nosw2")
			amax = max(h1.GetMaximum(), h2.GetMaximum())
		
		# 3point tracking
		if (do_t3):
			"""
			h3= TH1F("h3","h3",nbins,xlow,xhigh)
			t.Draw(var2+'>>h3',nowc4,'goff')
			if norm and h3.Integral()>0:
				h3.Scale(1./h3.Integral(),"nosw2")

			h4= TH1F("h4","h4",nbins,xlow,xhigh)
			t.Draw(var2+'>>h4',nowc2,'goff')
			if norm and h4.Integral()>0:
				h4.Scale(1./h4.Integral(),"nosw2")

			h5= TH1F("h5","h5",nbins,xlow,xhigh)
			t.Draw(var2+'>>h5',nowc3,'goff')
			if norm and h5.Integral()>0:
				h5.Scale(1./h5.Integral(),"nosw2")

			h6= TH1F("h6","h6",nbins,xlow,xhigh)
			t.Draw(var2+'>>h6',nowc1,'goff')
			if norm and h6.Integral()>0:
				h6.Scale(1./h6.Integral(),"nosw2")
			"""
			h3= TH1F("h3","h3",nbins,xlow,xhigh)
			t.Draw(var2+'>>h3',missUS,'goff')
			if norm and h3.Integral()>0:
				h3.Scale(1./h3.Integral(),"nosw2")
			#h3.Add(h1)

			h4= TH1F("h4","h4",nbins,xlow,xhigh)
			t.Draw(var2+'>>h4',missDS,'goff')
			if norm and h4.Integral()>0:
				h4.Scale(1./h4.Integral(),"nosw2")
			#h4.Add(h3)
			amax = max(h1.GetMaximum(), h3.GetMaximum(), h4.GetMaximum())
		
		if(do_t3 and do_old):
			amax = max(h1.GetMaximum(), h2.GetMaximum(), h3.GetMaximum(), h4.GetMaximum())

			

		# --------------------------------------------------------#

		pad = TPad("pad", "pad", 0,0,1,1)
		pad.Draw()
		pad.cd()

		gPad.SetTopMargin(0.05)  
		gPad.SetRightMargin(0.12) 
		gPad.SetLeftMargin(0.12)  
		gPad.SetBottomMargin(0.12)

		

		# new 4point tracks are green, draw them now

		if do_datamc:
			h1.SetMarkerStyle(104)
			h1.SetMarkerSize(4)
			h1.SetMarkerColor(1)
			
			h1.GetXaxis().SetTitle("Kinetic Energy [GeV]")
		else:
			h1.SetLineWidth(lw)
			h1.SetLineColor(420)
			h1.SetFillColorAlpha(417,alf)	
			h1.GetXaxis().SetTitle(vartitle)		

		# totmax is retrieved by GetMaximumForVar which is just a beast - redo this
		h1.SetMaximum(amax*1.1)
		#amax=150
		#print("Warning setting maximum to 150 for KE plots")
		#h1.SetMaximum(amax*1.1)

		h1.GetXaxis().SetNdivisions(510)
		h1.GetYaxis().SetNdivisions(5)

		
		h1.GetYaxis().SetTitle(ytitle)
		h1.GetYaxis().SetTitleOffset(1.6)

		h1.GetYaxis().SetLabelFont(43)
		h1.GetXaxis().SetLabelFont(43)

		h1.GetXaxis().SetLabelSize(30)
		h1.GetYaxis().SetLabelSize(30)
		h1.GetYaxis().SetMaxDigits(3)
		h1.GetXaxis().SetMaxDigits(3)

		h1.GetYaxis().SetTitleFont(43)
		h1.GetXaxis().SetTitleFont(43)

		h1.GetXaxis().SetTitleSize(36)
		h1.GetYaxis().SetTitleSize(36)

		h1.GetXaxis().CenterTitle()
		h1.GetYaxis().CenterTitle()

		# if we want to fit the peak
		if (do_fit):
			# this is for the signal peak which i think should be gaussian
			hmean = h1.GetMean()
			hrms = h1.GetRMS()

			g1 = TF1 ( "g1" ,"gaus" ,xpeak-0.05,xpeak+0.05)
			g1.SetParameters(100,xpeak,hrms)
			#h1.Fit(g1,"R") # fit the whole range  
			h1.Fit(g1) # fit the whole range  
			par=np.zeros(6)                                                                                                                                    
			g1.GetParameters(par[:3])
			gcons=g1.GetParameter(0)
			gmean=g1.GetParameter(1)
			gsigma=g1.GetParameter(2)

			# for the background peak at 1 GeV which is interacting protons and looks quadratic (why?)
			# use the parameters from a fit where there is no contamination from stopping protons, eg plane5
			# p0 = -1392.58
			# p1 =  2.79918
			# p2 = -0.00138153
			#gint = TF1 ( "gint" ,"pol2" ,900,1150)
			#gint = TF1 ( "gint" ,"pol2" ,xpeak,hrms)
			#gint.SetParameters(-1392.58,2.79918,-0.00138153)
			#gint.SetParameters(gcons,gmean,gsigma)
			#h1.Fit(gint,"R") # fit the whole range  
			                                                                                                                                   
			# gint.GetParameters(par[3:6])
			# gintcons=gint.GetParameter(0)
			# gintmean=gint.GetParameter(1)
			# gintsigma=gint.GetParameter(2)
			# h1.Fit(gint,"R+")

			# g4 = TF1 ( "g4" ,"gaus" ,gmean-10 ,gmean+10)
			# g4.SetParameters(gcons,gmean,gsigma)
			# h1.Fit(g4,"R+") # fit the peak                                                                                                                                            
			# g4.GetParameters(par[3:6])
			# gcons=g4.GetParameter(0)
			# gmean=g4.GetParameter(1)
			# gsigma=g4.GetParameter(2)

			# # Use the parameters on the sum. now we are not doing a sum, just the peak                                                                                                                                        
			#gg = TF1("gg", "gaus(0)+pol2(3)", gmean-50, 1150)
			#gg.SetParameters(par);

		if do_datamc:
			h1.DrawCopy("p")
		else:
			h1.DrawCopy()			

		# in case we want to add the uncorrected momentum
		if(do_datamc):
			h1b.SetLineColor(632)
			h1b.SetLineStyle(7)
			h1b.SetFillColor(0)
			h1b.SetLineWidth(lw)
				
			h1b.SetLineColor(860)
			h1b.SetLineStyle(1)	
			h1b.SetLineWidth(2)
			h1b.DrawCopy("same")
		# if we want the original tracks drawn
		if(do_old):
			h2.SetLineColor(863)
			h2.SetFillColorAlpha(865,0.8)
			h2.SetFillStyle(3305)
			gStyle.SetHatchesSpacing(0.5)
			h2.SetLineWidth(lw)
			h2.DrawCopy("same")

		if(do_4p):
			h1b.SetLineColor(863)
			h1b.SetLineStyle(7)
			h1b.SetFillColor(0)
			h1b.SetLineWidth(lw)
			h1b.DrawCopy("same")		

		# if we want the 3point tracks drawn
		if (do_t3):
			h3.SetLineColor(1)
			h3.SetLineWidth(lw)
			h3.SetLineStyle(9)
			h3.DrawCopy("same")

			h4.SetLineColor(880)
			h4.SetLineWidth(lw)
			h4.SetLineStyle(7)
			h4.DrawCopy("same")

			# h5.SetLineColor(860)
			# h5.SetLineWidth(lw)
			# h5.SetLineStyle(2)
			# h5.DrawCopy("same")

			# h6.SetLineColor(1)
			# h6.SetLineWidth(lw)
			# h6.SetLineStyle(10)
			# h6.DrawCopy("same")



		if (do_fit):
			g1.SetLineWidth(5)
			g1.SetLineColor(860)
			#h1.Fit(g1,"R+")
			h1.Fit(g1)
			chi2   = g1.GetChisquare()
			ndof   = g1.GetNDF ()
			gmean  = g1.GetParameter(1)
			gsigma = g1.GetParameter(2)

			"""
			gint.SetLineColor(632)
			gint.SetLineWidth(5)
			gint.SetLineStyle(7)
			h1.Fit(gint,"R+")
			int_chi2   = gint.GetChisquare()
			int_ndof   = gint.GetNDF ()
			int_p0  = gint.GetParameter(0)
			int_p1  = gint.GetParameter(1)
			int_p2 = gint.GetParameter(2)
			"""

		# add some vertical lines if we are plotting magdist
		if (varshort == "magdist"):
			l = TLine(0.,0.,0.,amax*1.1)
			lup = TLine(8.,0.,8.,amax*1.1)
			lup.SetLineStyle(7)
			ld = TLine(-8.,0.,-8.,amax*1.1)
			ld.SetLineStyle(7)
			l.Draw()
			lup.Draw()
			ld.Draw()


		# position the legend and labels
		nxbins = h1.GetXaxis().GetNbins()
		nxbins80 = int(0.6*float(nxbins))
		text_x_pos = h1.GetXaxis().GetBinCenter(nxbins80 )

		
		# period and particle
		if(s_particle!="all"):
			latex.DrawText(text_x_pos ,amax*1.05 , "Period "+s_period +" ("+s_particle+")")
		else:
			latex.DrawText(text_x_pos ,amax*1.05 , "Period "+s_period)

		# polarity
		latex.DrawText(text_x_pos ,amax*0.97 , s_polarity)

		latex.DrawText(text_x_pos ,amax*0.89 , s_momentum)

		latex.DrawText(text_x_pos ,amax*0.81 ,"quality cut level "+s_quality)

		# current range
		#latex.DrawText(text_x_pos ,amax*0.73 ,s_amps)

		# transverse magnet entry point 
		#latex.DrawText(text_x_pos ,amax*0.65 ,s_magdist)

		# plots of ke by last plane hit
		if(lastplane>0):
			latex.DrawText(text_x_pos ,amax*0.73 ,"last plane "+s_lastplane)

		if do_fit:
			latex.SetTextColor(860)
			latex.DrawText(text_x_pos ,amax*0.65, "Stopping particles")
			latex.DrawText(text_x_pos ,amax*0.57, " Mean = %.2f GeV " %( gmean ))
			latex.DrawText(text_x_pos ,amax*0.49 , " Width = %.2f GeV " %( gsigma))
			latex.DrawLatex(text_x_pos ,amax*0.41 , " #chi^{2}/n = %.1f " %(chi2 / ndof ))
			#latex.SetTextColor(632)
			#latex.DrawText(text_x_pos ,amax*0.33, "Interacting protons")
			#latex.DrawText(text_x_pos ,amax*0.25, " f(KE) = %.0f + %.0f x + %.3f x^2  " %( int_p0, int_p1, int_p2 ))
			#latex.DrawLatex(text_x_pos ,amax*0.17 , " #chi^{2}/n = %.1f " %(int_chi2 / int_ndof ))

		# track types	
		if(do_old==False):
			if(do_t3==False):
				leg = TLegend(0.55,0.6,.9,.7)
			else:
				leg = TLegend(0.55,0.45,.9,.7)
		else:
			leg = TLegend(0.55,0.5,.9,.7)
		leg.SetNColumns(1)
		leg.SetBorderSize(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetTextFont(43)
		leg.SetTextSize(34)
		
		#if(varshort=='p' and do_t3==False):
			#leg.AddEntry(h1,"New 4 point","F")
			#leg.AddEntry(h1,"New ","F")
			#leg.AddEntry(h1b,"No correction ","F")
		if(do_old):
			leg.AddEntry(h1,"New ","F")
			leg.AddEntry(h2,"Original ","F")
		if(do_4p):
			leg.AddEntry(h1b,"New 4 point ","F")
		elif (do_t3):
			leg.AddEntry(h3,"+miss US hit","F")
			leg.AddEntry(h4,"+miss DS hit","F")
			#leg.AddEntry(h4,"3 point (no wc2)","F")
			#leg.AddEntry(h6,"3 point (no wc1)","F")
		#else:

		leg.Draw()



		gPad.Update()
		gPad.Modified()

		print("h1.Integral(): ",h1.Integral())

		c.Print(pngname)
		c.Close()


if __name__ == "__main__":
    main()


"""
def SetupVar(varshort,norm, particle="all",momentum=0,current=0):

	if(norm==False):
		ytitle    = "Number of tracks"
	else:
		ytitle    = "Number of tracks (normalised to unity)"


	if (varshort == "mass"):
		var1="_wc_mass"
		var2="_wcn_mass"
		vartitle ="Reconstructed beamline track mass [GeV]"
		n = 250
		xlow = 0
		xhigh = 2.5
		if particle=="proton":
			n = 80
			xlow = 0.8
			xhigh = 1.2
		elif particle=="pimu":
			n = 80
			xlow = 0
			xhigh = 0.4
		elif particle=="kaon":
			n = 80
			xlow = 0.4
			xhigh = 0.8		
		elif particle=="ckov":
			n = 80
			xlow = 0
			xhigh = 0.4

	elif (varshort == "p"):
		var1="_wc_p"
		var2="_wcn_p"
		vartitle ="Reconstructed beamline track momentum [MeV]"
		n = 32
		xlow = 350
		xhigh = 1950
		if momentum>0 :
			n = 35
			xlow = momentum-250
			xhigh = momentum+450	
		elif current >0:
			xlow = current-250
			xhigh = current+450					
	
	elif (varshort == "pp"):
		var1="_wcn_pp"
		var2="_wcn_pp"
		vartitle ="Uncorrected Reconstructed beamline track momentum [MeV]"

		n = 140
		xlow = 350
		xhigh = 1750

	elif (varshort == "ke"):
		var1="_wcn_ke"
		var2="_wcn_ke"
		vartitle ="WC track KE [MeV]"
		n = 160
		xlow = 400
		xhigh = 2000
		#if momentum>0 :
		#	n = 35
		#	xlow = momentum-250
		#	xhigh = momentum+450

	elif (varshort == "last"):
		var1="_hit_lastplane"
		var2="_hit_lastplane"
		vartitle ="Last plane hit"
		xlow=1
		xhigh=62
		n=61	

	elif (varshort == "magdist"):
		var1="_wc_magdist"
		var2="_wcn_magdist"
		vartitle ="Transverse distance between track and magnet axis [cm]"
		n = 60
		xlow = -20
		xhigh = 40


	elif (varshort == "ykink"):
		var1="_wc_ykink"
		var2="_wcn_ykink"
		#vartitle ="Angular difference (dy/dz) between upstream and downstream track"
		vartitle ="y-kink"
		n = 30
		xlow = 0
		xhigh = 0.03

	
	elif (varshort == "residual"):
		var1="_wc_residual"
		var2="_wcn_residual"
		vartitle ="Track fit average residual"#  #sum_{n} ((y_i - slope*z_i - intercept  ) / (#sqrt{1+slope^2})^2 / (n-2)"
		n = 60
		xlow = 0
		xhigh = 15


	elif (varshort == "x"):
		var1="_wc_x"
		var2="_wcn_x"
		vartitle ="Projected track x-position relative to NOvA front face [cm]"
		n = 40
		xlow = -20
		xhigh = 20


	elif (varshort == "y"):
		var1="_wc_y"
		var2="_wcn_y"
		vartitle ="Projected track y-position relative to NOvA front face [cm]"
		n = 40
		xlow = -20
		xhigh = 20

	
	elif (varshort == "mex"):
		var1="_wc_mex"
		var2="_wcn_mex"
		vartitle ="Magnet entry x-position relative to magnet [cm]"
		n = 60
		xlow = -20
		xhigh = 40

	
	elif (varshort == "mey"):
		var1="_wc_mey"
		var2="_wcn_mey"
		vartitle ="Magnet entry y-position relative to magnet [cm]"
		n = 40
		xlow = -20
		xhigh = 20

	
	# for _wc_ the mez variable is offset by -1040. I do not know why
	elif (varshort == "mez"):
		var1="_wc_mez"
		var2="_wcn_mez"
		vartitle ="Magnet entry z-position relative to magnet [cm]"
		n = 80
		xlow = -4 # -1044
		xhigh = 4 # -1039


	elif (varshort == "theta"):
		var1="_wc_ditheta"
		var2="_wcn_ditheta"
		vartitle ="Downstream track direction theta [radians]"
		n = 50
		xlow = 0
		xhigh = 0.05


	elif (varshort == "phi"):
		var1="_wc_diphi"
		var2="_wcn_diphi"
		vartitle ="Downstream track direction phi [radians]"
		n = 64
		xlow = -3.2
		xhigh = 3.2


	elif (varshort == "dix"):
		var1="_wc_dix"
		var2="_wcn_dix"
		vartitle ="Downstream track direction x-component [unit vector]"
		n = 50
		xlow = 0
		xhigh = 0.05
	
	
	elif (varshort == "diy"):
		var1="_wc_diy"
		var2="_wcn_diy"
		vartitle ="Downstream track direction y-component [unit vector]"
		n = 30
		xlow = 0
		xhigh = 0.03
	
	
	elif (varshort == "diz"):
		var1="_wc_diz"
		var2="_wcn_diz"
		vartitle ="Downstream track direction z-component [unit vector]"
		n = 50
		xlow = 0.9995
		xhigh = 1

	
	elif (varshort == "ddx"):
		var1="_wc_ddx"
		var2="_wcn_ddx"
		vartitle ="Difference in x_0 between us and ds tracks [cm]"
		n = 300
		xlow = -60
		xhigh = 240

	elif (varshort == "ddy"):
		var1="_wc_ddy"
		var2="_wcn_ddy"
		vartitle ="Difference in y_o between us and ds tracks [cm]"
		n = 60
		xlow = -30
		xhigh = 30
	
	elif (varshort == "ddz"):
		var1="_wc_ddz"
		var2="_wcn_ddz"
		vartitle ="Difference in z_0 between us and ds tracks [cm]"
		n = 50
		xlow = -10
		xhigh = 40

	elif (varshort == "ddz"):
		var1="_wc_ddz"
		var2="_wcn_ddz"
		vartitle ="Difference in z-intercept between upstream and downstream tracks [cm]"
		n = 50
		xlow = -10
		xhigh = 40

	elif (varshort == "x1"):
		var1="_wc_x1"
		var2="_wcn_x1"
		vartitle ="Wirechamber 1 hit x-position [cm]"
		wc1_center =  -455.752 
		n = 50
		xlow = wc1_center-100
		xhigh = wc1_center+100

	elif (varshort == "x2"):
		var1="_wc_x2"
		var2="_wcn_x2"
		vartitle ="Wirechamber 2 hit x-position [cm]"
		wc2_center =  -859.993 
		n = 50
		xlow = wc2_center-100
		xhigh = wc2_center+100

	elif (varshort == "x3"):
		var1="_wc_x3"
		var2="_wcn_x3"
		vartitle ="Wirechamber 3 hit x-position [cm]"
		wc3_center =  -1352.85 
		n = 50
		xlow = wc3_center-100
		xhigh = wc3_center+100

	elif (varshort == "x4"):
		var1="_wc_x4"
		var2="_wcn_x4"
		vartitle ="Wirechamber 4 hit x-position [cm]"
		wc4_center =  -1353.87 
		n = 50
		xlow = wc4_center-100
		xhigh = wc4_center+100

	elif (varshort == "y1"):
		var1="_wc_y1"
		var2="_wcn_y1"
		vartitle ="Wirechamber 1 hit y-position [cm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y2"):
		var1="_wc_y2"
		var2="_wcn_y2"
		vartitle ="Wirechamber 2 hit y-position [cm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y3"):
		var1="_wc_y3"
		var2="_wcn_y3"
		vartitle ="Wirechamber 3 hit y-position [cm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y4"):
		var1="_wc_y4"
		var2="_wcn_y4"
		vartitle ="Wirechamber 4 hit y-position [cm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "beta"):
		var1="_tof_beta"
		var2="_tof_beta"
		vartitle ="Particle speed [c]"
		n = 250
		xlow = 0.
		xhigh = 2.5
	elif (varshort == "hitdr"):
		var1="_hitvec_dr"
		var2="_hitvec_dr"
		vartitle ="dr(hit,wctrack) [cm]"
		xlow=0
		xhigh=50
		n=50					
	elif (varshort == "hitdx"):
		var1="_hitvec_dx"
		var2="_hitvec_dx"
		vartitle ="dx(hit,wctrack) [cm]"
		xlow=0
		xhigh=30
		n=30
	elif (varshort == "hitdy"):
		var1="_hitvec_dy"
		var2="_hitvec_dy"
		vartitle ="dy(hit,wctrack) [cm]"
		xlow=0
		xhigh=30
		n=30
	elif (varshort == "hitpe"):
		var1="_hitvec_pe"
		var2="_hitvec_pe"
		vartitle ="hit energy [PE]"
		xlow=0
		xhigh=600
		n=60
	elif (varshort == "intensity"):
		var1="_ev_intensity6"
		var2="_ev_intensity6"
		vartitle ="Beam intensity [ppp] "
		n = 100
		xlow = 0
		xhigh = 12e9
	
	elif (varshort == "run"):
		var1="_ev_run"
		var2="_ev_run"
		vartitle ="Run number "
		n = 50
		xlow  = 100000
		xhigh = 105000
	elif (varshort == "width"):
		var1="_hit_width"
		var2="_hit_width"
		vartitle ="Hit width "
		n = 100
		xlow  = 1
		xhigh = 101
	elif (varshort == "avgpe"):
		var1="_hit_avgpe"
		var2="_hit_avgpe"
		vartitle ="Average hit PE "
		n = 100
		xlow  = 0
		xhigh = 1000
	elif (varshort == "avgdr"):
		var1="_hit_avgdr"
		var2="_hit_avgdr"
		vartitle ="Average hit delta R "
		n = 150
		xlow  = 0
		xhigh = 150
	elif (varshort == "n"):
		var1="_hit_n"
		var2="_hit_n"
		vartitle ="N hits"
		n = 20
		xlow  = 0
		xhigh = 20
	elif (varshort == "totpe"):
		var1="_hit_totpe"
		var2="_hit_totpe"
		vartitle ="Total hit PE [counts]"
		n = 30
		xlow  = 0
		xhigh = 30000
	elif (varshort == "gev"):
		var1="_chit_gev"
		var2="_chit_gev"
		vartitle ="Total hit Energy [GeV]"
		n = 60
		xlow  = 0
		xhigh = 1.5
	elif (varshort == "frac"):
		var1="_chit_frac"
		var2="_chit_frac"
		vartitle ="Fraction of cell hits calibrated"
		n = 25
		xlow  = 0
		xhigh = 2.5
	elif (varshort == "detx"):
		var1="_hitvec_x"
		var2="_hitvec_x"
		vartitle ="X position of plane 0 detector hit"
		n = 400
		xlow  = -200
		xhigh = 200
	elif (varshort == "len"):
		var1="_prong_len"
		var2="_prong_len"
		vartitle ="Prong length [cm]"
		n = 45
		xlow  = 1
		xhigh = 451
	elif (varshort == "dedx"):
		var1="_prong_dedx"
		var2="_prong_dedx"
		vartitle ="Prong dE/dx [GeV/cm]"
		n = 100
		xlow  = 0.001
		xhigh = 0.011		
	else:
		print("Variable name %s not recognised, returning null properties"%(varshort))
		return "","","",0,0,0

	return var1, var2, vartitle, ytitle, n, xlow, xhigh
"""




