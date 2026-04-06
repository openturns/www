"""
Script to produce the composed distribution on the www front page.
Adapted from:
https://github.com/openturns/openturns/blob/master/python/doc/_templates/DistributionHighDimension.rst_t
"""

# %%
import openturns as ot
from matplotlib import pyplot as plt
import openturns.viewer as otv

# %%
R = ot.CorrelationMatrix(2)
R[0, 1] = 0.3
copula = ot.NormalCopula(R)
marginals = [ot.Uniform(), ot.Normal()]
distribution = ot.JointDistribution(marginals, copula)

# %%
# Compute bounds
dimension = distribution.getDimension()
mean = distribution.getMean()
std = distribution.getStandardDeviation()
xMin = [-1.2, -3.0]
xMax = [1.2, 3.0]


# %%
# Create a sample
size = 1000
sample = distribution.getSample(size)
sampleMin = sample.getMin()
sampleMax = sample.getMax()


# %%
def fromColorToAlphaColor(color, a):
    r, g, b = ot.Drawable.ConvertToRGB(color)
    h, s, v = ot.Drawable.ConvertFromRGBIntoHSV(r, g, b)
    newColor = ot.Polygon.ConvertFromHSVA(h, s, v, a)
    return newColor


# %%
numberOfContours = 4
ot.ResourceMap.SetAsUnsignedInteger("Contour-DefaultLevelsNumber", numberOfContours)
palette = ot.Drawable.BuildDefaultPalette(numberOfContours)

# %%
colorPDFMarginal = palette[0]
colorPDFContour = palette[0]
colorCloud = fromColorToAlphaColor(palette[1], 0.05)

# %%
grid = ot.GridLayout(dimension, dimension)
for j in range(dimension):
    for i in range(dimension):
        if i == j:
            graph = distribution.drawMarginal1DPDF(i, xMin[i], xMax[i], 256)
            graph.setColors([colorPDFMarginal])
            graph.setXTitle(r"$x_{" + str(i + 1) + r"}$")
            graph.setYTitle(r"PDF")
            graph.setTitle("")
            graph.setGrid(False)
        else:
            graph = ot.Graph("", r"$x_{" + str(j + 1) + r"}$", r"$x_{" + str(i + 1) + r"}$", True)
            cloud = ot.Cloud(sample.getMarginal([j, i]))
            cloud.setPointStyle("bullet")
            cloud.setColor(colorCloud)
            graph.add(cloud)
            curve = distribution.drawMarginal2DPDF(
                j, i, [xMin[j], xMin[i]], [xMax[j], xMax[i]], [256] * 2
            ).getDrawable(0).getImplementation()
            curve.setColor(colorPDFContour)
            curve.setColorBarPosition("")
            graph.add(curve)
            graph.setGrid(False)
        graph.setLegends([""])
        grid.setGraph(i, j, graph)

grid.setTitle("")

# %%
figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


# %%
view = otv.View(
    grid,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.7, hspace=1.0, bottom=0.22, left=0.2, right=0.9)
view.save(
    "../../_static/img/probabilistic_modeling.png",
    dpi=dpi,
)

# %%
