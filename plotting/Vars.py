# set up variable for making 1D or 2D plots 

def SetupVar(varshort,particle,momentum):

	if (varshort == "mass"):
		var1="_wc_mass"
		var2="_wcn_mass"
		vartitle ="WC track mass [GeV]"
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
		vartitle ="WC track momentum [MeV]"
		n = 140
		xlow = 350
		xhigh = 1750
		if momentum>0 :
			n = 30
			xlow = momentum-150
			xhigh = momentum+250			

	elif (varshort == "ke"):
		var1="_wcn_ke"
		var2="_wcn_ke"
		vartitle ="WC track KE [MeV]"
		n = 40
		xlow = 0
		xhigh = 2000


	elif (varshort == "pp"):
		var1="_wcn_pp"
		var2="_wcn_pp"
		vartitle ="Uncorrected Reconstructed beamline track momentum [MeV]"

		n = 140
		xlow = 350
		xhigh = 1750


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
		vartitle ="WC1 hit x-position [mm]"
		wc1_center =  -455.752 
		n = 50
		xlow = wc1_center-100
		xhigh = wc1_center+100

	elif (varshort == "x2"):
		var1="_wc_x2"
		var2="_wcn_x2"
		vartitle ="WC2 hit x-position [mm]"
		wc2_center =  -859.993 
		n = 50
		xlow = wc2_center-100
		xhigh = wc2_center+100

	elif (varshort == "x3"):
		var1="_wc_x3"
		var2="_wcn_x3"
		vartitle ="WC3 hit x-position [mm]"
		wc3_center =  -1352.85 
		n = 50
		xlow = wc3_center-100
		xhigh = wc3_center+100

	elif (varshort == "x4"):
		var1="_wc_x4"
		var2="_wcn_x4"
		vartitle ="WC4 hit x-position [mm]"
		wc4_center =  -1353.87 
		n = 50
		xlow = wc4_center-100
		xhigh = wc4_center+100

	elif (varshort == "y1"):
		var1="_wc_y1"
		var2="_wcn_y1"
		vartitle ="WC 1 hit y-position [mm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y2"):
		var1="_wc_y2"
		var2="_wcn_y2"
		vartitle ="WC2 hit y-position [mm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y3"):
		var1="_wc_y3"
		var2="_wcn_y3"
		vartitle ="WC3 hit y-position [mm]"
		n = 50
		xlow = -100
		xhigh = 100

	elif (varshort == "y4"):
		var1="_wc_y4"
		var2="_wcn_y4"
		vartitle ="WC4 hit y-position [mm]"
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
		xlow=0
		xhigh=600
		n=60
	elif (varshort == "avgdr"):
		var1="_hit_avgdr"
		var2="_hit_avgdr"
		vartitle ="Average hit delta R "
		xlow=0
		xhigh=50
		n=50
	elif (varshort == "last"):
		var1="_hit_lastplane"
		var2="_hit_lastplane"
		vartitle ="Last plane hit"
		xlow=1
		xhigh=21
		n=20		
	elif (varshort == "n"):
		var1="_hit_n"
		var2="_hit_n"
		vartitle ="N hits"
		n = 100
		xlow  = 0
		xhigh = 200
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
	elif (varshort == "hitx"):
		var1="_hitvec_x"
		var2="_hitvec_x"
		vartitle ="hit x [cm]"
		xlow  = -124.706 - 1.72842
		xhigh = 124.704  + 1.72842
		n = 64
	elif (varshort == "hity"):
		var1="_hitvec_y"
		var2="_hitvec_y"
		vartitle ="hit y [cm]"
		xlow  = -123.334 - 1.72842
		xhigh = 126.078  + 1.72842
		n = 64
	elif (varshort == "hitz"):
		var1="_hitvec_z"
		var2="_hitvec_z"
		vartitle ="hit z [cm]"
		xlow  = 3.3829  - 2.78193
		xhigh = 418.033 + 2.78193
		n = 63
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
	elif (varshort == "hitgev"):
		var1="_hitvec_gev"
		var2="_hitvec_gev"
		vartitle ="hit energy [GeV]"
		xlow  = 0
		xhigh = 0.05
		n = 50
	elif (varshort == "plen"):
		var1="_prong_len"
		var2="_prong_len"
		vartitle ="Prong length [cm]"
		n = 45
		xlow  = 1
		xhigh = 451
	elif (varshort == "pdedx"):
		var1="_prong_dedx"
		var2="_prong_dedx"
		vartitle ="Prong dE/dx [GeV/cm]"
		n = 100
		xlow  = 0.001
		xhigh = 0.011		
	elif (varshort == "pgev"):
		var1="_prong_gev"
		var2="_prong_gev"
		vartitle ="Prong Energy [GeV]"
		n = 50
		xlow  = 0
		xhigh = 0.5	
	elif (varshort == "pnhits"):
		var1="_prong_nhits"
		var2="_prong_nhits"
		vartitle ="Prong N hits"
		n = 79
		xlow  = 1
		xhigh = 80	
	else:
		print("Variable name %s not recognised, returning null properties"%(varshort))
		return "","",0,0,0

	return var1, vartitle, n, xlow, xhigh
