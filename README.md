# dwarf_test_apiV2
Dwarf II and Dwarf 3, test program for Api V2.0 in python

This test program permits to send frames to the dwarfII telescope.

It uses the new api V2.0.

The frames that can be tested are : 
- connect to the dwarf with bluetooth
- Sendind config parameter : Time and Timezone
- Do a calibration
- Do a goto to differents target (Polaris, Vega, M42 and M31)
- Do a goto to a solar system target : Jupiter
- Do manual target
- Change the parameters of you tele lens
- Take Tele photo, Wide Photo
- Download last image or previous one or history one (Tele and Wide)
- Download list of Wide or Tele photos present on the Dwarf.
- Start a imaging session
- Download images from last session
- Even do a Siril live integration with the current imaging session
- And many others functions

Installation

1. Clone this repository 

2. Then Install the dwarf_python_api library with :
  
Install :

      python -m pip install -r requirements.txt
      python -m pip install -r requirements-local.txt --target .

   This project uses the dwarf_python_api library that must be installed locally in the root path of this project
   with using the parameter --target .

   Don't miss the dot at the end of the line

Then you can start it with => python .\main.py

Cloud detector funcion : WIP
this script take a wide image each 30s and compare them to detect if clous are coming

Install :

      python -m pip install -r requirements-cloud.txt
      python -m pip install -r requirements-local.txt --target .

then launch the script with: python .\detect_cloud.py

How to use: 
a menu is diplaying
----------------------------------
    Detect Cloud application,
    Connect first to the Dwarf
----------------------------------
C. Connect Dwarf
S. Show Status data
D. Force Disconnection
----------------------------------
    Detect Cloud application
----------------------------------
GO. Start Cloud detection
CTRL+C. Stop Cloud detection
----------------------------------
           CONFIG Command
----------------------------------
BR. Read Bluetooth Param Config Information
BS. Save Bluetooth Param Config Information and for Connection
C1. Read Saved Config Camera Data
C2. Input Camera Data to Config
C3. Read Current Dwarf Camera Data
C4. Import Saved Config Camera Data into Dwarf
U. Unset HOST MASTER
L. Go Live Action
0. Exit

Type : C to detect and connect your dwarf, then go

Maybe a problem can occurs, the script uses ftp to download the image file, it shows the IP it uses.
if the IP is not the same as the one diplayed after connection, you can update the config.ini file.

Update the last line : ftp_host = 192.168.x.x by yours
This will be corrected later
