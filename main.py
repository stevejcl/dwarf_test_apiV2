import configparser
import re
from datetime import datetime

from dwarf_python_api.lib.dwarf_utils import perform_goto
from dwarf_python_api.lib.dwarf_utils import perform_goto_stellar
from dwarf_python_api.lib.dwarf_utils import perform_time
from dwarf_python_api.lib.dwarf_utils import perform_timezone
from dwarf_python_api.lib.dwarf_utils import perform_calibration
from dwarf_python_api.lib.dwarf_utils import perform_decoding_test
from dwarf_python_api.lib.dwarf_utils import perform_decode_wireshark
from dwarf_python_api.lib.dwarf_utils import read_longitude
from dwarf_python_api.lib.dwarf_utils import read_latitude
from dwarf_python_api.lib.dwarf_utils import read_camera_exposure
from dwarf_python_api.lib.dwarf_utils import read_camera_gain
from dwarf_python_api.lib.dwarf_utils import read_camera_IR
from dwarf_python_api.lib.dwarf_utils import read_camera_binning
from dwarf_python_api.lib.dwarf_utils import read_camera_format
from dwarf_python_api.lib.dwarf_utils import read_camera_count
from dwarf_python_api.lib.dwarf_utils import parse_ra_to_float
from dwarf_python_api.lib.dwarf_utils import parse_dec_to_float
from dwarf_python_api.lib.dwarf_utils import perform_takeAstroPhoto
from dwarf_python_api.lib.dwarf_utils import perform_stopAstroPhoto
from dwarf_python_api.lib.dwarf_utils import perform_GoLive
from dwarf_python_api.lib.dwarf_utils import permform_update_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_camera_setting
from dwarf_python_api.lib.dwarf_utils import perform_get_all_feature_camera_setting
from dwarf_python_api.lib.dwarf_utils import unset_HostMaster
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_wifi_type
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoAP
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country_list
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_country
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_psd
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_autoSTA
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_ssid
from dwarf_python_api.lib.dwarf_utils import read_bluetooth_ble_STA_pwd
from dwarf_python_api.lib.data_utils import get_exposure_name_by_index
from dwarf_python_api.lib.data_utils import get_gain_name_by_index
from dwarf_python_api.lib.dwarf_utils import motor_action
from dwarf_python_api.lib.dwarf_utils import perform_takePhoto
from dwarf_python_api.lib.dwarf_utils import perform_start_autofocus
from dwarf_python_api.lib.dwarf_utils import perform_stop_autofocus
from dwarf_python_api.get_live_data_dwarf import get_live_data

from dwarf_ble_connect.connect_bluetooth import connect_bluetooth

def display_menu():
    print("")
    print("----------------------------------")
    print("  After the bluetooth connection, ")
    print("    a Time and Time Zone Frames   ")
    print("     are automatically sent.      ")
    print("----------------------------------")
    print("    Don't forget to send them     ")
    print("if not using bluetooth connection ")
    print("----------------------------------")
    print("1. Send Time Frame")
    print("2. Send TimeZone Frame")
    print("3. Send Calibration Frame")
    print("4. Send GoTo Polaris")
    print("5. Send GoTo Vega")
    print("6. Send GoTo M42")
    print("7. Send GoTo M31")
    print("8. Send GoTo Jupiter")
    print("9. Send GoTo Manual Target")
    print("10. Input Longitude & Latitude")
    print("11. Unset HOST MASTER")
    print("B. Bluetooth Functions")
    print("C. Camera Data Function")
    print("L. Get Live Data Function")
    print("M. Motor Function")
    print("T. Test Frames Decoding")
    print("0. Exit")

def display_menu_test():
    print("")
    print("------------------")
    print("T1. Decoding Test Frames 1")
    print("T2. Decoding Test Frames 2")
    print("T3. Decoding Test Frames 3")
    print("T4. Decoding All Test Frames")
    print("D. Decoding Unmasked Wireshark Frame")
    print("0. Return")

