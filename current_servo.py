from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

def squarewave(t, duration, freq, low, high):
	f = t/duration
	return (high-low)*(np.round(t*freq) % 2) + low

start()
t = 0
# t += quad_MOT.customramp(t, 10, squarewave, 10, -0.7, -0.8, samplerate = 1e3)
quad_MOT.constant(0.1, -2)
t1_enable.go_high(0.1)
t=0.1
t+=0.02
quad_MOT.constant(t, 1)
t1_enable.go_low(t)
t+=0.01
testin1.acquire('fluo', 0, t)
testin0.acquire('curr', 0, t)
stop(t)