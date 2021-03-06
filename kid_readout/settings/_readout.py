"""
This is a template local settings file for the computer `readout` running the STAR Cryo cryostat in 1132.
"""
import time as _time

from kid_readout.analysis.resources import experiments as _experiments

CRYOSTAT = 'STARCryo'
COOLDOWN = _experiments.get_experiment_info_at(_time.time(), cryostat=CRYOSTAT)

LOG_DIR = '/data/readout/log'
TEMPERATURE_LOG_DIR = '/data/readout/SRS'

SRS_TEMPERATURE_SERIAL_PORT = '/dev/serial/by-id/usb-FTDI_USB_to_Serial_Cable_FTGQM0GY-if00-port0'

LOCKIN_SERIAL_PORT = '/dev/serial/by-id/usb-Keyspan__a_division_of_InnoSys_Inc._Keyspan_USA-19H-if00-port0'
