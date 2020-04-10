from labscript import *
from labscript_utils import h5_lock
from labscript_devices.PulseBlasterUSB import PulseBlasterUSB
from labscript_devices.PineBlaster import PineBlaster
from labscript_devices.NI_DAQmx.labscript_devices import NI_DAQmx
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6738
from labscript_devices.NI_DAQmx.labscript_devices import NI_USB_6229
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


NI_PCIe_6738(name='Dev2',  parent_device= NI6738_clock, clock_terminal='/Dev2/PFI0', max_AO_sample_rate=400e3)
# AnalogOut(name='a5', parent_device=Dev1, connection='ao5')
# AnalogOut(name='a6', parent_device=Dev1, connection='ao6')
# AnalogOut(name='a7', parent_device=Dev1, connection='ao7')
# AnalogOut(name='a8', parent_device=Dev1, connection='ao8')
# AnalogOut(name='a9', parent_device=Dev1, connection='ao9')
# AnalogOut(name='a10', parent_device=Dev1, connection='ao10')
# AnalogOut(name='a26', parent_device=Dev1, connection='ao26')
# AnalogOut(name='a27', parent_device=Dev1, connection='ao27')
# DigitalOut(name='d0', parent_device=Dev1, connection='port0/line0')
# DigitalOut(name='d1', parent_device=Dev1, connection='port0/line1')

#magnetic transport USB_6229
# NI_USB_6229(name='ni_usb_6229_1',
#          parent_device=ni_usb_6229_1_clock,
#          MAX_name='Dev3',
#          clock_terminal='/Dev3/PFI0',
#          num_AO=4,
#          range_AO=[-10, 10],
#          sample_rate_AO=700e3,
#          static_AO=True,
#          num_DO=16,
#          sample_rate_DO=1e6,
#          num_AI=8,
#          clock_terminal_AI='/Dev3/PFI1',
#          sample_rate_AI=1000,
#          mode_AI='labscript',# 'labscript', 'gated', 'triggered'
#          num_PFI=0)
NI_USB_6229(name='ni_usb_6229_1',
         parent_device=ni_usb_6229_1_clock,
         MAX_name='Dev3',
         clock_terminal='/Dev3/PFI0',
         clock_terminal_AI='/Dev3/PFI1')

# TekScope(name = 'monitor1', addr='USB0::0x0699::0x0368::C102920::INSTR')
# NovaTechDDS9M(name='novatechdds9m_2', parent_device=NT_COM4_clock, com_port='com4',
              # baud_rate=19200, default_baud_rate=19200, update_mode='asynchronous')

# DDS(name='repump_lock', parent_device=novatechdds9m_2, connection='channel 0')
# DDS(name='cooling_lock', parent_device=novatechdds9m_2, connection='channel 1')
# StaticDDS(name='COM4_2', parent_device=novatechdds9m_2, connection='channel 2')
# StaticDDS(name='COM4_3', parent_device=novatechdds9m_2, connection='channel 3')
#

if __name__ == '__main__':
	start()
	# a5.constant(0.5, value=0.3)
	# a5.constant(0.7, value=0.0)
	stop(1)