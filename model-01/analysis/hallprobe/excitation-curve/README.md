# Excitation Curve

Excitation curves for the 45 degrees and 15 degrees of the Linac spectrometer
is build using the hallprobe-mapped field at 4.15A rescaled to give the correct
central field value which was independently measured on 2018-11-24 for a number of
excitation currents. A polynomial fit of order 6 is used on the raw central
field data to filter out measurement noise.

## measured_field.py

The script ```measured_field.py``` contains the central field data and also the
fitting algorithm, as well utilities to calculate fields for different
excitation current values.
