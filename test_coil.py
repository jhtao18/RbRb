from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connectiontable')

start()
t = 0
a6.constant(t, value=5.8)
t += 0.5
a6.constant(t, value=0)
t += 8
stop(t)