from labscript_devices.NI_DAQmx.labscript_devices import NI_USB_6229
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6738


NI_PCIe_6738(name='ni_pcie_6738',  parent_device= NI6738_clock, 
        MAX_name='Dev2', clock_terminal='/Dev2/PFI0')
# AnalogOut(name='a5', parent_device=Dev1, connection='ao5')
# AnalogOut(name='a27', parent_device=Dev1, connection='ao27')
# DigitalOut(name='d0', parent_device=Dev1, connection='port0/line0')
# DigitalOut(name='d1', parent_device=Dev1, connection='port0/line1')
#-----------------------------------------------------------------------


#█▀▄▀█ █▀▀█ █▀▀▀ █▀▀▄ █▀▀ ▀▀█▀▀ ░▀░ █▀▀   ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄ █▀▀ █▀▀█ █▀▀█ █▀▀█ ▀▀█▀▀
#█░▀░█ █▄▄█ █░▀█ █░░█ █▀▀ ░░█░░ ▀█▀ █░░   ░░█░░ █▄▄▀ █▄▄█ █░░█ ▀▀█ █░░█ █░░█ █▄▄▀ ░░█░░
#▀░░░▀ ▀░░▀ ▀▀▀▀ ▀░░▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀▀▀   ░░▀░░ ▀░▀▀ ▀░░▀ ▀░░▀ ▀▀▀ █▀▀▀ ▀▀▀▀ ▀░▀▀ ░░▀░░
NI_USB_6229(name='ni_usb_6229_1',
         parent_device=ni_usb_6229_1_clock,
         MAX_name='Dev3',
         clock_terminal='/Dev3/PFI0')
#-----------------------------------------------------------------------