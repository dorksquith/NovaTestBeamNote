#!/usr/bin/python
import ROOT
from ROOT import TCut
#Cuts
# ----------------------------------------------------------------#
# PARSE THE SWITCHES, SET UP THE CUTS, AND SET THE OUTPUT PNG NAME
# ----------------------------------------------------------------#

def SetupCuts(args):

	base=TCut("")

	# switch for if we are making plane-by-plane plots
	# do_pbp = args.planebyplane

	period = args.period
	s_period = str(period)
	periodshort=s_period

	# switch for polarity selection	
	polarity     = args.polarity # negative:0, positive:1, both:2
	polarity_cut = GetCut("polarity",polarity)
	print("polarity cut: ", polarity_cut)
	polshort     = GetShort("polarity",polarity)
	s_polarity   = GetLabel("polarity",polarity)
	cutP   = TCut(polarity_cut)
	# which cuts to actually apply
	base += cutP

	# switch for quality cuts selection
	level       = args.cutlevel 
	quality_cut = GetCut("quality",level)
	qualshort   = GetShort("quality",level)
	s_quality   = GetLabel("quality",level)
	cutQ   = TCut(quality_cut)
	base += cutQ

	# switch for which particle to plot ( a mass cut except in the case of ckov)
	particle     = args.particle
	particle_cut = GetCut("particle", particle)
	partshort    = GetShort("particle", particle)
	s_particle   = GetLabel("particle", particle)
	cutPID = TCut(particle_cut)
	base += cutPID

	# switch for which momentum range to plot
	momentum     = args.momentum
	momentum_cut = GetCut("momentum", momentum)
	momshort     = GetShort("momentum", momentum)
	s_momentum   = GetLabel("momentum", momentum)
	cutMom = TCut(momentum_cut)
	base += cutMom

	# switch to ensure the momentum and current are consistent (within N%)
	cp      = args.cp 
	cp_cut  = GetCut("cp",cp)
	cpshort = GetShort("cp",cp)
	s_cp    = GetLabel("cp",cp)
	cutCP   = TCut(cp_cut)
	base += cutCP



	# switch for selecting a particular plane to plot
	plane      = args.plane
	plane_cut  = GetCut("plane",plane)
	planeshort = GetShort("plane",plane)
	s_plane    = GetLabel("plane",plane)
	

	# switch for selecting tracks with N wirechambers missing 
	wcmiss      = args.wcmissing
	wcmiss_cut  = GetCut("wcmiss",wcmiss)
	wcmshort    = GetShort("wcmiss",wcmiss)
	s_wcmiss    = GetLabel("wcmiss",wcmiss)
	cutWCM      = TCut(wcmiss_cut)

	pngname_prefix = partshort+"_"+periodshort+"_"
	pngname_suffix = "_"+qualshort+"_"+polshort+"_"+momshort+"_"+cpshort+".png"

	return base, pngname_prefix, pngname_suffix, s_period, s_particle, s_momentum, s_polarity, s_quality


def GetCut(cutname, cutvalue):

	cut = ""

	if cutname == "polarity":
		if cutvalue > -1:
			cut = "_ev_polarity=="+str(cutvalue)

	if cutname == "quality":
		if (cutvalue==1):
			cut = "_pass_trigger"
		elif (cutvalue==2):
			cut = "_pass_trigger && _pass_tof"
		elif (cutvalue==3):
			cut = "_pass_trigger && _pass_tof && _pass_deadtime_info && _pass_deadtime_det"
		elif (cutvalue==4):
			cut = "_pass_trigger && _pass_tof && _pass_deadtime_info && _pass_deadtime_det && _pass_intimehit"
	
	if cutname == "particle":
		if cutvalue=="proton":
			cut = "_wcn_mass > 0.93 && _wcn_mass <0.97"
		if cutvalue=="pimu":
			cut = "_wcn_mass > 0 && _wcn_mass <0.3"
		if cutvalue=="kaon":
			cut = "_wcn_mass > 0.4 && _wcn_mass <0.6"
		if cutvalue=="ckov":
			cut = "_pass_cherenkov"

	if cutname == "momentum":
		if cutvalue > 0:
			cut = "_wcn_p>"+str(cutvalue-100)+" && _wcn_p<"+str(cutvalue+100)


	if cutname == "cp":

		if cutvalue > 0:
			cut = "_ev_current > _wcn_pp-"+str(150)+" && _ev_current< _wcn_pp+"+str(100)
			
	if cutname == "plane":
			cut = "_hitvec_plane=="+str(cutvalue)

	if cutname == "wcmiss":
			cut = "_wcn_missing=="+str(cutvalue)

	return cut




def GetShort(cutname, cutvalue):
	shortname=""

	if cutname == "polarity":
		if cutvalue == 0:
			shortname = "neg"
		elif cutvalue == 1:
			shortname = "pos"
		else:
			shortname = "posneg"
	
	if cutname == "quality":
		shortname = "level"+str(cutvalue)

	if cutname == "particle":
		shortname = cutvalue

	if cutname == "momentum":
		shortname = "AllMom"
		if cutvalue>0:
			shortname ="Mom"+str(cutvalue)

	if cutname == "cp":
		shortname = "Cur"+str(cutvalue)

	if cutname == "plane":
		shortname = "plane"+str(cutvalue)

	if cutname == "wcmiss":
		shortname = "wcmiss"+str(cutvalue)

	return shortname




def GetLabel(cutname,cutvalue):
	print("cutvalue: ",cutvalue)
	if type(cutvalue) == float:
		print("int(cutvalue): ",int(cutvalue))
		cutvalue = int(cutvalue)

	label=""
	if cutname == "polarity":
		if cutvalue == 0:
			label = "Negative"
		elif cutvalue == 1:
			label = "Positive"
		else:
			label = "+/- polarity"	

	if cutname == "quality":
		label = "level "+str(cutvalue)

	if cutname == "particle":
		if cutvalue == "all":
			label=""
		else:
			label = cutvalue

	if cutname == "momentum":
		if cutvalue > 0:

			label = str(cutvalue-100)+" < p < "+str(cutvalue+100)+" MeV"
		else:
			label = str(0)+" < p < "+str(2000)+" MeV"

	if cutname == "cp":
		label = ""

	if cutname == "plane":
		label = "Plane "+str(cutvalue)
	
	if cutname == "wcmiss":
		label = "WC miss "+str(cutvalue)

	return label