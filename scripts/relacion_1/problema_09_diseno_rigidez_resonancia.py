#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 09: Diseno de Rigidez para Evitar la Zona de Amplificacion (Resonancia)
================================================================================

Estructura con maquinaria industrial. Se debe disenar la rigidez
para alejar la frecuencia natural de la frecuencia de excitacion.

Ejecutar: python problema_09_diseno_rigidez_resonancia.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

omega_exc = 35.0    # rad/s - Frecuencia de excitacion de la maquina
m = 1500.0          # kg - Masa vibratoria total
k_existente = 1.0e7  # N/m - Rigidez estructural existente

# Criterio de diseno: omega_n >= 3 * omega_exc (es decir, beta = omega_exc/omega_n <= 1/3)
factor_seguridad = 3.0

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 70)
print("PROBLEMA 09: DISENO DE RIGIDEZ PARA EVITAR RESONANCIA")
print("=" * 70)
print()

print("Datos del problema:")
print(f"  Frecuencia de excitacion omega_exc = {omega_exc} rad/s")
print(f"  Masa vibratoria m = {m} kg")
print(f"  Rigidez existente k_existente = {k_existente/1e6:.1f} MN/m")
print(f"  Criterio: omega_n >= {factor_seguridad} * omega_exc")
print()

# 1. Frecuencia natural minima requerida
omega_n_min = factor_seguridad * omega_exc

print("1. FRECUENCIA NATURAL MINIMA REQUERIDA:")
print(f"   omega_n_min = {factor_seguridad} * omega_exc")
print(f"   omega_n_min = {factor_seguridad} * {omega_exc} rad/s")
print(f"   omega_n_min = {omega_n_min} rad/s")
print()

# Verificar beta de diseno
beta_diseno = omega_exc / omega_n_min
print(f"   Ratio de frecuencias de diseno:")
print(f"   beta = omega_exc/omega_n = {omega_exc}/{omega_n_min} = {beta_diseno:.3f}")
print()

# 2. Rigidez total requerida
k_req = m * omega_n_min**2

print("2. RIGIDEZ TOTAL REQUERIDA:")
print(f"   k_req = m * omega_n_min^2")
print(f"   k_req = {m} kg * ({omega_n_min} rad/s)^2")
print(f"   k_req = {m} * {omega_n_min**2}")
print(f"   k_req = {k_req:,.0f} N/m = {k_req/1e6:.3f} MN/m")
print()

# 3. Rigidez adicional necesaria
delta_k = k_req - k_existente

print("3. RIGIDEZ ADICIONAL NECESARIA:")
print(f"   Delta_k = k_req - k_existente")
print(f"   Delta_k = {k_req/1e6:.3f} MN/m - {k_existente/1e6:.1f} MN/m")
print(f"   Delta_k = {delta_k/1e6:.3f} MN/m = {delta_k/1e3:.1f} kN/m")
print()

# Verificacion: frecuencia actual sin refuerzo
omega_n_actual = np.sqrt(k_existente / m)
beta_actual = omega_exc / omega_n_actual

print("VERIFICACION - Estado actual (sin refuerzo):")
print(f"   omega_n_actual = sqrt(k_existente/m) = sqrt({k_existente/1e6:.1f}e6/{m})")
print(f"   omega_n_actual = {omega_n_actual:.2f} rad/s")
print(f"   beta_actual = omega_exc/omega_n = {omega_exc}/{omega_n_actual:.2f} = {beta_actual:.2f}")
print(f"   PELIGRO: beta_actual = {beta_actual:.2f} esta en zona de resonancia (0.5 < beta < 2)")
print()

# =============================================================================
# GRAFICO: FACTOR DE AMPLIFICACION vs BETA
# =============================================================================

# Crear vector beta
beta = np.linspace(0.01, 3, 500)

# Factor de amplificacion dinamica (DAF) para varios zeta
zetas = [0.02, 0.05, 0.10, 0.20]

def DAF(beta, zeta):
    """Factor de amplificacion dinamica D = 1/sqrt((1-beta^2)^2 + (2*zeta*beta)^2)"""
    return 1 / np.sqrt((1 - beta**2)**2 + (2 * zeta * beta)**2)

# Crear figura
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['blue', 'green', 'orange', 'red']
for zeta, color in zip(zetas, colors):
    D = DAF(beta, zeta)
    ax.plot(beta, D, color=color, linewidth=1.5,
            label=r'$\zeta$ = ' + f'{zeta*100:.0f}%')

# Zona de resonancia peligrosa
ax.axvspan(0.5, 2.0, alpha=0.15, color='red', label='Zona critica (0.5 < beta < 2)')

# Marcar beta de diseno y beta actual
ax.axvline(x=beta_diseno, color='green', linestyle='--', linewidth=2,
           label=f'Diseno: beta = {beta_diseno:.2f}')
ax.axvline(x=beta_actual, color='darkred', linestyle=':', linewidth=2,
           label=f'Actual: beta = {beta_actual:.2f}')

# Linea de resonancia
ax.axvline(x=1.0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)

# Configuracion
ax.set_xlabel(r'Ratio de frecuencias $\beta = \omega/\omega_n$', fontsize=12)
ax.set_ylabel(r'Factor de amplificacion dinamica $D$', fontsize=12)
ax.set_title('Factor de Amplificacion Dinamica vs Ratio de Frecuencias\n' +
             'Diseno de rigidez para evitar resonancia', fontsize=12)
ax.set_xlim([0, 3])
ax.set_ylim([0, 12])
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=9)

# Anotaciones
ax.annotate('RESONANCIA', xy=(1, 11), fontsize=10, ha='center',
            color='darkred', weight='bold')
ax.annotate('Zona segura\n(alta rigidez)', xy=(0.2, 3), fontsize=9,
            ha='center', color='green')
ax.annotate('Zona segura\n(aislamiento)', xy=(2.5, 3), fontsize=9,
            ha='center', color='blue')

plt.tight_layout()

# Guardar
output_path = "../figs/fig_problema_09_amplificacion_beta.pdf"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Figura guardada: {output_path}")
plt.close()

# =============================================================================
# RESUMEN
# =============================================================================

print()
print("=" * 70)
print("RESUMEN")
print("=" * 70)
print(f"  Frecuencia natural minima omega_n_min = {omega_n_min} rad/s")
print(f"  Rigidez total requerida k_req = {k_req/1e6:.3f} MN/m")
print(f"  Rigidez adicional Delta_k = {delta_k/1e3:.1f} kN/m ({delta_k/1e6:.3f} MN/m)")
print()
print("  Estado actual (sin refuerzo):")
print(f"    omega_n = {omega_n_actual:.2f} rad/s, beta = {beta_actual:.2f} (PELIGROSO)")
print()
print("  Estado con refuerzo:")
print(f"    omega_n = {omega_n_min:.0f} rad/s, beta = {beta_diseno:.3f} (SEGURO)")
print()
