# -*- coding: utf-8 -*-
"""
Librería Dinámica - Herramientas para Cálculo Dinámico de Estructuras
=====================================================================

Módulos disponibles:
- sdof: Sistemas de un grado de libertad (SDOF)
- mdof: Sistemas de múltiples grados de libertad (MDOF)
- tmd: Absorbedores de masa sintonizada (TMD)
- integracion: Métodos de integración numérica (Newmark, diferencias centrales)
- frecuencial: Análisis en el dominio de la frecuencia
- utils: Utilidades, gráficas y visualización de modos
"""

from .sdof import SDOF
from .mdof import (MDOF, shear_building, shear_building_uniforme,
                   frecuencias_shear_uniforme, modos_shear_uniforme,
                   condensacion_guyan, amortiguamiento_rayleigh, newmark_mdof,
                   # Combinación modal
                   combinacion_srss, combinacion_cqc, coeficiente_cqc,
                   matriz_correlacion_cqc, comparar_srss_cqc)
from .tmd import (TMDOptimo, den_hartog, warburton, frf_con_tmd,
                  comparar_con_sin_tmd, tabla_diseno_tmd, diseno_tmd_edificio)
from .integracion import newmark, diferencias_centrales, duhamel
from .frecuencial import frf_receptancia, frf_movilidad, frf_acelerancia, espectro_respuesta
from .utils import (configurar_graficas,
                    # Visualización de modos
                    graficar_modos_edificio, graficar_respuesta_modal,
                    graficar_frf_mdof, graficar_matriz_correlacion,
                    graficar_espectro_respuesta)

__version__ = '1.2.0'
__author__ = 'Cálculo Dinámico de Estructuras'

__all__ = [
    # SDOF
    'SDOF',
    # MDOF
    'MDOF',
    'shear_building',
    'shear_building_uniforme',
    'frecuencias_shear_uniforme',
    'modos_shear_uniforme',
    'condensacion_guyan',
    'amortiguamiento_rayleigh',
    'newmark_mdof',
    # Combinación modal (SRSS/CQC)
    'combinacion_srss',
    'combinacion_cqc',
    'coeficiente_cqc',
    'matriz_correlacion_cqc',
    'comparar_srss_cqc',
    # TMD (Den Hartog)
    'TMDOptimo',
    'den_hartog',
    'warburton',
    'frf_con_tmd',
    'comparar_con_sin_tmd',
    'tabla_diseno_tmd',
    'diseno_tmd_edificio',
    # Integración
    'newmark',
    'diferencias_centrales',
    'duhamel',
    # Frecuencial
    'frf_receptancia',
    'frf_movilidad',
    'frf_acelerancia',
    'espectro_respuesta',
    # Utils y Visualización
    'configurar_graficas',
    'graficar_modos_edificio',
    'graficar_respuesta_modal',
    'graficar_frf_mdof',
    'graficar_matriz_correlacion',
    'graficar_espectro_respuesta'
]
