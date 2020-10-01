from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import_or_reload('labscriptlib.RbRb.connectiontable')

start()
t=0
path = 'C:/Users/RbRb/Desktop/monitor1.png'
monitor1.save_screenshot(path)
t+=5
stop(t)