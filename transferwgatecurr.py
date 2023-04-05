# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
from time import sleep
import os

# Set inputs
gate_max_voltage = 40 
set_sd_voltage = 0
averages = 10
fileloc = '' # directory to save data
filename = 'transfercurve.txt' # name of file

# Calculate other inputs
gate_min_voltage = -gate_max_voltage
data_points = abs(2*gate_max_voltage+1)
filepath = os.path.join(fileloc, filename)


# Gate Keithley (25): sweeping over gate voltages, measure current

# Connect and configure the instrument
sourcemeter = Keithley2400("GPIB::25") 
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.apply_voltage(voltage_range=None, compliance_current=0.1)
sourcemeter.measure_current(nplc=1, current=0.000105, auto_range=True)
sleep(0.1)  # wait here to give the instrument time to react
sourcemeter.stop_buffer()
sourcemeter.disable_buffer()
sourcemeter.enable_source()


# SD Keithley (24): set sd voltage, measure current

# Connect and configure the instrument
sourcemeter1 = Keithley2400("GPIB::24") 
sourcemeter1.reset()
sourcemeter1.use_front_terminals()
sourcemeter1.apply_voltage(voltage_range=None, compliance_current=0.1)
sourcemeter1.measure_current(nplc=1, current=0.000105, auto_range=True)
sleep(0.1)  # wait here to give the instrument time to react
sourcemeter1.stop_buffer()
sourcemeter1.disable_buffer()
sourcemeter1.enable_source()


# Allocate arrays to store the measurement results
voltages = np.linspace(gate_min_voltage, gate_max_voltage, num=data_points)
currents_gate = np.zeros_like(voltages)
currents_gate_stds = np.zeros_like(voltages)
currents_sd = np.zeros_like(voltages)
currents_sd_stds = np.zeros_like(voltages)



# Loop through each voltage point, measure and record the two currents
for i in range(data_points):

    sourcemeter1.config_buffer(averages)
    sourcemeter1.source_voltage = set_sd_voltage
    sourcemeter1.start_buffer()
    sourcemeter1.wait_for_buffer()

    sourcemeter.config_buffer(averages)
    sourcemeter.source_voltage = voltages[i]
    sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()

    # Record the average and standard deviation
    currents_gate[i] = sourcemeter.means[1]
    sleep(0.5)
    currents_gate_stds[i] = sourcemeter.standard_devs[1]
    sleep(0.5) #do we need this?
    currents_sd[i] = sourcemeter1.means[1]
    sleep(0.5)
    currents_sd_stds[i] = sourcemeter1.standard_devs[1]


# Save the data columns in a CSV file
data = pd.DataFrame({
    'Gate Voltage (V)': voltages,
    'Gate Current (A)': currents_gate,
    'Gate Current Std (A)': currents_gate_stds,
    'SD Current (A)': currents_sd,
    'SD Current Std (A)':currents_sd_stds,
})
data.to_csv(filepath)

sourcemeter.shutdown()
sourcemeter1.shutdown()