def display_menu_camera():
    print("")
    print("------------------")
    print("C1. Read Saved Config Camera Data")
    print("C2. Input Camera Data to Config")
    print("C3. Read Current DwarfII Camera Data")
    print("C4. Import Saved Config Camera Data into DwarfII")
    print("C5. Start Imaging Session")
    print("C6. Stop Imaging Session")
    print("C7. Go Live Action")
    print("C8. Take one Photo Only")
    print("C9. Astro Autofocus")
    print("C10. Astro Infinite Autofocus")
    print("C11. Stop Astro Autofocus")
    print("0. Return")

def display_menu_bluetooth():
    print("")
    print("------------------")
    print("C. connect Bluetooth and Start STA Mode")
    print("R. Read Bluetooth Param Config Information")
    print("S. Save Bluetooth Param Config Information and for Connection")
    print("0. Return")

def display_menu_motor():
    print("")
    print("------------------")
    print("C. Closed Barrel Position")
    print("I. Init Horizontal Position")
    print("P. Polar Align Position")
    print("S. Turn 90° for Second Polar Align Position")
    print("RR. Option RR. Reset Rotation Axis")
    print("RS. Option RS. Reset Pitch Axis")
    print("0. Return")

def get_user_choice():
    choice = input("Enter your choice (1-11) or (B,C,L,M,T) or 0 to exit: ")
    return choice

def get_user_choice_test():
    choice = input("Enter your choice (T1 to T4) or D or 0 to return to main menu: ")
    return choice

def get_user_choice_camera():
    choice = input("Enter your choice (C1 to C11) or 0 to return to main menu: ")
    return choice

def get_user_choice_bluetooth():
    choice = input("Enter your choice C,R,S or 0 to return to main menu: ")
    return choice

def get_user_choice_motor():
    choice = input("Enter your choice C,I,P,S or 0 to return to main menu: ")
    return choice

def option_1():
    print("You selected Option 1: Send Time Frame")
    print("")
    # Add your Option 1 functionality here
    perform_time()

def option_2():
    print("You selected Option 2:  Send TimeZone Frame")
    print("")
    # Add your Option 2 functionality here
    perform_timezone()

def option_3():
    print("You selected Option 3: Send Calibration Frame")
    print("")
    # Add your Option 3 functionality here
    perform_calibration()

def option_4():
    print("You selected Option 4: Send GoTo Polaris")
    print("")
    # Add your Option 4 functionality here
    perform_goto_target("Polaris")

def option_5():
    print("You selected Option 5: Send GoTo Vega")
    print("")
    # Add your Option 5 functionality here
    perform_goto_target("Vega")

def option_6():
    print("You selected Option 6: Send GoTo M42")
    print("")
    # Add your Option 6 functionality here
    perform_goto_target("M42")

def option_7():
    print("You selected Option 7: Send GoTo M31")
    print("")
    # Add your Option 7 functionality here
    perform_goto_target("M31")

def option_8():
    print("You selected Option 8: Send GoTo Jupiter")
    print("")
    # Add your Option 8 functionality here
    select_solar_target("Jupiter")

def option_9():
    print("You selected Option 9: Manual Target")
    print("")
    # Add your Option 9 functionality here
    input_manual_target()

def option_10():
    print("You selected Option 10: Input Data : Longitude, Latitude and TimeZone")
    input_data()
    # Add your Option 10 functionality here

def option_11():
    print("You selected Option 11: Set HOST MASTER")
    unset_HostMaster()
    # Add your Option 11 functionality here

def option_C():
    print("You selected Option C: Camera Data function")
    choice_camera()
    # Add your Option C functionality here

def option_B():
    print("You selected Option B: Bluetooth Functions")
    choice_bluetooth()
    # Add your Option 3 functionality here

def option_L():
    print("You selected Option L: Get Live Data Functions")
    get_live_data()
    # Add your Option 3 functionality here

