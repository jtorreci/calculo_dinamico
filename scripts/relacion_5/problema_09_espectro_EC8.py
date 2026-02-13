"""
Problema 09: Espectro de diseño Eurocode 8
==========================================
Construcción del espectro elástico EC8 para diferentes tipos de suelo.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Parámetros EC8
# =============================================================================
print("=" * 60)
print("PROBLEMA 09: ESPECTRO DE DISEÑO EC8")
print("=" * 60)

# Aceleración de diseño
agR = 0.16  # g
gamma_I = 1.2
ag = gamma_I * agR
g = 9.81

print(f"\nDatos:")
print(f"  agR = {agR}g")
print(f"  gamma_I = {gamma_I}")
print(f"  ag = {ag}g = {ag*g:.2f} m/s²")

# Parámetros por tipo de suelo
suelos = {
    'A': {'S': 1.0, 'TB': 0.15, 'TC': 0.4, 'TD': 2.0, 'color': 'b', 'desc': 'Roca'},
    'B': {'S': 1.2, 'TB': 0.15, 'TC': 0.5, 'TD': 2.0, 'color': 'g', 'desc': 'Suelo rígido'},
    'C': {'S': 1.15, 'TB': 0.20, 'TC': 0.6, 'TD': 2.0, 'color': 'orange', 'desc': 'Suelo denso'},
    'D': {'S': 1.35, 'TB': 0.20, 'TC': 0.8, 'TD': 2.0, 'color': 'r', 'desc': 'Suelo blando'}
}

# =============================================================================
# Función del espectro EC8
# =============================================================================
def Se_EC8(T, ag, S, TB, TC, TD, eta=1.0):
    """Espectro elástico EC8"""
    T = np.atleast_1d(T)
    Se = np.zeros_like(T)

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
# Cálculo de espectros
# =============================================================================
T = np.linspace(0.01, 4.0, 500)

print("\n" + "=" * 60)
print("ESPECTROS POR TIPO DE SUELO")
print("=" * 60)
print(f"\n{'Suelo':<8} {'S':<6} {'TB':<6} {'TC':<6} {'Se_max (g)':<12}")
print("-" * 40)

for tipo, params in suelos.items():
    Se_max = ag * params['S'] * 2.5
    print(f"{tipo:<8} {params['S']:<6.2f} {params['TB']:<6.2f} {params['TC']:<6.2f} {Se_max:<12.3f}")

# =============================================================================
# Gráficas
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Espectros por tipo de suelo
ax1 = axes[0]
for tipo, params in suelos.items():
    Se = Se_EC8(T, ag, params['S'], params['TB'], params['TC'], params['TD'])
    ax1.plot(T, Se, params['color'], linewidth=2,
             label=f"Suelo {tipo} ({params['desc']})")

ax1.axhline(y=ag, color='k', linestyle='--', alpha=0.5, label=f'ag = {ag:.3f}g')
ax1.set_xlabel('Período T (s)', fontsize=12)
ax1.set_ylabel('Se/g', fontsize=12)
ax1.set_title('Espectro elástico EC8 por tipo de suelo', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 4)
ax1.set_ylim(0, 0.7)

# Panel 2: Espectro suelo C con zonas
ax2 = axes[1]
params_C = suelos['C']
Se_C = Se_EC8(T, ag, params_C['S'], params_C['TB'], params_C['TC'], params_C['TD'])
ax2.plot(T, Se_C, 'orange', linewidth=2.5, label='Suelo C')

# Marcar puntos característicos
TB, TC, TD = params_C['TB'], params_C['TC'], params_C['TD']
Se_plateau = ag * params_C['S'] * 2.5

ax2.axvline(x=TB, color='gray', linestyle=':', alpha=0.7)
ax2.axvline(x=TC, color='gray', linestyle=':', alpha=0.7)
ax2.axvline(x=TD, color='gray', linestyle=':', alpha=0.7)

ax2.annotate(f'TB={TB}s', (TB, 0.02), fontsize=10, ha='center')
ax2.annotate(f'TC={TC}s', (TC, 0.02), fontsize=10, ha='center')
ax2.annotate(f'TD={TD}s', (TD, 0.02), fontsize=10, ha='center')

# Zonas
ax2.fill_between(T[T<=TB], 0, Se_C[T<=TB], alpha=0.2, color='blue', label='Rampa')
ax2.fill_between(T[(T>TB)&(T<=TC)], 0, Se_C[(T>TB)&(T<=TC)], alpha=0.2, color='green', label='Plateau')
ax2.fill_between(T[(T>TC)&(T<=TD)], 0, Se_C[(T>TC)&(T<=TD)], alpha=0.2, color='orange', label='Descenso 1/T')
ax2.fill_between(T[T>TD], 0, Se_C[T>TD], alpha=0.2, color='red', label='Descenso 1/T²')

ax2.set_xlabel('Período T (s)', fontsize=12)
ax2.set_ylabel('Se/g', fontsize=12)
ax2.set_title('Zonas del espectro EC8 (Suelo C)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 4)
ax2.set_ylim(0, 0.7)

plt.tight_layout()
plt.savefig('../figs/fig_problema_09_espectro_EC8.png', dpi=150, bbox_inches='tight')
plt.savefig('../figs/fig_problema_09_espectro_EC8.pdf', bbox_inches='tight')
print("\n[Figura guardada en figs/fig_problema_09_espectro_EC8.pdf]")
plt.close()
