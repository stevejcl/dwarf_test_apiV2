from lib.websockets_utils import connect_socket
from lib.websockets_testV2 import fct_show_test

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

def read_latitude():
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        latitude = config.getfloat('CONFIG', 'LATITUDE')
        return latitude
    except configparser.NoOptionError:
        print("latitude not found.")
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
