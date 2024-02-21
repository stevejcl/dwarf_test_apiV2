import configparser
from datetime import datetime

from lib.dwarf_utils import perform_goto
from lib.dwarf_utils import perform_goto_stellar
from lib.dwarf_utils import perform_time
from lib.dwarf_utils import perform_timezone
from lib.dwarf_utils import perform_calibration
from lib.dwarf_utils import perform_decoding_test
from lib.dwarf_utils import perform_decode_wireshark
from lib.dwarf_utils import read_longitude
from lib.dwarf_utils import read_latitude
from lib.dwarf_utils import read_camera_exposure
from lib.dwarf_utils import read_camera_gain
from lib.dwarf_utils import read_camera_IR
from lib.dwarf_utils import read_camera_binning
from lib.dwarf_utils import read_camera_format
from lib.dwarf_utils import read_camera_count
from lib.dwarf_utils import parse_ra_to_float
from lib.dwarf_utils import parse_dec_to_float

def display_menu():
    print("")
    print("------------------")
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
    print("C. Camera Data Function")
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
    print("0. Return")

def get_user_choice():
    choice = input("Enter your choice (1-9) or (T1 to T4) or D or 0 to exit: ")
    return choice

def get_user_choice_test():
    choice = input("Enter your choice (T1 to T4) or D or 0 to return to main menu: ")
    return choice

def get_user_choice_camera():
    choice = input("Enter your choice (C1 to C4) or 0 to return to main menu: ")
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
    # Add your Option 3 functionality here
    select_solar_target("Jupiter")

def option_9():
    print("You selected Option 9: Manual Target")
    print("")
    # Add your Option 3 functionality here
    input_manual_target()

def option_10():
    print("You selected Option 10: Input Data : Longitude, Latitude and TimeZone")
    input_data()
    # Add your Option 3 functionality here

def option_C():
    print("You selected Option C: Camera Data function")
    choice_camera()
    # Add your Option 3 functionality here

def option_T():
    print("You selected Option T: Do Tests..")
    choice_test()
    # Add your Option 3 functionality here

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
    perform_decoding_test(True, False, False)

def option_C4():
    print("You selected Option C4. Import Saved Config Camera Data into DwarfII")
    print("")
    # Add your Option C4 functionality here
    perform_decoding_test(True, False, False)



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
    input_frame(False)

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
    camera_exposure = input("Enter the desired exposition in seconds (0 = auto - 15), use fraction for less than 1s (ex: 1/10):")
    if int(camera_exposure)<0 or int(camera_exposure) > 15:
        print("Input Data Error:", camera_exposure)
        camera_exposure = "1"
        print("Set to Default:", camera_exposure)
    else:
        print("You entered:", camera_exposure)
    camera_gain = input("Enter the desired gain between (0-240):")
    if int(camera_gain)<0 or int(camera_gain) > 240:
        print("Input Data Error:", camera_gain)
        camera_gain = "80"
        print("Set to Default:", camera_gain)
    else:
        print("You entered:", camera_gain)
    camera_IR = input("Enter the desired IR value: 0 for IRCut, 1 for IRPass:")
    if camera_IR!="0" and camera_IR !="1":
        print("Input Data Error:", camera_IR)
        camera_IR = "0"
        print("Set to Default (IRCut):", camera_IR)
    else:
        print("You entered:", camera_IR)
    camera_binning = input("Enter the desired Binning value: 0 for 4k, 1 for 2k:")
    if camera_binning!="0" and camera_binning !="1":
        print("Input Data Error:", camera_binning)
        camera_binning = "0"
        print("Set to Default (4k):", camera_binning)
    else:
        print("You entered:", camera_binning)
    camera_format = input("Enter the desired image format value: 0 for FITS, 1 for TIFF:")
    if camera_format!="0" and camera_format !="1":
        print("Input Data Error:", camera_format)
        camera_format = "0"
        print("Set to Default (FITS):", camera_format)
    else:
        print("You entered:", camera_format)
    camera_count = input("Enter the desired number of images for the session between (1-999):")
    if int(camera_count)<1 or int(camera_count) > 999:
        print("Input Data Error:", camera_count)
        camera_count = "999"
        print("Set to Default:", camera_count)
    else:
        print("You entered:", camera_count)
    update_cameraconfig(camera_exposure, camera_gain, camera_IR, camera_binning, camera_format, camera_count)

def read_camera_data():
    camera_exposure = read_camera_exposure()
    print("the exposition is: ", camera_exposure)
    camera_gain = read_camera_gain()
    print("the gain is:", camera_gain)
    camera_IR = read_camera_IR()
    print("the IR value is:", camera_IR)
    camera_binning = read_camera_binning()
    print("the Binning value is:", camera_binning)
    camera_format = read_camera_format()
    print("the image format value is:", camera_format)
    camera_count = read_camera_count()
    print("the number of images for the session is:", camera_count)

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
    manual_RA = input("Enter the Right Ascension (hr:mm:ss.s): ")
    print("You entered:", manual_RA)
    print("Converted to:", parse_ra_to_float(manual_RA))
    manual_declination = input("Enter the Declination (<sign>deg:mm:ss.s): ")
    print("You entered:", manual_declination)
    print("Converted to:", parse_dec_to_float(manual_declination))
    print("")
    # Convert to decimal value if not enterered
    perform_goto(parse_ra_to_float(manual_RA), parse_dec_to_float(manual_declination), target_name)


def input_frame(masked):
    user_frame = input("Enter the wireshark capture frame payload data (option copy as C String): ")
    user_maskedcode = ""
    print("You entered:", user_frame)
    if (masked):
        user_maskedcode = input("Enter the masked code: ")
        print("You entered:", user_maskedcode)
    perform_decode_wireshark(user_frame, masked, user_maskedcode)

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
    config['CONFIG']['EXPOSURE'] = camera_exposure
    config['CONFIG']['GAIN'] = camera_gain
    config['CONFIG']['IRCUT'] = camera_IR
    config['CONFIG']['BINNING'] = camera_binning
    config['CONFIG']['FORMAT'] = camera_format
    config['CONFIG']['COUNT'] = camera_count

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

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
            option_24()

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

        elif user_choice == 'C':
            option_C()

        elif user_choice == 'T':
            option_T()

        elif user_choice == '0':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a correct_value.")

if __name__ == "__main__":
    main()
