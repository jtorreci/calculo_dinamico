#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 06: Pasarela simplemente apoyada con masa concentrada
======================================================================

Genera diagrama TikZ de viga simplemente apoyada con masa en el centro.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene, Bar, Mass, SupportPinned, SupportRoller, Force

# =============================================================================
# CREAR ESCENA
# =============================================================================

scene = Scene(world_bounds=(0, 0, 10, 4))

# Viga (pasarela)
scene.add(Bar(name="viga", p0=(1, 2), p1=(9, 2), thickness=0.08))

# Apoyos
scene.add(SupportPinned(at=(1, 2), angle_deg=0))
scene.add(SupportRoller(at=(9, 2), angle_deg=0))

# Masa concentrada en el centro
scene.add(Mass(
    at=(5, 2.0),
    size=(1.2, 0.8),
    kind="rect",
    label="M"
))

# Flecha indicando desplazamiento vertical
scene.add(Force(
    p0=(5, 0.8),
    p1=(5, 1.5),
    label="u(t)",
    arrow_style="stealth"
))

# Anotaciones de dimensiones usando barras auxiliares
# Linea de cota L
scene.add(Bar(name="cota_izq", p0=(1, 0.4), p1=(1, 0.8), thickness=0.02))
scene.add(Bar(name="cota_der", p0=(9, 0.4), p1=(9, 0.8), thickness=0.02))
scene.add(Bar(name="cota_L", p0=(1, 0.6), p1=(9, 0.6), thickness=0.02))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Agregar anotacion de L manualmente
tikz_code = tikz_code.replace(
    r'\end{tikzpicture}',
    r'  \node at (5, 0.35) {$L$};' + '\n' + r'\end{tikzpicture}'
)

# Guardar archivo
output_path = "../figs/fig_problema_06_pasarela_apoyada.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