def option_M():
    print("You selected Option M: Motor Functions")
    choice_motor()
    # Add your Option 3 functionality here

def option_T():
    print("You selected Option T: Do Tests..")
    choice_test()
    # Add your Option T functionality here

def option_C1():
    print("You selected Option C1. Read Saved Config Camera Data")
    print("")
    # Add your Option C11 functionality here
    read_camera_data()

def option_C2():
    print("You selected Option C2. Input Camera Data to Config")
    print("")
    # Add your Option C2 functionality here
    input_camera_data()

def option_C3():
    print("You selected Option C3. Read Current DwarfII Camera Data")
    print("")
    # Add your Option C3 functionality here
    camera_exposure = False
    camera_gain = False
    camera_binning = False
    camera_IR = False
    camera_format = False
    camera_count = False

    result = perform_get_all_camera_setting()
    result_feature = perform_get_all_feature_camera_setting()
    print("------------------")

    # ALL PARAMS
    if (result):
        # get Camera
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]

           camera_exposure = str(get_exposure_name_by_index(index_value))
           print("the exposition is: ", camera_exposure)
        else:
           print("the exposition has not been found")

        # get Gain
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
           index_value = matching_entry["index"]

           camera_gain = str(get_gain_name_by_index(index_value))
           print("the gain is: ", camera_gain)
        else:
           print("the gain has not been found")

        # get IR
        target_id = 8

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result["all_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_IR = str(matching_entry["index"])

            if (camera_IR == "0"):
                print("the IR value is: IRCut")
            else:
                print("the IR value is: IRPass")
        else:
           print("the IRfilter has not been found")
    else:
       print("the exposition has not been found")
       print("the gain has not been found")
       print("the IRfilter has not been found")

    # ALL FEATURE PARAMS
    if result_feature : 
        # get binning
        target_id = 0

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_binning = str(matching_entry["index"])
            if (camera_binning == "0"):
                print("the Binning value is 4k")
            else:
                print("the Binning value is 2k")
        else:
           print("the Binning value has not been found")

        # get camera_format
        target_id = 2

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_format = str(matching_entry["index"])
            if (camera_format == "0"):
                print("the image format value is: FITS")
            else:
                print("the image format value is: TIFF")
        else:
           print("the image format value has not been found")

        # get camera_count
        target_id = 1

        # Find the entry with the matching id
        matching_entry = next((entry for entry in result_feature["all_feature_params"] if entry["id"] == target_id), None)

        if matching_entry:
            # Extract specific fields for the matching entry
            camera_count = str(round(matching_entry["continue_value"]))

            print("the number of images for the session is:", camera_count)
        else:
           print("the number of images for the session has not been found")
    else:
       print("the Binning value has not been found")
       print("the image format value has not been found")
       print("the number of images for the session has not been found")


def option_C4():
    print("You selected Option C4. Import Saved Config Camera Data into DwarfII")
    print("")
    # Add your Option C4 functionality here
    if (camera_exposure := read_camera_exposure()):
        print("the exposition is: ", camera_exposure)
        permform_update_camera_setting("exposure", camera_exposure)

    if (camera_gain := read_camera_gain()):
        print("the gain is:", camera_gain)
        permform_update_camera_setting("gain", camera_gain)

    if (camera_IR := read_camera_IR()):
        print("the IR value is:", camera_IR)
        permform_update_camera_setting("IR", camera_IR)

    if (camera_binning := read_camera_binning()):
        print("the Binning value is:", camera_binning)
        permform_update_camera_setting("binning", camera_binning)

    if (camera_format := read_camera_format()):
        print("the image format value is:", camera_format)
        permform_update_camera_setting("fileFormat", camera_format)

    if (camera_count := read_camera_count()):
        print("the number of images for the session is:", camera_count)
        permform_update_camera_setting("count", camera_count)

def option_C5():
    print("You selected Option C5. Start Imaging Session")
    print("")
    # Add your Option C5 functionality here
    perform_takeAstroPhoto()

def option_C6():
    print("You selected Option C6. Stop Imaging Session")
    print("")
    # Add your Option C6 functionality here
    perform_stopAstroPhoto()

def option_C7():
    print("You selected Option C7. Go Live Action")
    print("")
    # Add your Option C7 functionality here
    perform_GoLive()

def option_C8():
    print("You selected Option C8. Take one Photo Only")
    print("")
    # Add your Option C8 functionality here
    perform_takePhoto()

def option_C9():
    print("You selected Option C9. Astro Autofocus")
    print("")
    # Add your Option C8 functionality here
    perform_start_autofocus(False)

def option_C10():
    print("You selected Option C10. Astro Infinite Autofocus")
    print("")
    # Add your Option C8 functionality here
    perform_start_autofocus(True)

def option_C11():
    print("You selected Option C11. Stop Astro Autofocus")
    print("")
    # Add your Option C8 functionality here
    perform_stop_autofocus()

def option_BC():
    print("You selected Option C. connect Bluetooth and Start STA Mode")
    print("")
    # Add your Option BC functionality here
    if (connect_bluetooth()):

        #init Frame : TIME and TIMZONE
        result = perform_time()
       
        if result:
           perform_timezone()

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

def option_MC():
    print("You selected Option C. Closed Barrel Position")
    print("")
    # Add your Option MC functionality here
    motor_action(1)

def option_MI():
    print("You selected Option I. Init Horizontal Position")
    print("")
    # Add your Option MI functionality here
    motor_action(2)

def option_MP():
    print("You selected Option P. Polar Align Position")
    print("")
    # Add your Option MP functionality here
    motor_action(3)

def option_MS():
    print("You selected Option S. Turn 90° for Second Polar Align Position")
    print("")
    # Add your Option MS functionality here
    motor_action(4)

def option_RR():
    print("You selected Option RR. Reset Rotation Axis")
    print("")
    # Add your Option RR functionality here
    motor_action(5)

def option_RS():
    print("You selected Option RS.  Reset Pitch Axis")
    print("")
    # Add your Option MS functionality here
    motor_action(6)

def option_20():
    print("You selected Option T1: Decoding Test Frames 1")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(True, False, False)

def option_21():
    print("You selected Option T2: Decoding Test Frames 2")
    print("")
    # Add your Option T2 functionality here
    perform_decoding_test(False, True, False)

def option_22():
    print("You selected Option T3: Decoding Test Frames 3")
    print("")
    # Add your Option T3 functionality here
    perform_decoding_test(False, False, True)

def option_23():
    print("You selected Option T4: Decoding Test All Frames")
    print("")
    # Add your Option T4 functionality here
    perform_decoding_test(True, True, True)

def option_24():
    print("You selected Option D. Decoding Unmasked Wireshark Frame")
    print("")
    # Add your Option D1 functionality here
    return input_frame(False)

def input_data():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

def input_camera_data():
    prompt = "Enter the desired exposition in seconds (0 = auto - 15), use fraction for less than 1s (ex: 1/10):"
    camera_exposure_init = read_camera_exposure()
    camera_exposure = input(f"{prompt}[{camera_exposure_init}]:") if camera_exposure_init else input(prompt+"[1]")
    if not camera_exposure and not camera_exposure_init:
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif camera_exposure and (int(camera_exposure)<0 or int(camera_exposure) > 15):
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    elif (camera_exposure):
        print("You entered:", camera_exposure)
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
    prompt = "Enter the desired IR value: 0 for IRCut, 1 for IRPass:"
    camera_IR = input(f"{prompt}[{camera_IR_init}]:") if camera_IR_init else input(prompt+"[IRCut]")
    if not camera_IR and not camera_IR_init:
        camera_IR = "0"
        print("Set to Default (IRCut):", camera_IR)
    elif camera_IR and (camera_IR!="0" and camera_IR !="1"):
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (IRCut):", camera_IR)
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
    update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count)

