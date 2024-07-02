# dwarf_test_apiV2
Dwarf II, test program for Api V2.0

This test program permits to send frames to the dwarfII telescope.

It uses the new api V2.0.

The frames that can be tested are : 
- Sendind config parameter : Time and Timezone
- Do a calibration
- Do a goto to differents target (Polaris, Vega, M42 and M31)
- Do a goto to a solar system target : Jupiter

After validation, it will be used for updating the dwarf_tcp_server program that use Stellarium to make goto on the dwarf II.

Installation

First Install library with python -m pip install -r requirements

Then you need the dwarf_python_api found also on my github

you can direct download the release tar file on github

This library must be installed locally in the root pass of this project with the parameter --target 

=> cd Path_to_clone_version_of_dwarf_test_apiV2
=> python -m pip install  Path_to_downloaded_dwarf_python_api/dwarf_python_api-1.1.0.tar.gz --target .

then you can start it with => python .\main.py