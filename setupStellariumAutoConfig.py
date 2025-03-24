from cx_Freeze import setup, Executable
import sys

# Define the base for a GUI application
base = 'Win32GUI' if sys.platform=='win32' else None
# Setup function
setup(
    name="Stellarium_auto_config",
    version="1.0",
    description="Stellarium_auto_config",
    executables=[Executable("stellarium_auto_config.py")]
)
