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
