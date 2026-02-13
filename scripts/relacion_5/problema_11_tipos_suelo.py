"""
Problema 11: Efecto del tipo de suelo en espectros
===================================================
Comparación de la respuesta espectral para diferentes tipos de suelo EC8.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Parámetros
# =============================================================================
print("=" * 60)
print("PROBLEMA 11: EFECTO DEL TIPO DE SUELO")
print("=" * 60)

g = 9.81
ag = 0.2  # g (aceleración de diseño)

# Parámetros EC8 por tipo de suelo
suelos = {
    'A': {'S': 1.0, 'TB': 0.15, 'TC': 0.4, 'TD': 2.0, 'desc': 'Roca'},
    'B': {'S': 1.2, 'TB': 0.15, 'TC': 0.5, 'TD': 2.0, 'desc': 'Suelo rígido'},
    'C': {'S': 1.15, 'TB': 0.20, 'TC': 0.6, 'TD': 2.0, 'desc': 'Suelo denso'},
    'D': {'S': 1.35, 'TB': 0.20, 'TC': 0.8, 'TD': 2.0, 'desc': 'Suelo blando'}
}

# =============================================================================
# Función del espectro EC8
# =============================================================================
def Se_EC8(T, ag, S, TB, TC, TD, eta=1.0):
    """Espectro elástico EC8 (retorna en g)"""
    T = np.atleast_1d(T)
    Se = np.zeros_like(T, dtype=float)

    for i, t in enumerate(T):
        if t <= 0:
            Se[i] = ag * S
        elif t <= TB:
            Se[i] = ag * S * (1 + t/TB * (eta*2.5 - 1))
        elif t <= TC:
            Se[i] = ag * S * eta * 2.5
        elif t <= TD:
            Se[i] = ag * S * eta * 2.5 * TC / t
        else:
            Se[i] = ag * S * eta * 2.5 * TC * TD / t**2

    return Se

# =============================================================================
# Cálculos
# =============================================================================
T = np.linspace(0.01, 4.0, 500)

# Período del edificio
T_edif = 0.7  # s

print(f"\nEdificio con T = {T_edif} s")
print(f"Aceleración de diseño ag = {ag}g")
print("\n" + "-" * 50)
print(f"{'Suelo':<10} {'Se_max (g)':<12} {'Se(T={T_edif}s)':<14} {'Ratio vs A':<10}")
print("-" * 50)

Se_A_T = Se_EC8(T_edif, ag, suelos['A']['S'], suelos['A']['TB'],
                suelos['A']['TC'], suelos['A']['TD'])[0]

for tipo, params in suelos.items():
    Se = Se_EC8(T, ag, params['S'], params['TB'], params['TC'], params['TD'])
    Se_T = Se_EC8(T_edif, ag, params['S'], params['TB'], params['TC'], params['TD'])[0]
    Se_max = ag * params['S'] * 2.5
    ratio = Se_T / Se_A_T
    print(f"{tipo:<10} {Se_max:<12.3f} {Se_T:<14.3f} {ratio:<10.2f}")

# =============================================================================
# Gráficas
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
colors = {'A': 'blue', 'B': 'green', 'C': 'orange', 'D': 'red'}

# Panel 1: Espectros
ax1 = axes[0]
for tipo, params in suelos.items():
    Se = Se_EC8(T, ag, params['S'], params['TB'], params['TC'], params['TD'])
    ax1.plot(T, Se, colors[tipo], linewidth=2, label=f"Suelo {tipo}")

# Marcar período del edificio
ax1.axvline(x=T_edif, color='k', linestyle='--', linewidth=1.5, label=f'T = {T_edif} s')

# Marcar puntos de intersección
for tipo, params in suelos.items():
    Se_T = Se_EC8(T_edif, ag, params['S'], params['TB'], params['TC'], params['TD'])[0]
    ax1.plot(T_edif, Se_T, 'o', color=colors[tipo], markersize=10,
             markeredgecolor='black', markeredgewidth=1.5)

ax1.set_xlabel('Período T (s)', fontsize=12)
ax1.set_ylabel('Se/g', fontsize=12)
ax1.set_title('Espectros EC8 por tipo de suelo', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 4)
ax1.set_ylim(0, 0.75)

# Panel 2: Amplificación respecto a suelo A
ax2 = axes[1]
T_range = np.linspace(0.1, 3.0, 100)

for tipo, params in suelos.items():
    if tipo == 'A':
        continue
    Se_tipo = Se_EC8(T_range, ag, params['S'], params['TB'], params['TC'], params['TD'])
    Se_A = Se_EC8(T_range, ag, suelos['A']['S'], suelos['A']['TB'],
                  suelos['A']['TC'], suelos['A']['TD'])
    ratio = Se_tipo / Se_A
    ax2.plot(T_range, ratio, colors[tipo], linewidth=2, label=f"Suelo {tipo}/A")

ax2.axhline(y=1.0, color='blue', linestyle='--', alpha=0.5, label='Suelo A (ref)')
ax2.axvline(x=T_edif, color='k', linestyle=':', linewidth=1.5)

ax2.set_xlabel('Período T (s)', fontsize=12)
ax2.set_ylabel('Amplificación respecto a Suelo A', fontsize=12)
ax2.set_title('Efecto de amplificación por tipo de suelo', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 3)
ax2.set_ylim(0.8, 3.0)

plt.tight_layout()
plt.savefig('../figs/fig_problema_11_tipos_suelo.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_11_tipos_suelo.pdf', bbox_inches='tight')
print("\n[Figura guardada en figs/fig_problema_11_tipos_suelo.pdf]")
plt.close()
