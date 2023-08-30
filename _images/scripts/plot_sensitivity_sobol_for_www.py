"""
Script to produce the composed distribution image on the www front page.
Adapted from:
http://openturns.github.io/openturns/latest/auto_reliability_sensitivity/sensitivity_analysis/plot_sensitivity_sobol.html
"""


# %%
from openturns.usecases import ishigami_function
import openturns as ot
import openturns.viewer as otv
from matplotlib import pylab as plt

ot.Log.Show(ot.Log.NONE)

im = ishigami_function.IshigamiModel()

input_names = im.distributionX.getDescription()

# %%
n = 10000
sampleX = im.distributionX.getSample(n)
sampleY = im.model(sampleX)


# %%
size = 1000
sie = ot.SobolIndicesExperiment(im.distributionX, size)
inputDesign = sie.generate()
input_names = im.distributionX.getDescription()
inputDesign.setDescription(input_names)
inputDesign.getSize()

outputDesign = im.model(inputDesign)

sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)

palette = ot.Drawable.BuildDefaultPalette(2)
colorFirstOrder = palette[0]
colorTotal = palette[1]


def updateGraphColorOfDrawble(graph, index, color):
    drawable = graph.getDrawable(index)
    drawable.setColor(color)
    graph.setDrawable(drawable, index)
    return graph


"""
0 : first order points
1 : total points
2 : texts
3 : first order bar of x1
4 : total bar of x1
5 : first order bar of x2
6 : total bar of x2
7 : first order bar of x3
8 : total bar of x3
"""

# %%
graph = sensitivityAnalysis.draw()
updateGraphColorOfDrawble(graph, 2, "black")
for index in [0, 3, 5, 7]:
    updateGraphColorOfDrawble(graph, index, colorFirstOrder)
for index in [1, 4, 6, 8]:
    updateGraphColorOfDrawble(graph, index, colorTotal)

figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


view = otv.View(
    graph,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.5, hspace=0.5, bottom=0.22, right=0.7)
view.save(
    "../../_static/img/reliability_sensitivity.png",
    dpi=dpi,
)
