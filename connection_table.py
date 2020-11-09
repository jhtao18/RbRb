import sys
sys.path.append(r'C:\Users\RbRb\labscript-suite\userlib\labscriptlib\RbRb')
from labscript import *
from labscript_utils import h5_lock
from labscript_utils import import_or_reload
from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
# from labscript_devices.PineBlaster import PineBlaster
from labscript_devices.TekScope.labscript_devices import TekScope
from labscript_devices.NovaTechDDS9M import NovaTechDDS9M

#PineBlaster(name='pineblaster_0', usbport='com4')
PulseBlasterUSB(name='pb0', board_number=0, pulse_width='minimum', programming_scheme='pb_stop_programming/STOP')
ClockLine(name='NI6738_clock', pseudoclock=pb0.pseudoclock, connection='flag 0')
ClockLine(name='ni_usb_6229_clock', pseudoclock=pb0.pseudoclock, connection='flag 2')
ClockLine(name='ni_usb_6229_table2_clock', pseudoclock=pb0.pseudoclock, connection='flag 1')
ClockLine(name='ni_usb_6002_clock', pseudoclock=pb0.pseudoclock, connection='flag 7')
Trigger(name='camera_trigger_Science_flea', parent_device=pb0.direct_outputs, connection='flag 5', trigger_edge_type='rising')
Trigger(name='camera_trigger_MOT_XY_flea', parent_device=pb0.direct_outputs, connection='flag 6', trigger_edge_type='rising')
Trigger(name='camera_trigger_MOT_YZ_flea', parent_device=pb0.direct_outputs, connection='flag 8', trigger_edge_type='rising')

# DigitalOut(name='PB_12', parent_device=pb0.direct_outputs, connection='flag 12')
# DigitalOut(name='PB_13', parent_device=pb0.direct_outputs, connection='flag 13')
# DigitalOut(name='PB_14', parent_device=pb0.direct_outputs, connection='flag 14')
# Trigger(name='scope_trigger', parent_device=pb0.direct_outputs,
        # connection='flag 16', trigger_edge_type='rising')

import_or_reload('shared.NI')
import_or_reload('shared.camera')


#TekScope(name = 'monitor1', addr='USB0::0x0699::0x0368::C102918::INSTR')#, parent_device=do2, connection='trigger', trigger_edge_type='rising')
ClockLine(name='NT_rb_clock', pseudoclock=pb0.pseudoclock, connection='flag 4')
ClockLine(name='NT_rf_clock', pseudoclock=pb0.pseudoclock, connection='flag 3')
NovaTechDDS9M(name='novatechdds9m_rb', parent_device=NT_rb_clock, com_port='com6',
              baud_rate=19200, default_baud_rate=19200, update_mode='asynchronous')
NovaTechDDS9M(name='novatechdds9m_rf', parent_device=NT_rf_clock, com_port='com4',
              baud_rate=19200, default_baud_rate=19200, update_mode='asynchronous')

DDS(name='Repump', parent_device=novatechdds9m_rb, connection='channel 1')
DDS(name='Cooling', parent_device=novatechdds9m_rb, connection='channel 0')
DDS(name='Evap_rf', parent_device=novatechdds9m_rf, connection='channel 0')


if __name__ == '__main__':
	start()
	stop(1)