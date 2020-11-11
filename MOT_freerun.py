from labscript import *
from labscriptlib.common.utils import Limits
from labscriptlib.common.functions import *
from labscript_utils import import_or_reload

import_or_reload('labscriptlib.RbRb.connection_table')
MHz = 1e6
us = 1e-6
ms = 1e-3
nt_step = 0.15*ms
#calibrated intensity zeros
probe_z = -0.06
cool_z = -0.058
rep_z = -0.057
opt_z = -0.06
#

def set_freq(ch, t, freq):
    ch.setfreq(t, freq)
    # ch.setfreq(t+nt_step, freq)
    
def set_amp(ch, t, amp):
    ch.setamp(t, amp)
    # ch.setamp(t+nt_step, amp)

class MOT:
    def __init__(self, t, cooling_freq, repump_freq, quad_curr):
        #Novatech beatnote lock
        self.cooling_freq = cooling_freq
        self.repump_freq = repump_freq
        self.quad_curr = quad_curr
        quad_MOT.constant(t, 1)
        transport1.constant(t, 1)
        transport2.constant(t, 1)
        transport3.constant(t, 1)
        t1_0.go_low(t)
        t1_1.go_low(t)
        t2_0.go_low(t)
        t2_1.go_low(t)
        t3_0.go_low(t)
        t3_1.go_low(t)
        t4_0.go_low(t)
        t4_1.go_low(t)
        set_freq(Cooling, t, cent)
        set_freq(Repump, t, self.repump_freq)
        set_amp(Repump, t, 1)
        set_amp(Cooling, t, 1)
        evap_switch.go_low(t)
        evap_int.constant(t, 0)
        self.t_t, self.t_I = [], []
        MOT_Probe_AOM.go_low(t)
        Probe_int.constant(t, probe_z)
        Cooling_AOM.go_low(t)
        Repump_AOM.go_low(t)
        OptPump_AOM.go_low(t)
        
    # IAN: make "DefaultValues" method that init calls and that you call at end end of sequence.
    
    def load(self, start_time, load_time, B_bias, UV_onoff):
        t = start_time
        if UV_onoff:
            UV.go_high(t)
        UV.go_low(t+min(load_time,dur_UV))
        t1_enable.go_high(t-1*ms)
        quad_MOT.constant(t, value=self.quad_curr)
        Cooling_AOM.go_high(t)
        Repump_AOM.go_high(t)
        MOT_Probe_AOM.go_low(t)
        self.set_bias(t, B_bias)
        Cool_int.constant(t, mot_cool_int) # IBS: should be optimized, and set so 0 is 0
        Repump_int.constant(t, mot_rep_int)# IBS: should be optimized, and set so 0 is 0
        Shutter_Cooling.open(t)
        Shutter_Repump.open(t)
        Shutter_Opt_pumping.open(t) # Note: this is due to the minimum exposure 5ms of SR475, move to PG cooling.
        t+=load_time
        return t
        
    def set_bias(self, start, B_bias):
        x_shim.constant(start, B_bias[0], units='A')
        y_shim.constant(start, B_bias[1], units='A')
        z_shim.constant(start, B_bias[2], units='A')
        
        
if __name__ == '__main__':
    B_bias_MOT = np.array([B_bias_mot_x,B_bias_mot_y, B_bias_mot_z])
    start()
    t = 0.2

    New_MOT = MOT(t, cooling_freq=cent, repump_freq=repump_freq, quad_curr=quad) #82.231 1->1' 84.688 1->2'
    
    t = New_MOT.load(t, load_time, B_bias_MOT, UV_onoff=False)
    stop(t)
    