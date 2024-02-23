import configparser
import time

from datetime import datetime
from lib.dwarf_utils import perform_time
from lib.dwarf_utils import perform_timezone

from lib.dwarf_utils import perfom_GoLive
from lib.dwarf_utils import perform_calibration
from lib.dwarf_utils import perform_goto
from lib.dwarf_utils import perform_goto_stellar
from lib.dwarf_utils import parse_ra_to_float
from lib.dwarf_utils import parse_dec_to_float
from lib.dwarf_utils import perfom_takeAstroPhoto

# JSON ENTRY FILE

    programm = 
        { command : {
                calibration : {
                    do_action : false;
                    wait_before : time_sec;
                    wait_after : time_sec;
                }
                goto_solar :  {
                    do_action : false;
                    target : planet_name;
                    wait_after : time_sec;
                }
                goto_manual :  {
                    do_action : false;
                    target : target_name;
                    ra_coord : ra_coord;
                    dec_coord : dec_coord;
                    wait_after : time_sec;
                }
                setup_camera :  {
                    do_action : false;
                    exposure : exposure_strvalue;
                    gain : gain_strvalue;
                    binning : binning_val;   # "0": 4k - "1": 2k
                    IRCut : IRCut_val;     # "0": IRCut - "1": IRPass
                    count : nb_image;
                    wait_after : time_sec;
                }
            }
        }


def start_session(programm)

    calibration = programm.calibration.do_action
    goto_solar = programm.goto_solar.do_action
    if (goto_solar)
        target_name = programm.goto_solar.target
    goto_manual = programm.goto_manual.do_action
    if (goto_manual)
        manual_RA = programm.goto_manual.ra_coord
        manual_declination = programm.goto_manual.dec_coord
        target_name = programm.goto_manual.target


    take_photo = programm.setup_camera.do_action
    if (take_photo)
         if(programm.setup_camera.exposure)
             exp_val = programm.setup_camera.exposure

         if(programm.setup_camera.gain)
             gain_val = programm.setup_camera.gain
 
         if(programm.setup_camera.binning)
             binning_val = programm.setup_camera.binning

         if(programm.setup_camera.IRCut)
             IR_val = programm.setup_camera.IRCut

         if(programm.setup_camera.count)
             count_val = programm.setup_camera.count

    # init camera are always done at startup
    # TO DO add error_control
    continu_action = True
    perform_time()
    if (read_longitude() and read_lattitude())
        perform_timezone()
    else 
        stop_action()

    continu_action = perfom_GoLive()
    verify_action(continu_action, "step_1")

    continu_action = permform_update_camera_setting("exposure", "1")
    verify_action(continu_action, "step_1")
    continu_action = permform_update_camera_setting("gain", "80")
    verify_action(continu_action, "step_1")
    continu_action = permform_update_camera_setting("IR", "1")
    verify_action(continu_action, "step_1")
    continu_action = permform_update_camera_setting("binning", "0")
    verify_action(continu_action, "step_1")

    if (calibration)
        time.sleep(programm.calibration.wait_before)
        continu_action = perform_calibration()
        time.sleep(programm.calibration.wait_after)
    verify_action(continu_action, "step_1")

    if (goto_solar)
        continu_action = select_solar_target (target): 
        time.sleep(programm.goto_solar.wait_after)
    verify_action(continu_action, "step_1")

    if (goto_manual)
        try:
            decimal_RA = float(manual_RA)
        except ValueError:
            decimal_RA = parse_ra_to_float(manual_RA)
        try:
            decimal_Dec = float(manual_declination)
        except ValueError:
            decimal_Dec = parse_ra_to_float(manual_declination)
        perform_goto(decimal_RA, decimal_Dec, target_name)
        time.sleep(programm.goto_manual.wait_after)
    verify_action(continu_action, "step_1")

    if (setup_photo)
        if (exp_val)
            permform_update_camera_setting("exposure", exp_val)
        if (exposure)
            permform_update_camera_setting("gain", gain_val)
        if (IR_val)
            permform_update_camera_setting("IR", IR_val)
        if (binning_val)
            permform_update_camera_setting("binning", binning_val)
        if (count_val)
            permform_update_camera_setting("count", count_val)
        time.sleep(programm.setup_camera.wait_after)

        verify_action(continu_action, "step_1")

        perfom_takeAstroPhoto()   

        verify_action(continu_action, "step_1")
