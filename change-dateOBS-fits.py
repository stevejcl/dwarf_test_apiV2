from astropy.io import fits
from datetime import datetime
import sys, re

def convert_date(old_date):
    # Parse the old format 'YYYY-MM-DD-HH-MM-SS-SSS'
    try:
        date_obj = datetime.strptime(old_date, '%Y-%m-%d-%H-%M-%S-%f')
        # Convert to the new format 'yyyy-mm-ddTHH:MM:SS.sss'
        new_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Trim to milliseconds
    except ValueError:
        raise ValueError(f"Invalid DATE_OBS format: {old_date}")
    return new_date

def is_date_in_correct_format(date_str):
    # Regular expression for 'yyyy-mm-ddTHH:MM:SS[.sss]'
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?$'
    return bool(re.match(pattern, date_str))

# Read the FITS file
input_file = "test_HD 8890_15s_60_0011.fits"
data, header = fits.getdata(input_file, header=True)

# Convert DATE_OBS if needed
old_date = header.get('DATE-OBS')
if old_date:
    if is_date_in_correct_format(old_date):
        print(f"DATE-OBS ({old_date}) is already in the correct format for {input_file}")
        sys.exit()
else:
    print(f"DATE_OBS is not present for {input_file}")
    sys.exit()
    
new_date = convert_date(old_date)

print(f"DATE-OBS will change from {old_date} to {new_date}")

# Update the header
header['DATE-OBS'] = new_date

# Save the changes to the FITS file
fits.writeto(input_file, data, header, overwrite=True)

print(f"DATE-OBS has been updated from {old_date} to {new_date}")
