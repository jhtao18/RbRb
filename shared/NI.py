from labscript import *
from labscript_utils import h5_lock
from labscript_utils import import_or_reload
from labscript_devices.NI_DAQmx.labscript_devices import NI_USB_6229
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6738


NI_PCIe_6738(name='ni_pcie_6738',  parent_device= NI6738_clock, 
        MAX_name='Dev2', clock_terminal='/Dev2/PFI0')
AnalogOut(name='a5', parent_device=ni_pcie_6738, connection='ao5')
AnalogOut(name='a6', parent_device=ni_pcie_6738, connection='ao6')
# DigitalOut(name='d0', parent_device=Dev1, connection='port0/line0')
# DigitalOut(name='d1', parent_device=Dev1, connection='port0/line1')
#-----------------------------------------------------------------------


#magnetic transport
NI_USB_6229(name='ni_usb_6229_1',
         parent_device=ni_usb_6229_1_clock,
         MAX_name='Dev3',
         clock_terminal='/Dev3/PFI0')
#-----------------------------------------------------------------------