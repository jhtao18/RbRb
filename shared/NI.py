from labscript import *
from labscript_utils import h5_lock
from labscript_utils import import_or_reload
from labscript_devices.NI_DAQmx.labscript_devices import NI_USB_6229
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6738
from labscript_devices.NI_DAQmx.labscript_devices import NI_DAQmx
from labscript_devices.NI_DAQmx.labscript_devices import NI_USB_6002


NI_PCIe_6738(name='ni_pcie_6738',  parent_device= NI6738_clock, 
        MAX_name='Dev4', clock_terminal='/Dev4/PFI0', max_AO_sample_rate = 400e3)
AnalogOut(name='Repump_int', parent_device=ni_pcie_6738, connection='ao2')
AnalogOut(name='Cool_int', parent_device=ni_pcie_6738, connection='ao3')
AnalogOut(name='Probe_int', parent_device=ni_pcie_6738, connection='ao4')
AnalogOut(name='OptPump_int', parent_device=ni_pcie_6738, connection='ao5')
AnalogOut(name='evap_int', parent_device=ni_pcie_6738, connection='ao6')
AnalogOut(name='ao7', parent_device=ni_pcie_6738, connection='ao7')
# AnalogOut(name='ao2', parent_device=ni_pcie_6738, connection='ao2')
# AnalogOut(name='ao3', parent_device=ni_pcie_6738, connection='ao3')
# DigitalOut(name='d0', parent_device=ni_pcie_6738, connection='port0/line0')
# DigitalOut(name='d1', parent_device=ni_pcie_6738, connection='port0/line1')
#-----------------------------------------------------------------------

#magnetic transport
NI_USB_6229(name='ni_usb_6229',
         parent_device=ni_usb_6229_clock,
         MAX_name='Dev5',
         clock_terminal='/Dev5/PFI0')
DigitalOut(name='t1_enable', parent_device=ni_usb_6229, connection='port0/line0')
DigitalOut(name='t1_0', parent_device=ni_usb_6229, connection='port0/line1')
DigitalOut(name='t1_1', parent_device=ni_usb_6229, connection='port0/line2')
DigitalOut(name='t2_enable', parent_device=ni_usb_6229, connection='port0/line3')
DigitalOut(name='t2_0', parent_device=ni_usb_6229, connection='port0/line4')
DigitalOut(name='t2_1', parent_device=ni_usb_6229, connection='port0/line5')
DigitalOut(name='t3_enable', parent_device=ni_usb_6229, connection='port0/line6')
DigitalOut(name='t3_0', parent_device=ni_usb_6229, connection='port0/line7')
DigitalOut(name='t3_1', parent_device=ni_usb_6229, connection='port0/line8')
DigitalOut(name='t4_enable', parent_device=ni_usb_6229, connection='port0/line9')
DigitalOut(name='t4_0', parent_device=ni_usb_6229, connection='port0/line10')
DigitalOut(name='t4_1', parent_device=ni_usb_6229, connection='port0/line11')
DigitalOut(name='x_shim_disable', parent_device=ni_usb_6229, connection='port0/line12')
DigitalOut(name='y_shim_disable', parent_device=ni_usb_6229, connection='port0/line13')
DigitalOut(name='z_shim_disable', parent_device=ni_usb_6229, connection='port0/line14')
DigitalOut(name='UV', parent_device=ni_usb_6229, connection='port0/line15')
AnalogOut(name='quad_MOT', parent_device=ni_usb_6229, connection='ao0')
AnalogOut(name='transport1', parent_device=ni_usb_6229, connection='ao1')
AnalogOut(name='transport2', parent_device=ni_usb_6229, connection='ao2')
AnalogOut(name='transport3', parent_device=ni_usb_6229, connection='ao3')
AnalogIn(name='testin0', parent_device=ni_usb_6229, connection='ai0')
AnalogIn(name='testin1', parent_device=ni_usb_6229, connection='ai1')
AnalogIn(name='testin2', parent_device=ni_usb_6229, connection='ai2')
AnalogIn(name='testin3', parent_device=ni_usb_6229, connection='ai3')
AnalogIn(name='testin4', parent_device=ni_usb_6229, connection='ai4')
AnalogIn(name='testin5', parent_device=ni_usb_6229, connection='ai5')
AnalogIn(name='testin6', parent_device=ni_usb_6229, connection='ai6')


NI_USB_6229(name='ni_usb_6229_table2',
         parent_device=ni_usb_6229_table2_clock,
         MAX_name='Dev3',
         clock_terminal='/Dev3/PFI0')
DigitalOut(name='Repump_AOM', parent_device=ni_usb_6229_table2, connection='port0/line0')
DigitalOut(name='MOT_Probe_AOM', parent_device=ni_usb_6229_table2, connection='port0/line1')
DigitalOut(name='Cooling_AOM', parent_device=ni_usb_6229_table2, connection='port0/line2')
DigitalOut(name='do3', parent_device=ni_usb_6229_table2, connection='port0/line3')
DigitalOut(name='OptPump_AOM', parent_device=ni_usb_6229_table2, connection='port0/line4')

DigitalOut(name='evap_switch', parent_device=ni_usb_6229_table2, connection='port0/line5')
DigitalOut(name='do6', parent_device=ni_usb_6229_table2, connection='port0/line6')
DigitalOut(name='do7', parent_device=ni_usb_6229_table2, connection='port0/line7')
DigitalOut(name='do8', parent_device=ni_usb_6229_table2, connection='port0/line8')
DigitalOut(name='do9', parent_device=ni_usb_6229_table2, connection='port0/line9')
# DigitalOut(name='Shutter_Cooling', parent_device=ni_usb_6229_table2, connection='port0/line12')
# DigitalOut(name='Shutter_Repump', parent_device=ni_usb_6229_table2, connection='port0/line13')
# DigitalOut(name='Shutter_Opt_pumping', parent_device=ni_usb_6229_table2, connection='port0/line14')
# DigitalOut(name='Shutter_Probe', parent_device=ni_usb_6229_table2, connection='port0/line15')
Shutter(name='Shutter_Cooling', parent_device=ni_usb_6229_table2, connection='port0/line12', delay=(3*ms, 2*ms))
Shutter(name='Shutter_Repump', parent_device=ni_usb_6229_table2, connection='port0/line13', delay=(6*ms, 3*ms))
Shutter(name='Shutter_Opt_pumping', parent_device=ni_usb_6229_table2, connection='port0/line14', delay=(2.1*ms, 3.3*ms))#2.1,3.3
Shutter(name='Shutter_Probe', parent_device=ni_usb_6229_table2, connection='port0/line15', delay=(3.3*ms, 3*ms))
AnalogOut(name='quad_MOT2', parent_device=ni_usb_6229_table2, connection='ao0')
AnalogOut(name='x_shim', parent_device=ni_usb_6229_table2, connection='ao1')
AnalogOut(name='y_shim', parent_device=ni_usb_6229_table2, connection='ao2')
AnalogOut(name='z_shim', parent_device=ni_usb_6229_table2, connection='ao3')

#-----------------------------------------------------------------------

NI_USB_6002(name='ni_usb_6002',
         parent_device=ni_usb_6002_clock,
         MAX_name='Dev1',
		 clock_terminal='/Dev1/PFI1')
AnalogIn(name='ai0', parent_device=ni_usb_6002, connection='ai0')
AnalogIn(name='ai1', parent_device=ni_usb_6002, connection='ai1')
AnalogIn(name='ai2', parent_device=ni_usb_6002, connection='ai2')
AnalogIn(name='ai3', parent_device=ni_usb_6002, connection='ai3')
#-----------------------------------------------------------------------