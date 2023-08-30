"""
Script to produce the kriging image on the www front page.
Adapted from:
http://openturns.github.io/openturns/latest/auto_meta_modeling/kriging_metamodel/plot_kriging_1d.html
"""

# %%
import openturns as ot
import openturns.viewer as viewer
from matplotlib import pylab as plt

ot.Log.Show(ot.Log.NONE)

# %%
g = ot.SymbolicFunction(["x"], ["sin(x)"])

# %%
x_train = ot.Sample([[x] for x in [1.0, 3.0, 4.0, 6.0, 7.9, 11.0, 11.5]])
y_train = g(x_train)
n_train = x_train.getSize()

# %%
xmin = 0.0
xmax = 12.0
n_test = 100
step = (xmax - xmin) / (n_test - 1)
myRegularGrid = ot.RegularGrid(xmin, step, n_test)
x_test = myRegularGrid.getVertices()
y_test = g(x_test)


# %%
def plot_data_train(x_train, y_train, colorDataTrain):
    """Plot the data (x_train,y_train) as a Cloud, in red"""
    graph_train = ot.Cloud(x_train, y_train)
    graph_train.setColor(colorDataTrain)
    graph_train.setLegend("Data")
    graph_train.setPointStyle("circle")
    return graph_train


# %%
def plot_data_test(x_test, y_test, colorDataTest):
    """Plot the data (x_test,y_test) as a Curve, in dashed black"""
    graphF = ot.Curve(x_test, y_test)
    graphF.setLegend("Exact")
    graphF.setColor(colorDataTest)
    graphF.setLineStyle("dashed")
    graphF.setLineWidth(2.0)
    return graphF


# %%
dimension = 1
basis = ot.ConstantBasisFactory(dimension).build()
# basis = ot.LinearBasisFactory(dimension).build()
basis = ot.QuadraticBasisFactory(dimension).build()
covarianceModel = ot.MaternModel([1.0] * dimension, 1.5)
algo = ot.KrigingAlgorithm(x_train, y_train, covarianceModel, basis)
algo.run()
result = algo.getResult()
print(result)

# %%
krigeageMM = result.getMetaModel()
y_test_MM = krigeageMM(x_test)


# %%
def plot_data_kriging(x_test, y_test_MM, colorKriging):
    """Plots (x_test,y_test_MM) from the metamodel as a Curve, in blue"""
    graphK = ot.Curve(x_test, y_test_MM)
    graphK.setColor(colorKriging)
    graphK.setLegend("Kriging")
    graphK.setLineWidth(2.0)
    return graphK


# %%


def computeQuantileAlpha(alpha):
    """
    Compute the normal bilateral quantile of level alpha.
    Return the upper bound.
    """
    bilateralCI = ot.Normal().computeBilateralConfidenceInterval(alpha)
    return bilateralCI.getUpperBound()[0]


alpha = 0.95
quantileAlpha = computeQuantileAlpha(alpha)
print(f"Quantile of level alpha = {alpha}: {quantileAlpha}")

# %%
sqrt = ot.SymbolicFunction(["x"], ["sqrt(x)"])
epsilon = ot.Sample(n_test, [1.0e-8])
conditionalVariance = result.getConditionalMarginalVariance(x_test) + epsilon
conditionalSigma = sqrt(conditionalVariance)


# %%
def computeBoundsConfidenceInterval(quantileAlpha):
    dataLower = [
        [y_test_MM[i, 0] - quantileAlpha * conditionalSigma[i, 0]]
        for i in range(n_test)
    ]
    dataUpper = [
        [y_test_MM[i, 0] + quantileAlpha * conditionalSigma[i, 0]]
        for i in range(n_test)
    ]
    dataLower = ot.Sample(dataLower)
    dataUpper = ot.Sample(dataUpper)
    return dataLower, dataUpper


# %%


def plot_kriging_bounds(dataLower, dataUpper, n_test, color):
    """
    From two lists containing the lower and upper bounds of the region,
    create a PolygonArray.
    Default color is green given by HSV values in color list.
    """
    vLow = [[x_test[i, 0], dataLower[i, 0]] for i in range(n_test)]
    vUp = [[x_test[i, 0], dataUpper[i, 0]] for i in range(n_test)]
    polyData = [[vLow[i], vLow[i + 1], vUp[i + 1], vUp[i]] for i in range(n_test - 1)]
    polygonList = [ot.Polygon(polyData[i], color, color) for i in range(n_test - 1)]
    boundsPoly = ot.PolygonArray(polygonList)
    return boundsPoly


# %%
palette = ot.Drawable.BuildDefaultPalette(3)
colorDataTrain = palette[0]
colorDataTest = palette[1]
colorKriging = palette[2]
colorKrigingBounds = ot.Drawable.ConvertFromName("gray")

# %%
graph = ot.Graph(f"Kriging, n={n_train}", "", "", True, "")
alpha = 0.95
quantileAlpha = computeQuantileAlpha(alpha)
vLow, vUp = computeBoundsConfidenceInterval(quantileAlpha)
boundsPoly = plot_kriging_bounds(vLow, vUp, n_test, colorKrigingBounds)
boundsPoly.setLegend(f" {100.0 * alpha}%% bounds")
graph.add(boundsPoly)

graph.add(plot_data_test(x_test, y_test, colorDataTest))
graph.add(plot_data_train(x_train, y_train, colorDataTrain))
graph.add(plot_data_kriging(x_test, y_test_MM, colorKriging))

graph.setAxes(True)
graph.setXTitle("X")
graph.setYTitle("Y")
graph.setLegendPosition("topright")

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
    "../../_static/img/meta_modeling.png",
    dpi=dpi,
)


# %%
