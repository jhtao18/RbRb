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
import_or_reload('labscriptlib.RbRb.transport.new_transport_optimisation')
from labscriptlib.RbRb.transport.new_transport_optimisation import transport
tswitch = transport.t_switchover
class current_switch:
    def __init__(self, time_t0_on, time_t0_off, time_t1_on, time_t1_off, time_te_on, time_te_off):
        self.time_t0_on = time_t0_on
        self.time_t0_off = time_t0_off
        self.time_t1_on = time_t1_on
        self.time_t1_off = time_t1_off
        self.time_te_on = time_te_on
        self.time_te_off = time_te_off
        
def set_freq(ch, t, freq):
    ch.setfreq(t, freq)
    # ch.setfreq(t+nt_step, freq)
    
def set_amp(ch, t, amp):
    ch.setamp(t, amp)
    # ch.setamp(t+nt_step, amp)

def Channel_n(n):
    if n==0:
        return 4#biasx, t_biasx
    if n in [1,5,9]:
        return 0#curr0, t0
    if n in [2,6]:
        return 1#curr1, t1
    if n in [3,7,10]:
        return 2#curr2, t2
    if n in [4,8,11]:
        return 3#np.array(curr3), t3
        
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
        set_freq(Cooling, t, cent)
        set_freq(Repump, t, self.repump_freq)
        set_amp(Repump, t, 1)
        set_amp(Cooling, t, 1)
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
        
    def compress(self, start, duration, curr_s, curr_e, freq_c_s, freq_c_e, B_bias_start, B_bias_end):
        quad_MOT.customramp(start,  duration, HalfGaussRamp, curr_s, curr_e, duration, samplerate=1/CMOT_step)
        x_shim.customramp(start, duration, HalfGaussRamp, B_bias_start[0], B_bias_end[0], duration, samplerate=1/CMOT_step, units='A')
        y_shim.customramp(start, duration,HalfGaussRamp, B_bias_start[1], B_bias_end[1], duration, samplerate=1/CMOT_step, units='A')
        z_shim.customramp(start, duration, HalfGaussRamp, B_bias_start[2], B_bias_end[2], duration, samplerate=1/CMOT_step, units='A')      
        Cooling.frequency.customramp(start, duration, HalfGaussRamp, freq_c_s, freq_c_e, duration, samplerate=1/CMOT_step) # IBS: note novatech is limited to 110 us steps!!! just a note
        self.quad_curr = curr_e
        Cool_int.constant(start, com_cool_int) # IBS: should be optimized, and set so 0 is 0
        Repump_int.constant(start, com_rep_int) # IBS: should be optimized, and set so 0 is 0
        return start + duration
        
    def move(self, start, duration, B_bias_start, B_bias_end):
        x_shim.customramp(start, duration, LineRamp, B_bias_start[0], B_bias_end[0], samplerate=1/0.2/ms, units='A')
        y_shim.customramp(start, duration, LineRamp, B_bias_start[1], B_bias_end[1], samplerate=1/0.2/ms, units='A')
        z_shim.customramp(start, duration, LineRamp, B_bias_start[2], B_bias_end[2], samplerate=1/0.2/ms, units='A')
        return start + duration
        
    def set_bias(self, start, B_bias):
        x_shim.constant(start, B_bias[0], units='A')
        y_shim.constant(start, B_bias[1], units='A')
        z_shim.constant(start, B_bias[2], units='A')
        
    def pol_grad(self, start, duration, freq_c_s, freq_c_e, B_bias):
        t1_enable.go_low(start)
        self.set_bias(start, B_bias) # IBS: should be optimized (critical) done
        Cooling.frequency.customramp(start, duration-opt_adv, LineRamp, freq_c_s, freq_c_e, samplerate=1/mol_freq_step) # IBS: timing code is future bug. 
        Cool_int.constant(start, mol_cool_int)
        # Repump_int.constant(start, mol_rep_int_end)
        Repump_int.customramp(start, duration, LineRamp, mol_rep_int_start, mol_rep_int_end, samplerate=1/mol_freq_step)
        t = start+duration
        return t
        
    def opt_pump(self, start, duration):
        Cooling_AOM.go_low(start-opt_adv)
        Cool_int.constant(start, cool_z)
        set_freq(Cooling, start-opt_adv, res+opt_f*MHz)
        # IAN: Repump power matters here
        OptPump_AOM.go_high(start)
        OptPump_AOM.go_low(start+duration)
        OptPump_int.constant(start, OptPumpint)
        OptPump_int.constant(start+duration, opt_z)
        Repump_int.constant(start, opt_rep_int)
        Repump_AOM.go_low(start+duration)
        Repump_int.constant(start+duration, rep_z)
        self.set_bias(start-0.5*ms, np.array(B_bias_optpump)) # IAN: How fast does bias actually change? (Field)
        # def parabolay(t, dur, h, c): return -t*(t-dur)*h/dur**2 *4 +c
        # b_mi = (1,7)
        # x_shim.customramp(start+duration, 2*ms, LineRamp, B_bias_optpump[0], 0.5*B_bias_optpump[0], samplerate=1/0.02/ms, units='A')
        # y_shim.customramp(start+duration, 2*ms, parabolay, 1, B_bias_optpump[1], samplerate=1/0.02/ms, units='A')
        # z_shim.customramp(start+duration, 2*ms, LineRamp, B_bias_optpump[2], 0.5*B_bias_optpump[2], samplerate=1/0.02/ms, units='A')
        
        # x_shim.customramp(start+duration, 2*ms, LineRamp, B_bias_optpump[0], b_mi[0], samplerate=1/0.02/ms, units='A')
        # y_shim.customramp(start+duration, 2*ms, parabolay, 1, B_bias_optpump[1], samplerate=1/0.02/ms, units='A')
        # z_shim.customramp(start+duration, 2*ms, LineRamp, B_bias_optpump[2], b_mi[1], samplerate=1/0.02/ms, units='A')
        # x_shim.customramp(start+duration+2*ms, 2.5*ms, LineRamp, b_mi[0], -B_bias_optpump[0]/np.linalg.norm(B_bias_optpump)*0.7, samplerate=1/0.02/ms, units='A')
        # y_shim.customramp(start+duration+2*ms, 2*ms, parabolay, 1, B_bias_optpump[1], samplerate=1/0.02/ms, units='A')
        # z_shim.customramp(start+duration+2*ms, 2*ms, LineRamp, b_mi[1], -1*B_bias_optpump[2]/np.linalg.norm(B_bias_optpump)*0.7, samplerate=1/0.02/ms, units='A')
        return start+duration
        
    def mag_trap(self, start, duration, quad_start, B_bias_start, B_bias_final):
        Cooling.setfreq(start+10*ms, res)
        # Cooling.setfreq(start+duration-50*ms, res)
        Shutter_Cooling.close(start+10*ms)
        Shutter_Repump.close(start+10*ms) # maybe ad 10 ms here because of OP.
        Shutter_Probe.close(start+10*ms)
        Shutter_Opt_pumping.close(start+10*ms) # Ian: When does shutter open?  So in this function command the shutter to open "6 ms" in advance!  Just rely on shutter class.
        
        t1_enable.go_high(start-0.1*ms) # IAN: precommand by some amount so it is rising during end of OP.
        quad_MOT.constant(start-0.2*ms, value=quad_start)
        x_shim.customramp(start+quad_bias_delay*2, bias_dur*ms, LineRamp, B_bias_mol[0], B_bias_start[0], samplerate=1/0.2/ms, units='A') # IBS: make equal to PG cooling at first. 
        y_shim.customramp(start+quad_bias_delay*2, bias_dur*ms, LineRamp, B_bias_mol[1], B_bias_start[1], samplerate=1/0.2/ms, units='A')
        z_shim.customramp(start+quad_bias_delay*2, bias_dur*ms, LineRamp, B_bias_mol[2], B_bias_start[2], samplerate=1/0.2/ms, units='A')
        quad_MOT.customramp(start+hold_time_start*ms, dur_quad_ramp*ms, LineRamp, quad_start, quad_com, samplerate=1/0.5/ms)
        x_shim.customramp(start+quad_bias_delay+hold_time_start*ms, bias_dur*ms, LineRamp, B_bias_start[0], B_bias_final[0], samplerate=1/0.2/ms, units='A') # IBS: make equal to PG cooling at first. 
        y_shim.customramp(start+quad_bias_delay+hold_time_start*ms, bias_dur*ms, LineRamp, B_bias_start[1], B_bias_final[1], samplerate=1/0.2/ms, units='A')
        z_shim.customramp(start+quad_bias_delay+hold_time_start*ms, bias_dur*ms, LineRamp, B_bias_start[2], B_bias_final[2], samplerate=1/0.2/ms, units='A')
        return start+duration
        
    def deload(self, start):
        Cooling_AOM.go_low(start-0*ms)
        Repump_AOM.go_low(start)
        OptPump_AOM.go_low(start)
        Cool_int.constant(start, value=0, units='Vshift')
        Repump_int.constant(start, value=0, units='Vshift')
        OptPump_int.constant(start, value=0, units='Vshift')
        # Shutter_Cooling.close(start)
        # Shutter_Repump.close(start)
        quad_MOT.constant(start,value=1)
        transport1.constant(start,value=1)
        transport2.constant(start,value=1)
        transport3.constant(start,value=1)
        t1_enable.go_low(start)
        t2_enable.go_low(start)
        t3_enable.go_low(start)
        t4_enable.go_low(start)
        self.set_bias(start, B_bias_mol) # Dont want to do this!  Want to go to "true zero"
        
        # t3_0.go_high(start)
        # t3_1.go_high(start)
        # t3_enable.go_high(start)
        # transport2.constant(start, -0.1)
        return start
        
    def depump(self, start, duration):
        Repump_AOM.go_low(start)
        Repump_int.constant(start, -0.057)
        return start+duration
        
    def fluorescence(self, start, end):
        testin0.acquire('curr0', start, end)
        testin1.acquire('curr1', start, end)
        testin2.acquire('curr2', start, end)    
        testin3.acquire('curr3', start, end)    
        testin4.acquire('fluo', start, end)
        testin5.acquire('biasx', start, end)
        testin6.acquire('biasy', start, end)
        Repump_monitor.acquire('Repump_monitor', start, end)
        Cooling_monitor.acquire('Cooling_monitor', start, end)
        # testin0_table.acquire('B_sensor', start, end)
        return 'Collected as fluo'
        
    def probe_yz(self, start, duration, frametype):
        if not frametype=='bg':
            do8.go_high(start)
            # Probe_int.constant(start-0.2*ms, probe_MOT_int) # IAN: analog is fast
            Probe_int.constant(start, probe_MOT_int)
            MOT_Probe_AOM.go_high(start)
            MOT_Probe_AOM.go_low(start+duration)
            Probe_int.constant(start+duration, probe_z)

            set_freq(Cooling, start-prob_adv, res+0.0*MHz) # IAN: usually better to set this at the end of OP
            
            # print(start)
            Repump_AOM.go_high(start)
            Repump_int.constant(start, 0.6) #0.6 before
            # Repump_int.constant(start, -0.057)
            # Repump_AOM.go_low(start)
            # Repump_int.constant(start, rep_z)
            # Shutter_Repump.open(start-prob_adv-10*ms)
            
            Shutter_Probe.open(start-3*ms)
        MOT_YZ_flea.expose(start-0.01*ms,'abs_img', trigger_duration=duration+0.01*ms, frametype=frametype) # IAN: needs ~10 us pretrigger to get our of contineous clean mode.
        
    def probe_xy(self, start, duration, frametype):#absorption imaging
        if not frametype=='bg':
            
            OptPump_int.constant(start-0.0*ms, probe_xy_int)
            OptPump_AOM.go_high(start)
            Shutter_Opt_pumping.open(start-0.9*ms)
            OptPump_AOM.go_low(start+duration)
            OptPump_int.constant(start+duration, -0.06)
            set_freq(Cooling, start-prob_adv, res+probe_xy_freq*MHz) 
            
            # self.set_bias(start-1*ms, B_bias=-B_bias_optpump/np.linalg.norm(B_bias_optpump)*0.2)
            
            Cooling_AOM.go_low(start-t_of_f)
            Cool_int.constant(start-t_of_f, value=0, units='Vshift')
            # Repump_AOM.go_low(start-t_of_f)
            # Repump_int.constant(start-t_of_f, -0.057)
            Repump_AOM.go_high(start)
            Repump_int.constant(start, 1) #0.6 before
            Shutter_Repump.open(start-1*ms)
            
            # Cooling_AOM.go_high(start+duration+1*ms)
            # Cool_int.constant(start+duration+1*ms, value=mot_cool_int, units='Vshift')
        MOT_XY_flea.expose(start,'abs_img', trigger_duration=duration, frametype=frametype) # IAN: needs ~10 us pretrigger to get our of contineous clean mode.
        
    def probe_fluo(self, start, duration, frametype):
        set_freq(Cooling, start-prob_adv, res+detun/16*MHz)
        Cooling_AOM.go_high(start)
        Cool_int.constant(start, mot_cool_int)
        # Cooling_AOM.go_low(start+duration)
        # Cool_int.constant(start+duration, 0)
        Repump_AOM.go_high(start)
        Repump_int.constant(start, mot_rep_int)
        # Repump_AOM.go_low(start+duration)
        # Repump_int.constant(start+duration, 0)
        Shutter_Cooling.go_high(start-prob_adv*6.5)
        Shutter_Repump.go_high(start-prob_adv*1)
        print(start)
        MOT_YZ_flea.expose(start-0.01*ms,'fluo_img', trigger_duration=duration+0.01*ms, frametype=frametype)
        return start+duration
        
    def probe_science(self, start, duration, frametype):#absorption imaging
        if not frametype=='bg':
            Probe_int.constant(start-0.2*ms, probe_Science_int) # IAN: analog is fast
            MOT_Probe_AOM.go_high(start)
            MOT_Probe_AOM.go_low(start+duration)
            
            # Shutter_Probe.open(start-prob_adv-3*ms)
            set_freq(Cooling, start-prob_adv, res)
            
        Science_flea.expose(start-0.01*ms,'science_img', trigger_duration=duration, frametype=frametype)
        
        
    def new_transport_switch(self, start, duration, switch):#tswitch, order='normal'):
        t = start
        for ch in range(4):
            for time in switch[ch].time_t0_on:
                # print(switch[ch].time_t0_on)
                exec("t"+str(ch+1)+"_0.go_high("+str(t+time)+")")
            for time in switch[ch].time_t0_off:
                exec("t"+str(ch+1)+"_0.go_low("+str(t+time)+")")
            for time in switch[ch].time_t1_on:
                exec("t"+str(ch+1)+"_1.go_high("+str(t+time)+")")
            for time in switch[ch].time_t1_off:
                exec("t"+str(ch+1)+"_1.go_low("+str(t+time)+")")
            for time in switch[ch].time_te_on:
                exec("t"+str(ch+1)+"_enable.go_high("+str(t+time)+")")
            # for time in switch[ch].time_te_off:
                # exec("t"+str(ch+1)+"_enable.go_low("+str(t+time)+")")

        # if order=='normal':
            # t2_enable.go_high(t)
            # t3_enable.go_high(t + tswitch[0])
            # t4_enable.go_high(t + tswitch[1]-0*ms)
            # t1_enable.go_low(t + tswitch[1])


            # t1_0.go_high(t + tswitch[2])
            # t2_enable.go_low(t + tswitch[2])
            # t1_enable.go_high(t + tswitch[2])

            # t2_0.go_high(t + tswitch[3])
            # t3_enable.go_low(t + tswitch[3])
            # t2_enable.go_high(t + tswitch[3])

            # t3_0.go_high(t + tswitch[4])
            # t4_enable.go_low(t + tswitch[4])
            # t3_enable.go_high(t + tswitch[4])

            # # t4_0.go_high(t + tswitch[5])
            # # t1_enable.go_low(t + tswitch[5])
            # # t4_enable.go_high(t + tswitch[5])

            # # t1_0.go_low(t + tswitch[6])
            # # t1_1.go_high(t + tswitch[6])
            # # t2_enable.go_low(t + tswitch[6])
            # # t1_enable.go_high(t + tswitch[6])

            # # t3_0.go_low(t + tswitch[7])
            # # t3_1.go_high(t + tswitch[7])
            # # t2_enable.go_low(t + tswitch[8])
            
            
            # # t4_0.go_low(t + tswitch[8])
            # # t4_1.go_high(t + tswitch[8])
            
            # # t1_enable.go_low(t + tswitch[9])
        # else:
            # # t2_enable.go_low(2*start+duration-t)
            # # t3_enable.go_low(2*start+duration-t - tswitch[0])
            # # t4_enable.go_low(2*start+duration-t - tswitch[1])
            # # t1_enable.go_high(2*start+duration-t - tswitch[1])


            # # t1_0.go_low(2*start+duration-t - tswitch[2])
            # # t2_enable.go_high(2*start+duration-t - tswitch[2])
            # # t1_enable.go_low(2*start+duration-t - tswitch[2])

            # # t2_0.go_low(2*start+duration-t - tswitch[3])
            # # t3_enable.go_high(2*start+duration-t - tswitch[3])
            # # t2_enable.go_low(2*start+duration-t - tswitch[3])

            # # t3_0.go_low(2*start+duration-t - tswitch[4])
            # # t4_enable.go_high(2*start+duration-t - tswitch[4])
            # # t3_enable.go_low(2*start+duration-t - tswitch[4])

            # # t4_0.go_low(2*start+duration-t - tswitch[5])
            # # t1_enable.go_high(2*start+duration-t - tswitch[5])
            # # t4_enable.go_low(2*start+duration-t - tswitch[5])

            # # t1_0.go_high(2*start+duration-t - tswitch[6])
            # # t1_1.go_low(2*start+duration-t - tswitch[6])
            # # t2_enable.go_high(2*start+duration-t - tswitch[6])
            # # t1_enable.go_low(2*start+duration-t - tswitch[6])

            # # t3_0.go_high(2*start+duration-t - tswitch[7])
            # # t3_1.go_low(2*start+duration-t - tswitch[7])
            
            
            # # t4_0.go_high(2*start+duration-t - tswitch[8])
            # # t4_1.go_low(2*start+duration-t - tswitch[8])
            
            # # t1_enable.go_high(2*start+duration-t - tswitch[9])
            # pass
            
    def transport_currents(self, t, duration, transport_currents_interp_ch):
        return transport_currents_interp_ch(t)
        
    def new_transport(self, start, duration, B_bias_start, bias_r_yx, inverse=False):
        t = start
        # import_or_reload('labscriptlib.RbRb.transport.new_transport_optimisation')
        # from labscriptlib.RbRb.transport.new_transport_optimisation import transport
        # tswitch = transport.t_switchover
        # print(t, tswitch)
        curr_ratio=[curr_r0, curr_r1, curr_r2, curr_r3]
        from scipy.interpolate import interp1d
        self.t_t = np.arange(0, duration, transport_step)
        I_coils = transport.currents_at_time(self.t_t)
        if inverse:
            I_coils = np.array([np.flip(I_coil) for I_coil in I_coils])
        # #-------------#probe along the line at the center of certain coils.
        # t_coil_probe = transport.t_coils[ind_probe_coils]-2*ms
        # # ch_coil_probe = Channel_n(ind_probe_coils)
        # if t_coil_probe<=duration:
            # ind_t_coil_probe_start = round(t_coil_probe/duration*len(self.t_t))
            # ind_t_coil_probe_end = min( round((t_coil_probe+dur_probe_coils)/duration*len(self.t_t)), round((t+duration)/duration*len(self.t_t)))
            # # print(t_coil_probe, t_coil_probe+dur_probe_coils, len(self.t_I[0]))
            # curr_coil1 = I_coils[ind_probe_coils, ind_t_coil_probe_start]
            # curr_coil2 = I_coils[ind_probe_coils-1, ind_t_coil_probe_start]
            # curr_coil3 = I_coils[ind_probe_coils+1, ind_t_coil_probe_start]
            # # print(curr_coil1)
            # for coil in range(len(I_coils)):
                # I_coils[coil, ind_t_coil_probe_start:] = -0.01
            # I_coils[ind_probe_coils,ind_t_coil_probe_start:ind_t_coil_probe_end] = curr_coil1
            # I_coils[ind_probe_coils-1,ind_t_coil_probe_start:ind_t_coil_probe_end] = curr_coil2
            # I_coils[ind_probe_coils+1,ind_t_coil_probe_start:ind_t_coil_probe_end] = curr_coil3
            # # if t_coil_probe+dur_probe_coils > dur_transport:
            # t1_enable.go_low(start+t_coil_probe+dur_probe_coils )
            # t2_enable.go_low(start+t_coil_probe+dur_probe_coils)
            # t3_enable.go_low(start+t_coil_probe+dur_probe_coils)
            # t4_enable.go_low(start+t_coil_probe+dur_probe_coils)
            # self.probe_yz(start+t_coil_probe+dur_probe_coils+t_of_f, probe_yz_time, 'atom')
            # exec("New_MOT.probe_"+probe_direction+"(start+t_coil_probe+dur_probe_coils+t_of_f+0.2, probe_"+probe_direction+"_time, 'probe')")
        # #-----------------probe along the line
        
        self.t_I = np.zeros((6,len(self.t_t)))
        for ch in [0,2,3]:
            self.t_I[ch,:] = transport.currents_for_channel(self.t_t, duration, ch+1, ratio=-1/40*curr_ratio[ch], B_bias=B_bias_start, I_coils=I_coils)
        self.t_I[1,:] = transport.currents_for_channel(self.t_t, duration, 1+1, ratio=-1/40*10/3*curr_ratio[ch], B_bias=B_bias_start, I_coils=I_coils)
        self.t_I[4,:] = transport.currents_for_channel(self.t_t, duration, 4+1, ratio=-0.5, B_bias=B_bias_start[0]) 
        self.t_I[5,:] = transport.currents_for_channel(self.t_t, duration, 4+1, ratio=-0.5*bias_ratio_yx, B_bias=B_bias_start[1])
        transport_currents_interp = [interp1d(
            self.t_t, self.t_I[ch,:], 'cubic', fill_value='extrapolate'
        ) for ch in range(6)]
        
        coil_sw_list = ['','00','00','00','00','10','10','10','10','01','01','01']
        switch = [current_switch([],[],[],[],[],[]) for ch in range(4)]
        for coil in range(1,len(I_coils)):
            coil_dur = self.t_t[np.argwhere(I_coils[coil]>0)]
            if len(coil_dur)>0:
                st, end = coil_dur[0][0], coil_dur[-1][0]
                switch[Channel_n(coil)].time_te_on.append(st)
                switch[Channel_n(coil)].time_te_off.append(end)
                coil_sw = coil_sw_list[coil]
                if coil_sw[0]=='0':
                    switch[Channel_n(coil)].time_t0_off.append(st)
                elif coil_sw[0]=='1':
                    switch[Channel_n(coil)].time_t0_on.append(st)
                if coil_sw[1]=='0':
                    switch[Channel_n(coil)].time_t1_off.append(st)
                elif coil_sw[1]=='1':
                    switch[Channel_n(coil)].time_t1_on.append(st)

        
        # x_shim.customramp(t, bias_dur, LineRamp, B_bias_start[0], B_bias_end[0], samplerate=1/(bias_dur/2), units='A')
        # y_shim.customramp(t, bias_dur, LineRamp, B_bias_start[1], B_bias_end[1], samplerate=1/(bias_dur/2), units='A')
        x_shim.customramp(t, duration, self.transport_currents, transport_currents_interp[4], samplerate=1/transport_step, units='A')
        y_shim.customramp(t, duration, self.transport_currents, transport_currents_interp[5], samplerate=1/transport_step, units='A')
        # z_shim.customramp(t, bias_dur, LineRamp, B_bias_start[2], B_bias_end[2], samplerate=1/transport_step, units='A')
       
        #-------------transport starts--------------------
        # Select which current supply powers which coil(pair) at each switchover time:
        self.new_transport_switch(t, duration, switch)
        quad_MOT.customramp(t, duration, self.transport_currents, transport_currents_interp[0], samplerate=1/transport_step)
        transport1.customramp(t, duration, self.transport_currents, transport_currents_interp[1], samplerate=1/transport_step)
        transport2.customramp(t, duration, self.transport_currents, transport_currents_interp[2], samplerate=1/transport_step)
        transport3.customramp(t, duration, self.transport_currents, transport_currents_interp[3], samplerate=1/transport_step)
        t += duration
        #--------------transport ends------------------
        
        # #----------inverse---------------
        # # #probe along the line
        # # if t_tran_probe>duration:
            # # ind_t_tran_probe = round((1-t_tran_probe/duration)*len(self.t_I[0]))
            # # for ch in [0,1,2,3]:
                # # self.t_I[ch,0:ind_t_tran_probe] = 1
            # # for ch in [4,5]:
                # # self.t_I[ch,0:ind_t_tran_probe] = 0
            # # self.deload(start+t_tran_probe)
            # # self.probe_yz(start+t_tran_probe+t_of_f, probe_yz_time, 'atom')
        # # #probe along the line
        # self.new_transport_switch(t, duration, tswitch, order='inverse')
        # self.t_I = np.array([np.flip(self.t_I[ch,:]) for ch in range(0,4)])
        # transport_currents_interp = [interp1d(self.t_t, self.t_I[ch,:], 'cubic', fill_value='extrapolate') for ch in range(4)]
        # quad_MOT.customramp(t, duration, self.transport_currents, transport_currents_interp[0], samplerate=1/transport_step)
        # transport1.customramp(t, duration, self.transport_currents, transport_currents_interp[1], samplerate=1/transport_step)
        # transport2.customramp(t, duration, self.transport_currents, transport_currents_interp[2], samplerate=1/transport_step)
        # transport3.customramp(t, duration, self.transport_currents, transport_currents_interp[3], samplerate=1/transport_step)
        # # x_shim.customramp(t, bias_dur, LineRamp, B_bias_end[0], B_bias_start[0], samplerate=1/(bias_dur/2), units='A')
        # # y_shim.customramp(t, bias_dur, LineRamp, B_bias_end[1], B_bias_start[1], samplerate=1/(bias_dur/2), units='A')
        # # z_shim.customramp(t, bias_dur, LineRamp, B_bias_end[2], B_bias_start[2], samplerate=1/(bias_dur/2), units='A')
        # t += duration

        return t
        
    def evap(self, start, duration):
        t = start
        evap_switch.go_high(t)
        evap_int.constant(t, 0.6) # try 0.5 for full on (or measure)? Untill satuate, which is full on. so he wants max? One is max
        Evap_rf.setamp(t, 0.2) # IBS: use EITHER this or evap_int as a scan paramter, with the other set to max.
        t += Evap_rf.frequency.customramp(t, duration, LineRamp, initial_evap_freq*MHz, final_evap_freq*MHz, samplerate = 1/evap_step)
        evap_switch.go_low(t)
        evap_int.constant(t, 0)
        Evap_rf.setamp(t, 0)
        return t
        
