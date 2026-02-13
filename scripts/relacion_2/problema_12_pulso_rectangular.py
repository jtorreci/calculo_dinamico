#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 12: Respuesta a Pulso Rectangular
==========================================

Análisis de la respuesta de un sistema SDOF a un pulso rectangular
y cálculo del espectro de choque.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')

from libreria_dinamica import SDOF, newmark
from libreria_dinamica.utils import pulso_rectangular

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 5000      # kg - Masa de la máquina
f_n = 3       # Hz - Frecuencia natural
zeta = 0.08   # Amortiguamiento
F0 = 100000   # N - Amplitud del pulso (100 kN)
t_d = 0.05    # s - Duración del pulso

# =============================================================================
# CÁLCULOS
# =============================================================================

print("=" * 60)
print("PROBLEMA 12: RESPUESTA A PULSO RECTANGULAR")
print("=" * 60)

# Crear sistema
omega_n = 2 * np.pi * f_n
k = m * omega_n**2
c = 2 * zeta * np.sqrt(k * m)
sistema = SDOF(m, k, c=c)

print(f"\nDatos del sistema:")
print(f"  m = {m} kg")
print(f"  f_n = {f_n} Hz")
print(f"  T_n = {sistema.T_n:.3f} s")
print(f"  zeta = {zeta}")
print(f"  k = {k/1e6:.2f} MN/m")

print(f"\nDatos del pulso:")
print(f"  F0 = {F0/1000} kN")
print(f"  t_d = {t_d} s")

# Relación t_d/T_n
ratio_td_Tn = t_d / sistema.T_n
print(f"\nRelación t_d/T_n = {ratio_td_Tn:.3f}")
if ratio_td_Tn < 0.25:
    tipo_carga = "IMPULSIVA"
elif ratio_td_Tn < 3:
    tipo_carga = "INTERMEDIA"
else:
    tipo_carga = "CUASI-ESTÁTICA"
print(f"  Tipo de carga: {tipo_carga}")

# Impulso total
I = F0 * t_d
print(f"\nImpulso total I = F0 * t_d = {I/1000:.1f} kN·s")

# Factor de amplificación dinámica teórico
DAF_teorico = 2 * np.sin(np.pi * ratio_td_Tn)
print(f"\nFactor de amplificación (teórico):")
print(f"  DAF = 2*sin(pi*t_d/T_n) = {DAF_teorico:.3f}")

# Desplazamiento estático
u_st = F0 / k
print(f"\nDesplazamiento estático: u_st = F0/k = {u_st*1000:.2f} mm")

# Integración numérica
dt = sistema.T_n / 50
t = np.arange(0, 1.5, dt)
F = pulso_rectangular(t, F0, t_d)

u, v, a = newmark(m, c, k, F, dt)

u_max = np.max(np.abs(u))
DAF_numerico = u_max / u_st

print(f"\nResultados numéricos:")
print(f"  u_max = {u_max*1000:.2f} mm")
print(f"  DAF = u_max / u_st = {DAF_numerico:.3f}")

# Comparación
print(f"\n--- Comparación ---")
print(f"  DAF teórico: {DAF_teorico:.3f}")
print(f"  DAF numérico: {DAF_numerico:.3f}")
print(f"  Error: {abs(DAF_teorico - DAF_numerico)/DAF_teorico*100:.1f}%")

# =============================================================================
# ESPECTRO DE CHOQUE
# =============================================================================

print(f"\n--- Espectro de Choque (SRS) ---")

# Rango de t_d/T_n para el espectro
ratio_range = np.linspace(0.01, 3, 100)
T_n_range = t_d / ratio_range  # T_n para cada ratio

DAF_srs = np.zeros_like(ratio_range)

for i, T_ni in enumerate(T_n_range):
    omega_ni = 2 * np.pi / T_ni
    k_i = m * omega_ni**2
    c_i = 2 * zeta * np.sqrt(k_i * m)

    dt_i = T_ni / 30
    t_i = np.arange(0, max(3 * T_ni, 2 * t_d), dt_i)
    F_i = pulso_rectangular(t_i, F0, t_d)

    u_i, _, _ = newmark(m, c_i, k_i, F_i, dt_i)
    u_st_i = F0 / k_i
    DAF_srs[i] = np.max(np.abs(u_i)) / u_st_i

