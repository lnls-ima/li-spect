#!/usr/bin/env python-sirius
"""Measured linac spectrometer field."""

import sys
import numpy as np
import matplotlib.pyplot as plt
import siriuspy.util as _u


_default_fit_order = 6
_default_prec = 6


meas_peak_field = np.array([
    # This measurements were performed in 2018-11-24 by
    # James Citadini using what he called "Medidor Group 3"
    #
    # current [A], field[G]
    #
    [0.00, 6.25],
    [2.00, -1118.54],
    [4.00, -2244],
    [6.00, -3366.35],
    [8.00, -4486],
    [10.00, -5588.6],
    [12.00, -6672.6],
    [14.00, -7733.6],
    [16.00, -8758.6],
    [18.00, -9708.2],
    [16.00, -8822.6],
    [12.00, -6733],
    [6.00, -3411.2],
    [2.00, -1155.2],
    [0.00, -30.4],
    [-2.00, 1098.8],
    [-4.00, 2228.8],
    [-6.00, 3355.6],
    [-8.00, 4479],
    [-10.00, 5586.2],
    [-12.00, 6672.6],
    [-14.00, 7731.2],
    [-16.00, 8755.8],
    [-18.00, 9707.2],
    [-16.00, 8820.4],
    [-12.00, 6725.2],
    [-6.00, 3408.2],
    [-2.00, 1151.2],
    [0.00, 26],
    [18.00, -9739.8],
    [-18.00, 9738.2],
    [0.00, 4.6], ])


curr_folders = [
    'current-02p00A',
    'current-04p00A',
    'current-04p15A',
    'current-06p00A',
    'current-08p00A',
    'current-10p00A',
    'current-12p00A',
    'current-14p00A',
    'current-16p00A',
    'current-18p00A',
    'current-20p00A',
]


def poly_fit(order=_default_fit_order):
    """Poly fit to data."""
    currents = meas_peak_field[:, 0]
    fields = meas_peak_field[:, 1]
    coeffs = np.polyfit(currents, fields, order)
    poly = np.poly1d(coeffs)
    return poly


def plot_rawdata():
    """Plot field x current."""
    currents = meas_peak_field[:, 0]
    fields = meas_peak_field[:, 1]
    plt.plot(currents, fields, 'o')
    plt.title('Measured Linac Spectrometer Central Field')
    plt.xlabel('Current [A]')
    plt.ylabel('Field [G]')
    plt.grid()
    plt.show()


def plot_polyfit(order=_default_fit_order):
    """Plot polyfit."""
    p = poly_fit(order=order)
    currents = meas_peak_field[:, 0]
    fields = meas_peak_field[:, 1]
    cfit = np.linspace(min(currents), max(currents), 1000)
    # cfit = np.linspace(-20,20,1000)
    ffit = p(cfit)
    plt.title('Linac Spectrometer Central Field')
    plt.plot(cfit, ffit, label='polyfit (order={})'.format(order))
    plt.plot(currents, fields, 'o', label='measured')
    plt.xlabel('Current [A]')
    plt.ylabel('Field [G]')
    plt.legend()
    plt.grid()
    plt.show()


def calc_field(cfit, prec=_default_prec, order=_default_fit_order):
    """Calc field from polynominal fit."""
    cfit = np.array(cfit)
    p = poly_fit(order=order)
    ffit = p(cfit)
    print('current [A]    fitted_field[G]')
    fmt = '{:+.'+str(prec)+'e} {:+.'+str(prec)+'e}'
    for i in range(len(cfit)):
        print(fmt.format(cfit[i], ffit[i]))


def get_energies(deg):
    """."""
    dc = {'15deg/': 15.0, '45deg/': 45.0}
    currents, energies, bls = [], [], []
    for cf in curr_folders:
        fname = deg + cf + '/trajectory.in'
        with open(fname) as fp:
            data = fp.readlines()
        for line in data:
            if 'beam_energy' in line:
                energy = 1e3*float(line.split()[1])
                break
        current = float(
            cf.replace('current-', '').replace('A', '').replace('p', '.'))
        br, *_ = _u.beam_rigidity(energy/1e3)
        bl = np.pi * (dc[deg] / 180.0) * br
        currents.append(current)
        energies.append(energy)
        bls.append(bl)
    return currents, energies, bls


