import openturns as ot
from openturns.viewer import View

threshold = 10.0
N = 10000
distribution = ot.Normal(2)
X = ot.RandomVector(distribution)
f = ot.SymbolicFunction(["x", "y"], ["x^2+y^2"])
Y = ot.CompositeRandomVector(f, X)
event = ot.ThresholdEvent(Y, ot.Greater(), threshold)
algo = ot.ProbabilitySimulationAlgorithm(event, ot.MonteCarloExperiment(1))
algo.setConvergenceStrategy(ot.Full())
algo.setMaximumOuterSampling(N)
algo.setMaximumCoefficientOfVariation(0.0)
algo.setMaximumStandardDeviation(0.0)
algo.run()
pRef = ot.ChiSquare(2).computeComplementaryCDF(threshold)

# Draw convergence
graph = algo.drawProbabilityConvergence()
graph.setXMargin(0.0)
graph.setLogScale(1)
graph.setLegendPosition("topright")
graph.setXTitle(r"n")
graph.setYTitle(r"$\hat{p}_n$")
graph.setTitle("Monte Carlo simulation - convergence history")
ref = ot.Curve([[1, pRef], [N, pRef]])
ref.setColor("black")
ref.setLineStyle("dashed")
ref.setLegend(r"$p_{ref}$")
graph.add(ref)
view = View(graph, (800, 600))
view.save("../plot_monte_carlo.png")
view.close()
