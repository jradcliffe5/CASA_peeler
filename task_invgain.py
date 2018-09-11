from taskinit import *

# invgain is released under a BSD 3-Clause License
# See LICENSE for details

# HISTORY:
#   1.0  16Sep2015  Initial version.
#   1.1  27Sep2016  Fixed typos, no functionality change
#   1.2  13Oct2016  Fixed license, no changes to code
#   1.3  24Oct2016  Included doi in readme, no changes to code
#

def invgain(caltable,field,spw,scan,obsid):

    #
    # Task invgain
    #
    #    Invert gain solutions, overwriting caltable.
    #    Christopher A. Hales
    #
    #    Version 1.3 (tested with CASA Version 4.7.0)
    #    24 October 2016
    
    casalog.origin('invgain')
    
    selection=''
    if len(field)>0:
        if not field.isdigit():
            casalog.post('*** ERROR: This version does not support multiple FIELD_ID selection.', 'ERROR')
            casalog.post('*** ERROR: Exiting invgain.', 'ERROR')
            return
        
        selection=selection+'FIELD_ID=='+field+'&&'
    
    if len(spw)>0:
        if not spw.isdigit():
            casalog.post('*** ERROR: This version does not support multiple SPECTRAL_WINDOW_ID selection.', 'ERROR')
            casalog.post('*** ERROR: Exiting invgain.', 'ERROR')
            return
        
        selection=selection+'SPECTRAL_WINDOW_ID=='+spw+'&&'
    
    if len(scan)>0:
        if not scan.isdigit():
            casalog.post('*** ERROR: This version does not support multiple SCAN_NUMBER selection.', 'ERROR')
            casalog.post('*** ERROR: Exiting invgain.', 'ERROR')
            return
        
        selection=selection+'SCAN_NUMBER=='+scan+'&&'
    
    if len(obsid)>0:
        if not obsid.isdigit():
            casalog.post('*** ERROR: This version does not support multiple OBSERVATION_ID selection.', 'ERROR')
            casalog.post('*** ERROR: Exiting invgain.', 'ERROR')
            return
        
        selection=selection+'OBSERVATION_ID=='+obsid+'&&'
    
    tb.open(caltable,nomodify=False)
    
    if len(selection)>0:
        selection=selection[:-2]
        subt=tb.query(selection)
        temp=subt.getcol('CPARAM')
        subt.putcol('CPARAM',1/temp)
        subt.done()
    else:
        temp=tb.getcol('CPARAM')
        tb.putcol('CPARAM',1/temp)
    
    tb.done()