# =============================================================================
# GRÁFICAS
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Subplot 1: Pulso y respuesta
ax1 = axes[0, 0]
ax1_twin = ax1.twinx()

l1, = ax1.plot(t * 1000, F / 1000, 'b-', linewidth=2, label='Fuerza')
ax1.fill_between(t * 1000, 0, F / 1000, alpha=0.2)
ax1.set_ylabel('Fuerza [kN]', fontsize=11, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

l2, = ax1_twin.plot(t * 1000, u * 1000, 'r-', linewidth=2, label='Desplazamiento')
ax1_twin.set_ylabel('Desplazamiento [mm]', fontsize=11, color='red')
ax1_twin.tick_params(axis='y', labelcolor='red')

ax1.set_xlabel('Tiempo [ms]', fontsize=11)
ax1.set_title('Pulso Rectangular y Respuesta', fontsize=12, fontweight='bold')
ax1.legend([l1, l2], ['Fuerza', 'Desplazamiento'], loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, 500])

# Subplot 2: Respuesta ampliada
ax2 = axes[0, 1]
ax2.plot(t * 1000, u * 1000, 'b-', linewidth=2)
ax2.axhline(u_max * 1000, color='red', linestyle='--', alpha=0.5,
            label=f'$u_{{max}}$ = {u_max*1000:.1f} mm')
ax2.axhline(u_st * 1000, color='green', linestyle=':', alpha=0.5,
            label=f'$u_{{st}}$ = {u_st*1000:.1f} mm')
ax2.axhline(-u_max * 1000, color='red', linestyle='--', alpha=0.5)
ax2.axvline(t_d * 1000, color='gray', linestyle='--', alpha=0.5)
ax2.set_xlabel('Tiempo [ms]', fontsize=11)
ax2.set_ylabel('Desplazamiento [mm]', fontsize=11)
ax2.set_title(f'Respuesta (DAF = {DAF_numerico:.2f})', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 1000])

# Subplot 3: Espectro de choque
ax3 = axes[1, 0]
ax3.plot(ratio_range, DAF_srs, 'b-', linewidth=2)
ax3.axhline(2, color='red', linestyle='--', alpha=0.5, label='DAF = 2')
ax3.axhline(1, color='gray', linestyle=':', alpha=0.5, label='DAF = 1')
ax3.axvline(ratio_td_Tn, color='green', linestyle='--',
            label=f'$t_d/T_n$ = {ratio_td_Tn:.2f}')
ax3.set_xlabel('$t_d / T_n$', fontsize=11)
ax3.set_ylabel('Factor de Amplificación Dinámica', fontsize=11)
ax3.set_title('Espectro de Choque (Pulso Rectangular)', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3)
ax3.set_xlim([0, 3])
ax3.set_ylim([0, 2.5])

# Anotaciones de zonas
ax3.annotate('Impulsiva', xy=(0.1, 0.5), fontsize=9, color='blue')
ax3.annotate('Intermedia', xy=(1.0, 2.1), fontsize=9, color='blue')
ax3.annotate('Cuasi-estática', xy=(2.5, 2.1), fontsize=9, color='blue')

# Subplot 4: Comparación DAF teórico vs numérico
ax4 = axes[1, 1]
DAF_teorico_curve = 2 * np.abs(np.sin(np.pi * ratio_range))
ax4.plot(ratio_range, DAF_teorico_curve, 'r--', linewidth=2, label='Teórico ($\\zeta$=0)')
ax4.plot(ratio_range, DAF_srs, 'b-', linewidth=2, label=f'Numérico ($\\zeta$={zeta})')
ax4.set_xlabel('$t_d / T_n$', fontsize=11)
ax4.set_ylabel('Factor de Amplificación Dinámica', fontsize=11)
ax4.set_title('Comparación Teórico vs Numérico', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim([0, 3])
ax4.set_ylim([0, 2.5])

plt.suptitle(f'Respuesta a Pulso Rectangular: m={m} kg, f_n={f_n} Hz, $\\zeta$={zeta}',
             fontsize=13, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('../figs/fig_problema_12_pulso.pdf', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nFigura guardada: figs/fig_problema_12_pulso.pdf")
