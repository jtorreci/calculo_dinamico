#!/usr/bin/env python3
"""
Figura Problema 01: Esquema del hangar como sistema SDOF
=========================================================

Genera diagrama TikZ del hangar modelado como masa-resorte.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene
from structdraw.primitives import Bar, Mass, Spring, SupportFixed, Force

# =============================================================================
# CREAR ESCENA
# =============================================================================

scene = Scene(world_bounds=(0, 0, 8, 4))

# Muro de empotramiento (lado izquierdo) - usando barras
scene.add(Bar(name="wall_top", p0=(0.5, 3), p1=(0.5, 1), thickness=0.10))

# Resorte representando rigidez de columnas
scene.add(Spring(
    p0=(0.5, 2),
    p1=(4.0, 2),
    n_coils=8,
    amplitude=0.2,
    label="k",
    style="helix",
    wire_diameter=0.15
))

# Masa concentrada (cubierta del hangar)
scene.add(Mass(
    at=(4.5, 2),
    size=(1.5, 1.0),
    label="m",
    kind="rounded",
    corner_radius=0.05,
    fill = "lightblue!30"
))

# Fuerza sísmica (opcional)
scene.add(Force(
    p0=(7, 2),
    p1=(5.5, 2),
    label="F(t)",
    arrow_style="stealth"
))

# Apoyo fijo (suelo)
scene.add(SupportFixed(at=(0.5, 2), angle_deg=90))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Guardar archivo
output_path = "../figs/fig_problema_01_hangar.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
print()
print("Código TikZ:")
print("-" * 40)
print(tikz_code)
