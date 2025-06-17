"""
Script to produce the copula image on the www front page.
Adapted from:
http://openturns.github.io/openturns/latest/auto_data_analysis/statistical_tests/plot_test_copula.html
"""
# %%
import openturns as ot
import openturns.viewer as viewer
from matplotlib import pylab as plt

ot.Log.Show(ot.Log.NONE)


# %%
dimension = 2
marginals = [ot.Normal()] * dimension
dist = ot.ComposedDistribution(marginals, ot.GumbelCopula(dimension))
N = 500
sample = dist.getSample(N)

# %%
estimated = ot.GumbelCopulaFactory().build(sample)
print(estimated)


def fromColorToAlphaColor(color, a):
    r, g, b = ot.Drawable.ConvertToRGB(color)
    h, s, v = ot.Drawable.ConvertFromRGBIntoHSV(r, g, b)
    newColor = ot.Polygon.ConvertFromHSVA(h, s, v, a)
    return newColor


palette = ot.Drawable.BuildDefaultPalette(2)
cloudColor = fromColorToAlphaColor(palette[0], 0.5)
copulaColor = palette[1]


# %%
ranksTransf = ot.MarginalTransformationEvaluation(
    marginals, ot.MarginalTransformationEvaluation.FROM
)
rankSample = ranksTransf(sample)
rankCloud = ot.Cloud(rankSample, "blue", "plus", "sample")
rankCloud.setPointStyle("bullet")
rankCloud.setColor(cloudColor)

# %%
myGraph = ot.Graph(
    f"Parametric estimation of the copula, n = {N}", r"$u_1$", r"$u_2$", True, "topleft"
)
myGraph.setLegendPosition("bottomright")
myGraph.add(rankCloud)


# %%
numberOfContours = 5
ot.ResourceMap.SetAsUnsignedInteger("Contour-DefaultLevelsNumber", numberOfContours)
minPoint = [0.0] * 2
maxPoint = [1.0] * 2
pointNumber = [201] * 2
graphCop = estimated.drawPDF(minPoint, maxPoint, pointNumber)
contour = graphCop.getDrawable(0).getImplementation()
levels = contour.getLevels()
contour.setLegend("Gumbel")
contour.setColor(copulaColor)
contour.setLevels(levels)
myGraph.add(contour)


figure_width_in_pixels = 400
figure_height_in_pixels = 280
dpi = 90
figure_width_in_inches = figure_width_in_pixels / dpi
figure_height_in_pixels = figure_height_in_pixels / dpi


view = viewer.View(
    myGraph,
    figure_kw={
        "figsize": (figure_width_in_inches, figure_height_in_pixels),
        "dpi": dpi,
    },
    legend_kw={"bbox_to_anchor": (1.0, 1.0), "loc": "upper left"},
)
plt.subplots_adjust(wspace=0.5, hspace=0.5, bottom=0.22, right=0.7)
plt.axis("equal")
view.save(
    "../../_static/img/data_analysis.png",
    dpi=dpi,
)
