#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 29: Aislamiento de Vibraciones (Aceleracion Transmitida)
=================================================================

Maquina industrial montada sobre aisladores.
Calcula la frecuencia natural maxima y rigidez para lograr TR <= 5%.

Ejecutar: python problema_29_transmisibilidad.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 100.0       # kg - Masa de la maquina
f_exc = 15.0    # Hz - Frecuencia de operacion
zeta = 0.05     # Razon de amortiguamiento del aislador (5%)
TR_max = 0.05   # Transmisibilidad maxima requerida (5%)

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 70)
print("PROBLEMA 29: AISLAMIENTO DE VIBRACIONES - TRANSMISIBILIDAD")
print("=" * 70)
print()

print("Datos del problema:")
print(f"  Masa de la maquina m = {m} kg")
print(f"  Frecuencia de operacion f = {f_exc} Hz")
print(f"  Razon de amortiguamiento zeta = {zeta} ({zeta*100:.0f}%)")
print(f"  Transmisibilidad maxima TR_max = {TR_max} ({TR_max*100:.0f}%)")
print()

# 1. Frecuencia de excitacion en rad/s
omega = 2 * np.pi * f_exc

print("1. FRECUENCIA DE EXCITACION (omega):")
print(f"   omega = 2*pi*f = 2*pi*{f_exc}")
print(f"   omega = {omega:.2f} rad/s = 30*pi rad/s")
print()

# 2. Frecuencia natural maxima
# Usando aproximacion simplificada para omega >> omega_n y zeta pequeno:
# TR ~ 1 / (omega/omega_n)^2
# Para TR = 0.05: (omega/omega_n)^2 >= 1/0.05 = 20
# omega/omega_n >= sqrt(20) = 4.472
# omega_n <= omega / 4.472

beta_min_squared = 1 / TR_max
beta_min = np.sqrt(beta_min_squared)
omega_n_max = omega / beta_min
f_n_max = omega_n_max / (2 * np.pi)
T_n_min = 1 / f_n_max

print("2. FRECUENCIA NATURAL MAXIMA (omega_n_max):")
print("   Para aislamiento efectivo, usamos la aproximacion simplificada:")
print(f"   TR ~ 1/(omega/omega_n)^2 <= {TR_max}")
print()
print(f"   (omega/omega_n)^2 >= 1/{TR_max} = {beta_min_squared}")
print(f"   omega/omega_n >= sqrt({beta_min_squared}) = {beta_min:.3f}")
print()
print(f"   Por tanto:")
print(f"   omega_n <= omega / {beta_min:.3f}")
print(f"   omega_n <= {omega:.2f} / {beta_min:.3f}")
print(f"   omega_n_max = {omega_n_max:.2f} rad/s")
print()
print(f"   Equivalente: f_n_max = {f_n_max:.2f} Hz, T_n_min = {T_n_min:.3f} s")
print()

# 3. Rigidez maxima
k_max = m * omega_n_max**2

print("3. RIGIDEZ MAXIMA DEL AISLADOR (k_max):")
print(f"   k_max = m * omega_n_max^2")
print(f"   k_max = {m} kg * ({omega_n_max:.2f} rad/s)^2")
print(f"   k_max = {m} * {omega_n_max**2:.1f}")
print(f"   k_max = {k_max:,.0f} N/m = {k_max/1e3:.1f} kN/m")
print()

# =============================================================================
# GRAFICO DE TRANSMISIBILIDAD
# =============================================================================

# Crear vector beta (ratio de frecuencias)
beta = np.linspace(0.01, 5, 500)

def TR_func(beta, zeta):
    """
    Transmisibilidad: TR = sqrt((1 + (2*zeta*beta)^2) / ((1-beta^2)^2 + (2*zeta*beta)^2))
    """
    num = 1 + (2 * zeta * beta)**2
    den = (1 - beta**2)**2 + (2 * zeta * beta)**2
    return np.sqrt(num / den)

# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- Panel izquierdo: TR vs beta (escala lineal) ---
zetas_plot = [0.00, 0.05, 0.10, 0.20, 0.50]
colors = ['black', 'blue', 'green', 'orange', 'red']
linestyles = [':', '-', '-', '-', '-']

for z, color, ls in zip(zetas_plot, colors, linestyles):
    TR = TR_func(beta, z)
    lw = 2 if z == zeta else 1.2
    label = r'$\zeta$ = ' + f'{z*100:.0f}%'
    if z == 0:
        label = r'$\zeta$ = 0 (sin amortiguamiento)'
    ax1.plot(beta, TR, color=color, linestyle=ls, linewidth=lw, label=label)

# Zona de aislamiento (beta > sqrt(2))
ax1.axvspan(np.sqrt(2), 5, alpha=0.1, color='green', label='Zona de aislamiento')

# Linea de TR_max
ax1.axhline(y=TR_max, color='purple', linestyle='--', linewidth=1.5,
            label=f'TR_max = {TR_max*100:.0f}%')

