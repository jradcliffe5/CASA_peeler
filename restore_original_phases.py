def restore_original_phases(index, msfile, final_sc_table, interp):
	split(vis=msfile,outputvis='temp1.ms')
	os.system('cp -r %s %s_non_inverted' % (final_sc_table,final_sc_table))
	invgain(caltable=final_sc_table)
	applycal(vis='temp1.ms',gaintable=final_sc_table,interp=interp,calwt=[False],parang=True,applymode='calonly')
	split(vis='temp1.ms',outputvis='%s_peel_S%d.ms' % (msfile.split('.ms')[0],index))
	os.system('rm -r temp1.ms*')

restore_original_phases(index=5, msfile='JVLA2006_HDF_peel_S1_peel_S2_peel_S3_peel_S4_split.ms', final_sc_table='S5_sc1', interp='linear')
