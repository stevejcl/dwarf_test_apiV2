from lib.websockets_utils import connect_socket
from lib.websockets_testV2 import fct_show_test
from lib.websockets_testV2 import fct_decode_wireshark

from lib.data_utils import get_exposure_index_by_name
from lib.data_utils import get_gain_index_by_name

import lib.my_logger as log

import proto.astro_pb2 as astro
import proto.system_pb2 as system
import proto.camera_pb2 as camera
import proto.protocol_pb2 as protocol

import configparser
import time
import math



def read_longitude():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        longitude = config.getfloat('CONFIG', 'LONGITUDE')
        return longitude
    except configparser.NoOptionError:
        print("longitude not found.")
        return None
    except configparser.NoSectionError:
        print("Data not found.")
        return None

def read_latitude():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        latitude = config.getfloat('CONFIG', 'LATITUDE')
        return latitude
    except configparser.NoOptionError:
        print("latitude not found.")
        return None
    except configparser.NoSectionError:
        print("Data not found.")
        return None

def read_timezone():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        timezone = config.get('CONFIG', 'TIMEZONE')
        return timezone
    except configparser.NoOptionError:
        print("timezone not found.")
        return None
    except configparser.NoSectionError:
        print("Data not found.")
        return None

def read_camera_exposure():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_exposure = config.get('CONFIG', 'EXPOSURE')
        return camera_exposure
    except configparser.NoOptionError:
        print("camera exposure not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def read_camera_gain():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_gain = config.get('CONFIG', 'GAIN')
        return camera_gain
    except configparser.NoOptionError:
        print("camera gain not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def read_camera_IR():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_IR = config.get('CONFIG', 'IRCUT')
        return camera_IR
    except configparser.NoOptionError:
        print("camera IRCUT value not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def read_camera_binning():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_binning = config.get('CONFIG', 'BINNING')
        return camera_binning
    except configparser.NoOptionError:
        print("camera binning not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def read_camera_format():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_format = config.get('CONFIG', 'FORMAT')
        return camera_format
    except configparser.NoOptionError:
        print("camera format of image not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def read_camera_count():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        camera_count = config.get('CONFIG', 'COUNT')
        return camera_count
    except configparser.NoOptionError:
        print("Nb of images to take not found.")
        return False
    except configparser.NoSectionError:
        print("Data not found.")
        return False

def parse_ra_to_float(ra_string):
    # Split the RA string into hours, minutes, and seconds
    hours, minutes, seconds = map(float, ra_string.split(':'))

    # Convert to decimal degrees
    ra_decimal = hours + minutes / 60 + seconds / 3600

    return ra_decimal
    
def parse_dec_to_float(dec_string):
    # Split the Dec string into degrees, minutes, and seconds
    if dec_string[0] == '-':
        sign = -1
        dec_string = dec_string[1:]
    else:
        sign = 1
    print(dec_string)
    degrees, minutes, seconds = map(float, dec_string.split(':'))

    # Convert to decimal degrees
    dec_decimal = sign * degrees + minutes / 60 + seconds / 3600

    return dec_decimal

def perform_getstatus():
    # GET STATUS
    module_id = 1  # MODULE_TELEPHOTO
    type_id = 0; #REQUEST

    ReqGetSystemWorkingState_message = camera.ReqGetSystemWorkingState()

    command = 10039 #CMD_CAMERA_TELE_GET_SYSTEM_WORKING_STATE
    response = connect_socket(ReqGetSystemWorkingState_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("Get Status success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_goto(ra, dec, target):

    # GOTO
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqGotoDSO_message = astro.ReqGotoDSO()
    ReqGotoDSO_message.ra = ra
    ReqGotoDSO_message.dec = dec
    ReqGotoDSO_message.target_name = target

    command = 11002 #CMD_ASTRO_START_GOTO_DSO
    response = connect_socket(ReqGotoDSO_message, command, type_id, module_id)

    if response is not False: 

      if response == "ok":
          log.debug("Goto success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_goto_stellar(target_id, target_name):

    if read_longitude() is None:
        print("Longitude is not defined! ")
        return

    if read_latitude() is None:
        print("Latitude is not defined! ")
        return

    # GOTO
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqGotoSolarSystem_message = astro.ReqGotoSolarSystem()
    ReqGotoSolarSystem_message.index = target_id
    ReqGotoSolarSystem_message.lon = read_longitude()
    ReqGotoSolarSystem_message.lat = read_latitude()
    ReqGotoSolarSystem_message.target_name = target_name

    command = 11003 #CMD_ASTRO_START_GOTO_SOLAR_SYSTEM
    response = connect_socket(ReqGotoSolarSystem_message, command, type_id, module_id)

    if response is not False: 

      if response == "ok":
          log.debug("Goto success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perfom_takeAstroPhoto():

    # START CAPTURE RAW LIVE STACKING
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqCaptureRawLiveStacking_message = astro.ReqCaptureRawLiveStacking()

    command = 11005 #CMD_ASTRO_START_CAPTURE_RAW_LIVE_STACKING
    response = connect_socket(ReqCaptureRawLiveStacking_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("START CAPTURE RAW LIVE STACKING success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perfom_stopAstroPhoto():

    # STOP CAPTURE RAW LIVE STACKING
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqStopCaptureRawLiveStacking_message = astro.ReqStopCaptureRawLiveStacking()

    command = 11006 #CMD_ASTRO_STOP_CAPTURE_RAW_LIVE_STACKING
    response = connect_socket(ReqStopCaptureRawLiveStacking_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("STOP CAPTURE RAW LIVE STACKING success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perfom_GoLive():

    # CMD_ASTRO_GO_LIVE
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqGoLive_message = astro.ReqGoLive()

    command = 11010 #CMD_ASTRO_GO_LIVE
    response = connect_socket(ReqGoLive_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("GO LIVE success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_time():

    # SET TIME
    module_id = 4  # MODULE_SYSTEM
    type_id = 0; #REQUEST

    ReqSetTime_message = system.ReqSetTime()
    ReqSetTime_message.timestamp = math.floor(time.time())

    command = 13000 #CMD_SYSTEM_SET_TIME
    response = connect_socket(ReqSetTime_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("Set Time success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_timezone():

    # SET TIMEZONE
    module_id = 4  # MODULE_SYSTEM
    type_id = 0; #REQUEST

    ReqSetTimezone_message = system.ReqSetTimezone()
    ReqSetTimezone_message.timezone = read_timezone()

    command = 13001 #CMD_SYSTEM_SET_TIME_ZONE
    response = connect_socket(ReqSetTimezone_message, command, type_id, module_id)

    if response is not False: 

      if response == 0:
          log.debug("Set TimeZone success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_calibration():

    # CALIBRATION
    module_id = 3  # MODULE_ASTRO
    type_id = 0; #REQUEST

    ReqStartCalibration_message = astro.ReqStartCalibration ()

    command = 11000 #CMD_ASTRO_START_CALIBRATION

    response = connect_socket(ReqStartCalibration_message, command, type_id, module_id)

    if response is not False: 

      if response == "ok":
          log.debug("Goto success")
          return True
      else:
          log.error("Error:", response)
    else:
        log.error("Dwarf API:", "Dwarf II not connected")

    return False

def perform_decoding_test(show_test, show_test1, show_test2):

    fct_show_test(show_test, show_test1, show_test2)


def perform_decode_wireshark(user_frame, masked, user_maskedcode):

    fct_decode_wireshark(user_frame, masked, user_maskedcode)

def format_double(value_str):
    try:
        value = float(value_str)
        if value <= 0:
            return value_str
        elif 0 < value < 1:
            # Représenter sous la forme "1/x"
            denominator = int(1 / value)
            return f"1/{denominator}"
        else:
            # Conserver la représentation en virgule flottante pour d'autres cas
            return value_str
    except ValueError:
        # La chaîne n'est pas un nombre valide
        return value_str

def perform_get_all_camera_setting():

  module_id = 1  # MODULE_TELE_CAMERA
  type_id = 0; #REQUEST

  ReqGetAllParams_message = camera.ReqGetAllParams ()

  command = 10036; #CMD_CAMERA_TELE_GET_ALL_PARAMS

  response = connect_socket(ReqGetAllParams_message, command, type_id, module_id)
  
  return response


def perform_get_all_feature_camera_setting():

  module_id = 1  # MODULE_TELE_CAMERA
  type_id = 0; #REQUEST

  ReqGetAllFeatureParams_message = camera.ReqGetAllFeatureParams ()

  command = 10038; #CMD_CAMERA_TELE_GET_ALL_FEATURE_PARAMS

  response = connect_socket(ReqGetAllFeatureParams_message, command, type_id, module_id)

  return response

def perform_get_camera_setting( type):

  # brightness
  module_id = 1  # MODULE_TELE_CAMERA
  type_id = 0; #REQUEST

  ReqGetBrightness_message = camera.ReqGetBrightness ()

  command = 10016; #CMD_CAMERA_TELE_GET_BRIGHTNESS

  response = connect_socket(ReqGetBrightness_message, command, type_id, module_id)

  ReqGetContrast_message = camera.ReqGetContrast ()

  command = 10018; #CMD_CAMERA_TELE_GET_CONTRAST

  response = connect_socket(ReqGetContrast_message, command, type_id, module_id)

  if (type == "exposure"):
    # exposure
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqGetExp_message = camera.ReqGetExp ()

    command = 10010; #CMD_CAMERA_TELE_GET_EXP

    response = connect_socket(ReqGetExp_message, command, type_id, module_id)

    return format_double(response)

  elif (type == "gain"):
    # gain
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqGetGain_message = camera.ReqGetGain ()

    command = 10014; #CMD_CAMERA_TELE_GET_GAIN

    response = connect_socket(ReqGetGain_message, command, type_id, module_id)

    return response

  elif (type == "IR"):
    # gain
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqGetIrCut_message = camera.ReqSetIrCut ()

    command = 10032; #CMD_CAMERA_TELE_GET_IRCUT

    response = connect_socket(ReqGetIrCut_message, command, type_id, module_id)

    return response

  elif (type == "binning"):
    # binning
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 0; # "Astro binning"
    ReqSetFeatureParams_message.param.mode_index = 0;
    ReqSetFeatureParams_message.param.index = int(value);
    ReqSetFeatureParams_message.param.continue_value = 0;

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)

  elif (type == "fileFormat"):
    # fileFormat
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 2; # "Astro format"
    ReqSetFeatureParams_message.param.mode_index = 0;
    ReqSetFeatureParams_message.param.index = int(value);
    ReqSetFeatureParams_message.param.continue_value = 0;

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)

  elif (type == "count"):
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 1; # "Astro img_to_take"
    ReqSetFeatureParams_message.param.mode_index = 1;
    ReqSetFeatureParams_message.param.index = 0;
    ReqSetFeatureParams_message.param.continue_value = int(value);

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM
    cmd = Dwarfii_Api.DwarfCMD.CMD_CAMERA_TELE_SET_FEATURE_PARAM;

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)

def permform_update_camera_setting( type, value):

  if (type == "exposure"):
    # exposure_mode
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetExpMode_message = camera.ReqSetExpMode ()
    ReqSetExpMode_message.mode = 1

    command = 10007; #CMD_CAMERA_TELE_SET_EXP_MODE

    response = connect_socket(ReqSetExpMode_message, command, type_id, module_id)

    # exposure

    ReqSetExp_message = camera.ReqSetExp ()
    ReqSetExp_message.index = get_exposure_index_by_name(str(value))

    command = 10009; #CMD_CAMERA_TELE_SET_EXP

    response = connect_socket(ReqSetExp_message, command, type_id, module_id)


  elif (type == "gain"):
    # gain 
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetGain_message = camera.ReqSetGain ()
    ReqSetGain_message.index = get_gain_index_by_name(str(value))

    command = 10013; #CMD_CAMERA_TELE_SET_GAIN

    response = connect_socket(ReqSetGain_message, command, type_id, module_id)

  elif (type == "IR"):
    # gain
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetIrCut_message = camera.ReqSetIrCut ()
    ReqSetIrCut_message.value = int(value)

    command = 10031; #CMD_CAMERA_TELE_SET_IRCUT

    response = connect_socket(ReqSetIrCut_message, command, type_id, module_id)

  elif (type == "binning"):
    # binning
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 0; # "Astro binning"
    ReqSetFeatureParams_message.param.mode_index = 0;
    ReqSetFeatureParams_message.param.index = int(value);
    ReqSetFeatureParams_message.param.continue_value = 0;

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)

  elif (type == "fileFormat"):
    # fileFormat
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 2; # "Astro format"
    ReqSetFeatureParams_message.param.mode_index = 0;
    ReqSetFeatureParams_message.param.index = int(value);
    ReqSetFeatureParams_message.param.continue_value = 0;

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)

  elif (type == "count"):
    module_id = 1  # MODULE_TELE_CAMERA
    type_id = 0; #REQUEST

    ReqSetFeatureParams_message = camera.ReqSetFeatureParams ()
    ReqSetFeatureParams_message.param.hasAuto = False;
    ReqSetFeatureParams_message.param.auto_mode = 1; # Manual
    ReqSetFeatureParams_message.param.id = 1; # "Astro img_to_take"
    ReqSetFeatureParams_message.param.mode_index = 1;
    ReqSetFeatureParams_message.param.index = 0;
    ReqSetFeatureParams_message.param.continue_value = int(value);

    command = 10037; #CMD_CAMERA_TELE_SET_FEATURE_PARAM

    response = connect_socket(ReqSetFeatureParams_message, command, type_id, module_id)
