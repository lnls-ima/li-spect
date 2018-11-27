# Excitation Curve

Excitation curves for the 45 degrees and 15 degrees of the Linac spectrometer
are built using the hallprobe fieldmaps for 4.15A excitation current. This
fieldmap is rescaled for other excitation current values so as to give correct
correct central peak field value which was independently measured on 2018-11-24 for a number of
excitation currents. A polynomial fit of order 6 is used on the raw central
field data to filter out measurement noise.

## measured_field.py

The script ```measured_field.py``` contains the central field data and also the
fitting algorithm, as well utilities to calculate fields for different
excitation current values.