def read_camera_data():
    print("The values in the Config File are : ")
    print("-----------------------------------")
    if (camera_exposure := read_camera_exposure()):
        print("the exposition is: ", camera_exposure)
    if (camera_gain := read_camera_gain()):
        print("the gain is:", camera_gain)
    if (camera_IR := read_camera_IR()):
        if (camera_IR == "0"):
            print("the IR value is: IRCut")
        else:
            print("the IR value is: IRPass")
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
    update_htmlfile(ble_psd, ble_STA_ssid, ble_STA_pwd)

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

def input_test():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

def input_manual_target():
    target_name = input("Enter a name for the target: ")
    print("You entered:", target_name)
    manual_RA = input("Enter the Right Ascension (hr:mm:ss.s) or decimal: ")
    print("You entered:", manual_RA)
    try:
        decimal_RA = float(manual_RA)
    except ValueError:
        decimal_RA = parse_ra_to_float(manual_RA)
    print("Converted to:", decimal_RA)
    manual_declination = input("Enter the Declination (<sign>deg:mm:ss.s) or decimal: ")
    print("You entered:", manual_declination)
    try:
        decimal_Dec = float(manual_declination)
    except ValueError:
        decimal_Dec = parse_ra_to_float(manual_declination)
    print("Converted to:", decimal_Dec)
    print("")
    go_goto = input("Press Enter to continue or 0 to exit: ")
    if (go_goto !="0"):
        # Convert to decimal value if not enterered
        perform_goto(decimal_RA, decimal_Dec, target_name)
    else:
        exit

