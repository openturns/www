from openturns.viewer import View
import openturns as ot

sampleSize = 4
dimension = 1

f = ot.SymbolicFunction(['x'], ['0.5*x^2 + sin(2.5*x)'])

# Database
xMin = -0.9
xMax = 1.9
X = ot.LHSExperiment(ot.Uniform(xMin, xMax), sampleSize, False, False).generate()
Y = f(X)

# create algorithm
basis = ot.ConstantBasisFactory(dimension).build()
covarianceModel = ot.MaternModel([1.0], 1.5)

ot.Log.Show(ot.Log.INFO)
algo = ot.KrigingAlgorithm(X, Y, covarianceModel, basis)
algo.run()

# perform an evaluation
result = algo.getResult()
meta = result.getMetaModel()
graph_meta = meta.draw(xMin, xMax)
data = graph_meta.getDrawable(0).getData()
xGrid = data.getMarginal(0)
covGrid = result.getConditionalCovariance(xGrid)
a = ot.DistFunc.qNormal(0.975)
c = ot.Cloud([data[2]])
c.setPointStyle("square")
c.setColor("green")
c.setLegend("95% confidence bound")
dataLower = [[data[i, 0], data[i, 1] - a * covGrid[i, i]] for i in range(len(data))]
dataUpper = [[data[i, 0], data[i, 1] + a * covGrid[i, i]] for i in range(len(data))]
bounds = ot.PolygonArray([ot.Polygon([dataLower[i], dataLower[i+1], dataUpper[i+1], dataUpper[i]], "green", "green") for i in range(len(dataLower)-1)])
graph = ot.Graph()
graph.setLegendPosition("bottomright")
graph.setAxes(True)
graph.setGrid(True)
graph.add(c)
graph.add(bounds)

d = f.draw(xMin, xMax).getDrawable(0)
d.setLineStyle("dashed")
d.setColor("magenta")
d.setLineWidth(2)
graph.add(d)
graph.add(graph_meta)
cloud = ot.Cloud(X, Y)
cloud.setPointStyle("circle")
cloud.setColor("red")
graph.add(cloud)
graph.setTitle("Kriging meta-modeling")
graph.setXTitle(r"$x$")
graph.setYTitle(r"$f$")
graph.setLegends(["95% conf. bounds", "true function", "meta-model", "data"])
view = View(graph, (800, 600))
view.save("../plot_kriging.png")
view.close()
