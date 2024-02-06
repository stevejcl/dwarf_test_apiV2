import configparser
from datetime import datetime

from lib.dwarf_utils import perform_goto
from lib.dwarf_utils import perform_goto_stellar
from lib.dwarf_utils import perform_time
from lib.dwarf_utils import perform_timezone
from lib.dwarf_utils import perform_calibration
from lib.dwarf_utils import perform_decoding_test

from lib.dwarf_utils import read_longitude
from lib.dwarf_utils import read_latitude

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
    print("9. Input Longitude & Latitude")
    print("T1. Decoding Test Frames 1")
    print("T2. Decoding Test Frames 2")
    print("T3. Decoding Test Frames 3")
    print("T4. Decoding All Test Frames")
    print("0. Exit")

def get_user_choice():
    choice = input("Enter your choice (1-9) or (T1 to T4) or 0 to exit: ")
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
    print("You selected Option 9: Input Data : Longitude, Latitude and TimeZone")
    input_data()
    # Add your Option 3 functionality here

def option_10():
    print("You selected Option T1: Decoding Test Frames 1")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(True, False, False)

def option_11():
    print("You selected Option T2: Decoding Test Frames 2")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(False, True, False)

def option_12():
    print("You selected Option T3: Decoding Test Frames 3")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(False, False, True)

def option_13():
    print("You selected Option T4: Decoding Test All Frames")
    print("")
    # Add your Option T1 functionality here
    perform_decoding_test(True, True, True)

def input_data():
    user_longitude = input("Enter your Longitude: ")
    print("You entered:", user_longitude)
    user_latitude = input("Enter your Latitude: ")
    print("You entered:", user_latitude)
    user_timezone = input("Enter your TimeZone: ")
    print("You entered:", user_timezone)
    print("")
    update_config(user_longitude, user_latitude, user_timezone)

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

        elif user_choice == 'T1':
            option_10()

        elif user_choice == 'T2':
            option_11()

        elif user_choice == 'T3':
            option_12()

        elif user_choice == 'T4':
            option_13()

        elif user_choice == '0':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

if __name__ == "__main__":
    main()