def input_frame(masked):
    user_frame = input("Enter the wireshark capture frame payload data (option copy as C String) or 0 to return to previous menu: ")
    user_maskedcode = ""
    if (user_frame == "0"):
      return '0'
    else:
      print("You entered:", user_frame)
      if (masked):
          user_maskedcode = input("Enter the masked code: ")
          print("You entered:", user_maskedcode)
      perform_decode_wireshark(user_frame, masked, user_maskedcode)
      input_frame(masked)
      return ''

def select_solar_target (target):
   
    target_name = target
    target_id = None
   
    if (target == "Mercury"):
        target_id = 1

    if (target == "Venus"):
        target_id = 2

    if (target == "Mars"):
        target_id = 3

    if (target == "Jupiter"):
        target_id = 4

    if (target == "Saturn"):
        target_id = 5

    if (target == "Uranus"):
        target_id = 6

    if (target == "Neptune"):
        target_id = 7

    if (target == "moon"):
        target_id = 8

    if (target == "Sun"):
        target_id = 9

    perform_goto_stellar(target_id, target_name)

def update_config(longitude, latitude, timezone):
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Update the value in the CONFIG section
    config['CONFIG']['LONGITUDE'] = longitude
    config['CONFIG']['LATITUDE'] = latitude
    config['CONFIG']['TIMEZONE'] = timezone

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count):

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

def update_htmlfile(ble_psd, ble_STA_ssid, ble_STA_pwd):

  # Specify the path to your HTML file
  html_file_path = 'dwarf_ble_connect/connect_dwarf.html'

  # Read the HTML file
  with open(html_file_path, 'r') as html_file:
    lines = html_file.readlines()

  # Define the pattern to match JavaScript variable assignments
  pattern1 = re.compile(r'let BluetoothPWD = ".*?";')
  pattern2 = re.compile(r'let BleSTASSIDDwarf = ".*?";')
  pattern3 = re.compile(r'let BleSTAPWDDwarf = ".*?";')

  # Loop through each line and replace the target line if found
  modified_lines = []
  for line in lines:
    if pattern1.match(line):
      # Replace the line with the new variable assignment
      modified_lines.append(f'let BluetoothPWD = "{ble_psd}";\n')
    elif pattern2.match(line):
      # Replace the line with the new variable assignment
      modified_lines.append(f'let BleSTASSIDDwarf = "{ble_STA_ssid}";\n')
    elif pattern3.match(line):
      # Replace the line with the new variable assignment
      modified_lines.append(f'let BleSTAPWDDwarf = "{ble_STA_pwd}";\n')
    else:
      modified_lines.append(line)

  # Write the modified content back to the HTML file
  with open(html_file_path, 'w') as html_file:
    html_file.writelines(modified_lines)

  print("The Html file to connect to Bluetooth has been updated  accordingly")

