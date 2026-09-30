"""
Serie de Fourier de una señal periódica, calculada paso a paso.

Una señal f(t) de periodo T se aproxima por

    f(t) ≈ a0/2 + Σ_(n=1..N) [a_n cos(w_n t) + b_n sen(w_n t)],   w_n = 2π n / T

    a_n = (2/T) ∫_0^T f(t) cos(w_n t) dt
    b_n = (2/T) ∫_0^T f(t) sen(w_n t) dt

o, en forma de amplitud y fase,

    f(t) ≈ a0/2 + Σ A_n sen(w_n t + θ_n),   A_n = √(a_n² + b_n²),  θ_n = atan2(a_n, b_n)

FORMULACIÓN ELEGIDA: las integrales se evalúan LITERALMENTE con la regla del
trapecio sobre M intervalos iguales de [0, T]. La FFT (``numpy.fft.rfft``) se
presenta después como una forma rápida de obtener exactamente los mismos
números cuando la señal es periódica.

Organización del fichero
------------------------
1. CÁLCULO : señales, generador pseudoaleatorio, coeficientes, sumas parciales, errores.
2. PROCESO : construcción de los casos del cuaderno y barridos en n o en N.
3. DIBUJO  : funciones gráficas que reciben resultados ya calculados.
"""

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "figure.figsize": (10, 4),
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "lines.linewidth": 1.6,
    "legend.fontsize": 9,
})


# =============================================================================
# 1. CÁLCULO
# =============================================================================

# --- Malla de tiempo ---------------------------------------------------------

def malla_periodo(T, M):
    """M + 1 instantes equiespaciados t_k = k T / M, k = 0..M (incluye t = T)."""
    return np.linspace(0.0, T, M + 1)


def frecuencia_armonico(n, T):
    """Frecuencia circular del armónico n:  w_n = 2π n / T  [rad/s]."""
    return 2.0 * np.pi * n / T


# --- Señales -----------------------------------------------------------------

def suma_armonicos(t, componentes):
    """Suma de senos y cosenos:  f(t) = Σ A_i sen(2π f_i t + φ_i)  (o cos).

    ``componentes`` es una lista de diccionarios con las claves
    ``amplitud``, ``frecuencia`` [Hz], ``fase`` [rad] y ``tipo`` ("sen" o "cos").
    """
    t = np.asarray(t, dtype=float)
    f = np.zeros_like(t)
    for c in componentes:
        argumento = 2.0 * np.pi * c["frecuencia"] * t + c.get("fase", 0.0)
        funcion = np.cos if c.get("tipo", "sen") == "cos" else np.sin
        f += c["amplitud"] * funcion(argumento)
    return f


def lcg(n_valores, semilla=12345, a=1664525, c=1013904223, m=2**32):
    """Generador congruencial lineal  x_(k+1) = (a x_k + c) mod m.

    Devuelve x_1 .. x_n (enteros); la semilla x_0 no se incluye.
    Se usan enteros de Python para que el resultado sea idéntico al de la
    página interactiva (sin desbordamientos ni redondeos).
    """
    x = semilla
    valores = []
    for _ in range(n_valores):
        x = (a * x + c) % m
        valores.append(x)
    return valores


def normalizar_lcg(enteros, m=2**32):
    """Pasa los enteros del LCG al intervalo [-1, 1):  v = 2 x / m - 1."""
    return np.array([2.0 * x / m - 1.0 for x in enteros])


def interpolacion_periodica(t, valores_nodos, T):
    """Interpolación lineal a trozos y periódica de periodo T.

    El nodo j (j = 0..J-1) está en t_j = j T / J y el nodo J coincide con el 0,
    de modo que la señal cierra el periodo sin salto.
    """
    J = len(valores_nodos)
    t_nodos = np.arange(J + 1) * T / J
    v_nodos = np.append(valores_nodos, valores_nodos[0])
    return np.interp(np.mod(t, T), t_nodos, v_nodos)


def leer_registro(ruta, dt_archivo, factor=1.0):
    """Lee un registro de valores equiespaciados (p. ej. formato 8F10.5).

    Las líneas que no son completamente numéricas (cabecera) se ignoran.
    Devuelve (t, valores); ``factor`` multiplica los valores (9.81 para g → m/s²).
    """
    datos = []
    for linea in Path(ruta).read_text().splitlines():
        try:
            datos.extend(float(x) for x in linea.split())
        except ValueError:
            continue
    valores = factor * np.array(datos)
    return dt_archivo * np.arange(len(valores)), valores


# --- Coeficientes ------------------------------------------------------------

