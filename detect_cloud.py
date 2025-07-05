import configparser
from datetime import datetime
import time
import os
from cloud_detector import detect_cloud_photo_histogram_and_stars

from dwarf_python_api.lib.dwarf_utils import perform_disconnect
from dwarf_python_api.lib.dwarf_utils import perform_time
from dwarf_python_api.lib.dwarf_utils import perform_timezone
from dwarf_python_api.lib.dwarf_utils import read_longitude
from dwarf_python_api.lib.dwarf_utils import read_latitude
from dwarf_python_api.lib.dwarf_utils import read_camera_exposure
from dwarf_python_api.lib.dwarf_utils import read_camera_gain
from dwarf_python_api.lib.dwarf_utils import read_camera_IR
from dwarf_python_api.lib.dwarf_utils import read_camera_binning
from dwarf_python_api.lib.dwarf_utils import read_camera_format
from dwarf_python_api.lib.dwarf_utils import read_camera_count
from dwarf_python_api.lib.dwarf_utils import read_camera_wide_exposure
from dwarf_python_api.lib.dwarf_utils import read_camera_wide_gain
from dwarf_python_api.lib.dwarf_utils import perform_GoLive
from dwarf_python_api.lib.dwarf_utils import perform_takeWidePhoto
from dwarf_python_api.lib.dwarf_utils import perform_update_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_feature_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_camera_wide_setting
from dwarf_python_api.lib.dwarf_utils import unset_HostMaster
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_wifi_type
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoAP
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country_list
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_psd
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoSTA
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_ssid
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_pwd
from dwarf_python_api.lib.dwarf_utils import save_bluetooth_config_from_ini_file
from dwarf_python_api.lib.dwarf_utils import perform_get_camera_setting

from dwarf_python_api.lib.data_utils import get_exposure_name_by_index
from dwarf_python_api.lib.data_utils import get_gain_name_by_index
from dwarf_python_api.lib.data_wide_utils import get_wide_exposure_name_by_index
from dwarf_python_api.lib.data_wide_utils import get_wide_gain_name_by_index


from dwarf_python_api.get_live_data_dwarf import getGetLastPhoto, getlistPhoto, read_config
import dwarf_python_api.get_config_data

from dwarf_ble_connect.connect_bluetooth import connect_bluetooth
from dwarf_ble_connect.lib.connect_direct_bluetooth import connect_ble_direct_dwarf, connect_ble_dwarf_win
from dwarf_python_api.lib.websockets_utils import get_client_status

global is_connected
is_connected = False

def display_menu():
    print("")
    print("----------------------------------")
    print("    Detect Cloud application,     ")
    print("    Connect first to the Dwarf    ")
    print("----------------------------------")
    print("C. Connect Dwarf")
    print("S. Show Status data")
    print("D. Force Disconnection")

    print("----------------------------------")
    print("    Detect Cloud application      ")
    print("----------------------------------")

    print("GO. Start Cloud detection")
    print("CTRL+C. Stop Cloud detection")

    print("----------------------------------")
    print("           CONFIG Command         ")
    print("----------------------------------")

    print("BR. Read Bluetooth Param Config Information")
    print("BS. Save Bluetooth Param Config Information and for Connection")
    print("C1. Read Saved Config Camera Data")
    print("C2. Input Camera Data to Config")
    print("C3. Read Current Dwarf Camera Data")
    print("C4. Import Saved Config Camera Data into Dwarf")

    print("U. Unset HOST MASTER")
    print("L. Go Live Action")
    print("0. Exit")


def get_user_choice():
    try:
        choice = input("Enter your choice (C,BR,BS,C1 to C4,S,U,L,D and GO or STOP) or 0 to exit: ")
    except KeyboardInterrupt:
        print("Operation interrupted by the user (CTRL+C).")
        choice = '0'
    return choice

def option_U():
    print("You selected Option Y: Set HOST MASTER")
    unset_HostMaster()
    # Add your Option 12 functionality here

def option_D():
    print("You selected Option D: Force Disconnection")
    perform_disconnect()
    # Add your Option D functionality here

