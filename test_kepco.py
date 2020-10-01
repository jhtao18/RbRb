from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

start()
t = 0
OptPump_AOM.go_high(t)
MOT_Probe_AOM.go_high(t)
dur = 100*1e-3
high = 10
low = -10
z_shim.constant(t,low)
t+=dur
z_shim.constant(t, high)
t+=0.5*dur

z_shim.constant(t,0)
t+=3
stop(t)