# Marcar beta de diseno
ax1.axvline(x=beta_min, color='purple', linestyle=':', linewidth=1.5)
ax1.annotate(f'beta_min = {beta_min:.2f}', xy=(beta_min, TR_max),
             xytext=(beta_min+0.5, TR_max+0.3), fontsize=9,
             arrowprops=dict(arrowstyle='->', color='purple', lw=0.8))

# Punto critico sqrt(2)
ax1.axvline(x=np.sqrt(2), color='gray', linestyle='-.', linewidth=1, alpha=0.7)
ax1.annotate(r'$\sqrt{2}$', xy=(np.sqrt(2), 0.1), fontsize=10, ha='center')

ax1.set_xlabel(r'Ratio de frecuencias $\beta = \omega/\omega_n$', fontsize=11)
ax1.set_ylabel('Transmisibilidad TR', fontsize=11)
ax1.set_title('Transmisibilidad vs Ratio de Frecuencias', fontsize=12)
ax1.set_xlim([0, 5])
ax1.set_ylim([0, 4])
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=9)

# --- Panel derecho: TR vs beta (escala log) ---
for z, color, ls in zip(zetas_plot, colors, linestyles):
    TR = TR_func(beta, z)
    lw = 2 if z == zeta else 1.2
    label = r'$\zeta$ = ' + f'{z*100:.0f}%'
    if z == 0:
        label = r'$\zeta$ = 0'
    ax2.loglog(beta, TR, color=color, linestyle=ls, linewidth=lw, label=label)

# Lineas de referencia
ax2.axhline(y=TR_max, color='purple', linestyle='--', linewidth=1.5,
            label=f'TR = {TR_max*100:.0f}%')
ax2.axhline(y=1, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax2.axvline(x=np.sqrt(2), color='gray', linestyle='-.', linewidth=1, alpha=0.7)
ax2.axvline(x=beta_min, color='purple', linestyle=':', linewidth=1.5)

# Aproximacion TR ~ 1/beta^2
beta_approx = np.linspace(2, 5, 100)
TR_approx = 1 / beta_approx**2
ax2.loglog(beta_approx, TR_approx, 'k--', linewidth=1, alpha=0.5,
           label=r'Aprox: TR $\approx 1/\beta^2$')

ax2.set_xlabel(r'Ratio de frecuencias $\beta = \omega/\omega_n$', fontsize=11)
ax2.set_ylabel('Transmisibilidad TR', fontsize=11)
ax2.set_title('Transmisibilidad (Escala Logaritmica)\n' +
              f'Diseno: beta >= {beta_min:.2f} para TR <= {TR_max*100:.0f}%', fontsize=11)
ax2.set_xlim([0.1, 5])
ax2.set_ylim([0.01, 20])
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(loc='upper right', fontsize=8)

plt.tight_layout()

# Guardar
output_path = "../figs/fig_problema_29_transmisibilidad.pdf"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Figura guardada: {output_path}")
plt.close()

# =============================================================================
# VERIFICACION CON FORMULA EXACTA
# =============================================================================

print()
print("VERIFICACION CON FORMULA EXACTA DE TRANSMISIBILIDAD:")
print("   TR = sqrt((1 + (2*zeta*beta)^2) / ((1-beta^2)^2 + (2*zeta*beta)^2))")
print()
TR_exact = TR_func(beta_min, zeta)
print(f"   Para beta = {beta_min:.3f} y zeta = {zeta}:")
print(f"   TR_exact = {TR_exact:.4f} = {TR_exact*100:.2f}%")
print()
if TR_exact <= TR_max:
    print(f"   CUMPLE: TR = {TR_exact*100:.2f}% <= {TR_max*100:.0f}%")
else:
    print(f"   NO CUMPLE con aproximacion. Recalcular con formula exacta.")
print()

# =============================================================================
# RESUMEN
# =============================================================================

print()
print("=" * 70)
print("RESUMEN")
print("=" * 70)
print(f"  Frecuencia de excitacion omega = {omega:.2f} rad/s (f = {f_exc} Hz)")
print(f"  Frecuencia natural maxima omega_n_max = {omega_n_max:.2f} rad/s")
print(f"  Frecuencia natural maxima f_n_max = {f_n_max:.2f} Hz")
print(f"  Rigidez maxima k_max = {k_max/1e3:.1f} kN/m ({k_max:,.0f} N/m)")
print()
print(f"  Ratio de frecuencias minimo beta_min = {beta_min:.3f}")
print(f"  Transmisibilidad de diseno TR = {TR_exact*100:.2f}%")
print()
print("  INTERPRETACION: Para lograr TR <= 5%, la frecuencia natural")
print(f"  del aislador debe ser como maximo {f_n_max:.1f} Hz, lo que")
print(f"  corresponde a una rigidez de {k_max/1e3:.1f} kN/m.")
print()
