#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 24: Rigidez de Marco (Idealización SDOF)
==================================================

Pórtico de un nivel con columnas empotradas y viga rígida.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA (unidades SI)
# =============================================================================

E = 200e9           # Pa (N/m²) - módulo de elasticidad del acero (200 GPa)
I_c = 3.5e-4        # m⁴ - momento de inercia de columna (HEB 300)
h = 3.6             # m - altura de columna
n_columnas = 2      # número de columnas

# =============================================================================
# CÁLCULOS
# =============================================================================

# Rigidez de una columna biempotrada (extremos fijos)
k_columna = 12 * E * I_c / h**3

# Rigidez total del pórtico (columnas en paralelo)
k_total = n_columnas * k_columna

# Comparación con otras condiciones de extremo
# Columna articulada-empotrada (un extremo libre para rotar)
k_artic_emp = 3 * E * I_c / h**3
k_total_artic = n_columnas * k_artic_emp

# Ratio de rigidez
ratio = k_total / k_total_artic

print("=" * 60)
print("PROBLEMA 24: RIGIDEZ DE PORTICO SDOF")
print("=" * 60)
print(f"\nDatos:")
print(f"  E = {E/1e9:.0f} GPa")
print(f"  I_c = {I_c:.4e} m^4")
print(f"  Altura h = {h} m")
print(f"  Numero de columnas: {n_columnas}")

print(f"\n--- Columna Biempotrada (viga rigida) ---")
print(f"  k_columna = 12*E*I/h^3 = {k_columna/1e6:.2f} MN/m = {k_columna/1e3:.0f} kN/m")
print(f"  k_total = {n_columnas} x {k_columna/1e3:.0f} = {k_total/1e3:.0f} kN/m")

print(f"\n--- Efecto de Flexibilidad de Viga ---")
print(f"  Si la viga NO fuera rigida (articulada en columna):")
print(f"  k_columna = 3*E*I/h^3 = {k_artic_emp/1e3:.0f} kN/m")
print(f"  k_total = {n_columnas} x {k_artic_emp/1e3:.0f} = {k_total_artic/1e3:.0f} kN/m")
print(f"  Ratio k_rigida/k_flexible = {ratio:.1f}")
print(f"  La viga rigida proporciona {ratio:.0f}x mas rigidez lateral")

# =============================================================================
# GRÁFICA
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: Comparación de rigidez según condición de extremo
ax1 = axes[0]

condiciones = ['Viga Rígida\n(biempotrada)', 'Viga Flexible\n(articulada)']
rigideces = [k_total/1e3, k_total_artic/1e3]  # en kN/m
colores = ['steelblue', 'lightcoral']

bars = ax1.bar(condiciones, rigideces, color=colores, edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Rigidez Lateral (kN/m)', fontsize=11)
ax1.set_title('Efecto de la Condición de Extremo', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Valores sobre barras
for bar, val in zip(bars, rigideces):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'{val:.0f} kN/m', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Anotación del ratio
ax1.annotate(f'×{ratio:.0f}', xy=(0.5, k_total_artic/1e3 + (k_total - k_total_artic)/2e3),
             fontsize=16, fontweight='bold', color='darkgreen', ha='center')

# Gráfica 2: Variación de rigidez con altura
ax2 = axes[1]

h_range = np.linspace(2.5, 6.0, 100)  # 2.5 a 6.0 metros
k_range_biemp = n_columnas * 12 * E * I_c / h_range**3
k_range_artic = n_columnas * 3 * E * I_c / h_range**3

ax2.plot(h_range, k_range_biemp/1e3, 'steelblue', linewidth=2, label='Viga rígida (12EI/h³)')
ax2.plot(h_range, k_range_artic/1e3, 'coral', linewidth=2, label='Viga flexible (3EI/h³)')

# Punto del problema
ax2.plot(h, k_total/1e3, 'ko', markersize=10, markerfacecolor='steelblue',
         label=f'Diseño: h={h} m, k={k_total/1e3:.0f} kN/m')

ax2.set_xlabel('Altura de Columna (m)', fontsize=11)
ax2.set_ylabel('Rigidez Lateral Total (kN/m)', fontsize=11)
ax2.set_title('Rigidez vs Altura de Columna', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([2.5, 6.0])

# Anotación sobre sensibilidad
ax2.text(4.5, max(k_range_biemp/1e3)*0.7, r'$k \propto 1/h^3$', fontsize=14, style='italic', color='gray')

plt.tight_layout()
plt.savefig('../figs/fig_problema_24_portico_rigidez.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_24_portico_rigidez.pdf")
