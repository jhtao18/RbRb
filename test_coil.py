from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

start()
t = 0
dur = 500*1e-3
high = -1
low = -0.05
# t1_enable.go_low(0)
t4_enable.go_high(0.01)
t3_enable.go_high(0.01)
t4_1.go_high(0.01)
t3_1.go_high(0.01)
transport3.constant(0.01,low)
t+=dur
transport2.customramp(t, dur, HalfGaussRamp, -1.5, 0, 1.5*dur, samplerate=1/0.002)
t+=transport3.customramp(t, dur, HalfGaussRamp, low, high, dur, samplerate=1/0.002)
t+=transport3.customramp(t, dur, LineRamp, high, low, samplerate=1/0.002)
# transport3.constant(t, high)
# t+=dur
transport3.constant(t, low)
t+=dur
t4_enable.go_low(t)
t3_enable.go_low(t)
transport3.constant(t, 0)
t+=0.2
start = 0
end = t

testin0.acquire('curr0', start, end)
testin1.acquire('curr1', start, end)
testin2.acquire('curr2', start, end)    
testin3.acquire('curr3', start, end)    
testin4.acquire('fluo', start, end)
testin5.acquire('biasx', start, end)
testin6.acquire('biasy', start, end)
stop(t)