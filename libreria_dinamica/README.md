# Libreria Dinamica v1.2.0

Biblioteca Python para calculo dinamico de estructuras.

## Instalacion

```python
import sys
sys.path.insert(0, 'ruta/a/scripts')
from libreria_dinamica import *
```

## Modulos

| Modulo | Descripcion |
|--------|-------------|
| `sdof` | Sistemas de un grado de libertad |
| `mdof` | Sistemas MDOF y analisis modal |
| `tmd` | Absorbedores de masa sintonizada |
| `integracion` | Newmark, diferencias centrales, Duhamel |
| `frecuencial` | FRF, espectros de respuesta |
| `utils` | Graficas y visualizacion |

---

## Nuevas funcionalidades v1.2.0

### 1. Combinacion Modal SRSS/CQC

```python
from libreria_dinamica import combinacion_srss, combinacion_cqc, comparar_srss_cqc
import numpy as np

# Respuestas maximas de cada modo
R_modal = np.array([100, 80, 30])  # ej: cortantes modales [kN]
omega = np.array([10, 12, 25])     # frecuencias [rad/s]
zeta = 0.05                         # amortiguamiento 5%

# SRSS (modos independientes)
R_srss = combinacion_srss(R_modal)
print(f"SRSS: {R_srss:.1f} kN")

# CQC (considera correlacion entre modos cercanos)
R_cqc = combinacion_cqc(R_modal, omega, zeta)
print(f"CQC: {R_cqc:.1f} kN")

# Comparacion automatica con recomendacion
resultado = comparar_srss_cqc(R_modal, omega, zeta)
print(f"Diferencia: {resultado['diferencia_pct']:.1f}%")
print(f"Recomendacion: {resultado['recomendacion']}")
```

**Funciones disponibles:**
- `combinacion_srss(R)` - Raiz cuadrada de suma de cuadrados
- `combinacion_cqc(R, omega, zeta)` - Combinacion cuadratica completa
- `coeficiente_cqc(wi, wj, zi, zj)` - Coeficiente de correlacion
- `matriz_correlacion_cqc(omega, zeta)` - Matriz completa
- `comparar_srss_cqc(R, omega, zeta)` - Comparacion con recomendacion

---

### 2. Diseno de TMD (Den Hartog)

```python
from libreria_dinamica import den_hartog, warburton, diseno_tmd_edificio
import numpy as np

# Estructura principal
m_s = 1e6                          # masa [kg]
omega_s = 2 * np.pi * 0.5          # frecuencia 0.5 Hz
k_s = omega_s**2 * m_s             # rigidez [N/m]
mu = 0.02                          # ratio de masas 2%

# Diseno optimo (Den Hartog, estructura sin amortiguamiento)
tmd = den_hartog(m_s, k_s, mu)
print(f"Masa TMD: {tmd.m_d/1000:.1f} t")
print(f"f_opt: {tmd.f_opt:.3f}")
print(f"zeta_opt: {tmd.zeta_opt*100:.1f}%")

# Diseno para estructura amortiguada (Warburton)
tmd_w = warburton(m_s, k_s, mu, zeta_s=0.02)

# Funcion de alto nivel para edificios
tmd_edificio = diseno_tmd_edificio(m_modal=800e3, k_modal=k_s,
                                    mu=0.02, zeta_s=0.02)
```

**Funciones disponibles:**
- `den_hartog(m_s, k_s, mu)` - Diseno optimo clasico
- `warburton(m_s, k_s, mu, zeta_s)` - Extension para estructura amortiguada
- `frf_con_tmd(omega, m_s, k_s, c_s, tmd)` - FRF del sistema con TMD
- `comparar_con_sin_tmd(...)` - Comparacion antes/despues
- `tabla_diseno_tmd(m_s, k_s)` - Tabla para varios ratios de masa
- `diseno_tmd_edificio(...)` - Funcion de alto nivel

---

### 3. Visualizacion de Modos

```python
from libreria_dinamica import (MDOF, shear_building_uniforme,
                                graficar_modos_edificio,
                                graficar_matriz_correlacion)
import numpy as np

# Crear sistema MDOF
M, K = shear_building_uniforme(5, m=1000, k=200000)
sistema = MDOF(M, K)

# Graficar modos de vibracion
fig = graficar_modos_edificio(sistema.phi,
                               frecuencias=sistema.f_n,
                               n_modos=3)
fig.savefig('modos.pdf')

# Graficar matriz de correlacion CQC
from libreria_dinamica import matriz_correlacion_cqc
rho = matriz_correlacion_cqc(sistema.omega, zeta=0.05)
fig2 = graficar_matriz_correlacion(rho)
```

**Funciones de visualizacion:**
- `graficar_modos_edificio(phi, alturas, frecuencias)` - Perfiles modales
- `graficar_respuesta_modal(t, x)` - Respuesta temporal multi-DOF
- `graficar_frf_mdof(omega, H)` - Diagrama de Bode
- `graficar_matriz_correlacion(rho)` - Mapa de calor CQC
- `graficar_espectro_respuesta(T, Sa)` - Espectros de respuesta

---

## Referencia Rapida

### SDOF
```python
from libreria_dinamica import SDOF

sistema = SDOF(m=1000, k=40000, zeta=0.05)
print(f"f_n = {sistema.f_n:.2f} Hz")
print(f"T_n = {sistema.T_n:.3f} s")

# Vibracion libre
t = np.linspace(0, 5, 500)
u = sistema.vibracion_libre(t, u0=0.01, v0=0)
```

### MDOF
```python
from libreria_dinamica import MDOF, shear_building

m = np.array([1000, 1000, 1000])
k = np.array([200000, 200000, 200000])
M, K = shear_building(m, k)

sistema = MDOF(M, K)
print(f"Frecuencias: {sistema.f_n} Hz")
print(f"Modos:\n{sistema.phi}")

# Factores de participacion y masas efectivas
Gamma = sistema.factores_participacion()
M_eff, pct, M_tot = sistema.masas_efectivas()
```

### Integracion Temporal
```python
from libreria_dinamica import newmark, newmark_mdof

# SDOF
t, u, v, a = newmark(m, c, k, F, dt)

# MDOF
u, v, a = newmark_mdof(M, C, K, F, dt)
```

---

## Historial de Versiones

| Version | Fecha | Cambios |
|---------|-------|---------|
| 1.2.0 | Dic 2025 | SRSS/CQC, TMD, visualizacion de modos |
| 1.1.0 | Dic 2025 | Condensacion Guyan, Rayleigh |
| 1.0.0 | Dic 2024 | Version inicial |

---

## Referencias

- Chopra, A.K. (2017). "Dynamics of Structures", 5th ed.
- Den Hartog, J.P. (1956). "Mechanical Vibrations", 4th ed.
- Der Kiureghian, A. (1981). "A response spectrum method for random vibration."
- Eurocodigo 8 (EC8): Diseno sismorresistente de estructuras.
