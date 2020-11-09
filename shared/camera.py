import sys
sys.path.append(r'C:\Users\RbRb\labscript-suite\userlib\labscriptlib\RbRb')
from labscript_devices.FlyCapture2Camera.labscript_devices import FlyCapture2Camera
from labscript_devices.IMAQdxCamera.labscript_devices import IMAQdxCamera
from labscript_utils import import_or_reload

MOT_XY_flea_camera_attributes = {
    'AcquisitionAttributes::VideoMode': 'Format 7, Mode 0, 648 x 488',
    'AcquisitionAttributes::PixelFormat': 'Mono 16',
    # 'AcquisitionAttributes::VideoMode': '640 x 480 Mono 16 60.00 fps',
    'AcquisitionAttributes::PacketSize': 1500,
    'AcquisitionAttributes::Timeout': 5000,
    'CameraAttributes::AutoExposure::Mode': 'Off',
    'CameraAttributes::Brightness::Mode': 'Ignored',
    'CameraAttributes::FrameRate::Mode': 'Auto',
    'CameraAttributes::Gain::Mode': 'Absolute',
    'CameraAttributes::Gain::Value': '-3', # decrease me
    'CameraAttributes::Gamma::Mode': 'Off',
    'CameraAttributes::Sharpness::Mode': 'Off',
    # 'CameraAttributes::Shutter::Mode': 'Absolute',
    # 'CameraAttributes::Shutter::Value': '0.000010',
    'CameraAttributes::Trigger::TriggerActivation': 'Level High',
    'CameraAttributes::Trigger::TriggerMode': 'Mode1',
    'CameraAttributes::Trigger::TriggerParameter': 0,
    'CameraAttributes::Trigger::TriggerSource': 'Source 0',
    'AcquisitionAttributes::BitsPerPixel': '12-bit',
    # 'AcquisitionAttributes::VideoMode': '640 x 480 Mono 16 60.00 fps',
   # 'CameraAttributes::ImageFormatControl::PixelFormat': 'Mono 16', # IBS change
}

MOT_YZ_flea_camera_attributes = {
    'AcquisitionAttributes::VideoMode': '640 x 480 Mono 16 60.00 fps',
    # 'AcquisitionAttributes::PacketSize': 1500,
    'AcquisitionAttributes::Timeout': 5000,
    'CameraAttributes::AutoExposure::Mode': 'Off',
    'CameraAttributes::Brightness::Mode': 'Ignored',
    'CameraAttributes::FrameRate::Mode': 'Auto',
    'CameraAttributes::Gain::Mode': 'Absolute',
    'CameraAttributes::Gain::Value': '10', 
    'CameraAttributes::Gamma::Mode': 'Off',
    'CameraAttributes::Sharpness::Mode': 'Off',
    # 'CameraAttributes::Shutter::Mode': 'Absolute',
    # 'CameraAttributes::Shutter::Value': '0.000010',
    'CameraAttributes::Trigger::TriggerActivation': 'Level High',
    'CameraAttributes::Trigger::TriggerMode': 'Mode1',
    'CameraAttributes::Trigger::TriggerParameter': 0,
    'CameraAttributes::Trigger::TriggerSource': 'Source 0',
    'AcquisitionAttributes::BitsPerPixel': '12-bit'
}

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
manual_mode_camera_attributes = MOT_XY_flea_camera_attributes.copy()
manual_mode_camera_attributes['CameraAttributes::Trigger::TriggerMode'] = 'Mode3'
IMAQdxCamera(name='MOT_XY_flea', parent_device=camera_trigger_MOT_XY_flea, connection='trigger', serial_number=0xB09D01009014EC, camera_attributes=MOT_XY_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='XY')
manual_mode_camera_attributes = MOT_YZ_flea_camera_attributes.copy()
manual_mode_camera_attributes['CameraAttributes::Trigger::TriggerMode'] = 'Mode3'
IMAQdxCamera(name='MOT_YZ_flea', parent_device=camera_trigger_MOT_YZ_flea, connection='trigger', serial_number=0xB09D01009014EE, camera_attributes=MOT_YZ_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='YZ')

manual_mode_camera_attributes = Science_flea_camera_attributes.copy()
manual_mode_camera_attributes['CameraAttributes::Acquisition::Trigger::TriggerMode'] = 'Off'
IMAQdxCamera(name='Science_flea', parent_device=camera_trigger_Science_flea, connection='trigger', trigger_edge_type='rising', serial_number=0xF315BC7CB, camera_attributes=Science_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='science')
# MOT_XY_flea_camera_attributes = dict([['AcquisitionAttributes::AdvancedEthernet::Controller::DestinationMode', 'Unicast'],
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
#FlyCapture2Camera(name='MOT_XY_flea', parent_device=camera_trigger_flea, connection='trigger', serial_number=0x009014EC, camera_attributes=MOT_XY_flea_camera_attributes, manual_mode_camera_attributes=manual_mode_camera_attributes, orientation='side')
