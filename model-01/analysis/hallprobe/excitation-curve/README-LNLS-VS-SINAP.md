# Linac Beam Energy

A discrepancy between beam energy values as measured with the spectrometer and
with dipoles of the linac-booster transport line (TB) has been observed.
While the excitation curve of the spectrometer gives a value of 142 MeV for
the beam during machine comissioning of 2018-10/2018-11, the corresponding
value from TB dipoles' excitation curve is 127 Mev, a difference of ~12%.

## Magnetic measurements

In order to assess the origin of this discrepancy we looked at the

* **M0** [raw excitation data](magnets-measurement-data-from-Li-Xuan.xlsx) provided by **SINAP** team

and compared it to field measurements of the spectrometer done in the **LNLS**.
There are two such measurements:

* **M1** Hallsensor fieldmap at excitation 4.15A at the IMA group's lab.
* **M2** Hallsensor peak on-site measurements taken on 2018-11-24 for various
excitation current values

Measurements **M1** and **M2** differ from each other in ~2.5% at low currents (4.15A).
The difference may be explained by different magnetic histories prior to the
measurements. It is worth noting that while a monopolar demagnetization curve
was used in **M1**, for **M2** the spectrometer had been demagnetized with a dipolar
curve.

At high current (17A) **M0**, **M1** and **M2** are all within 0.5% in terms of central
peak field, whereas at low current M0 differ from M1 at 3.0%

* **Source1** - Effective length is defined as the field integral on a trajectory divided by
measured central peak field. **M0** data shows an effective length of 0.4965 m
for all excitation currents.  Runge-Kutta trajectory analysis of **M1** at 17A,
calibrated to give peak fields of **M2**, yields an effective lengths of 0.4943 m
and 0.4673 m for the 15 and 45 degree trajectories, respectively. This shows
that the SINAP excitation curve for the spectrometer is probably using the
15-degree data, instead of the 45-degree data. This explains ~6% of the
~12% observed discrepancy.
* **Source2** - An additional source of the discrepancy was observed in how the SINAP
raw data was used in the energy measurement program: a quadratic polynomial was
fitted to the write the relation between field integral BL and excitation
current. The coefficients were:
  * BL(I) = -0.000147274 I² + 0.0294354992 I + 0.0016115352
But when used in the code the coeffcients were truncated to
  * BL(I) = -0.0001 I² + 0.0294 I + 0.0016
This truncation corresponds to an additional discrepancy of ~3%.

See [the plot](lnls-vs-sinap.svg) comparing all excitation curves.
