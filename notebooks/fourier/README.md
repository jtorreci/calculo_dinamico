# Análisis de Fourier paso a paso

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jtorreci/calculo_dinamico/blob/main/notebooks/fourier/fourier_paso_a_paso.ipynb)

Cuaderno de la sesión de introducción al análisis de Fourier en el cálculo dinámico de estructuras. Reproduce, paso a paso, la [página interactiva](https://jtorreci.github.io/calculo_dinamico/fourier/): las integrales de los coeficientes, un seno, una suma de senos, una señal pseudoaleatoria, su reconstrucción con un número creciente de armónicos y la equivalencia con la FFT.

## Ficheros

| Fichero | Contenido |
|---|---|
| `fourier_paso_a_paso.ipynb` | Cuaderno con la explicación, las figuras y los ejercicios propuestos. |
| `fourier.py` | Código reutilizable en tres capas: *1. CÁLCULO* (funciones puras), *2. PROCESO* (casos y barridos) y *3. DIBUJO* (solo gráficas). |
| `test_fourier.py` | Comprobaciones con pytest. |
| `verificacion.json` | Cifras de control que genera el cuaderno (LCG, coeficientes y errores). |
| `datos/ElCentro.txt` | Acelerograma de El Centro 1940, componente N-S, en g con Δt = 0,02 s (ejercicio 4). |

## Ejecución local

Se necesita Python 3.10 o posterior. Las dependencias se instalan con:

```bash
pip install numpy scipy matplotlib jupyter
pip install ipywidgets        # opcional: deslizador del paso 4
```

El cuaderno se abre desde esta carpeta, de modo que `fourier.py` y `datos/` queden junto a él:

```bash
jupyter notebook fourier_paso_a_paso.ipynb
```

Los parámetros se cambian en la celda «DATOS — modifique aquí» y después se ejecutan de nuevo todas las celdas. Sin `ipywidgets` el cuaderno funciona igual, porque la celda del deslizador dibuja entonces una lista fija de valores.

Las comprobaciones se ejecutan con `python -m pytest -q test_fourier.py`.

## Ejecución en Colab

En Google Colab el cuaderno se abre con el botón superior. Dado que Colab solo carga el fichero `.ipynb`, antes de ejecutarlo hay que subir `fourier.py` y la carpeta `datos/` al directorio de trabajo de la sesión.
