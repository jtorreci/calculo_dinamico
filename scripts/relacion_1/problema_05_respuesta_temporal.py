#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 05: Respuesta Temporal en Vibracion Libre Amortiguada
==============================================================

Turbina eolica sometida a rafaga de viento.
Calcula respuesta temporal y desplazamiento a t=1.5s.

Ejecutar: python problema_05_respuesta_temporal.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 5_000       # kg - Masa
k = 200_000     # N/m - Rigidez
zeta = 0.10     # Razon de amortiguamiento (10%)
u0 = 0.5        # m - Desplazamiento inicial
v0 = 0.0        # m/s - Velocidad inicial
t_interes = 1.5 # s - Tiempo de interes

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 60)
print("PROBLEMA 05: RESPUESTA TEMPORAL - TURBINA EOLICA")
print("=" * 60)
print()

print("Datos del problema:")
print(f"  m = {m:,} kg")
print(f"  k = {k:,} N/m")
print(f"  zeta = {zeta} ({zeta*100:.0f}%)")
print(f"  u(0) = {u0} m")
print(f"  v(0) = {v0} m/s")
print(f"  t de interes = {t_interes} s")
print()

# 1. Calcular omega_n y omega_D
omega_n = np.sqrt(k / m)
omega_d = omega_n * np.sqrt(1 - zeta**2)

print("1. Frecuencias naturales:")
print(f"   omega_n = sqrt(k/m) = sqrt({k}/{m})")
print(f"   omega_n = sqrt({k/m:.1f}) = {omega_n:.3f} rad/s")
print()
print(f"   omega_d = omega_n * sqrt(1 - zeta^2)")
print(f"   omega_d = {omega_n:.3f} * sqrt(1 - {zeta}^2)")
print(f"   omega_d = {omega_n:.3f} * sqrt({1 - zeta**2:.4f})")
print(f"   omega_d = {omega_d:.3f} rad/s")
print()

# 2. Coeficientes A y B
A = u0
B = (v0 + zeta * omega_n * u0) / omega_d

print("2. Coeficientes de la solucion:")
print(f"   A = u(0) = {A} m")
print()
print(f"   B = (v(0) + zeta * omega_n * u(0)) / omega_d")
print(f"   B = ({v0} + {zeta} * {omega_n:.3f} * {u0}) / {omega_d:.3f}")
print(f"   B = ({v0} + {zeta * omega_n * u0:.4f}) / {omega_d:.3f}")
print(f"   B = {zeta * omega_n * u0:.4f} / {omega_d:.3f}")
print(f"   B = {B:.5f} m")
print()

# 3. Desplazamiento en t = 1.5 s
def respuesta_libre(t, u0, v0, omega_n, omega_d, zeta):
    """Respuesta de vibracion libre subamortiguada."""
    A = u0
    B = (v0 + zeta * omega_n * u0) / omega_d
    envelope = np.exp(-zeta * omega_n * t)
    u = envelope * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    return u

u_t = respuesta_libre(t_interes, u0, v0, omega_n, omega_d, zeta)

print("3. Desplazamiento en t = 1.5 s:")
print()
print("   u(t) = e^(-zeta*omega_n*t) * [A*cos(omega_d*t) + B*sin(omega_d*t)]")
print()
print(f"   Exponente: -zeta*omega_n*t = -{zeta}*{omega_n:.3f}*{t_interes}")
print(f"            = {-zeta*omega_n*t_interes:.5f}")
print(f"   e^(...) = {np.exp(-zeta*omega_n*t_interes):.5f}")
print()
print(f"   Argumento trig: omega_d*t = {omega_d:.3f}*{t_interes} = {omega_d*t_interes:.4f} rad")
print(f"   cos({omega_d*t_interes:.4f}) = {np.cos(omega_d*t_interes):.5f}")
print(f"   sin({omega_d*t_interes:.4f}) = {np.sin(omega_d*t_interes):.5f}")
print()
print(f"   Termino coseno: A*cos(...) = {A}*{np.cos(omega_d*t_interes):.5f} = {A*np.cos(omega_d*t_interes):.5f}")
print(f"   Termino seno:   B*sin(...) = {B:.5f}*{np.sin(omega_d*t_interes):.5f} = {B*np.sin(omega_d*t_interes):.5f}")
print(f"   Suma: {A*np.cos(omega_d*t_interes) + B*np.sin(omega_d*t_interes):.5f}")
print()
print(f"   u(1.5) = {np.exp(-zeta*omega_n*t_interes):.5f} * ({A*np.cos(omega_d*t_interes) + B*np.sin(omega_d*t_interes):.5f})")
print(f"   u(1.5) = {u_t:.5f} m = {u_t*100:.2f} cm")
print()

# =============================================================================
# GRAFICO
# =============================================================================

# Tiempo de simulacion
T_n = 2 * np.pi / omega_n
t = np.linspace(0, 5 * T_n, 500)
u = respuesta_libre(t, u0, v0, omega_n, omega_d, zeta)

# Envolvente
env_pos = u0 * np.exp(-zeta * omega_n * t)
env_neg = -u0 * np.exp(-zeta * omega_n * t)

# Crear figura
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(t, u * 100, 'b-', linewidth=1.5, label='Respuesta u(t)')
ax.plot(t, env_pos * 100, 'r--', linewidth=1, alpha=0.7, label='Envolvente')
ax.plot(t, env_neg * 100, 'r--', linewidth=1, alpha=0.7)

# Marcar punto de interes
ax.plot(t_interes, u_t * 100, 'go', markersize=10, label=f't = {t_interes} s', zorder=5)
ax.annotate(f'u({t_interes}) = {u_t*100:.1f} cm',
            xy=(t_interes, u_t*100), xytext=(t_interes+0.3, u_t*100+10),
            fontsize=10, arrowprops=dict(arrowstyle='->', color='green'))

ax.set_xlabel('Tiempo (s)', fontsize=11)
ax.set_ylabel('Desplazamiento (cm)', fontsize=11)
ax.set_title(f'Vibracion Libre - Turbina Eolica ($\\zeta$ = {zeta*100:.0f}%)', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)
ax.axhline(y=0, color='k', linewidth=0.5)

plt.tight_layout()

output_path = "../figs/fig_problema_05_turbina.pdf"
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
print(f"  T_n = {2*np.pi/omega_n:.3f} s")
print(f"  A = {A} m, B = {B:.5f} m")
print(f"  u(1.5 s) = {u_t:.4f} m = {u_t*100:.2f} cm")
print()
print("INTERPRETACION:")
print(f"  A los {t_interes} s, el desplazamiento es {abs(u_t)*100:.1f} cm")
print(f"  (en direccion {'positiva' if u_t > 0 else 'negativa'})")
