from labscript import *
from labscript_utils import h5_lock
from labscript_utils import import_or_reload
from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
from labscript_devices.PineBlaster import PineBlaster
from labscript_devices.TekScope.labscript_devices import TekScope
from labscript_devices.NovaTechDDS9M import NovaTechDDS9M

#PineBlaster(name='pineblaster_0', usbport='com4')
PulseBlasterUSB(name='pb0', board_number=0)#, programming_scheme='pb_stop_programming/STOP')
ClockLine(name='NI6738_clock', pseudoclock=pb0.pseudoclock, connection='flag 0')
ClockLine(name='ni_usb_6229_1_clock', pseudoclock=pb0.pseudoclock, connection='flag 1')
# DigitalOut(name='PB_12', parent_device=pb0.direct_outputs, connection='flag 12')
# DigitalOut(name='PB_13', parent_device=pb0.direct_outputs, connection='flag 13')
# DigitalOut(name='PB_14', parent_device=pb0.direct_outputs, connection='flag 14')
# Trigger(name='scope_trigger', parent_device=pb0.direct_outputs,
        # connection='flag 16', trigger_edge_type='rising')

import_or_reload('labscriptlib.rbrb.shared.NI')

# TekScope(name = 'monitor1', addr='USB0::0x0699::0x0368::C102920::INSTR')
# NovaTechDDS9M(name='novatechdds9m_2', parent_device=NT_COM4_clock, com_port='com4',
              # baud_rate=19200, default_baud_rate=19200, update_mode='asynchronous')

# DDS(name='repump_lock', parent_device=novatechdds9m_2, connection='channel 0')
# DDS(name='cooling_lock', parent_device=novatechdds9m_2, connection='channel 1')
# StaticDDS(name='COM4_2', parent_device=novatechdds9m_2, connection='channel 2')
# StaticDDS(name='COM4_3', parent_device=novatechdds9m_2, connection='channel 3')

if __name__ == '__main__':
	start()
	stop(1)