if __name__ == '__main__':
    probe_yz_time = 0.024*ms
    probe_xy_time = 0.013*ms
    sci_probe_time = 0.048*ms
    probe_fluo_time = 0.05*ms

    B_bias_mol = (0,0,0)#*np.array([B_bias_mol_x,B_bias_mol_y,B_bias_mol_z])
    B_bias_optpump = np.array([B_bias_optpump_x,B_bias_optpump_y,B_bias_optpump_z])
    B_bias_capture_quad = np.array([B_bias_capture_quad_x,B_bias_capture_quad_y,B_bias_capture_quad_z])
    B_bias_final_quad = np.array([B_bias_final_quad_x,B_bias_final_quad_y,B_bias_final_quad_z])
    B_bias_tran = 0*np.array([B_bias_tran_x,B_bias_tran_y,B_bias_tran_z])
    B_bias_com = np.array([B_bias_com_x,B_bias_com_y, B_bias_com_z])
    B_bias_MOT = np.array([B_bias_mot_x,B_bias_mot_y, B_bias_mot_z])
    B_bias_move = 0*np.array([B_bias_mov_x, B_bias_mov_y, B_bias_mov_z])
    dur_magtrap = hold_time_start + hold_time_com + dur_quad_ramp
    start()
    t = 0

    New_MOT = MOT(t, cooling_freq=cent, repump_freq=repump_freq, quad_curr=quad) #82.231 1->1' 84.688 1->2'
    t += 1e-3
    # exec("New_MOT.probe_"+probe_direction+"(t, probe_"+probe_direction+"_time, 'bg')")
    t += 30e-3
    t += New_MOT.probe_fluo(t, probe_fluo_time, 'bg')
    t += 30e-3
    # New_MOT.probe_science(t, probe_yz_time, 'bg')
    t+= 30e-3
    
    # UV.go_high(t)
    # t+=5
    # UV.go_low(t)
    
    t = New_MOT.load(t, load_time, B_bias_MOT, UV_onoff=False)
    
    # # MOT_YZ_flea.expose(t-10*ms,'MOT_fluo_img', trigger_duration=0.1*ms, frametype='fluo_img')
    t = New_MOT.move(t, dur_MOT_move, np.array(B_bias_MOT), np.array(B_bias_move))
    t = New_MOT.compress(t, CMOT_dur, quad, compressed_MOT_quad, res+compress_freq_start*MHz, res+compress_freq_end*MHz, np.array(B_bias_move), np.array(B_bias_com)) # CMOT


    t = New_MOT.pol_grad(t, dur_mol, molasses_freq_start, molasses_freq_end, np.array(B_bias_mol)) # Molasses
    # # t = New_MOT.depump(t,4*ms) 
    # # t = New_MOT.grey_mol(t, 3, grey_cool_freq, grey_rep_freq) # grey molasses
    t=New_MOT.opt_pump(t, duration=dur_OptPumping*ms)
    # # UV.go_high(t)
    t = New_MOT.mag_trap(t, duration=dur_magtrap*ms, quad_start=quad_trap, B_bias_start=np.array(B_bias_capture_quad), B_bias_final= np.array(B_bias_final_quad))
    # # UV.go_low(t)
    
    
    # # t+=dur_transport*2
    # t = New_MOT.move(t, dur_tran_bias*ms, np.array(B_bias_final_quad), np.array(B_bias_tran))
    # New_MOT.fluorescence(t,t+dur_transport+2)
    # t = New_MOT.new_transport(t, duration= dur_transport, B_bias_start=np.array(B_bias_tran), bias_r_yx=bias_ratio_yx)
    # t = New_MOT.new_transport(t, duration= dur_transport, B_bias_start=np.array(B_bias_tran), bias_r_yx=bias_ratio_yx, inverse=True)
    # # t = New_MOT.evap(t, dur_evap)
    # t+= 10
    New_MOT.deload(t)
    t += t_of_f
    New_MOT.probe_fluo(t, probe_fluo_time, 'fluo_img')
    # New_MOT.probe_science(t, sci_probe_time, 'atom')
    # exec("New_MOT.probe_"+probe_direction+"(t, probe_"+probe_direction+"_time, 'atom')")
    # t += 0.2
    # New_MOT.probe_science(t, sci_probe_time, 'probe')
    # exec("New_MOT.probe_"+probe_direction+"(t, probe_"+probe_direction+"_time, 'probe')")
    
    
    # IAN: usually dark is taken here
    
    t+=0.3
    # New_MOT.fluorescence(0,t)
    
    New_MOT.__init__(t, cooling_freq=cent, repump_freq=repump_freq, quad_curr=quad)
    
    
    # set_freq(Cooling, t-0.01, cent)
    # New_MOT.set_bias(t-0.01, [0,0,0])
    # quad_MOT.constant(t-0.01,value=1)
    # # transport1.constant(t-0.01,value=1)
    # # Cool_int.constant(t+0.12*ms, 0)
    # # Repump_int.constant(t+0.12*ms, 0)
    # Shutter_Probe.close(t)
    # # t+=9
    # # plt.show()
    t+=2.2
    stop(t)
    