def coeficientes_integral(t, f, n_max):
    """a_n y b_n (n = 0..n_max) por la regla del trapecio, literalmente.

        a_n = (2/T) ∫_0^T f cos(w_n t) dt,   b_n = (2/T) ∫_0^T f sen(w_n t) dt

    ``t`` es la malla de [0, T] con extremos incluidos (``malla_periodo``).
    """
    T = t[-1] - t[0]
    a = np.zeros(n_max + 1)
    b = np.zeros(n_max + 1)
    for n in range(n_max + 1):
        w = frecuencia_armonico(n, T)
        a[n] = 2.0 / T * np.trapezoid(f * np.cos(w * t), t)
        b[n] = 2.0 / T * np.trapezoid(f * np.sin(w * t), t)
    return a, b


def coeficientes_fft(f_muestras, n_max):
    """a_n y b_n (n = 0..n_max) con la FFT real de M muestras de un periodo.

    Con F_n = Σ_k f_k e^(-i 2π n k / M)  (k = 0..M-1, sin repetir t = T):

        a_n = 2 Re(F_n) / M,    b_n = -2 Im(F_n) / M

    Coincide con el trapecio periódico siempre que n_max < M/2.
    """
    M = len(f_muestras)
    F = np.fft.rfft(f_muestras)[: n_max + 1]
    return 2.0 * F.real / M, -2.0 * F.imag / M


def amplitud_fase(a, b):
    """A_n = √(a_n² + b_n²) y θ_n = atan2(a_n, b_n), con f ≈ a0/2 + Σ A_n sen(w_n t + θ_n).

    Es la misma convención que la página interactiva: un seno puro tiene θ = 0
    y un coseno, θ = π/2.

    Para n = 0 se devuelve A_0 = |a0|/2 (valor medio), para que el espectro de
    amplitudes muestre directamente la amplitud de cada término de la serie.
    """
    A = np.hypot(a, b)
    A[0] = abs(a[0]) / 2.0
    return A, np.arctan2(a, b)


# --- Reconstrucción y error --------------------------------------------------

def suma_parcial(t, a, b, N, T):
    """S_N(t) = a0/2 + Σ_(n=1..N) [a_n cos(w_n t) + b_n sen(w_n t)]."""
    S = np.full_like(np.asarray(t, dtype=float), a[0] / 2.0)
    for n in range(1, N + 1):
        w = frecuencia_armonico(n, T)
        S += a[n] * np.cos(w * t) + b[n] * np.sin(w * t)
    return S


def valor_eficaz(t, f):
    """Valor eficaz  RMS = √( (1/T) ∫_0^T f² dt )  por el trapecio."""
    T = t[-1] - t[0]
    return np.sqrt(np.trapezoid(f**2, t) / T)


def error_rms_relativo(t, f, S):
    """e_N = RMS(f - S_N) / RMS(f)."""
    return valor_eficaz(t, f - S) / valor_eficaz(t, f)


def potencia_parseval(a, b, N):
    """Potencia media de S_N:  a0²/4 + ½ Σ_(n=1..N) (a_n² + b_n²)."""
    return a[0] ** 2 / 4.0 + 0.5 * np.sum(a[1: N + 1] ** 2 + b[1: N + 1] ** 2)


# =============================================================================
# 2. PROCESO
# =============================================================================

def caso_senal(t, f, n_max, nombre=""):
    """Calcula coeficientes, amplitudes y fases de una señal ya muestreada.

    Devuelve un diccionario con t, f, T, n, w, a, b, A, fase y nombre.
    """
    T = t[-1] - t[0]
    a, b = coeficientes_integral(t, f, n_max)
    A, fase = amplitud_fase(a, b)
    n = np.arange(n_max + 1)
    return {"nombre": nombre, "t": t, "f": f, "T": T, "n": n,
            "w": frecuencia_armonico(n, T), "frec": n / T,
            "a": a, "b": b, "A": A, "fase": fase}


def caso_seno(T, frecuencia, M, n_max, amplitud=1.0):
    """Paso 1: un seno de frecuencia dada [Hz] analizado con periodo T."""
    t = malla_periodo(T, M)
    f = suma_armonicos(t, [{"amplitud": amplitud, "frecuencia": frecuencia}])
    return caso_senal(t, f, n_max, nombre=f"sen(2π·{frecuencia:g}·t)")


def caso_suma_senos(T, componentes, M, n_max):
    """Paso 2: suma de senos y cosenos definida por ``componentes``."""
    t = malla_periodo(T, M)
    return caso_senal(t, suma_armonicos(t, componentes), n_max, nombre="suma de senos")


def caso_pseudoaleatorio(T, n_nodos, semilla, M, n_max):
    """Paso 3: señal lineal a trozos con n_nodos valores del LCG."""
    enteros = lcg(n_nodos, semilla)
    valores = normalizar_lcg(enteros)
    t = malla_periodo(T, M)
    caso = caso_senal(t, interpolacion_periodica(t, valores, T), n_max,
                      nombre="señal pseudoaleatoria")
    caso.update({"enteros_lcg": enteros, "valores_nodos": valores,
                 "t_nodos": np.arange(n_nodos) * T / n_nodos})
    return caso


