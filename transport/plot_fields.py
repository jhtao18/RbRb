import numpy as np
import matplotlib.pyplot as plt

from torc import cm, gauss, gauss_per_cm

from labscriptlib.RbRb.transport.coils_RbRb import coils

"""This script plots the fields and diagonal elements of the gradient tensor produced by
each coil pair as a function of position along the transport axis"""

from matplotlib import rc
rc('text', usetex=False)

miny = min(coil.y for coil in coils)
maxy = max(coil.y for coil in coils)
y = np.linspace(miny, maxy, 1024)

B = {}
dBs_ds = {}
for coil in coils:
    B[coil.name] = coil.B((0, y, 0), I=1)
    dBs_ds[coil.name] = []
    for i, s_i in enumerate(['x', 'y', 'z']):
        dBs_ds[coil.name].append(coil.dB((0, y, 0), I=1, s=s_i)[i])

max_B = max(max(abs(B_coil_s)) for B_coil in B.values() for B_coil_s in B_coil)
max_dBs_ds = max(
    max(abs(dBs_ds_coil_s))
    for dBs_ds_coil in dBs_ds.values()
    for dBs_ds_coil_s in dBs_ds_coil
)

COLORS = [plt.cm.nipy_spectral(i) for i in np.linspace(0, 1, len(coils))]

fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 8))
for i, (ax, s_i) in enumerate(zip(axes, ['x', 'y', 'z'])):
    for coil, color in zip(coils, COLORS):
        ax.plot(y / cm, B[coil.name][i] / gauss, label=coil.name, color=color)
    ax.set_ylabel(Rf'$I^{{-1}}B_{s_i}$ (g A$^{{-1}}$)')
    ax.grid(True)
    ax.axis(xmin=miny / cm, xmax=maxy / cm)
    # No tick labels except on bottom plot:
    if s_i != 'z':
        ax.tick_params(axis='x', labelbottom=False)
plt.xlabel(R'distance $y$ from MOT along transport axis (cm)')
plt.subplots_adjust(left=0.1, right=0.8, top=0.95, bottom=0.1, hspace=0)
# Put a legend to the right of the middle axis
axes[1].legend(loc='center left', bbox_to_anchor=(1.0, 0.5))


fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 8))
for i, (ax, s_i) in enumerate(zip(axes, ['x', 'y', 'z'])):
    for coil, color in zip(coils, COLORS):
        ax.plot(
            y / cm, dBs_ds[coil.name][i] / gauss_per_cm, label=coil.name, color=color
        )
    ax.set_ylabel(
        Rf'$I^{{-1}}\partial B_{s_i}/\partial {s_i}$ (g cm$^{{-1}}$ A$^{{-1}}$)'
    )
    ax.grid(True)
    ax.axis(xmin=miny / cm, xmax=maxy / cm)
    # No tick labels except on bottom plot:
    if s_i != 'z':
        ax.tick_params(axis='x', labelbottom=False)
plt.xlabel(R'distance $y$ from MOT along transport axis (cm)')
plt.subplots_adjust(left=0.1, right=0.8, top=0.95, bottom=0.1, hspace=0)
# Put a legend to the right of the middle axis
axes[1].legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

plt.show()
