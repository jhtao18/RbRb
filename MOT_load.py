from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connectiontable')
MHz = 1e6
us = 1e-6
ms = 1e-3

#cent = 146.75*MHz#145.625*MHz
cent*=MHz

def load_MOT(t):
	Repump.setfreq(t, 82.231*MHz)
	Cooling.setfreq(t,cent)
	Repump.setamp(t, 1)
	Cooling.setamp(t, 1)
	quad_MOT.constant(t+0.01, value=quad)
	
	Cooling_AOM.go_high(t)
	Repump_AOM.go_high(t)
	MOT_Probe_AOM.go_low(t)
	t+=load_time
	Cooling_AOM.go_low(t)
	Repump_AOM.go_low(t)
	ai1.acquire('fluo', 0.01, t)
	return t

if __name__ == '__main__':
	start()
	t = 0
	t+=1
	t= load_MOT(t)
	t+=0.1
	stop(t)