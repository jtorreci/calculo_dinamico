#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 08: Diagramas de Bode de Sistemas SDOF
===============================================

Genera diagramas de Bode (magnitud y fase) para diferentes
valores de amortiguamiento.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')

from libreria_dinamica import frf_receptancia
from libreria_dinamica.frecuencial import diagrama_bode

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

omega_n = 10  # rad/s - Frecuencia natural
zetas = [0.01, 0.1, 0.5]  # Ratios de amortiguamiento
k = 1000  # N/m - Rigidez (arbitraria para normalización)

# Rango de frecuencias
omega = np.logspace(-1, 1.5, 500) * omega_n  # 0.1*omega_n a ~30*omega_n

# =============================================================================
# CÁLCULOS
# =============================================================================

print("=" * 60)
print("PROBLEMA 08: DIAGRAMAS DE BODE")
print("=" * 60)
print(f"\nDatos:")
print(f"  omega_n = {omega_n} rad/s")
print(f"  Amortiguamientos: zeta = {zetas}")

# Calcular FRF para cada amortiguamiento
resultados = {}
for zeta in zetas:
    m = k / omega_n**2
    c = 2 * zeta * np.sqrt(k * m)

    H = frf_receptancia(omega, m, c, k, normalizar=True)
    mag_dB, fase_deg = diagrama_bode(omega, H)

    resultados[zeta] = {'H': H, 'mag_dB': mag_dB, 'fase_deg': fase_deg}

    # Valores en resonancia
    idx_res = np.argmin(np.abs(omega - omega_n))
    print(f"\nzeta = {zeta}:")
    print(f"  Magnitud en resonancia: {mag_dB[idx_res]:.2f} dB")
    print(f"  |H|_max = 1/(2*zeta) = {1/(2*zeta):.2f}")
    print(f"  Fase en resonancia: {fase_deg[idx_res]:.1f}°")

# Calcular valores teóricos para la tabla
print("\n--- Tabla de valores ---")
r_values = [0.1, 0.5, 1.0, 2.0, 5.0]
print(f"{'r':>6} | ", end='')
for zeta in zetas:
    print(f"zeta={zeta} (dB, °) | ", end='')
print()
print("-" * 70)

for r in r_values:
    print(f"{r:>6.1f} | ", end='')
    for zeta in zetas:
        DAF = 1 / np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
        mag_dB = 20 * np.log10(DAF)
        fase = -np.arctan2(2*zeta*r, 1 - r**2) * 180 / np.pi
        print(f"{mag_dB:>7.2f}, {fase:>6.1f}° | ", end='')
    print()

# =============================================================================
# GRÁFICAS
# =============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

colores = ['blue', 'orange', 'green']
estilos = ['-', '--', '-.']

# Magnitud
for (zeta, datos), color, estilo in zip(resultados.items(), colores, estilos):
    ax1.semilogx(omega / omega_n, datos['mag_dB'], estilo, color=color,
                 linewidth=2, label=f'$\\zeta$ = {zeta}')

ax1.axhline(0, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(1, color='red', linestyle='--', alpha=0.5, label='$\\omega = \\omega_n$')
ax1.set_ylabel('Magnitud [dB]', fontsize=11)
ax1.set_title('Diagrama de Bode - Receptancia Normalizada', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3, which='both')
ax1.set_ylim([-40, 40])

# Añadir anotación de pendiente
ax1.annotate('-40 dB/década', xy=(5, -25), fontsize=9, color='gray')

# Fase
for (zeta, datos), color, estilo in zip(resultados.items(), colores, estilos):
    ax2.semilogx(omega / omega_n, datos['fase_deg'], estilo, color=color,
                 linewidth=2, label=f'$\\zeta$ = {zeta}')

ax2.axhline(-90, color='gray', linestyle=':', alpha=0.5)
ax2.axhline(-180, color='gray', linestyle=':', alpha=0.5)
ax2.axvline(1, color='red', linestyle='--', alpha=0.5)
ax2.set_xlabel('$\\omega / \\omega_n$', fontsize=11)
ax2.set_ylabel('Fase [°]', fontsize=11)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3, which='both')
ax2.set_ylim([-200, 20])
ax2.set_yticks([0, -45, -90, -135, -180])

plt.tight_layout()
plt.savefig('../figs/fig_problema_08_bode.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_08_bode.pdf")
