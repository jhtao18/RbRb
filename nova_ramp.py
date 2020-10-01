from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connectiontable')

MHz = 1e6
cent = 148.75*MHz#145.625*MHz
scan_span = 3.75*MHz

def linramp(t, duration, low, high):
	f = t/duration
	return (high-low)/duration*t + low

start()
t = 0
Repump.setfreq(t, 82.231*MHz)
Cooling.setamp(t, 1)
Repump.setamp(t, 1)
xx = 1
Cooling.setfreq(t,cent)
ao2.constant(t+0.1, value=5)
for f in range(round(xx*scan_span/MHz)):
	print(-f*MHz+cent)
	t+=1
	do0.go_high(t)
	do2.go_high(t)
	Cooling.frequency.ramp(t, 0.5, -(f-1)*MHz+cent, -f*MHz+cent, samplerate = 5)
	t+=3.5
	do2.go_low(t)
	do0.go_low(t)
for f in range(round(xx*scan_span/MHz)):
	print(f*MHz+cent-xx*scan_span)
	t+=1
	do0.go_high(t)
	do2.go_high(t)
	Cooling.frequency.ramp(t, 0.5, (f-1)*MHz+cent-xx*scan_span, f*MHz+cent-xx*scan_span, samplerate = 5)
	t+=3.5
	do2.go_low(t)
	do0.go_low(t)
# duration = xx
# Cooling.frequency.ramp(t, duration, cent-xx*scan_span/2, cent+xx*scan_span/2, samplerate = 50)
# t+=duration
# Cooling.frequency.ramp(t, duration, cent+xx*scan_span/2, cent-xx*scan_span/2, samplerate = 50)
# t+=duration
stop(t)