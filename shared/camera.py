import sys
sys.path.append(r'C:\Users\RbRb\labscript-suite\userlib\labscriptlib\RbRb')
from labscript_devices.FlyCapture2Camera.labscript_devices import FlyCapture2Camera
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
from labscript_utils import import_or_reload

MOT_flea_camera_attributes = {
    'AcquisitionAttributes::PacketSize': 5184,
    'AcquisitionAttributes::Timeout': 5000,
    'CameraAttributes::AutoExposure::Mode': 'Off',
    'CameraAttributes::Brightness::Mode': 'Ignored',
    'CameraAttributes::FrameRate::Mode': 'Auto',
    'CameraAttributes::Gain::Mode': 'Absolute',
    'CameraAttributes::Gain::Value': '12.5',
    'CameraAttributes::Gamma::Mode': 'Off',
    'CameraAttributes::Sharpness::Mode': 'Off',
    # 'CameraAttributes::Shutter::Mode': 'Absolute',
    # 'CameraAttributes::Shutter::Value': '0.000010',
    'CameraAttributes::Trigger::TriggerActivation': 'Level High',
    'CameraAttributes::Trigger::TriggerMode': 'Mode1',
    'CameraAttributes::Trigger::TriggerParameter': 0,
    'CameraAttributes::Trigger::TriggerSource': 'Source 0'
}
Science_flea_camera_attributes = {
    'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode': 'Unicast',
    'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMulticastAddress': '239.192.0.1',
    'AcquisitionAttributes::AdvancedEthernet::EventParameters::MaxOutstandingEvents': 50,
    'AcquisitionAttributes::AdvancedGenicam::EventsEnabled': 1,
    'AcquisitionAttributes::Bayer::Algorithm': 'Bilinear',
    'AcquisitionAttributes::Bayer::GainB': 1.0,
    'AcquisitionAttributes::Bayer::GainG': 1.0,
    'AcquisitionAttributes::Bayer::GainR': 1.0,
    'AcquisitionAttributes::Bayer::Pattern': 'Use hardware value',
    'AcquisitionAttributes::IncompleteBufferMode': 'Ignore',
    'AcquisitionAttributes::OutputImageType': 'Auto',
    'AcquisitionAttributes::PacketSize': 1500,
    'AcquisitionAttributes::Timeout': 5000,
    'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous',
    'CameraAttributes::AcquisitionControl::ExposureAuto': 'Off',
    'CameraAttributes::AcquisitionControl::ExposureMode': 'Timed',
    'CameraAttributes::AcquisitionControl::ExposureTime': 81.83717727661133,
    'CameraAttributes::AcquisitionControl::TriggerActivation': 'Rising Edge',
    'CameraAttributes::AcquisitionControl::TriggerMode': 'On',
    'CameraAttributes::AcquisitionControl::TriggerSelector': 'Frame Start',
    'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0',
    'CameraAttributes::AnalogControl::GainAuto': 'Off',
    'CameraAttributes::AnalogControl::Gain': 0,
    'CameraAttributes::AnalogControl::GammaEnabled': 0,
    'CameraAttributes::DeviceControl::DeviceUserID': 'XZ_Blackfly',
    'CameraAttributes::ImageFormatControl::Height': 2048,
    'CameraAttributes::ImageFormatControl::OffsetX': 0,
    'CameraAttributes::ImageFormatControl::OffsetY': 0,
    'CameraAttributes::ImageFormatControl::PixelFormat': 'Mono 8',
    'CameraAttributes::ImageFormatControl::TestPattern': 'Off',
    'CameraAttributes::ImageFormatControl::Width': 2448,
    'CameraAttributes::UserSetControl::UserSetDefault': 'Default',
    'CameraAttributes::UserSetControl::UserSetSelector': 'Default',
}
Science_flea_camera_attributes = {
 'AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode': 'Unicast' ,
 'CameraAttributes::AnalogControl::GainAuto': 'Off' ,
 'CameraAttributes::AnalogControl::BlackLevelEnabled': '0' ,
#  'CameraAttributes::AnalogControl::BlackLevel': '-10.367187' ,
 'CameraAttributes::AnalogControl::SharpnessEnabled': '0' ,
#  'CameraAttributes::AnalogControl::SharpnessAuto': 'Continuous' 
 'CameraAttributes::AcquisitionControl::TriggerSelector': 'Exposure Active' ,
 'CameraAttributes::AcquisitionControl::TriggerMode': 'On' ,
 'CameraAttributes::AcquisitionControl::TriggerSource': 'Line 0' ,
 'CameraAttributes::AcquisitionControl::TriggerActivation': 'Falling Edge' ,
 'CameraAttributes::AcquisitionControl::ExposureMode': 'Trigger Width' ,
 'CameraAttributes::AcquisitionControl::AcquisitionMode': 'Continuous' ,
#  'CameraAttributes::AcquisitionControl::AcquisitionFrameRateAuto': 'Continuous' ,
#  'CameraAttributes::AcquisitionControl::AcquisitionFrameRateEnabled': '1' ,
 'CameraAttributes::AcquisitionControl::SingleFrameAcquisitionMode': 'Free Running' ,
 'CameraAttributes::ImageFormatControl::PixelFormat': 'Mono 16' ,
 'CameraAttributes::ImageFormatControl::Width': '2448' ,
 'CameraAttributes::ImageFormatControl::Height': '2048' ,
 "CameraAttributes::ImageFormatControl::OffsetX": "0" ,
 "CameraAttributes::ImageFormatControl::OffsetY": "0" ,
 'CameraAttributes::ImageFormatControl::VideoMode': '0' ,
 'CameraAttributes::ImageFormatControl::BinningVertical': '1' ,
 'AcquisitionAttributes::BitsPerPixel': 'Use hardware value' ,
 'AcquisitionAttributes::ImageDecoderCopyMode': 'Auto' ,
 'AcquisitionAttributes::IncompleteBufferMode': 'Ignore' ,
 'AcquisitionAttributes::OutputImageType': 'Auto' ,
 'AcquisitionAttributes::OverwriteMode': 'Get Newest' ,
 'AcquisitionAttributes::PacketSize': '1500' ,
 'AcquisitionAttributes::ReceiveTimestampMode': 'None' ,
 'AcquisitionAttributes::Timeout': '2000' }
 