def producto_con_armonico(caso, n, funcion="sen"):
    """f(t)·sen(w_n t) (o cos) y el coeficiente que resulta de integrarlo."""
    w = frecuencia_armonico(n, caso["T"])
    base = np.sin(w * caso["t"]) if funcion == "sen" else np.cos(w * caso["t"])
    coef = caso["b"][n] if funcion == "sen" else caso["a"][n]
    return {"n": n, "funcion": funcion, "base": base,
            "producto": caso["f"] * base, "coeficiente": coef}


def barrido_reconstruccion(caso, lista_N):
    """Sumas parciales S_N, error RMS relativo y potencia de Parseval para cada N.

    Devuelve un diccionario con las listas N, S (N -> vector), e_rms,
    potencia_serie y la potencia media de la señal.
    """
    t, f, T = caso["t"], caso["f"], caso["T"]
    sumas, errores, potencias = {}, [], []
    for N in lista_N:
        S = suma_parcial(t, caso["a"], caso["b"], N, T)
        sumas[N] = S
        errores.append(error_rms_relativo(t, f, S))
        potencias.append(potencia_parseval(caso["a"], caso["b"], N))
    return {"N": list(lista_N), "S": sumas, "e_rms": np.array(errores),
            "potencia_serie": np.array(potencias),
            "potencia_senal": valor_eficaz(t, f) ** 2}


def comparar_integral_fft(caso, repeticiones=5):
    """Compara coeficientes y coste del cálculo literal frente a la FFT.

    Operaciones (productos) aproximadas:
        integral literal  ≈ 2 (n_max + 1)(M + 1)
        FFT de M muestras ≈ (M/2) log2(M)  (productos complejos)
    """
    t, f = caso["t"], caso["f"]
    M, n_max = len(t) - 1, len(caso["n"]) - 1

    def cronometrar(funcion):
        inicio = time.perf_counter()
        for _ in range(repeticiones):
            resultado = funcion()
        return resultado, (time.perf_counter() - inicio) / repeticiones

    (a_i, b_i), t_integral = cronometrar(lambda: coeficientes_integral(t, f, n_max))
    (a_f, b_f), t_fft = cronometrar(lambda: coeficientes_fft(f[:-1], n_max))
    return {"a_integral": a_i, "b_integral": b_i, "a_fft": a_f, "b_fft": b_f,
            "dif_max": max(np.max(np.abs(a_i - a_f)), np.max(np.abs(b_i - b_f))),
            "tiempo_integral": t_integral, "tiempo_fft": t_fft,
            "ops_integral": 2 * (n_max + 1) * (M + 1),
            "ops_fft": int(M / 2 * np.log2(M)), "M": M, "n_max": n_max}


# =============================================================================
# 3. DIBUJO
# =============================================================================

def dibujar_senal(caso, extra=None, titulo=None):
    """Señal f(t) sobre un periodo; ``extra`` = [(t, y, etiqueta), ...] se superpone."""
    figura, eje = plt.subplots(figsize=(10, 3.2))
    eje.plot(caso["t"], caso["f"], color="tab:blue", label="f(t)")
    for t, y, etiqueta in (extra or []):
        eje.plot(t, y, "--", color="tab:orange", label=etiqueta)
    eje.set_xlabel("t [s]")
    eje.set_ylabel("f(t)")
    eje.set_title(titulo or caso["nombre"])
    eje.legend(loc="upper right")
    return figura


def dibujar_producto(caso, producto):
    """f(t), la función de prueba y su producto con el área sombreada."""
    figura, (eje1, eje2) = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    t, n = caso["t"], producto["n"]
    nombre_base = f"{producto['funcion']}(ω_{n} t)"
    eje1.plot(t, caso["f"], color="tab:blue", label="f(t)")
    eje1.plot(t, producto["base"], "--", color="tab:orange", label=nombre_base)
    eje1.legend(loc="upper right")
    eje1.set_ylabel("señal")
    p = producto["producto"]
    eje2.plot(t, p, color="tab:green", label=f"f(t)·{nombre_base}")
    eje2.fill_between(t, p, where=p >= 0, color="tab:green", alpha=0.3)
    eje2.fill_between(t, p, where=p < 0, color="tab:red", alpha=0.3)
    letra = "b" if producto["funcion"] == "sen" else "a"
    eje2.set_title(f"{letra}_{n} = (2/T)·área = {producto['coeficiente']:.4f}")
    eje2.set_xlabel("t [s]")
    eje2.set_ylabel("producto")
    eje2.legend(loc="upper right")
    figura.tight_layout()
    return figura


