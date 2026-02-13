#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 24: Portico de un nivel con dos columnas
=========================================================

Genera diagrama TikZ de marco rigido con columnas empotradas
y viga infinitamente rigida en la parte superior.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene, Bar, Mass, Force
from structdraw.primitives import SupportFixed

# =============================================================================
# CREAR ESCENA
# =============================================================================

scene = Scene(world_bounds=(0, 0, 12, 7))

# --- CIMENTACION (empotramientos) ---
# Suelo izquierdo
#scene.add(Bar(name="suelo_izq", p0=(1.5, 1), p1=(3.5, 1), thickness=0.05))

scene.add(SupportFixed(at=(2.5, 1), angle_deg=0))
# Sombreado empotramiento izquierdo
# for i in range(4):
#     x_base = 1.7 + i * 0.4
#     scene.add(Bar(name=f"hatch_izq_{i}", p0=(x_base, 0.5), p1=(x_base + 0.25, 1), thickness=0.02))

# Suelo derecho
#scene.add(Bar(name="suelo_der", p0=(8.5, 1), p1=(10.5, 1), thickness=0.05))

scene.add(SupportFixed(at=(9.5, 1), angle_deg=0))
# Sombreado empotramiento derecho
# for i in range(4):
#     x_base = 8.7 + i * 0.4
#     scene.add(Bar(name=f"hatch_der_{i}", p0=(x_base, 0.5), p1=(x_base + 0.25, 1), thickness=0.02))

# --- COLUMNAS ---
# Columna izquierda
scene.add(Bar(name="col_izq", 
              p0=(2.5, 1), 
              p1=(2.5, 5), 
              thickness=0.15,
              show_axis=True,
              fill="red!20"))

# Columna derecha
scene.add(Bar(name="col_der", 
              p0=(9.5, 1), 
              p1=(9.5, 5), 
              thickness=0.15,
              show_axis=True,
              fill="red!20"))

# --- VIGA SUPERIOR (infinitamente rigida) ---
scene.add(Bar(name="viga", 
              p0=(2.5, 5),
              p1=(9.5, 5), 
              thickness=0.20,
              show_axis=True,
              fill="blue!20"))

# --- MASA EN LA VIGA ---
scene.add(Mass(
    at=(6, 5.0),
    size=(3.0, 0.6),
    kind="rect",
    label="m"
))

# --- FUERZA LATERAL ---
scene.add(Force(
    p0=(0.5, 5),
    p1=(2.0, 5),
    label="F(t)",
    arrow_style="stealth"
))

# --- FLECHA DE DESPLAZAMIENTO ---
scene.add(Force(
    p0=(10.5, 5),
    p1=(11.5, 5),
    label="u(t)",
    arrow_style="stealth"
))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Agregar anotaciones de dimensiones y rigidez
tikz_code = tikz_code.replace(
    r'\end{tikzpicture}',
    r'''  % Anotaciones
  % Altura h
  \draw[|<->|] (1, 1) -- (1, 5) node[midway, left, font=\small] {$h$};

  % Ancho entre columnas
  \draw[|<->|] (2.5, 0.3) -- (9.5, 0.3) node[midway, below, font=\small] {ancho};

  % Rigidez columnas
  \node[font=\footnotesize] at (2.5, 3) [left] {$k_c = \frac{12EI_c}{h^3}$};
  \node[font=\footnotesize] at (9.5, 3) [right] {$k_c$};

  % Rigidez total
  \node[font=\small] at (6, 6.8) {$k_{total} = 2 \cdot k_c$};
\end{tikzpicture}'''
)

# Guardar archivo
output_path = "../figs/fig_problema_24_portico.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