Science_flea_camera_attributes = {
    'AcquisitionAttributes::PacketSize': 1500,
    'CameraAttributes::Acquisition::AcquisitionMode': 'Continuous',
    'CameraAttributes::Acquisition::Trigger::TriggerActivation': 'RisingEdge',
    'CameraAttributes::Acquisition::Trigger::TriggerDelayAbs': 0.0,
    'CameraAttributes::Acquisition::Trigger::TriggerMode': 'On',
    'CameraAttributes::Acquisition::Trigger::TriggerSelector': 'FrameStart',
    'CameraAttributes::Acquisition::Trigger::TriggerSource': 'Line1',
    'CameraAttributes::Controls::Exposure::ExposureAuto': 'Off',
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoAdjustTol': 5,
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoAlg': 'Mean',
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoMax': 500000,
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoMin': 83,
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoOutliers': 0,
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoRate': 100,
    'CameraAttributes::Controls::Exposure::ExposureAutoControl::ExposureAutoTarget': 50,
    'CameraAttributes::Controls::Exposure::ExposureMode': 'Timed',
    'CameraAttributes::Controls::Exposure::ExposureTimeAbs': 95.0,
    'CameraAttributes::Controls::Exposure::ExposureTimePWL1': 0.0,
    'CameraAttributes::Controls::Exposure::ExposureTimePWL2': 0.0,
    'CameraAttributes::Controls::Exposure::ThresholdPWL1': 63,
    'CameraAttributes::Controls::Exposure::ThresholdPWL2': 63,
    'CameraAttributes::Controls::GainControl::Gain': 0.0,
    'CameraAttributes::Controls::GainControl::GainAuto': 'Off',
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoAdjustTol': 5,
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoMax': 26.0,
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoMin': 0.0,
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoOutliers': 0,
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoRate': 100,
    'CameraAttributes::Controls::GainControl::GainAutoControl::GainAutoTarget': 50,
    'CameraAttributes::Controls::GainControl::GainSelector': 'All',
    'CameraAttributes::Controls::Gamma': 1.0,
    'CameraAttributes::ImageFormat::PixelFormat': 'Mono12'
}
# IN USE
manual_mode_camera_attributes = MOT_flea_camera_attributes.copy()
manual_mode_camera_attributes['CameraAttributes::Trigger::TriggerMode'] = 'Mode3'
IMAQdxCamera(name='MOT_flea', parent_device=camera_trigger_MOT_flea, connection='trigger', serial_number=0xB09D01009014EC, camera_attributes=MOT_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='side')
# IMAQdxCamera(name='MOT_flea', parent_device=camera_trigger_Science_flea, connection='trigger', serial_number=0xF315BC7CB, camera_attributes=Science_flea_camera_attributes, manual_mode_camera_attributes=Science_flea_camera_attributes, orientation='side')

