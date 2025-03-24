import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Update Stellarium configuration")
parser.add_argument('--port', type=int, help='Port number to use for RemoteControl', default=8090)
args = parser.parse_args()

# Dynamically determine path (Windows / Linux / macOS)
if os.name == "nt":  # Windows
    config_path = os.path.join(os.getenv("APPDATA"), "Stellarium", "config.ini")
else:  # Linux & macOS
    config_path = os.path.expanduser("~/.stellarium/config.ini")

# Values for [RemoteControl]
remote_control_section = "[RemoteControl]"
remote_control_values = {
    "autostart": "true",
    "cors_origin": "*",
    "enable_cors": "true",
    "max_threads": "30",
    "min_threads": "1",
    "port": str(args.port),  # Use the port passed via command-line argument
    "use_password": "false"
}

# Value for [plugins_load_at_startup]
startup_section = "[plugins_load_at_startup]"
startup_value = {"RemoteControl": "true"}

# Read the config file
with open(config_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Variables for tracking
inside_remote_control = False
inside_startup = False
found_remote_control = set()
found_startup = False
new_lines = []

for line in lines:
    stripped_line = line.strip()

    # Section detection
    if stripped_line == remote_control_section:
        inside_remote_control = True
        new_lines.append(line)
        continue
    elif stripped_line == startup_section:
        inside_remote_control = False
        inside_startup = True
        found_startup = True
        new_lines.append(line)
        continue
    elif stripped_line.startswith("["):
        inside_remote_control = False
        inside_startup = False

    # Edit [RemoteControl]
    if inside_remote_control and "=" in line:
        key = line.split("=")[0].strip()
        found_remote_control.add(key)
        if key in remote_control_values:
            line = f"{key.ljust(42)}= {remote_control_values[key]}\n"
            del remote_control_values[key]  # Remove from the list of values to be added

    # Edit [plugins_load_at_startup]
    if inside_startup and "=" in line:
        key = line.split("=")[0].strip()
        if key == "RemoteControl":
            line = f"{key.ljust(42)}= {startup_value['RemoteControl']}\n"

    new_lines.append(line)

# Add missing values to [RemoteControl]
if remote_control_values:
    if not found_remote_control:  # Section did not exist, so we add it
        new_lines.append("\n" + remote_control_section + "\n")
    for key, value in remote_control_values.items():
        new_lines.append(f"{key.ljust(42)}= {value}\n")

# Add [plugins_load_at_startup] section if it didn't exist
if not found_startup:
    new_lines.append("\n" + startup_section + "\n")
    for key, value in startup_value.items():
        new_lines.append(f"{key.ljust(42)}= {value}\n")

# Save the updated config
with open(config_path, "w", encoding="utf-8") as file:
    file.writelines(new_lines)

print(f"Configuration updated in {config_path}")
