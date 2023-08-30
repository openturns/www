"""
Script to produce the trajectory sample on the www front page.
Adapted from:
http://openturns.github.io/openturns/latest/auto_functional_modeling/field_functions/plot_viscous_fall_field_function.html
"""

# %%
import openturns as ot
import openturns.viewer as viewer
from matplotlib import pylab as plt
import numpy as np

ot.Log.Show(ot.Log.NONE)

# %%
tmin = 0.0  # Minimum time
tmax = 12.0  # Maximum time
gridsize = 100  # Number of time steps
mesh = ot.IntervalMesher([gridsize - 1]).build(ot.Interval(tmin, tmax))

# %%
vertices = mesh.getVertices()

# %%
distZ0 = ot.Uniform(100.0, 150.0)
distV0 = ot.Normal(55.0, 10.0)
distM = ot.Normal(80.0, 8.0)
distC = ot.Uniform(0.0, 30.0)
distribution = ot.ComposedDistribution([distZ0, distV0, distM, distC])

# %%
dimension = distribution.getDimension()


# %%
def AltiFunc(X):
    g = 9.81
    z0 = X[0]
    v0 = X[1]
    m = X[2]
    c = X[3]
    tau = m / c
    vinf = -m * g / c
    t = np.array(vertices)
    z = z0 + vinf * t + tau * (v0 - vinf) * (1 - np.exp(-t / tau))
    z = np.maximum(z, 0.0)
    return [[zeta[0]] for zeta in z]


# %%
outputDimension = 1
alti = ot.PythonPointToFieldFunction(dimension, mesh, outputDimension, AltiFunc)

# %%
size = 10
inputSample = distribution.getSample(size)
outputSample = alti(inputSample)

# %%
ot.ResourceMap.SetAsUnsignedInteger("Drawable-DefaultPalettePhase", size)

# %%
graph = outputSample.drawMarginal(0)
graph.setTitle("Viscous free fall: %d trajectories" % (size))
graph.setXTitle(r"$t$")
graph.setYTitle(r"$z$")


figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


view = viewer.View(
    graph,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.5, hspace=0.5, bottom=0.22, right=0.7)
view.save(
    "../../_static/img/functional_modeling.png",
    dpi=dpi,
)
