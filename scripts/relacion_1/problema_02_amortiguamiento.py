#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema 02: Calculo de Amortiguamiento y Ecuacion de Movimiento
================================================================

Continuacion del Problema 01 - Hangar con amortiguamiento viscoso.
Calcula c_c, c, y formula la ecuacion de movimiento.

Ejecutar: python problema_02_amortiguamiento.py
"""

import numpy as np

# =============================================================================
# DATOS DEL PROBLEMA (del Problema 01)
# =============================================================================

W = 25_000  # kN - Peso de la cubierta
k = 15_000  # kN/m - Rigidez lateral
g = 9.81    # m/s^2

# Datos nuevos
zeta = 0.05  # Razon de amortiguamiento (5%)
P0 = 500     # kN - Amplitud de la carga de viento
omega_f = 10 # rad/s - Frecuencia de la carga

# =============================================================================
# SOLUCION
# =============================================================================

print("=" * 60)
print("PROBLEMA 02: AMORTIGUAMIENTO Y ECUACION DE MOVIMIENTO")
print("=" * 60)
print()

# Conversion de unidades
W_N = W * 1e3  # N
k_Nm = k * 1e3  # N/m
P0_N = P0 * 1e3  # N

# Valores del Problema 01
m = W_N / g
omega_n = np.sqrt(k_Nm / m)

print("Datos del Problema 01:")
print(f"  m = {m:,.0f} kg")
print(f"  k = {k_Nm:,.0f} N/m")
print(f"  omega_n = {omega_n:.3f} rad/s")
print()

print("Datos nuevos:")
print(f"  zeta = {zeta} ({zeta*100:.0f}%)")
print(f"  P(t) = {P0} sin({omega_f}t) kN")
print()

# 1. Amortiguamiento critico
c_c = 2 * m * omega_n
print("1. Coeficiente de amortiguamiento critico:")
print(f"   c_c = 2 * m * omega_n")
print(f"   c_c = 2 * {m:,.0f} * {omega_n:.3f}")
print(f"   c_c = {c_c:,.0f} N*s/m")
print(f"   c_c = {c_c/1e6:.3f} MN*s/m")
print()

# 2. Amortiguamiento real
c = zeta * c_c
print("2. Coeficiente de amortiguamiento real:")
print(f"   c = zeta * c_c")
print(f"   c = {zeta} * {c_c:,.0f}")
print(f"   c = {c:,.0f} N*s/m")
print(f"   c = {c/1e3:.1f} kN*s/m")
print()

# 3. Ecuacion de movimiento
print("3. Ecuacion diferencial del movimiento:")
print()
print("   Forma general: m*u'' + c*u' + k*u = P(t)")
print()
print("   Sustituyendo valores:")
print(f"   {m:,.0f} u''(t) + {c:,.0f} u'(t) + {k_Nm:,.0f} u(t) = {P0_N:,.0f} sin({omega_f}t)")
print()

# Forma normalizada
print("   Forma normalizada (dividiendo por m):")
print(f"   u'' + {2*zeta*omega_n:.3f} u' + {omega_n**2:.3f} u = {P0_N/m:.3f} sin({omega_f}t)")
print()

# =============================================================================
# ANALISIS ADICIONAL
# =============================================================================

print("=" * 60)
print("ANALISIS ADICIONAL")
print("=" * 60)
print()

# Relacion de frecuencias
beta = omega_f / omega_n
print(f"Relacion de frecuencias beta = omega_f/omega_n = {omega_f}/{omega_n:.3f} = {beta:.3f}")
print()

if beta < 1:
    print(f"  beta < 1: La frecuencia de excitacion es MENOR que la natural.")
    print(f"  El sistema esta en la zona pre-resonancia.")
elif beta > 1:
    print(f"  beta > 1: La frecuencia de excitacion es MAYOR que la natural.")
    print(f"  El sistema esta en la zona post-resonancia.")
else:
    print(f"  beta = 1: RESONANCIA! La frecuencia de excitacion coincide con la natural.")

print()

# Factor de amplificacion dinamica
H = 1 / np.sqrt((1 - beta**2)**2 + (2*zeta*beta)**2)
print(f"Factor de amplificacion dinamica:")
print(f"  H(beta) = 1/sqrt((1-beta^2)^2 + (2*zeta*beta)^2)")
print(f"  H({beta:.3f}) = {H:.3f}")
print()

# Desplazamiento estatico y dinamico
u_st = P0_N / k_Nm
u_max = u_st * H
print(f"Desplazamiento estatico: u_st = P0/k = {u_st*1000:.2f} mm")
print(f"Amplitud dinamica max:   u_max = u_st * H = {u_max*1000:.2f} mm")

# =============================================================================
# RESUMEN
# =============================================================================

print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"  Amortiguamiento critico:  c_c = {c_c/1e6:.3f} MN*s/m")
print(f"  Amortiguamiento real:     c = {c/1e3:.1f} kN*s/m")
print(f"  Razon de amortiguamiento: zeta = {zeta*100:.1f}%")
print(f"  Factor amplificacion:     H = {H:.3f}")
