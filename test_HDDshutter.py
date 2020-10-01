from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

start()
t = 0
start = t
OptPump_AOM.go_high(t)
t += 1
Shutter_Opt_pumping.open(t)
t += 1
Shutter_Opt_pumping.close(t)
t += 1
end = t
ai2.acquire('fluo', start, end)

stop(t)