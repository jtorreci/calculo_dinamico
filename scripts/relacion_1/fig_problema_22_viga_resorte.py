#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 22: Viga en voladizo con resorte en paralelo
============================================================

Genera diagrama TikZ de plataforma de laboratorio con viga cantilever
y resorte helicoidal actuando en paralelo.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene, Bar, Mass, Spring, Force
from structdraw.primitives import SupportFixed

# =============================================================================
# CREAR ESCENA
# =============================================================================

scene = Scene(world_bounds=(0, 0, 12, 6))

# Muro de empotramiento (lado izquierdo)
#scene.add(Bar(name="wall", p0=(1, 4.5), p1=(1, 1.5), thickness=0.15))
scene.add(SupportFixed(at=(1, 3), angle_deg=-90))
scene.add(SupportFixed(at=(8, 1.5), angle_deg=0))
# Sombreado del empotramiento
# for i in range(6):
#     y_base = 1.7 + i * 0.5
#     scene.add(Bar(name=f"hatch_{i}", p0=(0.3, y_base), p1=(1, y_base + 0.35), thickness=0.02))

# Viga en voladizo (representa k_viga)
scene.add(Bar(name="viga", p0=(1, 3), p1=(8, 3), thickness=0.12))

# Resorte helicoidal en paralelo (debajo de la viga)
scene.add(Spring(
    p0=(8, 1.5),
    p1=(8, 2.5),
    n_coils=4,
    amplitude=0.25,
    label=r"k_{\text{resorte}}",
    label_offset=(0.75, 0.0),
    style="helix"
))

# Conexion vertical del resorte al extremo de la viga
scene.add(Bar(name="conector", p0=(8, 1.5), p1=(8, 2.5), thickness=0.04))

# Masa concentrada en el extremo (equipo de laboratorio)
scene.add(Mass(
    at=(8, 3),
    size=(2.0, 1.0),
    kind="rect",
    label="W"
))

# Flecha indicando desplazamiento vertical
scene.add(Force(
    p0=(8, 3.5),
    p1=(8, 4.25),
    label="u(t)",
    arrow_style="stealth"
))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Agregar anotaciones
tikz_code = tikz_code.replace(
    r'\end{tikzpicture}',
    r'''  % Anotaciones
  \node[font=\small] at (4.5, 3.5) {Viga ($k_{viga}$)};
  \node[font=\footnotesize] at (4.5, 0.8) {$k_{eq} = k_{viga} + k_{resorte}$};

  % Cota L
  \draw[|<->|] (1, 5) -- (8, 5) node[midway, above, font=\small] {$L$};
\end{tikzpicture}'''
)

# Guardar archivo
output_path = "../figs/fig_problema_22_viga_resorte.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
