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
  
     python -m pip install -r requirements.txt
     python -m pip install -r requirements-local.txt --target .

   This project uses the dwarf_python_api library that must be installed locally in the root path of this project
   with using the parameter --target .

   Don't miss the dot at the end of the line

Then you can start it with => python .\main.py