def option_S():
    import json
    print("You selected Option S: Status Data")
    status = get_client_status()
    print(json.dumps(status, indent=4))
    # Add your Option M functionality here

def option_C1():
    print("You selected Option C1. Read Saved Config Camera Data")
    print("")
    # Add your Option C1 functionality here
    read_camera_data()

def option_C2():
    print("You selected Option C2. Input Camera Data to Config")
    print("")
    # Add your Option C2 functionality here
    input_camera_data()

def option_C3():
    print("You selected Option C3. Read Current Dwarf Camera Data")
    print("")
    # Add your Option C3 functionality here
    camera_exposure = False
    camera_gain = False
    camera_binning = False
    camera_IR = False
    camera_format = False
    camera_count = False
    camera_wide_exposure = False
    camera_wide_gain = False

    result = perform_get_all_camera_setting()
    result_feature = perform_get_all_feature_camera_setting()
    result_wide = perform_get_all_camera_wide_setting()
    print("------------------")

    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = str(data_config['dwarf_id'])
    print(f"Connected to Dwarf {int(dwarf_id)+1}")

    # ALL PARAMS
    print(f"debug: {result}")

    # ALL Wide PARAMS
    if (result_wide and not isinstance(result_wide,int)):
        # get Camera
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_wide["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]

           camera_wide_exposure = str(get_wide_exposure_name_by_index(index_value,dwarf_id))
           print("the wide exposition is: ", camera_wide_exposure)
        else:
           print("the wide exposition has not been found")

        # get Gain
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_wide["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]

           camera_wide_gain = str(get_wide_gain_name_by_index(index_value,dwarf_id))
           print("the wide gain is: ", camera_wide_gain)
        else:
           print("the wide gain has not been found")

    # error no response on D3
    # print("direct=> the wide gain is: ", perform_get_camera_setting("wide_gain"))
    

def option_C4():
    print("You selected Option C4. Import Saved Config Camera Data into Dwarf")
    print("")
    # Add your Option C4 functionality here
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = str(data_config['dwarf_id']) 
    print(f"Connected to Dwarf {dwarf_id}")

    if (camera_wide_exposure := read_camera_wide_exposure()):
        print("the wide exposition is: ", camera_wide_exposure)
        perform_update_camera_setting("wide_exposure", camera_wide_exposure, dwarf_id)

    if (camera_wide_gain := read_camera_wide_gain()):
        print("the wide gain is:", camera_wide_gain)
        perform_update_camera_setting("wide_gain", camera_wide_gain, dwarf_id)

def option_L():
    print("You selected Option L. Go Live Action")
    print("")
    # Add your Option L functionality here
    perform_GoLive()

def option_C():
    global is_connected

    print("You selected Option C. connect Bluetooth and Start STA Mode with Python")
    print("")
    # Add your Option BCD functionality here
    ble_psd = read_bluetooth_ble_psd() or "DWARF_12345678" 
    ble_STA_ssid = read_bluetooth_ble_STA_ssid() or ""
    ble_STA_pwd = read_bluetooth_ble_STA_pwd() or ""
    # Test Auto Select
    auto_select = "" # "DWARF3_3AD246" or 0 to give the list and "" to connect to the first after 10 s

    if (connect_ble_direct_dwarf(ble_psd, ble_STA_ssid, ble_STA_pwd,auto_select)):
        
        #init Frame : TIME and TIMZONE
        result = perform_time()
       
        if result:
           result = perform_timezone()
        else:
            print("Dwarf not connected, retry ...")

        is_connected = result
 
    else:
        is_connected = False
        print("Dwarf not connected, retry ...")

def option_BR():
    print("You selected Option R. Read Bluetooth Param Config Information")
    print("")
    # Add your Option BR functionality here
    read_bluetooth_data()

def option_BS():
    print("You selected Option S. Save Bluetooth Param Config Information")
    print("")
    # Add your Option BS functionality here
    input_bluetooth_data()

def input_data():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

def validate_input(input_str, min, max):
    try:
        if '/' in input_str:
            # Handle fraction input
            numerator, denominator = input_str.split("/")

            # Convert to integers
            numerator = int(numerator)
            denominator = int(denominator)

            # Check for zero division
            if denominator == 0:
                print("Invalid input. Denominator cannot be zero.")
                return False

            # Perform the division to get the decimal value
            result = numerator / denominator

        else:
            # Handle decimal or integer input
            result = float(input_str)  # Automatically handles both decimal and integer inputs

        # Check if result is greater than 0 and less than 100
        if min < result < max:
            return True
        else:
            print(f"Invalid input. The value is not between {min} and {max}.")
            return False
    
    except ValueError:
        print("Invalid input. Please provide a valid integer or fraction.")
        return False

def input_camera_data():
    # get dwarf type id
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = str(data_config['dwarf_id'])
    print(f"connected to Dwarf {dwarf_id}")
    if dwarf_id == "2":
        prompt = "Enter the desired exposition in seconds (0 = auto - 60), use fraction for less than 1s (ex: 1/10):"
    else:
        prompt = "Enter the desired exposition in seconds (0 = auto - 15), use fraction for less than 1s (ex: 1/10):"
    camera_exposure_init = read_camera_exposure()
    camera_exposure = input(f"{prompt}[{camera_exposure_init}]:") if camera_exposure_init else input(prompt+"[1]")
    if not camera_exposure and not camera_exposure_init:
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif dwarf_id == "1" and camera_exposure and not validate_input(camera_exposure, 0, 15):
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif dwarf_id == "2" and camera_exposure and not validate_input(camera_exposure, 0, 60):
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif (camera_exposure):
        print("You entered:", camera_exposure)
    elif dwarf_id == "1" and camera_exposure_init and not validate_input(camera_exposure_init, 0, 15):
        print("Input Data Error:", camera_exposure_init)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif dwarf_id == "2" and camera_exposure_init and not validate_input(camera_exposure_init, 0, 60):
        print("Input Data Error:", camera_exposure_init)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif (camera_exposure_init):
        camera_exposure = camera_exposure_init
        print("Saved value used:", camera_exposure)
    else:
        print("No value entered:")

    camera_gain_init = read_camera_gain()
    prompt = "Enter the desired gain between (0-240):"
    camera_gain = input(f"{prompt}[{camera_gain_init}]:") if camera_gain_init else input(prompt+"[80]")
    if not camera_gain and not camera_gain_init:
        camera_gain = "80"
        print("Set to Default:", camera_gain)
    elif camera_gain and (int(camera_gain)<0 or int(camera_gain) > 240):
        print("Input Data Error:", camera_gain)
        camera_gain = "80"
        print("Set to Default:", camera_gain)
    elif (camera_gain):
        print("You entered:", camera_gain)
    elif (camera_gain_init):
        camera_gain = camera_gain_init
        print("Saved value used:", camera_gain)
    else:
        print("No value entered:")

    camera_IR_init = read_camera_IR()
    if dwarf_id == "1":
        prompt = "Enter the desired IR value: 0 for IRCut, 1 for IRPass:"
    else:
        prompt = "Enter the desired IR value: 0 for VIS, 1 for ASTRO, 2 for DUAL-BAND:"
    camera_IR = input(f"{prompt}[{camera_IR_init}]:") if camera_IR_init else input(prompt+"[IRCut]")
    if not camera_IR and not camera_IR_init:
        camera_IR = "0"
        if dwarf_id == "1":
            print("Set to Default (IRCut):", camera_IR)
        else:
            print("Set to Default (VIS):", camera_IR)
    elif camera_IR and (camera_IR!="0" and camera_IR !="1" and dwarf_id == "1"):
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (IRCut):", camera_IR)
    elif camera_IR and (camera_IR!="0" and camera_IR !="1" and camera_IR !="2" and dwarf_id == "2"):
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (VIS):", camera_IR)
    else:
        print("You entered:", camera_IR)

    camera_binning_init = read_camera_binning()
    prompt = "Enter the desired Binning value: 0 for 4k, 1 for 2k:"
    camera_binning = input(f"{prompt}[{camera_binning_init}]:") if camera_binning_init else input(prompt+"[4k]")
    if not camera_binning and not camera_binning_init:
        camera_binning = "0"
        print("Set to Default (4k):", camera_binning)
    elif camera_binning and (camera_binning!="0" and camera_binning !="1"):
        print("Input Data Error:", camera_binning)
        camera_binning = "0"
        print("Set to Default (4k):", camera_binning)
    else:
        print("You entered:", camera_binning)

    camera_format_init = read_camera_format()
    prompt = "Enter the desired image format value: 0 for FITS, 1 for TIFF:"
    camera_format = input(f"{prompt}[{camera_format_init}]:") if camera_format_init else input(prompt+"[FITS]")
    if not camera_format and not camera_format_init:
        camera_format = "0"
        print("Set to Default (FITS):", camera_format)
    elif camera_format and (camera_format!="0" and camera_format !="1"):
        print("Input Data Error:", camera_format)
        camera_format = "0"
        print("Set to Default (FITS):", camera_format)
    else:
        print("You entered:", camera_format)

    camera_count_init = read_camera_count()
    prompt = "Enter the desired number of images for the session between (1-999)"
    camera_count = input(f"{prompt}[{camera_count_init}]:") if camera_count_init else input(prompt+"[999]")
    if not camera_count and not camera_count_init:
        camera_count = "999"
        print("Set to Default:", camera_count)
    elif camera_count and (int(camera_count)<1 or int(camera_count) > 999):
        print("Input Data Error:", camera_count)
        camera_count = "999"
        print("Set to Default:", camera_count)
    else:
        print("You entered:", camera_count)

    if dwarf_id == "2":
        prompt = "Enter the desired wide exposition in seconds (0 = auto - 60), use fraction for less than 1s (ex: 1/10):"
    else:
        prompt = "Enter the desired wide exposition in seconds (0 = auto - 1.0), use fraction for less than 1s (ex: 1/10):"
    camera_wide_exposure_init = read_camera_wide_exposure()
    camera_wide_exposure = input(f"{prompt}[{camera_wide_exposure_init}]:") if camera_wide_exposure_init else input(prompt+"[1]")
    if not camera_wide_exposure and not camera_wide_exposure_init:
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif dwarf_id == "1" and camera_wide_exposure and not validate_input(camera_wide_exposure, 0, 15):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif dwarf_id == "2" and camera_wide_exposure and not validate_input(camera_wide_exposure, 0, 60):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif (camera_wide_exposure):
        print("You entered:", camera_wide_exposure)
    elif dwarf_id == "1" and camera_wide_exposure_init and not validate_input(camera_wide_exposure_init, 0, 15):
        print("Input Data Error:", camera_wide_exposure)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif dwarf_id == "2" and camera_wide_exposure_init and not validate_input(camera_wide_exposure_init, 0, 60):
        print("Input Data Error:", camera_wide_exposure_init)
        camera_wide_exposure = "1"
        print("Set to Default:", camera_wide_exposure)
    elif (camera_wide_exposure_init):
        camera_wide_exposure = camera_wide_exposure_init
        print("Saved value used:", camera_wide_exposure)
    else:
        print("No value entered:")

    if dwarf_id == "2":
        prompt = "Enter the desired wide gain between (0-240):"
    else:
        prompt = "Enter the desired wide gain between (60-160):"
    camera_wide_gain_init = read_camera_wide_gain()
    camera_wide_gain = input(f"{prompt}[{camera_wide_gain_init}]:") if camera_wide_gain_init else input(prompt+"[80]")
    if not camera_wide_gain and not camera_wide_gain_init:
        if dwarf_id == "2":
            camera_wide_gain = "0"
        else:
            camera_wide_gain = "60"
        print("Set to Default:", camera_wide_gain)
    elif dwarf_id == "2" and camera_wide_gain and (int(camera_wide_gain)<0 or int(camera_wide_gain) > 240):
        print("Input Data Error:", camera_wide_gain)
        camera_wide_gain = "0"
        print("Set to Default:", camera_wide_gain)
    elif dwarf_id == "1" and camera_wide_gain and (int(camera_wide_gain)<60 or int(camera_wide_gain) > 160):
        print("Input Data Error:", camera_wide_gain)
        camera_wide_gain = "60"
        print("Set to Default:", camera_wide_gain)
    elif (camera_wide_gain):
        print("You entered:", camera_wide_gain)
    elif (camera_wide_gain_init):
        camera_wide_gain = camera_wide_gain_init
        print("Saved value used:", camera_wide_gain)
    else:
        print("No value entered:")

    update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count, camera_wide_exposure, camera_wide_gain)

def read_camera_data():
    print("The values in the Config File are : ")
    print("-----------------------------------")
    data_config = dwarf_python_api.get_config_data.get_config_data()
    dwarf_id = str(data_config['dwarf_id'])
    if (camera_exposure := read_camera_exposure()):
        print("the exposition is: ", camera_exposure)
    if (camera_gain := read_camera_gain()):
        print("the gain is:", camera_gain)
    if (camera_IR := read_camera_IR()):
        if dwarf_id == "1":
            if (camera_IR == "0") :
                print("the IR value is: IRCut")
            else:
                print("the IR value is: IRPass")
        else:
            if (camera_IR == "0") :
                print("the IR value is: VIS")
            elif (camera_IR == "1") :
                print("the IR value is: ASTRO")
            else:
                print("the IR value is: DUAL-BAND")
    if (camera_binning := read_camera_binning()):
        if (camera_binning == "0"):
            print("the Binning value is 4k")
        else:
            print("the Binning value is 2k")
    if (camera_format := read_camera_format()):
        if (camera_format == "0"):
            print("the image format value is: FITS")
        else:
            print("the image format value is: TIFF")
    if (camera_count := read_camera_count()):
        print("the number of images for the session is:", camera_count)
    if (camera_wide_exposure := read_camera_wide_exposure()):
        print("the wide exposition is: ", camera_wide_exposure)
    if (camera_wide_gain := read_camera_wide_gain()):
        print("the wide gain is:", camera_wide_gain)

def input_bluetooth_data():
    prompt = "Enter the desired AP wifi type  (0 = 5G (defaut), 1 = 2.4G) "
    ble_wifi_type_init = read_bluetooth_ble_wifi_type()
    ble_wifi_type = input(f"{prompt}[{ble_wifi_type_init}]:") if ble_wifi_type_init else input(prompt+"[0]")
    if not ble_wifi_type and not ble_wifi_type_init:
        ble_wifi_type = "0"
        print("Set to Default:", ble_wifi_type)
    elif ble_wifi_type and (int(ble_wifi_type)<0 or int(ble_wifi_type) > 1):
        print("Input Data Error:", ble_wifi_type)
        ble_wifi_type = "0"
        print("Set to Default:", ble_wifi_type)
    elif (ble_wifi_type):
        print("You entered:", ble_wifi_type)
    elif (ble_wifi_type_init):
        ble_wifi_type = ble_wifi_type_init
        print("Saved value used:", ble_wifi_type)
    else:
        print("No value entered:")

    prompt = "Enter the desired AP auto start  (0 = boot not start (defaut), 1 = boot start) "
    ble_autoAP_init = read_bluetooth_autoAP()
    ble_autoAP = input(f"{prompt}[{ble_autoAP_init}]:") if ble_autoAP_init else input(prompt+"[0]")
    if not ble_autoAP and not ble_autoAP_init:
        ble_autoAP = "0"
        print("Set to Default:", ble_autoAP)
    elif ble_autoAP and (int(ble_autoAP)<0 or int(ble_autoAP) > 1):
        print("Input Data Error:", ble_autoAP)
        ble_autoAP = "0"
        print("Set to Default:", ble_autoAP)
    elif (ble_autoAP):
        print("You entered:", ble_autoAP)
    elif (ble_autoAP_init):
        ble_autoAP = ble_autoAP_init
        print("Saved value used:", ble_autoAP)
    else:
        print("No value entered:")

    prompt = "Enter the desired Contry List config set  (0 = don't configure (defaut), 1 = configure) "
    ble_country_list_init = read_bluetooth_country_list()
    ble_country_list = input(f"{prompt}[{ble_country_list_init}]:") if ble_country_list_init else input(prompt+"[0]")
    if not ble_country_list and not ble_country_list_init:
        ble_country_list = "0"
        print("Set to Default:", ble_country_list)
    elif ble_country_list and (int(ble_country_list)<0 or int(ble_country_list) > 1):
        print("Input Data Error:", ble_country_list)
        ble_country_list = "0"
        print("Set to Default:", ble_country_list)
    elif (ble_country_list):
        print("You entered:", ble_country_list)
    elif (ble_country_list_init):
        ble_country_list = ble_country_list_init
        print("Saved value used:", ble_country_list)
    else:
        print("No value entered:")

    prompt = "Enter the desired Contry "
    ble_country_init = read_bluetooth_country()
    ble_country = input(f"{prompt}[{ble_country_init}]:") if ble_country_init else input(prompt)
    if not ble_country and not ble_country_init:
        ble_country = ""
    elif (ble_country):
        print("You entered:", ble_country)
    elif (ble_country_init):
        ble_country = ble_country_init
        print("Saved value used:", ble_country)
    else:
        print("No value entered:")

    prompt = "Enter the desired ble Password: "
    ble_psd_init = read_bluetooth_ble_psd()
    ble_psd = input(f"{prompt}[{ble_psd_init}]:") if ble_psd_init else input(prompt+"[DWARF_12345678]")
    if not ble_psd and not ble_psd_init:
        ble_psd = "DWARF_12345678"
        print("Set to Default:", ble_psd)
    elif (ble_psd):
        print("You entered:", ble_psd)
    elif (ble_psd_init):
        ble_psd = ble_psd_init
        print("Saved value used:", ble_psd)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA auto start  (0 = boot not start (defaut), 1 = boot start) "
    ble_autoSTA_init = read_bluetooth_autoSTA()
    ble_autoSTA = input(f"{prompt}[{ble_autoSTA_init}]:") if ble_autoSTA_init else input(prompt+"[0]")
    if not ble_autoSTA and not ble_autoSTA_init:
        ble_autoSTA = "0"
        print("Set to Default:", ble_autoSTA)
    elif ble_autoSTA and (int(ble_autoSTA)<0 or int(ble_autoSTA) > 1):
        print("Input Data Error:", ble_autoSTA)
        ble_autoSTA = "0"
        print("Set to Default:", ble_autoSTA)
    elif (ble_autoSTA):
        print("You entered:", ble_autoSTA)
    elif (ble_autoSTA_init):
        ble_autoSTA = ble_autoSTA_init
        print("Saved value used:", ble_autoSTA)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA ssid "
    ble_STA_ssid_init = read_bluetooth_ble_STA_ssid()
    ble_STA_ssid = input(f"{prompt}[{ble_STA_ssid_init}]:") if ble_STA_ssid_init else input(prompt)
    if (ble_STA_ssid):
        print("You entered:", ble_STA_ssid)
    elif (ble_STA_ssid_init):
        ble_STA_ssid = ble_STA_ssid_init
        print("Saved value used:", ble_STA_ssid)
    else:
        print("No value entered:")

    prompt = "Enter the desired STA Password "
    ble_STA_pwd_init = read_bluetooth_ble_STA_pwd()
    ble_STA_pwd = input(f"{prompt}[{ble_STA_pwd_init}]:") if ble_STA_pwd_init else input(prompt)
    if (ble_STA_pwd):
        print("You entered:", ble_STA_pwd)
    elif (ble_STA_pwd_init):
        ble_STA_pwd = ble_STA_pwd_init
        print("Saved value used:", ble_STA_pwd)
    else:
        print("No value entered:")

    update_bluetoothconfig(ble_wifi_type, ble_autoAP, ble_country_list, ble_country, ble_psd, ble_autoSTA, ble_STA_ssid, ble_STA_pwd)
    save_bluetooth_config_from_ini_file()

def read_bluetooth_data():
    print("The values in the Config File are : ")
    print("-----------------------------------")
    if (ble_wifi_type := read_bluetooth_ble_wifi_type()):
        if (ble_wifi_type == "0"):
            print("the AP wifi type is: 5G")
        else:
            print("the AP wifi type is: 2.4G")
    if (ble_autoAP := read_bluetooth_autoAP()):
        if (ble_autoAP == "0"):
            print("the AP auto start value is: boot not start")
        else:
            print("the AP auto start value: boot start")
    if (ble_country_list := read_bluetooth_country_list()):
        if (ble_country_list == "0"):
            print("the Contry List config set value is: don't configure")
        else:
            print("the Contry List config set value: configure")
    if (ble_country := read_bluetooth_country()):
        print("the country is: ", ble_country)
    if (ble_psd := read_bluetooth_ble_psd()):
        print("the ble Password is: ", ble_psd)
    if (ble_autoSTA := read_bluetooth_autoSTA()):
        if (ble_autoSTA == "0"):
            print("the STA auto start value is: boot not start")
        else:
            print("the STA auto start value: boot start")
    if (ble_STA_ssid := read_bluetooth_ble_STA_ssid()):
        print("the STA ssid is: ", ble_STA_ssid)
    if (ble_STA_pwd := read_bluetooth_ble_STA_pwd()):
        print("the STA Password is: ", ble_STA_pwd)

def update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count, camera_wide_exposure, camera_wide_gain):

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    if (camera_exposure):
        config['CONFIG']['EXPOSURE'] = camera_exposure
    if (camera_gain):
        config['CONFIG']['GAIN'] = camera_gain
    if (camera_IR):
        config['CONFIG']['IRCUT'] = camera_IR
    if (camera_binning):
        config['CONFIG']['BINNING'] = camera_binning
    if (camera_format):
        config['CONFIG']['FORMAT'] = camera_format
    if (camera_count):
        config['CONFIG']['COUNT'] = camera_count
    if (camera_wide_exposure):
        config['CONFIG']['WIDE_EXPOSURE'] = camera_wide_exposure
    if (camera_wide_gain):
        config['CONFIG']['WIDE_GAIN'] = camera_wide_gain

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def update_bluetoothconfig(ble_wifi_type, ble_autoAP, ble_country_list, ble_country, ble_psd, ble_autoSTA, ble_STA_ssid, ble_STA_pwd):

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    if (ble_wifi_type):
        config['CONFIG']['BLE_WIFI_TYPE'] = ble_wifi_type
    if (ble_autoAP):
        config['CONFIG']['BLE_AUTO_AP'] = ble_autoAP
    if (ble_country_list):
        config['CONFIG']['BLE_COUNTRY_LIST'] = ble_country_list
    if (ble_country):
        config['CONFIG']['BLE_COUNTRY'] = ble_country
    if (ble_psd):
        config['CONFIG']['BLE_PSD'] = ble_psd
    if (ble_autoSTA):
        config['CONFIG']['BLE_AUTO_STA'] = ble_autoSTA
    if (ble_STA_ssid):
        config['CONFIG']['BLE_STA_SSID'] = ble_STA_ssid
    if (ble_STA_pwd):
        config['CONFIG']['BLE_STA_PWD'] = ble_STA_pwd

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def read_config_images():
    global local_photo_directory

    config = configparser.ConfigParser()
    config.read('config.ini')
    log.notice("Read Config File.")

    try:
        local_photo_directory = config.get('CONFIG', 'LOCAL_PHOTO_DIRECTORY')
    except configparser.NoSectionError:
        log.error("ConfigFile not found.")
    except configparser.NoOptionError:
        log.error("Data not found.")