manual_mode_camera_attributes = Science_flea_camera_attributes.copy()
manual_mode_camera_attributes['CameraAttributes::Acquisition::Trigger::TriggerMode'] = 'Off'
# IMAQdxCamera(name='Science_flea', parent_device=camera_trigger_Science_flea, connection='trigger', serial_number=0xB09DDCBFE1, camera_attributes=Science_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='science')
IMAQdxCamera(name='Science_flea', parent_device=camera_trigger_Science_flea, connection='trigger', trigger_edge_type='rising', serial_number=0xF315BC7CB, camera_attributes=Science_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='science')
# MOT_flea_camera_attributes = dict([['AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode', 'Unicast'],
						# ['AcquisitionAttributes::AdvancedEthernet::EventParameters::MaxOutstandingEvents', '50'],
						# ["AcquisitionAttributes::PacketSize", "1500"],
						# ['CameraAttributes::Controls::Exposure::ExposureTimeAbs', "70"],
						# ["CameraAttributes::Acquisition::Trigger::TriggerSource", "Line1"],
						# ["CameraAttributes::Acquisition::Trigger::TriggerActivation", "RisingEdge"],
						# ['CameraAttributes::Acquisition::Trigger::TriggerSelector', 'FrameStart'],
						# ['CameraAttributes::Acquisition::Trigger::TriggerMode', 'On'],
						# #['CameraAttributes::Acquisition::Trigger::FrameStart::FrameStartTriggerMode', 'SyncIn1'],
						# ['CameraAttributes::Acquisition::AcquisitionMode', 'MultiFrame'],
						# ['CameraAttributes::Acquisition::AcquisitionFrameCount', 1]
						# # ['CameraAttributes::IO::SyncIn::SyncInSelector', 'SyncIn1'],
						# # ['CameraAttributes::IO::SyncOut::SyncOutSelector', 'SyncOut1'],
						# # ['CameraAttributes::IO::SyncOut::SyncOutSource', 'Exposing'],
						# # ['CameraAttributes::IO::SyncOut::SyncOutPolarity', 'Normal']
						# ])
#IMAQdxCamera(name='MOT_Mako', parent_device=camera_trigger_1, connection='trigger', trigger_edge_type='rising', serial_number=0x00F315C17A9, camera_attributes=IMAQdx_properties,orientation='side')

#an unused but worked class for flea cam
#FlyCapture2Camera(name='MOT_flea', parent_device=camera_trigger_flea, connection='trigger', serial_number=0x009014EC, camera_attributes=MOT_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='side')
