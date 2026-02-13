# -*- coding: utf-8 -*-
"""
Problema 01: Edificio de 2 plantas (shear building)
===================================================
Analisis modal de un edificio de 2 plantas con forjados rigidos.

Datos:
- m1 = m2 = 1000 kg
- k1 = k2 = 200 kN/m
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../../scripts')
from libreria_dinamica import MDOF, shear_building

# =============================================================================
# 1. Definicion del sistema
# =============================================================================
print("=" * 60)
print("PROBLEMA 01: EDIFICIO DE 2 PLANTAS (SHEAR BUILDING)")
print("=" * 60)

# Parametros
m = np.array([1000.0, 1000.0])  # kg
k = np.array([200e3, 200e3])     # N/m

# Construccion de matrices
M, K = shear_building(m, k)

print("\n1) MATRICES DEL SISTEMA")
print("-" * 40)
print("Matriz de masa M (kg):")
print(M)
print("\nMatriz de rigidez K (N/m):")
print(K)

# =============================================================================
# 2. Analisis modal
# =============================================================================
sistema = MDOF(M, K)

print("\n2) FRECUENCIAS NATURALES")
print("-" * 40)
print(f"w1 = {sistema.omega[0]:.3f} rad/s  (f1 = {sistema.freq[0]:.3f} Hz)")
print(f"w2 = {sistema.omega[1]:.3f} rad/s  (f2 = {sistema.freq[1]:.3f} Hz)")

print("\n3) MODOS DE VIBRACION (normalizados masa-unidad)")
print("-" * 40)
print("Modo 1:", sistema.phi[:, 0])
print("Modo 2:", sistema.phi[:, 1])

# =============================================================================
# 3. Factores de participacion y masas efectivas
# =============================================================================
r = np.array([1.0, 1.0])  # Vector de influencia para excitacion de base
Gamma = sistema.factores_participacion(r)
M_ef, M_ef_pct, M_total = sistema.masas_efectivas(r)

print("\n4) FACTORES DE PARTICIPACION MODAL")
print("-" * 40)
print(f"Gamma_1 = {Gamma[0]:.2f}")
print(f"Gamma_2 = {Gamma[1]:.2f}")

print("\n5) MASAS EFECTIVAS MODALES")
print("-" * 40)
print(f"M_ef,1 = {M_ef[0]:.1f} kg ({M_ef_pct[0]:.1f}%)")
print(f"M_ef,2 = {M_ef[1]:.1f} kg ({M_ef_pct[1]:.1f}%)")
print(f"Suma = {np.sum(M_ef):.1f} kg (M_total = {M_total:.1f} kg)")

# =============================================================================
# 4. Verificacion de ortogonalidad
# =============================================================================
print("\n6) VERIFICACION DE ORTOGONALIDAD")
print("-" * 40)
phi1, phi2 = sistema.phi[:, 0], sistema.phi[:, 1]
ort_M = phi1 @ M @ phi2
ort_K = phi1 @ K @ phi2
print(f"phi1^T M phi2 = {ort_M:.2e} (debe ser ~ 0)")
print(f"phi1^T K phi2 = {ort_K:.2e} (debe ser ~ 0)")
print(f"phi1^T M phi1 = {phi1 @ M @ phi1:.4f} (debe ser = 1)")
print(f"phi2^T M phi2 = {phi2 @ M @ phi2:.4f} (debe ser = 1)")

# =============================================================================
# 5. Graficas
# =============================================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

# 5.1 Modos de vibracion
ax1 = axes[0]
plantas = [0, 1, 2]
modo1_plot = np.concatenate([[0], sistema.phi[:, 0] / np.max(np.abs(sistema.phi[:, 0]))])
modo2_plot = np.concatenate([[0], sistema.phi[:, 1] / np.max(np.abs(sistema.phi[:, 1]))])

ax1.plot(modo1_plot, plantas, 'b-o', linewidth=2, markersize=10, label=f'Modo 1 (f={sistema.freq[0]:.2f} Hz)')
ax1.plot(modo2_plot, plantas, 'r-s', linewidth=2, markersize=10, label=f'Modo 2 (f={sistema.freq[1]:.2f} Hz)')
ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
ax1.set_xlabel('Desplazamiento normalizado')
ax1.set_ylabel('Planta')
ax1.set_yticks([0, 1, 2])
ax1.set_yticklabels(['Base', 'Planta 1', 'Planta 2'])
ax1.legend()
ax1.set_title('Modos de vibracion')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-1.5, 1.5)

# 5.2 Masas efectivas
ax2 = axes[1]
modos = ['Modo 1', 'Modo 2']
colors = ['steelblue', 'coral']
bars = ax2.bar(modos, M_ef_pct, color=colors, edgecolor='black')
ax2.axhline(y=90, color='green', linestyle='--', linewidth=1.5, label='90% (minimo sismico)')
ax2.set_ylabel('Masa efectiva (%)')
ax2.set_title('Participacion modal')
ax2.legend()
ax2.set_ylim(0, 100)
for bar, pct in zip(bars, M_ef_pct):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{pct:.1f}%', ha='center', fontsize=11, fontweight='bold')

# 5.3 Respuesta libre
ax3 = axes[2]
t = np.linspace(0, 2, 500)
x0 = np.array([0.01, 0.0])  # 10 mm en planta 1
v0 = np.array([0.0, 0.0])
x_t = sistema.respuesta_libre(x0, v0, t)

ax3.plot(t, x_t[0, :] * 1000, 'b-', linewidth=1.5, label='x1(t) - Planta 1')
ax3.plot(t, x_t[1, :] * 1000, 'r-', linewidth=1.5, label='x2(t) - Planta 2')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Desplazamiento (mm)')
ax3.set_title('Respuesta libre (x1(0)=10 mm)')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figs/fig_problema_01_analisis_modal.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_01_analisis_modal.pdf', bbox_inches='tight')
print("\n[Grafica guardada en figs/fig_problema_01_analisis_modal.png]")
plt.show()
