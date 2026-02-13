#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 28: Factor de Amplificación Dinámica - Curvas de Respuesta
===================================================================

Genera curvas del factor de amplificación dinámica (DAF) para
diferentes valores de amortiguamiento.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

zetas = [0.0, 0.1, 0.2, 0.5, 1.0]  # Ratios de amortiguamiento
r = np.linspace(0.01, 3.0, 500)  # Ratio de frecuencias omega/omega_n

# =============================================================================
# CÁLCULOS
# =============================================================================

print("=" * 60)
print("PROBLEMA 28: FACTOR DE AMPLIFICACIÓN DINÁMICA")
print("=" * 60)

def DAF(r, zeta):
    """Factor de amplificación dinámica."""
    if zeta == 0:
        # Evitar división por cero en resonancia
        result = np.ones_like(r)
        mask = r != 1
        result[mask] = 1 / np.abs(1 - r[mask]**2)
        result[~mask] = np.inf
        return result
    return 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)

def r_max(zeta):
    """Frecuencia del máximo DAF."""
    if zeta >= 1/np.sqrt(2):
        return 0
    return np.sqrt(1 - 2 * zeta**2)

def DAF_max(zeta):
    """Valor máximo del DAF."""
    if zeta == 0:
        return np.inf
    if zeta >= 1/np.sqrt(2):
        return 1
    return 1 / (2 * zeta * np.sqrt(1 - zeta**2))

# Tabla de valores
print("\n--- Tabla de DAF ---")
r_vals = [0, 0.5, 1.0, np.sqrt(2), 2.0, 3.0]
print(f"{'r':>8} |", end='')
for zeta in zetas:
    print(f" zeta={zeta:>3} |", end='')
print()
print("-" * 60)

for r_val in r_vals:
    print(f"{r_val:>8.3f} |", end='')
    for zeta in zetas:
        if r_val == 0:
            daf = 1.0
        elif r_val == 1.0 and zeta == 0:
            daf = float('inf')
        else:
            daf = DAF(np.array([r_val]), zeta)[0]
        if np.isinf(daf):
            print(f" {'inf':>7} |", end='')
        else:
            print(f" {daf:>7.3f} |", end='')
    print()

print("\n--- Frecuencia del máximo y DAF máximo ---")
for zeta in zetas:
    r_m = r_max(zeta)
    daf_m = DAF_max(zeta)
    print(f"zeta = {zeta}: r_max = {r_m:.3f}, DAF_max = {daf_m:.3f}" if not np.isinf(daf_m)
          else f"zeta = {zeta}: r_max = {r_m:.3f}, DAF_max = inf")

# Amortiguamiento óptimo
print(f"\nAmortiguamiento óptimo (DAF_max = 1): zeta = 1/sqrt(2) = {1/np.sqrt(2):.3f}")

# =============================================================================
# GRÁFICAS
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 7))

colores = ['blue', 'orange', 'green', 'red', 'purple']
estilos = ['-', '--', '-.', ':', '-']

for zeta, color, estilo in zip(zetas, colores, estilos):
    daf = DAF(r, zeta)
    # Limitar para visualización
    daf_plot = np.clip(daf, 0, 15)
    ax.plot(r, daf_plot, estilo, color=color, linewidth=2,
            label=f'$\\zeta$ = {zeta}')

# Líneas de referencia
ax.axhline(1, color='gray', linestyle=':', alpha=0.5, label='DAF = 1')
ax.axvline(1, color='gray', linestyle='--', alpha=0.3)
ax.axvline(np.sqrt(2), color='gray', linestyle='--', alpha=0.3)

# Anotaciones
ax.annotate('$r = 1$\n(resonancia)', xy=(1, 0.3), fontsize=9, ha='center')
ax.annotate('$r = \\sqrt{2}$', xy=(np.sqrt(2), 0.3), fontsize=9, ha='center')

ax.set_xlabel('$r = \\omega / \\omega_n$', fontsize=12)
ax.set_ylabel('DAF = $X / (F_0/k)$', fontsize=12)
ax.set_title('Factor de Amplificación Dinámica', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 3])
ax.set_ylim([0, 8])

# Región de aislamiento
ax.fill_between([np.sqrt(2), 3], [0, 0], [8, 8], alpha=0.1, color='green')
ax.text(2.2, 7, 'Zona de\naislamiento', fontsize=9, ha='center', color='green')

# Región de amplificación
ax.fill_between([0, np.sqrt(2)], [1, 1], [8, 8], alpha=0.1, color='red')
ax.text(0.7, 7, 'Zona de\namplificación', fontsize=9, ha='center', color='red')

plt.tight_layout()
plt.savefig('../figs/fig_problema_28_daf.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_28_daf.pdf")
