from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
#from .MOT_load import *
import_or_reload('labscriptlib.RbRb.connection_table')
MHz = 1e6
us = 1e-6
ms = 1e-3

def linramp(t, duration, low, high):
	return (high-low)/duration*t + low


if __name__ == '__main__':
	start()
	t = 0		
	Repump.setamp(t, 1)
	Cooling.setamp(t, 1)
	Repump.setfreq(t, 82.231*MHz)
	print(t)
	Cooling.setfreq(0, cent)
	
	Cooling.setfreq(2, cent-5*MHz)
	Cooling.setamp(2.001, 1)
	Cooling.setfreq(5, cent+10*MHz)
	Cooling.setamp(5.001, 1)
	
	#New_MOT.fluorescence(0,t)
	t=5
	t+=10
	Cooling.setfreq(15, cent)
	Cooling.setamp(14.999, 1)
	stop(t)