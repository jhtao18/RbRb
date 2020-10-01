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
cool_z = -0.06
rep_z = -0.06
opt_z = -0.06
#
import_or_reload('labscriptlib.RbRb.transport.new_transport_optimisation')
from labscriptlib.RbRb.transport.new_transport_optimisation import transport
tswitch = transport.t_switchover
# print(t, tswitch)
def Poly5(t, duration, c, w, B_bias=[0,0,0]):
    f = t/duration
    # y = c[0]+c[1]*f+c[2]*f**2+c[3]*f**3+c[4]*f**4
    expr='('
    for cmd in c:
        ci = c.index(cmd)
        wi = ci*2+1
        expr += '+('
        expr += cmd
        #np.logical_and(w[2]<f, f<w[3])
        ws = ['w[' + str(wi-1) + ']', 'w[' + str(wi) + ']']
        expr += ')*np.logical_and(f>' + ws[0] + ', f<' + ws[1] + ')'
    expr += ')'
    # print(expr, w)
    y = eval(expr)
    # if np.max(y)<-10:
        # print(f[0], y[0], '\n')
    return y

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
        quad_MOT.constant(t+0.01, value=self.quad_curr)
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
        Probe_int.constant(t, probe_z) # IBS: Probe go low? Fix knob!!
        
    # IAN: make "DefaultValues" method that init calls and that you call at end end of sequence.
    
    def load(self, start_time, load_time, B_bias, UV_onoff):
        t = start_time
        if UV_onoff:
            UV.go_high(t)
        UV.go_low(t+dur_UV)
        t1_enable.go_high(t)
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
        x_shim.customramp(start, duration, HalfGaussRamp, B_bias_start[0], B_bias_end[0], duration, samplerate=1/CMOT_step)
        y_shim.customramp(start, duration,HalfGaussRamp, B_bias_start[1], B_bias_end[1], duration, samplerate=1/CMOT_step)
        z_shim.customramp(start, duration, HalfGaussRamp, B_bias_start[2], B_bias_end[2], duration, samplerate=1/CMOT_step)      
        Cooling.frequency.customramp(start, duration, HalfGaussRamp, freq_c_s, freq_c_e, duration, samplerate=1/CMOT_step) # IBS: note novatech is limited to 110 us steps!!! just a note
        self.quad_curr = curr_e
        Cool_int.constant(start, com_cool_int) # IBS: should be optimized, and set so 0 is 0
        Repump_int.constant(start, com_rep_int) # IBS: should be optimized, and set so 0 is 0
        return start + duration
        
    def move(self, start, duration, B_bias_start, B_bias_end):
        x_shim.customramp(start, duration, LineRamp, B_bias_start[0], B_bias_end[0], samplerate=1/0.2/ms)
        y_shim.customramp(start, duration, LineRamp, B_bias_start[1], B_bias_end[1], samplerate=1/0.2/ms)
        z_shim.customramp(start, duration, LineRamp, B_bias_start[2], B_bias_end[2], samplerate=1/0.2/ms)
        return start + duration
        
    def set_bias(self, start, B_bias):
        x_shim.constant(start, B_bias[0])
        y_shim.constant(start, B_bias[1])
        z_shim.constant(start, B_bias[2])
        
    def pol_grad(self, start, duration, freq_c_s, freq_c_e, B_bias):
        t1_enable.go_low(start)
        self.set_bias(start, B_bias) # IBS: should be optimized (critical) done
        Cooling.frequency.customramp(start, duration-0.13*ms-opt_adv, LineRamp, freq_c_s, freq_c_e, samplerate=1/mol_freq_step) # IBS: timing code is future bug. 
        Cool_int.constant(start, mol_cool_int)
        # Repump_int.constant(start, mol_rep_int) # IBS: ramped with start and end optimized.
        Repump_int.customramp(start, duration, LineRamp, mol_rep_int_start, mol_rep_int_end, samplerate=1/mol_freq_step)
        t = start+duration
        return t
    
    # def grey_mol(self, start, duration, c_freq, r_freq):
        # t1_enable.go_low(start)
        # # t2_enable.go_low(start)
        # self.set_bias(start, np.array(B_bias))
        # Cooling.setfreq(start, c_freq)
        # Repump.setfreq(start, r_freq)
        # return start+duration
        
    def opt_pump(self, start, duration):
        Cooling_AOM.go_low(start-opt_adv) # IBS: unexpected side effect!!
        Cool_int.constant(start, cool_z)# IBS: Fix knob!!
        Shutter_Cooling.close(start) # IBS: careful about pretrigger here so it does not close during pol_grad
        set_freq(Cooling, start-opt_adv, res+opt_f*MHz)
        # IAN: Repump power matters here
        # IAN: In general always use the analog and digital to turn on and off beams at the same time.
        OptPump_AOM.go_high(start)
        OptPump_AOM.go_low(start+duration)
        OptPump_int.constant(start, OptPumpint)
        Repump_int.constant(start, opt_rep_int) # IBS: again knob!  
        self.set_bias(start-0.5*ms, np.array(B_bias_optpump)) # IAN: How fast does bias actually change? (Field)
        Shutter_Opt_pumping.close(start+duration+10*ms) # Ian: When does shutter open?  So in this function command the shutter to open "6 ms" in advance!  Just rely on shutter class.
        return start+duration
        
    def mag_trap(self, start, duration, quad, B_bias):
        Repump_AOM.go_low(start)
        Repump_int.constant(start, rep_z)
        Shutter_Repump.close(start+10*ms) # maybe ad 10 ms here because of OP.
        Shutter_Probe.close(start+10*ms)
        
        t1_enable.go_high(start) # IAN: precommand by some amount so it is rising during end of OP.
        quad_MOT.constant(start-0.2*ms, value=quad)
        x_shim.customramp(start, bias_dur*ms, LineRamp, B_bias_mol[0], B_bias[0], samplerate=1/0.2/ms) # IBS: make equal to PG cooling at first. 
        y_shim.customramp(start, bias_dur*ms, LineRamp, B_bias_mol[1], B_bias[1], samplerate=1/0.2/ms)
        z_shim.customramp(start, bias_dur*ms, LineRamp, B_bias_mol[2], B_bias[2], samplerate=1/0.2/ms)
        return start+duration
        
    def deload(self, start):
        Cooling_AOM.go_low(start)
        Repump_AOM.go_low(start)
        OptPump_AOM.go_low(start)
        Shutter_Cooling.close(start)
        # Shutter_Repump.close(start)
        quad_MOT.constant(start,value=1)
        transport1.constant(start,value=1)
        transport2.constant(start,value=1)
        transport3.constant(start,value=1)
        t1_enable.go_low(start)
        t2_enable.go_low(start)
        t3_enable.go_low(start)
        t4_enable.go_low(start)
        self.set_bias(start-0.5*ms, [0,0,0])
        
        # t3_0.go_high(start)
        # t3_1.go_high(start)
        # t3_enable.go_high(start)
        # transport2.constant(start, -0.1)
        return start
        
    def fluorescence(self, start, end):
        testin0.acquire('curr0', start, end)
        testin1.acquire('curr1', start, end)
        testin2.acquire('curr2', start, end)    
        testin3.acquire('curr3', start, end)    
        testin4.acquire('fluo', start, end)
        testin5.acquire('biasx', start, end)
        testin6.acquire('biasy', start, end)
        return 'Collected as fluo'
        
    def probe(self, start, duration, frametype):#absorption imaging
        # IAN: do want repump during imaging, in deload consider setting a x-bias field ~2 ms in advance
        if not frametype=='bg':
            Probe_int.constant(start-0.2*ms, probe_MOT_int) # IAN: analog is fast
            MOT_Probe_AOM.go_high(start)
            MOT_Probe_AOM.go_low(start+duration)
            set_freq(Cooling, start-prob_adv, res+0.0*MHz) # IAN: usually better to set this at the end of OP
            
            # Repump_AOM.go_high(start-10*ms)
            # Repump_int.constant(start-10*ms, 0)
            # Shutter_Repump.open(start-prob_adv-10*ms)
            
            Shutter_Probe.open(start-prob_adv-3*ms)
        MOT_flea.expose(start-0.01*ms,'abs_img', trigger_duration=duration, frametype=frametype) # IAN: needs ~10 us pretrigger to get our of contineous clean mode.
        
    def probe_science(self, start, duration, frametype):#absorption imaging
        if not frametype=='bg':
            Probe_int.constant(start-0.2*ms, probe_Science_int) # IAN: analog is fast
            MOT_Probe_AOM.go_high(start)
            MOT_Probe_AOM.go_low(start+duration)
            
            # Shutter_Probe.open(start-prob_adv-3*ms)
            set_freq(Cooling, start-prob_adv, res)
            
        Science_flea.expose(start-0.01*ms,'science_img', trigger_duration=duration, frametype=frametype)
        
    # def transport_map(self, ind, inverse=False):
        # map = [[0,0,0],[1,0,0],[2,0,0],[3,0,0], [0,1,0],[1,1,0],[2,1,0],[3,1,0], [0,0,1],[2,0,1],[3,0,1]] #[ch, t?_0, t?_1]
        # imap = [[0,4,8], [1,5], [2,6,9], [3,7,10]]
        # if not inverse:
            # return map[ind]
        # else:
            # return imap[ind]
            
    # def channel_cmd(self, ch, cmd, w):
        # ch_cmd = []
        # ch_w = []
        # for i in self.transport_map(ch, inverse=True):
            # ch_cmd.append(cmd[i])
            # ch_w.append(w[i][0])
            # ch_w.append(w[i][1])
        # return ch_cmd, ch_w
    
    # def generate_transport(self, cmd, w, t, duration):
        # ch_cmds, ch_ws = [], []
        # for ch in range(4):
            # ch_cmd, ch_w = self.channel_cmd(ch, cmd, w)
            # ch_cmds.append(ch_cmd)
            # ch_ws.append(ch_w)
        # self.generate_ch_transport(ch_cmds, ch_ws, t, duration)
        
    # def generate_ch_transport(self, ch_cmds, ch_ws, t, duration):
        # quad_MOT.customramp(t, duration, Poly5, ch_cmds[0], ch_ws[0], samplerate=1/transport_step)
        # transport1.customramp(t, duration, Poly5, ch_cmds[1], ch_ws[1], samplerate=1/transport_step)
        # transport2.customramp(t, duration, Poly5, ch_cmds[2], ch_ws[2], samplerate=1/transport_step)
        # transport3.customramp(t, duration, Poly5, ch_cmds[3], ch_ws[3], samplerate=1/transport_step)
        # for ch in range(len(ch_cmds)):
            # ind_list = self.transport_map(ch, inverse=True)
            # for ind in ind_list:
                # t_01 = self.transport_map(ind, inverse=False)[1:]
                # tstart, tend = ch_ws[ch][ind_list.index(ind)*2], ch_ws[ch][ind_list.index(ind)*2+1]
                # tstart, tend = t+tstart*duration, t+tend*duration
                # TTLname = 't' + str(ch+1) + '_'
                # exec(TTLname + 'enable.go_high(tstart)')
                # for c in range(2):
                    # high = ['.go_high(tstart)', '.go_low(tstart)']
                    # exec(TTLname + str(c)+ high[1-t_01[c]])
                # if not ind==10: #Do not turn off science coils
                    # exec(TTLname + 'enable.go_low(tend)')
        # return
                
    # def transport(self, start, duration, B_bias):
        # t = start
        
        # pks = []
        # for i in range(0,9):
            # pk = tran_trap
            # if i%2:
                # pk = pk*1.2
            # pks.append(pk)
        # cmd, w, tt = [], [], 0
        # tmp = t_Line(tt, 0.1, tran_trap, 0)
        # cmd.append(tmp[0])
        # w.append(tmp[1])
        # for i in range(0,9):
            # # print(pks , i)
            # tti = eval('tt'+str(i+1))
            # tpi = eval('tp'+str(i+1))
            # if tpi>=tti+0.19:   tpi = tti+0.19
            # tmp = t_Poly3(round(tti,5), 0.1*2, round(tpi,5), pks[i]*r)
            # cmd.append(tmp[0])
            # w.append(tmp[1])
        # # tmp = t_Line(tt-20*ms/duration, 0.091, 0, quad_trap)
        # tmp = t_ExpRamp(round(tts,5), round(1-tts,5), 0, quad_trap, 0.1)
        # # print(tmp)
        # cmd.append(tmp[0])
        # tmp[1][1] = 1.1
        # w.append(tmp[1])
            
        # self.generate_transport(cmd, w, t, duration)
        
        # t += duration
        # t += dur_magtrap_sci/2
        # return t
        
    def new_transport_switch(self, start, duration, tswitch, order='normal'):
        t = start
        if order=='normal':
            t2_enable.go_high(t)
            t3_enable.go_high(t + tswitch[0])
            t4_enable.go_high(t + tswitch[1]-0*ms)
            t1_enable.go_low(t + tswitch[1])


            t1_0.go_high(t + tswitch[2])
            t2_enable.go_low(t + tswitch[2])
            t1_enable.go_high(t + tswitch[2])

            t2_0.go_high(t + tswitch[3])
            t3_enable.go_low(t + tswitch[3])
            t2_enable.go_high(t + tswitch[3])

            t3_0.go_high(t + tswitch[4])
            t4_enable.go_low(t + tswitch[4])
            t3_enable.go_high(t + tswitch[4])

            t4_0.go_high(t + tswitch[5])
            t1_enable.go_low(t + tswitch[5])
            t4_enable.go_high(t + tswitch[5])

            t1_0.go_low(t + tswitch[6])
            t1_1.go_high(t + tswitch[6])
            t2_enable.go_low(t + tswitch[6])
            t1_enable.go_high(t + tswitch[6])

            t3_0.go_low(t + tswitch[7])
            t3_1.go_high(t + tswitch[7])
            t2_enable.go_low(t + tswitch[8])
            
            
            t4_0.go_low(t + tswitch[8])
            t4_1.go_high(t + tswitch[8])
            
            t1_enable.go_low(t + tswitch[9])
        else:
            t2_enable.go_low(2*start+duration-t)
            t3_enable.go_low(2*start+duration-t - tswitch[0])
            t4_enable.go_low(2*start+duration-t - tswitch[1])
            t1_enable.go_high(2*start+duration-t - tswitch[1])


            t1_0.go_low(2*start+duration-t - tswitch[2])
            t2_enable.go_high(2*start+duration-t - tswitch[2])
            t1_enable.go_low(2*start+duration-t - tswitch[2])

            t2_0.go_low(2*start+duration-t - tswitch[3])
            t3_enable.go_high(2*start+duration-t - tswitch[3])
            t2_enable.go_low(2*start+duration-t - tswitch[3])

            t3_0.go_low(2*start+duration-t - tswitch[4])
            t4_enable.go_high(2*start+duration-t - tswitch[4])
            t3_enable.go_low(2*start+duration-t - tswitch[4])

            t4_0.go_low(2*start+duration-t - tswitch[5])
            t1_enable.go_high(2*start+duration-t - tswitch[5])
            t4_enable.go_low(2*start+duration-t - tswitch[5])

            t1_0.go_high(2*start+duration-t - tswitch[6])
            t1_1.go_low(2*start+duration-t - tswitch[6])
            t2_enable.go_high(2*start+duration-t - tswitch[6])
            t1_enable.go_low(2*start+duration-t - tswitch[6])

            t3_0.go_high(2*start+duration-t - tswitch[7])
            t3_1.go_low(2*start+duration-t - tswitch[7])
            
            
            t4_0.go_high(2*start+duration-t - tswitch[8])
            t4_1.go_low(2*start+duration-t - tswitch[8])
            
            t1_enable.go_high(2*start+duration-t - tswitch[9])
            
    def transport_currents(self, t, duration, transport_currents_interp_ch):
        return transport_currents_interp_ch(t)
        
    def new_transport(self, start, duration, B_bias_start, B_bias_end, bias_dur, bias_r_yx):
        t = start
        # import_or_reload('labscriptlib.RbRb.transport.new_transport_optimisation')
        # from labscriptlib.RbRb.transport.new_transport_optimisation import transport
        # tswitch = transport.t_switchover
        # print(t, tswitch)
        
        from scipy.interpolate import interp1d
        self.t_t = np.arange(0, duration, transport_step)
        self.t_I = np.zeros((6,len(self.t_t)))
        for ch in range(4):
            self.t_I[ch,:] = transport.currents_for_channel(self.t_t, duration, ch+1, ratio=-1/40, B_bias=B_bias_start)
            if ch == 0: self.t_I[ch,:] = self.t_I[ch,:] + 0.025
            # else: self.t_I[ch,:] = self.t_I[ch,:] + 0.007
        self.t_I[4,:] = transport.currents_for_channel(self.t_t, duration, 4+1, ratio=-0.5, B_bias=B_bias_start[0]) 
        self.t_I[5,:] = transport.currents_for_channel(self.t_t, duration, 4+1, ratio=-0.5*bias_ratio_yx, B_bias=B_bias_start[1])
        # print(tswitch[1]-0.1, tswitch[1])
        #comment by Mingshu after tuning PID for the curr3
        # self.t_I[3] = self.t_I[3] - 0.12 * np.logical_and(tswitch[1]-0.1<self.t_t, self.t_t<=tswitch[1])
        
        transport_currents_interp = [interp1d(
            self.t_t, self.t_I[ch,:], 'cubic', fill_value='extrapolate'
        ) for ch in range(6)]
        
        # x_shim.customramp(t, bias_dur, LineRamp, B_bias_start[0], B_bias_end[0], samplerate=1/(bias_dur/2))
        # y_shim.customramp(t, bias_dur, LineRamp, B_bias_start[1], B_bias_end[1], samplerate=1/(bias_dur/2))
        x_shim.customramp(t, duration, self.transport_currents, transport_currents_interp[4], samplerate=1/transport_step)
        y_shim.customramp(t, duration, self.transport_currents, transport_currents_interp[5], samplerate=1/transport_step)
        z_shim.customramp(t, bias_dur, LineRamp, B_bias_start[2], B_bias_end[2], samplerate=1/(bias_dur/2))
       

        # Select which current supply powers which coil(pair) at each switchover time:
        self.new_transport_switch(t, duration, tswitch, order='normal')
        quad_MOT.customramp(t, duration, self.transport_currents, transport_currents_interp[0], samplerate=1/transport_step)
        transport1.customramp(t, duration, self.transport_currents, transport_currents_interp[1], samplerate=1/transport_step)
        transport2.customramp(t, duration, self.transport_currents, transport_currents_interp[2], samplerate=1/transport_step)
        transport3.customramp(t, duration, self.transport_currents, transport_currents_interp[3], samplerate=1/transport_step)
        t += duration
        
        # self.new_transport_switch(t, duration, tswitch, order='inverse')
        # self.t_I = np.array([np.flip(self.t_I[ch,:]) for ch in range(0,4)])
        # transport_currents_interp = [interp1d(self.t_t, self.t_I[ch,:], 'cubic', fill_value='extrapolate') for ch in range(4)]
        # quad_MOT.customramp(t, duration, self.transport_currents, transport_currents_interp[0], samplerate=1/transport_step)
        # transport1.customramp(t, duration, self.transport_currents, transport_currents_interp[1], samplerate=1/transport_step)
        # transport2.customramp(t, duration, self.transport_currents, transport_currents_interp[2], samplerate=1/transport_step)
        # transport3.customramp(t, duration, self.transport_currents, transport_currents_interp[3], samplerate=1/transport_step)
        # x_shim.customramp(t, bias_dur, LineRamp, B_bias_end[0], B_bias_start[0], samplerate=1/(bias_dur/2))
        # y_shim.customramp(t, bias_dur, LineRamp, B_bias_end[1], B_bias_start[1], samplerate=1/(bias_dur/2))
        # z_shim.customramp(t, bias_dur, LineRamp, B_bias_end[2], B_bias_start[2], samplerate=1/(bias_dur/2))
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
    probe_time = 0.012*ms
    sci_probe_time = 0.016*ms

    B_bias_move = np.array([B_bias_mov_x, B_bias_mov_y, B_bias_mov_z])
    B_bias_mol = np.array([B_bias_mol_x,B_bias_mol_y,B_bias_mol_z])
    B_bias_optpump = np.array([B_bias_optpump_x,B_bias_optpump_y,B_bias_optpump_z])
    B_bias_quad = np.array([B_bias_quad_x,B_bias_quad_y,B_bias_quad_z])
    B_bias_tran = np.array([B_bias_tran_x,B_bias_tran_y,B_bias_tran_z])
    B_bias_com = np.array([B_bias_com_x,B_bias_com_y, B_bias_com_z])
    B_bias_MOT = np.array([B_bias_mot_x,B_bias_mot_y, B_bias_mot_z])
    start()
    t = 0

    New_MOT = MOT(t, cooling_freq=cent, repump_freq=repump_freq, quad_curr=quad) #82.231 1->1' 84.688 1->2'
    
    New_MOT.probe(t+0.2, probe_time, 'bg') #background light capture
    New_MOT.probe_science(t+0.3, probe_time, 'bg')
    t+=0.4 # IAN: what is with this 1s delay?
    
    t = New_MOT.load(t, load_time, B_bias_MOT, UV_onoff=True)
    MOT_flea.expose(t-10*ms,'fluo_img', trigger_duration=0.1*ms, frametype='fluo_img')
    t = New_MOT.move(t, 100*ms, np.array(B_bias_MOT), np.array(B_bias_move))
    t = New_MOT.compress(t, CMOT_dur, quad, compressed_MOT_quad, cent, res+compress_freq*MHz, np.array(B_bias_move), np.array(B_bias_com)) # CMOT

    t = New_MOT.pol_grad(t, dur_mol, res+compress_freq*MHz, molasses_freq, np.array(B_bias_mol)) # Molasses
    # t = New_MOT.grey_mol(t, 3, grey_cool_freq, grey_rep_freq) # grey molasses
    t=New_MOT.opt_pump(t, duration=dur_OptPumping*ms)
    # magnetic trap
    t = New_MOT.mag_trap(t, duration=dur_magtrap*ms, quad=quad_trap, B_bias=np.array(B_bias_quad))
    #transport
    # t = New_MOT.transport(t, duration= dur_transport, B_bias=np.array(B_bias_quad)+ np.array([dxt,dyt,dzt]))
    
    # n_sw = 0
    # tt = t+tswitch[n_sw]+1*ms #To Mingshu: this way we can compare at the same condition -- back and forth
    # tt = 2*t+2*dur_transport- t - tswitch[n_sw]+1*ms
    # tt = t+0*ms+1*ms
    # t1_enable.go_low(tt)
    # t2_enable.go_low(tt)
    # t3_enable.go_low(tt)
    # t4_enable.go_low(tt)
    # t1_enable.go_low(tt+0.16)
    # t2_enable.go_low(tt+0.16)
    # t3_enable.go_low(tt+0.16)
    # t4_enable.go_low(tt+0.16)
    # New_MOT.set_bias(tt, [0,0,0])
    # print('t_p = ',tt)
    # New_MOT.probe(tt+3*ms, probe_time, 'atom')
    # New_MOT.probe(tt+3*ms+0.2, probe_time, 'probe')
    
    # t+=dur_transport*2
    # t+= hold_time
    # New_MOT.fluorescence(t,t+dur_transport)
    # t = New_MOT.new_transport(t, duration= dur_transport, B_bias_start=np.array(B_bias_quad), B_bias_end=np.array(B_bias_tran), bias_dur=dur_tran_bias*ms, bias_r_yx=bias_ratio_yx)
    # t = New_MOT.evap(t, dur_evap)
    
    New_MOT.deload(t)
    t += t_of_f
    # New_MOT.probe_science(t, sci_probe_time, 'atom')
    New_MOT.probe(t, probe_time, 'atom')
    t += 0.2
    # New_MOT.probe_science(t, sci_probe_time, 'probe')
    New_MOT.probe(t, probe_time, 'probe')
    
    # IAN: usually dark is taken here
    
    t+=0.2
    set_freq(Cooling, t-0.01, cent)
    New_MOT.set_bias(t-0.01, [0,0,0])
    quad_MOT.constant(t-0.01,value=1)
    # transport1.constant(t-0.01,value=1)
    # Cool_int.constant(t+0.12*ms, 0)
    # Repump_int.constant(t+0.12*ms, 0)
    Shutter_Probe.close(t)
    t+=0
    # plt.show()
    stop(t)
    