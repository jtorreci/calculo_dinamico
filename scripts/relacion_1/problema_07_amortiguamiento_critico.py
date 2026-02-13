#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 07: Amortiguamiento Critico de un Sistema SDOF
========================================================

Amortiguador industrial para maquina vibratoria.
Compara respuestas sub/critico/sobreamortiguado.

Ejecutar: python problema_07_amortiguamiento_critico.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

m = 200        # kg - Masa
omega_n = 50   # rad/s - Frecuencia natural
c_real = 10_000  # N*s/m - Amortiguador instalado por error

# Condiciones iniciales para grafico
u0 = 0.01      # m - Desplazamiento inicial (10 mm)
v0 = 0.0       # m/s - Velocidad inicial

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 60)
print("PROBLEMA 07: AMORTIGUAMIENTO CRITICO - MAQUINA INDUSTRIAL")
print("=" * 60)
print()

print("Datos del problema:")
print(f"  m = {m} kg")
print(f"  omega_n = {omega_n} rad/s")
print()

# 1. Rigidez necesaria
k = m * omega_n**2
print("1. Rigidez del resorte:")
print(f"   k = m * omega_n^2")
print(f"   k = {m} * {omega_n}^2")
print(f"   k = {m} * {omega_n**2}")
print(f"   k = {k:,} N/m = {k/1000:.0f} kN/m")
print()

# 2. Amortiguamiento critico
c_c = 2 * m * omega_n
print("2. Coeficiente de amortiguamiento critico:")
print(f"   c_c = 2 * m * omega_n")
print(f"   c_c = 2 * {m} * {omega_n}")
print(f"   c_c = {c_c:,} N*s/m")
print()

# Verificacion alternativa
c_c_alt = 2 * np.sqrt(k * m)
print(f"   Verificacion: c_c = 2*sqrt(k*m) = 2*sqrt({k}*{m}) = {c_c_alt:,.0f} N*s/m")
print()

# 3. Error de fabricacion
zeta_real = c_real / c_c
print("3. Analisis con c_real = 10,000 N*s/m:")
print(f"   zeta_real = c_real / c_c")
print(f"   zeta_real = {c_real:,} / {c_c:,}")
print(f"   zeta_real = {zeta_real}")
print()

if zeta_real < 1:
    clasificacion = "SUBAMORTIGUADO"
    descripcion = "El sistema OSCILARA antes de alcanzar el equilibrio."
elif zeta_real == 1:
    clasificacion = "CRITICAMENTE AMORTIGUADO"
    descripcion = "El sistema retorna al equilibrio sin oscilar en tiempo minimo."
else:
    clasificacion = "SOBREAMORTIGUADO"
    descripcion = "El sistema retorna lentamente sin oscilar."

print(f"   Como zeta = {zeta_real} {'<' if zeta_real < 1 else '>' if zeta_real > 1 else '='} 1:")
print(f"   El sistema es {clasificacion}")
print(f"   {descripcion}")
print()

# =============================================================================
# GRAFICO COMPARATIVO
# =============================================================================

# Tiempo de simulacion (5 periodos no amortiguados)
T_n = 2 * np.pi / omega_n
t = np.linspace(0, 5 * T_n, 1000)

def respuesta_subamortiguada(t, u0, v0, omega_n, zeta):
    omega_d = omega_n * np.sqrt(1 - zeta**2)
    A = u0
    B = (v0 + zeta * omega_n * u0) / omega_d
    return np.exp(-zeta * omega_n * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))

def respuesta_critica(t, u0, v0, omega_n):
    return np.exp(-omega_n * t) * (u0 + (v0 + omega_n * u0) * t)

def respuesta_sobreamortiguada(t, u0, v0, omega_n, zeta):
    sqrt_term = np.sqrt(zeta**2 - 1)
    r1 = -omega_n * (zeta + sqrt_term)
    r2 = -omega_n * (zeta - sqrt_term)
    A = (v0 - r2 * u0) / (r1 - r2)
    B = (r1 * u0 - v0) / (r1 - r2)
    return A * np.exp(r1 * t) + B * np.exp(r2 * t)

# Casos a comparar
casos = [
    (0.5, 'Subamortiguado ($\\zeta$ = 0.5)', 'b-'),
    (1.0, 'Critico ($\\zeta$ = 1.0)', 'r-'),
    (2.0, 'Sobreamortiguado ($\\zeta$ = 2.0)', 'g-'),
]

# Crear figura
fig, ax = plt.subplots(figsize=(10, 6))

for zeta, label, style in casos:
    if zeta < 1:
        u = respuesta_subamortiguada(t, u0, v0, omega_n, zeta)
    elif zeta == 1:
        u = respuesta_critica(t, u0, v0, omega_n)
    else:
        u = respuesta_sobreamortiguada(t, u0, v0, omega_n, zeta)

    ax.plot(t * 1000, u * 1000, style, linewidth=2, label=label)

ax.set_xlabel('Tiempo (ms)', fontsize=11)
ax.set_ylabel('Desplazamiento (mm)', fontsize=11)
ax.set_title('Comparacion de Regimenes de Amortiguamiento', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.set_xlim(0, t[-1] * 1000)

# Anotaciones
ax.annotate('Oscilaciones\ndecrecientes', xy=(150, 5), fontsize=9, ha='center', color='blue')
ax.annotate('Retorno\noptimo', xy=(80, 2), fontsize=9, ha='center', color='red')
ax.annotate('Retorno\nlento', xy=(300, 3), fontsize=9, ha='center', color='green')

plt.tight_layout()

output_path = "../figs/fig_problema_07_comparacion_zeta.pdf"
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
print(f"  Rigidez necesaria:        k = {k/1000:.0f} kN/m")
print(f"  Amortiguamiento critico:  c_c = {c_c:,} N*s/m")
print(f"  Amortiguamiento real:     c = {c_real:,} N*s/m")
print(f"  Razon de amortiguamiento: zeta = {zeta_real}")
print(f"  Clasificacion: {clasificacion}")