def dibujar_coeficientes(caso, cuales=("a", "b"), titulo=None):
    """Diagrama de barras de |a_n| y/o |b_n| frente a n."""
    figura, eje = plt.subplots(figsize=(10, 3.2))
    ancho = 0.8 / len(cuales)
    colores = {"a": "tab:blue", "b": "tab:orange"}
    for i, letra in enumerate(cuales):
        eje.bar(caso["n"] + (i - (len(cuales) - 1) / 2) * ancho, np.abs(caso[letra]),
                width=ancho, color=colores[letra], label=f"|{letra}_n|")
    eje.set_xlabel("armónico n")
    eje.set_ylabel("valor absoluto")
    eje.set_title(titulo or f"Coeficientes de {caso['nombre']}")
    eje.legend()
    return figura


def dibujar_espectro(caso, titulo=None):
    """Espectro de amplitudes A_n frente a la frecuencia n/T [Hz]."""
    figura, eje = plt.subplots(figsize=(10, 3.2))
    eje.stem(caso["frec"], caso["A"], basefmt=" ")
    eje.set_xlabel("frecuencia n/T [Hz]")
    eje.set_ylabel("amplitud A_n")
    eje.set_title(titulo or f"Espectro de amplitudes: {caso['nombre']}")
    return figura


def dibujar_nodos(caso):
    """Señal pseudoaleatoria con sus nodos marcados."""
    figura = dibujar_senal(caso)
    eje = figura.axes[0]
    eje.plot(caso["t_nodos"], caso["valores_nodos"], "o", color="tab:red",
             markersize=4, label="nodos (LCG)")
    eje.legend(loc="upper right")
    return figura


def dibujar_reconstrucciones(caso, barrido, lista_N, columnas=2):
    """Rejilla de subgráficas: f(t) y S_N(t) para cada N de ``lista_N``."""
    filas = int(np.ceil(len(lista_N) / columnas))
    figura, ejes = plt.subplots(filas, columnas, figsize=(11, 2.2 * filas),
                                sharex=True, sharey=True, squeeze=False)
    for eje, N in zip(ejes.flat, lista_N):
        indice = barrido["N"].index(N)
        eje.plot(caso["t"], caso["f"], color="0.6", lw=1.2, label="f(t)")
        eje.plot(caso["t"], barrido["S"][N], color="tab:blue", lw=1.3, label="S_N(t)")
        eje.set_title(f"N = {N}   (e_N = {barrido['e_rms'][indice]:.3f})", fontsize=10)
    for eje in ejes.flat[len(lista_N):]:
        eje.set_visible(False)
    ejes.flat[0].legend(loc="upper right")
    figura.supxlabel("t [s]")
    figura.tight_layout()
    return figura


def dibujar_una_reconstruccion(caso, barrido, N):
    """f(t) y S_N(t) para un único N (útil con un deslizador)."""
    indice = barrido["N"].index(N)
    figura, eje = plt.subplots(figsize=(10, 3.2))
    eje.plot(caso["t"], caso["f"], color="0.6", label="f(t)")
    eje.plot(caso["t"], barrido["S"][N], color="tab:blue", label=f"S_{N}(t)")
    eje.set_title(f"N = {N}   (e_N = {barrido['e_rms'][indice]:.4f})")
    eje.set_xlabel("t [s]")
    eje.legend(loc="upper right")
    return figura


def dibujar_error(barrido):
    """Error RMS relativo e_N frente a N, en escala logarítmica."""
    figura, eje = plt.subplots(figsize=(10, 3.2))
    N = np.array(barrido["N"])
    eje.semilogy(N, barrido["e_rms"], "o-", markersize=3)
    eje.set_xlabel("número de armónicos N")
    eje.set_ylabel("e_N = RMS(f − S_N)/RMS(f)")
    eje.set_title("Convergencia de la suma parcial")
    return figura


def dibujar_diferencia_fft(comparacion):
    """|a_n^integral − a_n^FFT| y |b_n^integral − b_n^FFT| frente a n."""
    figura, eje = plt.subplots(figsize=(10, 3.2))
    n = np.arange(comparacion["n_max"] + 1)
    piso = 1e-18  # evita log(0) si la diferencia es exactamente nula
    eje.semilogy(n, np.abs(comparacion["a_integral"] - comparacion["a_fft"]) + piso,
                 "o", markersize=3, label="|Δa_n|")
    eje.semilogy(n, np.abs(comparacion["b_integral"] - comparacion["b_fft"]) + piso,
                 "s", markersize=3, label="|Δb_n|")
    eje.set_xlabel("armónico n")
    eje.set_ylabel("diferencia absoluta")
    eje.set_title("Integral literal frente a FFT")
    eje.legend()
    return figura
