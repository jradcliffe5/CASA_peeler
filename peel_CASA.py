import os,sys
#from recipes.gaincal_unflag_nearest import *

def peel_CASA(vis,phasecenter,source_ID,solints,nterms,restart,refant):
	if restart ==False:
		delmod(vis=vis,scr=True,otf=True)
		if nterms > 1:
			deconvolver = 'mtmfs'
		else:
			deconvolver = 'clarkstokes'
		tclean(vis=vis,imagename='S%s_pre_peel'%source_ID,niter=10000,deconvolver=deconvolver,\
		nterms=nterms,interactive=True,imsize=[1024,1024],cell='0.2arcsec',stokes='RRLL',phasecenter=phasecenter,\
		usemask='user',savemodel='none',parallel=True,pblimit=0.001,weighting='natural')
		ft(vis=vis,model='S%s_pre_peel.model'%(source_ID),usescratch=True,incremental=False)
		j = range(len(solints))
	else:
		sc_cy = []
		for i in os.listdir('./'):
			if (i.endswith('.workdirectory')) and (i.startswith('S%s_sc' % source_ID)):
				sc_cy = sc_cy + [int(i.split('sc')[1].split('.')[0])]
		if not sc_cy:
			addition=0
		else:
			addition = np.max(sc_cy)
		print addition
		j = range(addition,len(solints)+addition)


	for i in range(len(solints)):
		gaincal(vis=vis, caltable='S%s_sc%s'%(source_ID,str(j[i]+1)), refant=refant, solint=solints[i],\
		minblperant=3, minsnr=1, calmode='p',parang=True)
		#fill_flagged_soln('S%s_sc%s'%(source_ID,str(j[i]+1)))
		applycal(vis=vis, gaintable='S%s_sc%s'%(source_ID,str(j[i]+1)), interp='linear', calwt=[False], parang=True, applymode='calonly')
		if (j[i]+1) == 1:
			mask = 'S%s_pre_peel.mask' % source_ID
		else:
			mask = 'S%s_sc%s.mask' % (source_ID,str(j[i]))
		delmod(vis=vis,scr=True,otf=True)
		tclean(vis=vis,imagename='S%s_sc%s'%(source_ID,str(j[i]+1)),niter=10000,deconvolver=deconvolver,\
		nterms=nterms,interactive=True,imsize=[1024,1024],cell='0.2arcsec',stokes='RRLL',phasecenter=phasecenter,\
		usemask='user',mask=mask,savemodel='none',parallel=True,pblimit=0.001,weighting='natural')
		ft(vis=vis,model='S%s_sc%s.model'%(source_ID,str(j[i]+1)),usescratch=True,incremental=False)
def uvsubber(vis, phasecenter, bychannel, byspw, nspw, nchan, source_ID, nterms):
	## There seems to be some issues here mainly due to the channelisation of the uvsubbing, the issue is currently unresolved and may need some time.
	## Instead the best way is to make a frequency dependent model which can be inputted into the measurement set without the use of incremental==True
	if nterms > 1:
		deconvolver = 'mtmfs'
	else:
		deconvolver = 'clarkstokes'
	delmod(vis=vis,scr=True,otf=True)
	if (bychannel == True) and (byspw == True):
		for i in range(nspw):
			for j in range(nchan):
				os.system('mkdir S%s_uvsub' % source_ID)
				tclean(vis=vis,imagename='S%s_uvsub/spw%d_chan%d' % (source_ID,i,j),spw='%d:%d' % (i,j),niter=5000,deconvolver='clarkstokes',interactive=True,\
				imsize=[1024,1024],cell='0.2arcsec',stokes='RRLL',phasecenter=phasecenter,\
				usemask='user',mask='S%s_pre_peel.mask' % source_ID, savemodel='none',parallel=True,pblimit=0.001)
				ft(vis=vis, spw='%d:%d' % (i,j), model='S%s_uvsub/spw%d_chan%d.model' % (source_ID,i,j),usescratch=True,incremental=False)
	else:
		tclean(vis=vis,imagename='S%s_uvsub' % source_ID,niter=10000, deconvolver=deconvolver, nterms=nterms, interactive=True, imsize=[1024,1024], cell='0.2arcsec',\
		mask='S%s_pre_peel.mask' % source_ID, savemodel='none', parallel=True, pblimit=0.001, phasecenter=phasecenter, stokes='RRLL')
		models = []
		for k in os.listdir('./'):
			if k.startswith('S%s_uvsub.model' % source_ID):
				models = models + [k]
		ft(vis=vis, model=models, nterms=nterms, usescratch=True)
	uvsub(vis=vis)

def restore_original_phases(index, msfile, final_sc_table, interp):
	split(vis=msfile,outputvis='temp1.ms')
	interpol = []
	for i in final_sc_table:
		os.system('cp -r %s %s_non_inverted' % (i,i))
		invgain(caltable=i)
		interpol = interpol + [interp]
	applycal(vis='temp1.ms',gaintable=final_sc_table,interp=interpol,calwt=[False],parang=True,applymode='calonly')
	split(vis='temp1.ms',outputvis='%s_peel_S%d.ms' % (msfile.split('.ms')[0],index))
	os.system('rm -r temp1.ms*')
### Inputs ####
vis = 'VLA1996_HDF_no_gaincurve_peel_S1_peel_S2_peel_S3_peel_S4_peel_S5.ms'
phasecenters = ['J2000 12h34m52.259s +62d02m35.618s', 'J2000 12h35m38.044s +62d19m32.097s',\
				'J2000 12h35m55.121s +61d48m14.455s', 'J2000 12h40m13.617s +62d26m29.237s',\
				'J2000 12h39m16.153s +62d00m17.036s','J2000 12h35m50.628s +62d27m58.484s',\
				 'J2000 12h36m51.943s +61d57m00.372s']
nterms = 1
refant='VA08'
do_sc = False
do_uvsub =True
do_restore = False
source_ID = 6

if do_sc == True:
	peel_CASA(vis=vis,phasecenter=phasecenters[source_ID-1],source_ID=source_ID,\
	solints=['5min','5min'],nterms=nterms,restart=False,refant=refant)

if do_uvsub == True:
	uvsubber(vis=vis, phasecenter=phasecenters[source_ID-1],source_ID=source_ID,\
	bychannel=True,byspw=True, nspw=2,nchan=7, nterms=1)

if do_restore == True:
	restore_original_phases(index=source_ID, msfile=vis, final_sc_table=['S4_sc2'], interp='linear')
