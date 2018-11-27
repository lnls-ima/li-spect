#!/usr/bin/env python-sirius

"""Analysis of LNLS-SINAP discrepancies in measured linac spect. excdata.

01. O spread na medida de campo de pico do LNLS é de ~2.5% em 4.15A
02. A diferença entre os valores de energia do feixe do linac calculados
    pela curva de excitação do SINAP e pelo curva de excitação dos dipolos
    da TB é de cerca de 12% (142 Mev e 127 MeV)
03. As medidas em alto campo (17A) do SINAP e do LNLS batem em ~0.5%.
04. As medidas em baixo campo (4A) do SINAP e do LNLS diferem em ~3%
05. O comprimento efetivo usado/medido pelo SINAP na curva de excitação
    é de 0.4965 m
06. O comprimento efetivo calculado através do Runge-Kutta das medidas do LNLS
    é de 0.4943m (15 deg) e 0.4673 (45 deg)
07. (a) Aparentemente o SINAP usou o efflen de 15 deg, ao invés do valor
    em 45 deg. Isto explica ~6% dos 12%.
08  (b) Também truncaram os coeficientes to fitting polinomial, o que resultou
    num erro de ~3%.
09  No final, devido aos erros (a) e (b), há uma discrepância entre LNLS e
    SINAP da ordem de 9% em alta corrente.
"""

import numpy as np
import matplotlib.pyplot as plt
import siriuspy.magnet.excdata as ed

lnls15 = ed.ExcitationData(filename_web='li-spect-15deg-lnls.txt')
lnls45 = ed.ExcitationData(filename_web='li-spect-45deg-lnls.txt')
sinap = ed.ExcitationData(filename_web='li-spect-sinap.txt')

coeffs_sinap = [-0.000147274, 0.0294354992, 0.0016115352]
coeffs_sinap_truncated = [-0.0001, 0.0294, 0.0016]
c = np.linspace(0, 20, 41)
bl = np.polyval(coeffs_sinap_truncated, c)

efflen_lnls_15deg_18A = 0.4943  # [m]
efflen_lnls_45deg_18A = 0.4673  # [m]
efflen_sinap_17A = 0.4965  # [m]

bl_lnls_18A = 0.4570
bl_sinap_truncated_18A = 0.4980


plt.plot(lnls15.currents, lnls15.multipoles['normal'][0], label='lnls15')
plt.plot(lnls45.currents, lnls45.multipoles['normal'][0], label='lnls45')
plt.plot(sinap.currents, sinap.multipoles['normal'][0], label='sinap-rawdata')
plt.plot(c, bl, label='sinap-truncated-fit')
plt.xlim(0, 20)
plt.ylim(0, 0.6)
plt.xlabel('Current [A]')
plt.ylabel('BL [T.m]')
plt.title('Excitation Curves for LINAC Spectrometer')
plt.legend()
plt.grid()
plt.show()