def plot_energies(deg):
    """."""
    currents, energies, bls = get_energies(deg)
    # print
    print('current[A] energy[MeV]    BL[T.m]')
    prec = 6
    fmt = '{:+06.2f}     {:+.'+str(prec)+'e}  {:+.'+str(prec)+'e}'
    for i in range(len(currents)):
        print(fmt.format(currents[i], energies[i], bls[i]))
    # plot
    plt.plot(currents, energies)
    plt.plot(currents, energies, 'o')
    plt.xlabel('Current [A]')
    plt.ylabel('Energy [MeV]')
    plt.grid()
    plt.show()


def fit_BL(deg):
    """."""
    currents, energies, bls = get_energies(deg)
    # fit
    coeffs = np.polyfit(currents, bls, 6)
    p = np.poly1d(coeffs)
    mi, ma = min(currents), max(currents)
    cfit = np.linspace(mi, ma, 1+ma-mi)
    blfit = p(cfit)
    # print
    print('current[A] BL[T.m]')
    prec = 6
    fmt = '{:+06.2f}     {:+.'+str(prec)+'e}'
    for i in range(len(cfit)):
        print(fmt.format(cfit[i], blfit[i]))
    # plot
    plt.plot(cfit, blfit)
    plt.plot(currents, bls, 'o')
    plt.xlabel('Current [A]')
    plt.ylabel('BL [T.m')
    plt.grid()
    plt.show()


def read_trajectory(fname):
    """."""
    with open(fname) as fp:
        data = fp.readlines()
    s, rx, rz = [], [], []
    for datum in data[2:]:
        line = datum.split()
        s.append(float(line[0]))
        rx.append(float(line[1]))
        rz.append(float(line[3]))
    return s, rx, rz


def plot_trajectories(deg):
    """."""
    plt.plot([-224.36, ]*2, [-200, 500], '--k', label='phys. z lims')
    plt.plot([+224.36, ]*2, [-200, 500], '--k')
    for cf in curr_folders:
        s, rx, rz = read_trajectory(deg + cf + '/trajectory.txt')
        plt.plot(rz, rx, '.', label=cf.replace('current-', ''))
    plt.xlabel('Z [mm]')
    plt.ylabel('X [mm]')
    plt.legend()
    plt.grid()
    plt.show()


def help():
    """Help."""
    print('script options:')
    print('  help')
    print('  plot-rawdata')
    print('  plot-polyfit')
    print('  calc [current-values]')
    print('  plot-energies-45deg')
    print('  plot-energies-15deg')
    print('  plot-trajectories-45deg')
    print('  plot-trajectories-15deg')
    print('  fit-bl-45deg')
    print('  fit-bl-15deg')


def main():
    """Run main function."""
    if len(sys.argv) < 2:
        help()
        return
    cmd = sys.argv[1]
    if cmd in ('help'):
        help()
    elif cmd in ('plot-rawdata'):
        plot_rawdata()
    elif cmd in ('plot-polyfit'):
        plot_polyfit()
    elif cmd in ('calc'):
        c = [float(v) for v in sys.argv[2:]]
        calc_field(c)
    elif cmd in ('plot-energies-45deg'):
        plot_energies('45deg/')
    elif cmd in ('plot-energies-15deg'):
        plot_energies('15deg/')
    elif cmd in ('plot-trajectories-45deg'):
        plot_trajectories('45deg/')
    elif cmd in ('plot-trajectories-15deg'):
        plot_trajectories('15deg/')
    elif cmd in ('fit-bl-15deg'):
        fit_BL('15deg/')
    elif cmd in ('fit-bl-45deg'):
        fit_BL('45deg/')


if __name__ == "__main__":
    main()