def perform_goto_target(target):
    # Inverse LONGITUDE for DwarfII !!!!!!!
    ra = None
    dec = None

    if (target == "Polaris"):
        ra = 2.5390302777777776;
        dec = 89.26980527777778;

    if (target == "Vega"):
        ra = 18.61522686111111;
        dec = 38.784415833333334;

    if (target == "M42"):
        ra = 5.588475138888889;
        dec = -5.3923;

    if (target == "M31"):
        ra = 0.7122101388888887;
        dec = 41.271721388888885;

    if (ra):
        return perform_goto(ra, dec, target)

    print(f"Error: Data for Target: {target} Not Found")

def choice_test():
    while True:
        display_menu_test()
        user_choice = get_user_choice_test()

        if user_choice == 'T1':
            option_20()

        elif user_choice == 'T2':
            option_21()

        elif user_choice == 'T3':
            option_22()

        elif user_choice == 'T4':
            option_23()

        elif user_choice == 'D':
            if (option_24() == '0'):
              break

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_camera():
    while True:
        display_menu_camera()
        user_choice = get_user_choice_camera()

        if user_choice == 'C1':
            option_C1()

        elif user_choice == 'C2':
            option_C2()

        elif user_choice == 'C3':
            option_C3()

        elif user_choice == 'C4':
            option_C4()

        elif user_choice == 'C5':
            option_C5()

        elif user_choice == 'C6':
            option_C6()

        elif user_choice == 'C7':
            option_C7()

        elif user_choice == 'C8':
            option_C8()

        elif user_choice == 'C9':
            option_C9()

        elif user_choice == 'C10':
            option_C10()

        elif user_choice == 'C11':
            option_C11()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_bluetooth():
    while True:
        display_menu_bluetooth()
        user_choice = get_user_choice_bluetooth()

        if user_choice == 'C':
            option_BC()

        elif user_choice == 'R':
            option_BR()

        elif user_choice == 'S':
            option_BS()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def choice_motor():
    while True:
        display_menu_motor()
        user_choice = get_user_choice_motor()

        if user_choice == 'C':
            option_MC()

        elif user_choice == 'I':
            option_MI()

        elif user_choice == 'P':
            option_MP()

        elif user_choice == 'S':
            option_MS()

        elif user_choice == 'RR':
            option_RR()

        elif user_choice == 'RS':
            option_RS()

        elif user_choice == '0':
            print("Return to the main menu")
            break

        else:
            print("Invalid choice. Please enter a correct value.")

def main():
    while True:
        display_menu()
        user_choice = get_user_choice()

        if user_choice == '1':
            option_1()

        elif user_choice == '2':
            option_2()

        elif user_choice == '3':
            option_3()

        elif user_choice == '4':
            option_4()

        elif user_choice == '5':
            option_5()

        elif user_choice == '6':
            option_6()

        elif user_choice == '7':
            option_7()

        elif user_choice == '8':
            option_8()

        elif user_choice == '9':
            option_9()

        elif user_choice == '10':
            option_10()

        elif user_choice == '11':
            option_11()

        elif user_choice == 'C':
            option_C()

        elif user_choice == 'B':
            option_B()

        elif user_choice == 'L':
            option_L()

        elif user_choice == 'M':
            option_M()

        elif user_choice == 'T':
            option_T()

        elif user_choice == '0':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a correct_value.")

if __name__ == "__main__":
    main()