def extract_real_last_photo(photo_list):

    # Filter valid photos (not in future, not corrupted)
    valid_photos = []
    now = datetime.now()
 
    if not photo_list:
        return None,None

    for entry in photo_list:
        file = entry['file']
        try:
            # Extract datetime part from filename
            filename = file.replace('.jpg', '')
            date_str = filename.split("_")[2]
            dt = datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S-%f")
            
            if dt <= now:
                valid_photos.append({'index': entry['index'], 'file': file, 'datetime': dt})
            else:
                print(f"⚠️ Skipped future photo: {file}")

        except Exception as e:
            print(f"⚠️ Could not parse file {file}: {e}")

    # Now sort descending by datetime (latest first)
    valid_photos.sort(key=lambda x: x['datetime'], reverse=True)

    # Safely access the latest
    if valid_photos:
        latest_photo = valid_photos[0]
        print(f"✅ Latest valid photo: {latest_photo['file']} taken at {latest_photo['datetime']}")
        return latest_photo['index'],latest_photo['file']
    else:
        print("❌ No valid photo found")
        return None,None

def start_detect_cloud(interval_seconds=30, max_cycles=None):
    global is_connected
    print("Starting Detect Cloud function")
    print("")

    try:
        if not is_connected:
            print("Dwarf is not connected!")
            print("Connect to the Dwarf first!")
            return

        data_config = dwarf_python_api.get_config_data.get_config_data()

        # determine index of real last photo
        read_config()
        # Local Photo directory to get images files 
        local_photo_directory = os.path.abspath(dwarf_python_api.get_live_data_dwarf.local_photo_directory)
        print(f"local_photo_directory: {local_photo_directory}")
        index_previous_photo = "0"
        file_previous_photo = None

        photo_list = getlistPhoto("WIDE", "all" , "0")
        print(photo_list)
        # Find the index of the last photo by comparing the date
        index_last_photo, file_last_photo = extract_real_last_photo(photo_list)
        if index_last_photo is not None:
            index_previous_photo = str(index_last_photo)
            file_previous_photo = file_last_photo
            print(f"index of the last photo is: {index_last_photo}")
        else:
            print("No photo found")

        #initial loop : one photo only
        local_previous_photo_path = None
        print("🌤️ Starting cloud detection loop... Press Ctrl+C to stop.")
        cycle_count = 0

        while True:

            if max_cycles and cycle_count >= max_cycles:
                print("🔁 Max cycles reached. Stopping.")
                break

            found_photo = False
            while not found_photo:  # add break with Control C !!!
                # Take a photo
                perform_takeWidePhoto()

                photo_list = getlistPhoto("WIDE",index_previous_photo,index_previous_photo)
                print(photo_list)
                # Find the index of this photo by comparing the date in the list : normaly the same
                index_current_photo, file_current_photo = extract_real_last_photo(photo_list)

                if index_current_photo is not None and file_current_photo == file_previous_photo:
                    print("⚠️ Warning: No new photo detected.")
                elif index_current_photo is not None:
                    index_last_photo = str(index_current_photo)
                    file_last_photo = file_current_photo
                    print(f"new photo found : {file_last_photo}")
                    found_photo = True
                else:
                    print("❌ Error: No photo found")

            # dowload photo : (local_photo_directory,file_last_photo)
            getGetLastPhoto(index_last_photo, "WIDE")
              
            local_last_photo_path = os.path.join(local_photo_directory, file_last_photo)        
            # check dir

            # compare the photo if local_previous_photo_path is set
            if local_previous_photo_path and local_last_photo_path:
                 print("🔎 Comparing photos for cloud detection...")
                 detect_cloud_photo_histogram_and_stars (local_previous_photo_path, local_last_photo_path)

            # wait interval_seconds
            time.sleep(interval_seconds)
            local_previous_photo_path = local_last_photo_path
            index_previous_photo = index_last_photo
            file_previous_photo = file_last_photo
            cycle_count += 1

    except KeyboardInterrupt:
        print("\n🛑 Loop stopped by user.")


def main():
    while True:
        display_menu()
        try:
            user_choice = get_user_choice().upper()
        except KeyboardInterrupt:
            my_logger.warning("Operation interrupted by the user (CTRL+C).")
            user_choice = '0'

        if user_choice == 'C':
            option_C()

        elif user_choice == 'BR':
            option_BR()

        elif user_choice == 'BS':
            option_BS()

        elif user_choice == 'C1':
            option_C1()

        elif user_choice == 'C2':
            option_C2()

        elif user_choice == 'C3':
            option_C3()

        elif user_choice == 'C4':
            option_C4()

        elif user_choice == 'S':
            option_S()

        elif user_choice == 'U':
            option_U()

        elif user_choice == 'L':
            option_L()

        elif user_choice == 'D':
            option_D()

        elif user_choice == 'GO':
            start_detect_cloud()

        elif user_choice == '0':
            perform_disconnect()
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a correct_value.")

if __name__ == "__main__":
    main()
