from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import_or_reload('labscriptlib.RbRb.connection_table')

start()
t = 0
ms=1e-3
duration=0.024*ms
t+=0.5
start = t
PI.expose(start-0.3,'abs_img', trigger_duration=0.024*ms, frametype='bg')
t+=10
PI.expose(t-0.01,'abs_img', trigger_duration=0.024*ms, frametype='bg2')
t+=10
PI.expose(t-0.01,'abs_img', trigger_duration=0.024*ms, frametype='bg3')
t+=0.5
print(PI.camera_attributes)
stop(t)