#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 01: Determinacion de Propiedades Fundamentales (SDOF)
==============================================================

Hangar para aeronaves modelado como SDOF.
Calcula masa, frecuencia natural y periodo.

Ejecutar: python problema_01_propiedades_sdof.py
"""

import numpy as np

# =============================================================================
# DATOS DEL PROBLEMA
# =============================================================================

W = 25_000  # kN - Peso de la cubierta
k = 15_000  # kN/m - Rigidez lateral
g = 9.81    # m/s^2 - Aceleracion de la gravedad

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 60)
print("PROBLEMA 01: PROPIEDADES FUNDAMENTALES SDOF - HANGAR")
print("=" * 60)
print()

# Conversion de unidades
W_N = W * 1e3  # N
k_Nm = k * 1e3  # N/m

print("Datos del problema:")
print(f"  Peso cubierta W = {W:,} kN = {W_N:,.0f} N")
print(f"  Rigidez lateral k = {k:,} kN/m = {k_Nm:,.0f} N/m")
print()

# 1. Masa concentrada
m = W_N / g
print("1. Masa concentrada:")
print(f"   m = W/g = {W_N:,.0f} / {g} = {m:,.0f} kg")
print(f"   m = {m/1e6:.3f} x 10^6 kg")
print()

# 2. Frecuencia circular natural
omega_n = np.sqrt(k_Nm / m)
print("2. Frecuencia circular natural:")
print(f"   omega_n = sqrt(k/m) = sqrt({k_Nm:,.0f} / {m:,.0f})")
print(f"   omega_n = sqrt({k_Nm/m:.4f}) = {omega_n:.3f} rad/s")
print()

# 3. Periodo natural
T_n = 2 * np.pi / omega_n
f_n = omega_n / (2 * np.pi)
print("3. Periodo y frecuencia natural:")
print(f"   T_n = 2*pi/omega_n = 2*pi/{omega_n:.3f} = {T_n:.3f} s")
print(f"   f_n = 1/T_n = {f_n:.3f} Hz")
print()

# =============================================================================
# RESUMEN
# =============================================================================

print("=" * 60)
print("RESUMEN DE RESULTADOS")
print("=" * 60)
print(f"  Masa:                m = {m:,.0f} kg ({m/1e6:.2f} t)")
print(f"  Frecuencia angular:  omega_n = {omega_n:.3f} rad/s")
print(f"  Frecuencia:          f_n = {f_n:.3f} Hz")
print(f"  Periodo:             T_n = {T_n:.3f} s")
print()

# =============================================================================
# INTERPRETACION FISICA
# =============================================================================

print("INTERPRETACION FISICA:")
print("-" * 40)
print(f"  El hangar oscila con un periodo de {T_n:.2f} segundos,")
print(f"  lo que corresponde a {f_n:.2f} ciclos por segundo.")
print()
print(f"  Este periodo relativamente largo ({T_n:.1f} s > 1 s) es tipico")
print(f"  de estructuras flexibles con grandes masas concentradas.")
print()

# Clasificacion sismica aproximada
if T_n < 0.5:
    clasificacion = "rigida (T < 0.5 s)"
elif T_n < 1.0:
    clasificacion = "moderadamente flexible (0.5 s < T < 1.0 s)"
elif T_n < 2.0:
    clasificacion = "flexible (1.0 s < T < 2.0 s)"
else:
    clasificacion = "muy flexible (T > 2.0 s)"

print(f"  Clasificacion sismica: Estructura {clasificacion}")
