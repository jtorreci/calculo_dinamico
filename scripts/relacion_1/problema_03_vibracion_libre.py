#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 03: Analisis de Vibracion Libre (Caso Subamortiguado)
==============================================================

Pilar de puente con amortiguamiento subcritico.
Calcula propiedades dinamicas y genera grafico de respuesta.

Ejecutar: python problema_03_vibracion_libre.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

T_n = 0.80   # s - Periodo natural no amortiguado
zeta = 0.02  # Razon de amortiguamiento (2%)

# Condiciones iniciales para la grafica
u0 = 0.05    # m - Desplazamiento inicial (50 mm)
v0 = 0.0     # m/s - Velocidad inicial

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 60)
print("PROBLEMA 03: VIBRACION LIBRE SUBAMORTIGUADA")
print("=" * 60)
print()

print("Datos del problema:")
print(f"  Periodo natural T_n = {T_n} s")
print(f"  Razon de amortiguamiento zeta = {zeta} ({zeta*100:.0f}%)")
print()

# 1. Frecuencia circular natural
omega_n = 2 * np.pi / T_n
f_n = 1 / T_n
print("1. Frecuencia circular natural no amortiguada:")
print(f"   omega_n = 2*pi/T_n = 2*pi/{T_n}")
print(f"   omega_n = {omega_n:.3f} rad/s")
print(f"   f_n = {f_n:.3f} Hz")
print()

# 2. Frecuencia amortiguada
omega_d = omega_n * np.sqrt(1 - zeta**2)
print("2. Frecuencia circular amortiguada:")
print(f"   omega_d = omega_n * sqrt(1 - zeta^2)")
print(f"   omega_d = {omega_n:.3f} * sqrt(1 - {zeta}^2)")
print(f"   omega_d = {omega_n:.3f} * sqrt({1 - zeta**2:.6f})")
print(f"   omega_d = {omega_d:.3f} rad/s")
print()

# 3. Periodo amortiguado
T_d = 2 * np.pi / omega_d
f_d = omega_d / (2 * np.pi)
print("3. Periodo de vibracion amortiguada:")
print(f"   T_d = 2*pi/omega_d = 2*pi/{omega_d:.3f}")
print(f"   T_d = {T_d:.4f} s")
print(f"   f_d = {f_d:.4f} Hz")
print()

# Diferencia porcentual
diff_T = (T_d - T_n) / T_n * 100
diff_f = (omega_d - omega_n) / omega_n * 100
print(f"   Diferencia T_d vs T_n: {diff_T:.4f}%")
print(f"   Diferencia omega_d vs omega_n: {diff_f:.4f}%")
print()

# 4. Clasificacion
print("4. Clasificacion del sistema:")
if zeta < 1:
    print(f"   Como 0 < zeta = {zeta} < 1, el sistema es SUBAMORTIGUADO")
    print("   El sistema oscila con amplitud decreciente.")
elif zeta == 1:
    print(f"   Como zeta = {zeta} = 1, el sistema es CRITICAMENTE AMORTIGUADO")
elif zeta > 1:
    print(f"   Como zeta = {zeta} > 1, el sistema es SOBREAMORTIGUADO")
print()

# =============================================================================
# GRAFICO DE VIBRACION LIBRE
# =============================================================================

# Tiempo de simulacion (10 periodos)
t = np.linspace(0, 10 * T_d, 1000)

# Respuesta libre amortiguada: u(t) = e^(-zeta*omega_n*t) * (A*cos(omega_d*t) + B*sin(omega_d*t))
# Con u(0) = u0 y v(0) = v0:
A = u0
B = (v0 + zeta * omega_n * u0) / omega_d

envelope = np.exp(-zeta * omega_n * t)
u = envelope * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))

# Envolvente
env_pos = u0 * np.exp(-zeta * omega_n * t)
env_neg = -u0 * np.exp(-zeta * omega_n * t)

# Crear figura
fig, ax = plt.subplots(figsize=(10, 5))

# Respuesta
ax.plot(t, u * 1000, 'b-', linewidth=1.5, label='Respuesta u(t)')

# Envolventes
ax.plot(t, env_pos * 1000, 'r--', linewidth=1, alpha=0.7,
        label=f'Envolvente $\\pm u_0 e^{{-\\zeta\\omega_n t}}$')
ax.plot(t, env_neg * 1000, 'r--', linewidth=1, alpha=0.7)

# Configuracion
ax.set_xlabel('Tiempo (s)', fontsize=11)
ax.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax.set_title(f'Vibracion Libre Subamortiguada ($\\zeta$ = {zeta*100:.0f}%, $T_n$ = {T_n} s)',
             fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)
ax.axhline(y=0, color='k', linewidth=0.5)

# Anotaciones
ax.annotate(f'$T_d$ = {T_d:.3f} s', xy=(T_d, u0*1000*0.8),
            fontsize=10, ha='center')

# Marcar picos
picos_t = []
picos_u = []
for i in range(1, len(t)-1):
    if u[i] > u[i-1] and u[i] > u[i+1] and u[i] > 0.001 * u0:
        picos_t.append(t[i])
        picos_u.append(u[i])

ax.plot(picos_t[:5], np.array(picos_u[:5])*1000, 'go', markersize=5,
        label='Picos', zorder=5)

plt.tight_layout()

# Guardar figura
output_path = "../figs/fig_problema_03_vibracion_libre.pdf"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Figura guardada: {output_path}")
plt.close()

# =============================================================================
# RESUMEN
# =============================================================================

print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"  omega_n = {omega_n:.3f} rad/s")
print(f"  omega_d = {omega_d:.3f} rad/s")
print(f"  T_n = {T_n:.4f} s")
print(f"  T_d = {T_d:.4f} s")
print(f"  Clasificacion: Subamortiguado (zeta = {zeta*100:.0f}%)")
print()
print("NOTA: Para amortiguamientos bajos (zeta < 20%), la diferencia")
print(f"      entre T_d y T_n es despreciable ({abs(diff_T):.2f}%).")
