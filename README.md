# Material Complementario: Calculo Dinamico de Estructuras

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18626756.svg)](https://doi.org/10.5281/zenodo.18626756)

Este repositorio contiene el material complementario del libro **"Calculo Avanzado de Estructuras: Calculo Dinamico"** y su **Libro de Problemas** para el Master de Ingenieria de Caminos.

| Publicacion | DOI |
|------------|-----|
| Libro de teoria | [10.5281/zenodo.18626756](https://doi.org/10.5281/zenodo.18626756) |
| Libro de problemas | [10.5281/zenodo.18626808](https://doi.org/10.5281/zenodo.18626808) |

## Estructura del Repositorio

```
github/
├── libreria_dinamica/    # Libreria Python para calculo dinamico
├── notebooks/            # Cuadernos Jupyter interactivos
├── scripts/              # Scripts Python de los problemas
│   ├── relacion_1/       # SDOF: Propiedades y vibracion libre
│   ├── relacion_2/       # SDOF: Respuesta forzada y metodos numericos
│   ├── relacion_3/       # MDOF: Sistemas de multiples grados de libertad
│   ├── relacion_4/       # Elementos continuos: vigas y placas
│   ├── relacion_5/       # Analisis sismico: espectros y normativa
│   └── relacion_6/       # Temas avanzados: no linealidad y control
└── presentaciones/       # Diapositivas del curso
```

## Libreria Dinamica

La carpeta `libreria_dinamica/` contiene una libreria Python modular para calculo dinamico estructural:

| Modulo | Descripcion |
|--------|-------------|
| `sdof.py` | Sistemas de 1 grado de libertad |
| `mdof.py` | Sistemas de multiples grados de libertad |
| `integracion.py` | Metodos de integracion temporal (Newmark, etc.) |
| `frecuencial.py` | Analisis en el dominio de la frecuencia |
| `tmd.py` | Amortiguadores de masa sintonizados (TMD) |
| `utils.py` | Funciones auxiliares y graficos |

### Instalacion

```bash
pip install numpy scipy matplotlib
```

### Uso basico

```python
from libreria_dinamica import SDOF, MDOF, shear_building

# Sistema SDOF
sistema = SDOF(m=1000, k=40000, zeta=0.05)
print(f"Frecuencia natural: {sistema.omega_n:.2f} rad/s")
print(f"Periodo: {sistema.T:.3f} s")

# Edificio de cortante 3 plantas
m = [1000, 1000, 1000]  # kg
k = [200e3, 200e3, 200e3]  # N/m
M, K = shear_building(m, k)
edificio = MDOF(M, K)
print(f"Frecuencias: {edificio.omega} rad/s")
```

## Scripts de Problemas

Cada relacion contiene scripts que resuelven los problemas del libro. Los scripts estan nombrados siguiendo el patron:

- `problema_XX_descripcion.py` - Solucion computacional del problema XX
- `fig_problema_XX_descripcion.py` - Generacion de figuras para el problema XX

### Ejemplo de ejecucion

```bash
cd scripts/relacion_1
python problema_01_propiedades_sdof.py
```

## Cuadernos Jupyter

Los notebooks proporcionan versiones interactivas de problemas seleccionados:

| Notebook | Tema |
|----------|------|
| `relacion_3_problema_01_edificio_2dof.ipynb` | Analisis modal edificio 2 plantas |
| `relacion_3_problema_21_cqc_srss.ipynb` | Combinacion modal CQC vs SRSS |
| `relacion_4_problema_01_voladizo.ipynb` | Vibracion de viga en voladizo |
| `relacion_5_problema_09_espectro_EC8.ipynb` | Espectro de respuesta EC8 |
| `relacion_5_problema_21_newmark.ipynb` | Integracion Newmark paso a paso |
| `relacion_6_problema_09_TMD.ipynb` | Diseno de TMD (Den Hartog) |

### Ejecucion

```bash
cd notebooks
jupyter notebook
```

## Presentaciones

La carpeta `presentaciones/` contiene las diapositivas del curso organizadas por temas:

- `pres01_*` - Introduccion a la dinamica estructural
- `pres02_*` - Sistemas de 1 grado de libertad (SDOF)
- `pres03_*` - Analisis en frecuencia
- `pres04_*` - Sistemas de multiples grados de libertad (MDOF)
- `pres05_*` - Elementos continuos
- `pres06_*` - Analisis sismico
- `pres07_*` - Temas avanzados

## Correspondencia con el Libro

| Relacion | Capitulos | Temas |
|----------|-----------|-------|
| 1 | 1-2 | Fundamentos SDOF, vibracion libre |
| 2 | 2-3 | Respuesta forzada, metodos numericos |
| 3 | 4-5 | Sistemas MDOF, analisis modal |
| 4 | 6 | Vigas, placas, elementos continuos |
| 5 | 7 | Analisis sismico, espectros, normativa |
| 6 | 8 | No linealidad, control de vibraciones |

## Requisitos

- Python >= 3.8
- NumPy >= 1.20
- SciPy >= 1.7
- Matplotlib >= 3.4
- Jupyter (opcional, para notebooks)

## Como citar

```bibtex
@book{torrecilla2025calculo,
  author    = {Torrecilla Pinero, Jesús},
  title     = {Cálculo Avanzado de Estructuras: Cálculo Dinámico},
  year      = {2025},
  publisher = {Universidad de Extremadura},
  doi       = {10.5281/zenodo.18626756}
}
```

## Licencia

Material docente bajo licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Contacto

Jesus Torrecilla Pinero
Escuela Politecnica de Caceres
Universidad de Extremadura
