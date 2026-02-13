#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 10: Pasarela en voladizo con masa en el extremo
===============================================================

Genera diagrama TikZ de viga en voladizo (cantilever) con masa concentrada.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene, Bar, Mass, Force
from structdraw.primitives import SupportFixed

# =============================================================================
# CREAR ESCENA
# =============================================================================

scene = Scene(world_bounds=(0, 0, 10, 5))

# # Muro de empotramiento (lado izquierdo)
# scene.add(Bar(name="wall", p0=(1, 3.5), p1=(1, 1.5), thickness=0.12))

# # Sombreado del empotramiento (lineas diagonales simuladas con barras finas)
# for i in range(5):
#     y_base = 1.7 + i * 0.4
#     scene.add(Bar(name=f"hatch_{i}", p0=(0.5, y_base), p1=(1, y_base + 0.3), thickness=0.02))

# Apoyo fijo (suelo)
scene.add(SupportFixed(at=(1, 2.5), angle_deg=-90))

# Viga en voladizo
scene.add(Bar(name="viga", p0=(1, 2.5), p1=(8, 2.5), thickness=0.08))

# Masa concentrada en el extremo libre
scene.add(Mass(
    at=(8.5, 2.5),
    size=(1.0, 0.8),
    kind="rect",
    label="m"
))

# Flecha indicando desplazamiento vertical
scene.add(Force(
    p0=(8.5, 1.5),
    p1=(8.5, 2.0),
    label="u(t)",
    arrow_style="stealth"
))

# Lineas de cota para L
scene.add(Bar(name="cota_izq", p0=(1, 1.0), p1=(1, 1.4), thickness=0.02))
scene.add(Bar(name="cota_der", p0=(8, 1.0), p1=(8, 1.4), thickness=0.02))
scene.add(Bar(name="cota_L", p0=(1, 1.2), p1=(8, 1.2), thickness=0.02))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Agregar anotacion de L manualmente
tikz_code = tikz_code.replace(
    r'\end{tikzpicture}',
    r'  \node at (4.5, 0.7) {$L$};' + '\n' + r'\end{tikzpicture}'
)

# Guardar archivo
output_path = "../figs/fig_problema_10_voladizo.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
