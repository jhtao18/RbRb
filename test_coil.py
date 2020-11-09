from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

start()
t = 0
dur = 100*1e-3
high = -0.7
low = -0.05
# t1_enable.go_low(0)
t2_enable.go_high(0.01)
# t3_enable.go_high(0.01)
# t2_1.go_high(0.01)
# t3_1.go_high(0.01)
transport1.constant(0.01,high)
t+=dur
# transport2.customramp(t, dur, HalfGaussRamp, -1.5, 0, 1.5*dur, samplerate=1/0.002)
# t+=transport1.customramp(t, dur/2, LineRamp, low, 3*high/4, samplerate=1/0.002)
# t+=transport1.customramp(t, dur/2, LineRamp, 3*high/4, high, samplerate=1/0.002)
# t+=transport1.customramp(t, dur, LineRamp, high, low, samplerate=1/0.002)
# transport3.constant(t, high)
# t+=dur
transport1.constant(t, low)
t+=dur
t2_enable.go_low(t)
# t3_enable.go_low(t)
transport1.constant(t, 0)
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
# testin0_table.acquire('B_sensor', start, end)
stop(t)