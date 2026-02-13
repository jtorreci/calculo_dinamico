#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 13: Estructura con atirantamiento para control de periodo
=========================================================================

Genera diagrama TikZ mostrando estructura original y con atirantamiento.
Muestra el concepto de rigidez adicional (Delta k).
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene, Bar, Mass, Spring, Force
from structdraw.primitives import SupportFixed

# =============================================================================
# CREAR ESCENA - Dos esquemas lado a lado
# =============================================================================

scene = Scene(world_bounds=(0, 0, 14, 5))

# --- ESQUEMA IZQUIERDO: Estructura original ---

# Suelo
#scene.add(Bar(name="suelo_izq", p0=(0.5, 1), p1=(4.5, 1), thickness=0.05))


# Apoyo fijo (suelo)
scene.add(SupportFixed(at=(2.5, 1), angle_deg=0))

# Columna (rigidez original k_actual)
scene.add(Bar(name="columna_izq", p0=(2.5, 1), p1=(2.5, 3), thickness=0.1))
scene.add(Spring(
    p0=(2.5, 1.5),
    p1=(2.5, 2.5),
    n_coils=4,
    amplitude=0.2,
    label=r"k_{\text{actual}}",
    label_offset=(0.75, 0.0),
    style="helix"
))

# Masa
scene.add(Mass(
    at=(2.5, 3.4),
    size=(2.0, 0.8),
    kind="rect",
    label="m"
))

# Titulo
# (se agregara manualmente en tikz)

# --- ESQUEMA DERECHO: Con atirantamiento ---

# Suelo
#scene.add(Bar(name="suelo_der", p0=(8.5, 1), p1=(13.5, 1), thickness=0.05))

# Apoyo fijo (suelo)
scene.add(SupportFixed(at=(10, 1), angle_deg=0))
scene.add(SupportFixed(at=(12, 1), angle_deg=0))
scene.add(SupportFixed(at=(8, 1), angle_deg=0))

# Rigidez original (resorte principal)
scene.add(Bar(name="columna_der", p0=(10, 1), p1=(10, 3), thickness=0.1))
scene.add(Spring(
    p0=(10, 1.5),
    p1=(10, 2.5),
    n_coils=4,
    amplitude=0.2,
    label=r"k_{\text{actual}}",
    label_offset=(0.75, -0.5),
    style="helix"
))

# Rigidez adicional (atirantamiento - segundo resorte en paralelo)

scene.add(Spring(
    p0=(12, 1),
    p1=(10, 3),
    n_coils=10,
    amplitude=0.15,
    label=r"\Delta k",
    fill="orange!30",
    style="helix"
))


scene.add(Spring(
    p0=(8, 1),
    p1=(10, 3),
    n_coils=10,
    amplitude=0.15,
    label=r"\Delta k",
    fill="orange!30",
    style="helix"
))

# Masa (conectada a ambos resortes)
scene.add(Mass(
    at=(10, 3.4),
    size=(2.0, 0.8),
    kind="rect",
    label="m"
))

# Flecha indicando desplazamiento
scene.add(Force(
    p0=(11.5, 3.4),
    p1=(12.3, 3.4),
    label="u(t)",
    arrow_style="stealth"
))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Agregar titulos y anotaciones
tikz_code = tikz_code.replace(
    r'\end{tikzpicture}',
    r'''  % Titulos
  \node[font=\small] at (2.5, 0.4) {Original: $T = 1.8$ s};
  \node[font=\small] at (11, 0.4) {Con atirantamiento: $T = 1.0$ s};

  % Flecha de transicion
  \draw[->, thick, dashed] (5, 2.5) -- (7.5, 2.5) node[midway, above, font=\footnotesize] {Refuerzo};
\end{tikzpicture}'''
)

# Guardar archivo
output_path = "../figs/fig_problema_13_atirantamiento.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
