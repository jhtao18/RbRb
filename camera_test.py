from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
#from .MOT_load import *
import_or_reload('labscriptlib.RbRb.connection_table')

if __name__ == '__main__':
	start()
	t = 0
	MOT_flea.expose(t,'abs_img', trigger_duration=0.1, frametype='atom')
	t+=0.2
	#MOT_flea.expose(t,'abs_img', trigger_duration=0.1, frametype='probe')
	t+=0.2
	stop(t)