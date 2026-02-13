#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura Problema 02: Esquema SDOF con amortiguador
=================================================

Genera diagrama TikZ del sistema masa-resorte-amortiguador.
"""

import sys
sys.path.insert(0, '../../../Libreria_dibujo/structdraw_studio_v0_4_3c')

from structdraw import Scene
from structdraw.primitives import Mass, Spring, Damper, Force, SupportFixed, Voigt

# =============================================================================
# CREAR ESCENA - Modelo Voigt (resorte y amortiguador en paralelo)
# =============================================================================

scene = Scene(world_bounds=(0, 0, 8, 3))

# Usar el modelo Voigt que ya incluye resorte y amortiguador en paralelo
# Nuevos parámetros: spring_kwargs y damper_kwargs permiten modificar muelle y amortiguador
scene.add(Voigt(
    p0=(1, 1.5),
    p1=(4, 1.5),
    branch_sep=0.6,
    damper_fill="gray!20",
    damper_piston_fill="gray!40",
    # Modificadores del muelle (opcional)
    spring_kwargs={
        'straight_ends': 0.15,  # longitud de líneas rectas en extremos
        'style': "helix",
        'n_coils': 8,
    },
    # Modificadores del amortiguador (opcional)
    damper_kwargs={
        'piston_thickness': 0.12,  # grosor del émbolo (más visible)
        'end_extend': 0.10,        # líneas de extensión en extremos
        'rod_width': 0.04,         # grosor del vástago
        'rod_penetration': 0.10,   # penetración del vástago en el émbolo
    }
))

# Masa concentrada
scene.add(Mass(
    at=(4.5, 1.5),
    size=(1.0, 0.8),
    kind="rect",
    label="m"
))

# Fuerza armonica
scene.add(Force(
    p0=(7.5, 1.5),
    p1=(6, 1.5),
    label="P(t)",
    arrow_style="stealth"
))

# Muro izquierdo (empotramiento)
scene.add(SupportFixed(at=(1, 1.5), angle_deg=-90))

# =============================================================================
# EXPORTAR A TIKZ
# =============================================================================

tikz_code = scene.to_tikz()

# Guardar archivo
output_path = "../figs/fig_problema_02_sdof_amortiguado.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(tikz_code)

print(f"Figura generada: {output_path}")
