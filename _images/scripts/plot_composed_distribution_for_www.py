"""
Script to produce the composed distribution on the www front page.
Adapted from:
https://github.com/openturns/openturns/blob/master/python/doc/_templates/DistributionHighDimension.rst_t
"""
import openturns as ot
from matplotlib import pyplot as plt
import openturns.viewer as otv

R = ot.CorrelationMatrix(3)
R[0, 1] = 0.5
R[0, 2] = 0.3
R[1, 2] = -0.2
copula = ot.NormalCopula(R)
marginals = [ot.Uniform(1.0, 2.0), ot.Normal(2.0, 3.0), ot.Gamma(5.5, 2.0)]
distribution = ot.ComposedDistribution(marginals, copula)

# Compute bounds
dimension = distribution.getDimension()
mean = distribution.getMean()
std = distribution.getStandardDeviation()
xMin = distribution.getRange().getLowerBound()
xMax = distribution.getRange().getUpperBound()
xMin = [max(xMin[i], mean[i] - 3.0 * std[i]) for i in range(dimension)]
xMax = [min(xMax[i], mean[i] + 3.0 * std[i]) for i in range(dimension)]

# Create a sample
size = 1000
sample = distribution.getSample(size)
sMin = sample.getMin()
sMax = sample.getMax()
xMin = [min(xMin[i], sMin[i]) for i in range(dimension)]
xMax = [max(xMax[i], sMax[i]) for i in range(dimension)]

# Adjust the bounds
multiplicationFactor = 1.0
xMin = [0.9, -8.35, 0.0]
xMax = [2.1, 11.15, 7.39]


def fromColorToAlphaColor(color, a):
    r, g, b = ot.Drawable.ConvertToRGB(color)
    h, s, v = ot.Drawable.ConvertFromRGBIntoHSV(r, g, b)
    newColor = ot.Polygon.ConvertFromHSVA(h, s, v, a)
    return newColor


numberOfContours = 4
ot.ResourceMap.SetAsUnsignedInteger("Contour-DefaultLevelsNumber", numberOfContours)
palette = ot.Drawable.BuildDefaultPalette(numberOfContours)

colorPDFMarginal = palette[0]
colorCloud = fromColorToAlphaColor(palette[0], 0.05)

n_rows = dimension
n_cols = dimension
grid = ot.GridLayout(3, 3)
for j in range(dimension):
    for i in range(dimension):
        if i == j:
            pdf_graph = distribution.drawMarginal1DPDF(i, xMin[i], xMax[i], 256)
            pdf_graph.setColors([colorPDFMarginal])
        else:
            pdf_graph = ot.Graph("", "", "", True)
            cloud = ot.Cloud(sample.getMarginal([i, j]))
            cloud.setPointStyle("bullet")
            cloud.setColor(colorCloud)
            pdf_graph.add(cloud)
            curve = distribution.drawMarginal2DPDF(
                i, j, [xMin[i], xMin[j]], [xMax[i], xMax[j]], [256] * 2
            )
            curve.setColors(palette)
            pdf_graph.add(curve)
        pdf_graph.setTitle("")
        pdf_graph.setXTitle("")
        pdf_graph.setYTitle("")
        if j == 0:
            pdf_graph.setYTitle(r"$x_" + str(i) + r"$")
        if i == dimension - 1:
            pdf_graph.setXTitle(r"$x_" + str(j) + r"$")
        pdf_graph.setLegends([""])
        grid.setGraph(i, j, pdf_graph)

grid.setTitle("ComposedDistribution: Uniform, Normal, Gamma")

figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


view = otv.View(
    grid,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.5, hspace=0.5, bottom=0.22)
view.save(
    "../../_static/img/probabilistic_modeling.png",
    dpi=dpi,
)
