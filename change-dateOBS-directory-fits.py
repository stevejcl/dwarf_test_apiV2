import os
import re
from astropy.io import fits
from datetime import datetime

def convert_date(old_date):
    # Check and convert different formats
    try:
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{3}$', old_date):
            # Format 'yyyy-mm-ddTHH:MM:SS-SSS'
            date_obj = datetime.strptime(old_date, '%Y-%m-%dT%H:%M:%S-%f')
            new_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Trim to milliseconds
        elif re.match(r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d{3}$', old_date):
            # Format 'YYYY-MM-DD-HH-MM-SS-SSS'
            date_obj = datetime.strptime(old_date, '%Y-%m-%d-%H-%M-%S-%f')
            new_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Trim to milliseconds
        else:
            raise ValueError(f"Unsupported DATE-OBS format: {old_date}")
    except ValueError as e:
        raise ValueError(f"Failed to convert DATE-OBS: {e}")
    return new_date

def is_date_in_correct_format(date_str):
    # Regular expression for 'yyyy-mm-ddTHH:MM:SS[.sss]'
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?$'
    return bool(re.match(pattern, date_str))

def update_fits_files_in_directory(directory):
    # Get a list of all FITS files in the specified directory
    fits_files = [f for f in os.listdir(directory) if f.lower().endswith('.fits')]
    
    for fits_file in fits_files:
        file_path = os.path.join(directory, fits_file)
        print(f"Processing {file_path}")
        
        try:
            # Read the FITS file
            data, header = fits.getdata(file_path, header=True)
            
            # Convert DATE-OBS if needed
            old_date = header.get('DATE-OBS')
            if old_date:
                if is_date_in_correct_format(old_date):
                    print(f"DATE-OBS is already in the correct format for {file_path}")
                    continue  # Skip this file
                
                # Convert to the new format
                new_date = convert_date(old_date)
                header['DATE-OBS'] = new_date
                
                # Save the updated FITS file
                fits.writeto(file_path, data, header, overwrite=True)
                print(f"Updated DATE-OBS from {old_date} to {new_date} for {file_path}")
            else:
                print(f"No DATE-OBS found in {file_path}")
        
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

# Prompt the user to input the directory path
directory_path = input("Enter the path to the directory containing FITS files: ")

# Update all FITS files in the specified directory
update_fits_files_in_directory(directory_path)
