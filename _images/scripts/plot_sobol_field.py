import openturns as ot
from openturns.viewer import View
from time import time

A = 4.0
N = 100
threshold = 1.0e-3

# Create a domain
f = ot.SymbolicFunction(["x0", "x1"], ["1.0 - (1.2 + cos(pi_ * x0))^2 - (1.2 + cos(pi_ * x1))^2"])
level = 0.0
domain = ot.LevelSet(f, ot.Less(), level)
interval = ot.Interval([-A]*2, [A]*2)
domain.setLowerBound(interval.getLowerBound())
domain.setUpperBound(interval.getUpperBound())
# Create the mesh
# To have a more symmetric mesh
ot.ResourceMap.SetAsBool("IntervalMesher-UseDiamond", True)
discretization = [N]*2
mesh = ot.LevelSetMesher(discretization).build(domain, interval)
print("vertices=", mesh.getVerticesNumber())
# Second, a model with functional output
class FUNC(ot.OpenTURNSPythonFunction):
    def __init__(self, mesh, KLResult):
        super(FUNC, self).__init__(KLResult.getEigenValues().getSize(), mesh.getVerticesNumber())
        self.mesh_ = mesh
        self.KLResult_ = KLResult
        self.nc_ = 0

    def _exec(self, X):
        self.nc_ += 1
        print("nc=", self.nc_)
        return self.KLResult_.liftAsField(X).getValues().asPoint()

# Covariance model
covariance = ot.SquaredExponential([0.1]*2)

print("Build KL quadrature")
ot.ResourceMap.SetAsScalar("KarhunenLoeveP1Algorithm-RegularizationFactor", 1.0e-12)
algo = ot.KarhunenLoeveP1Algorithm(mesh, covariance, threshold)
ot.Log.Show(ot.Log.INFO)
algo.run()
result = algo.getResult()

F = FUNC(mesh, result)
model = ot.Function(F)

dim = model.getInputDimension()
print("dim=", dim)
size = dim + 1
distribution = ot.ComposedDistribution([ot.Normal()]*dim)
weightedExperiment = ot.MonteCarloExperiment(distribution, size)
inSample, weights = weightedExperiment.generateWithWeights()
print("Sample model")
t0 = time()
outSample = model(inSample)
t1 = time()
print("t=", t1 - t0, "s, speed=", inSample.getSize() / (t1 - t0), "evals/s")

basis = ot.OrthogonalProductPolynomialFactory([ot.HermiteFactory()]*dim)
adaptive = ot.FixedStrategy(basis, dim+1)
projection = ot.LeastSquaresStrategy(weightedExperiment)
algo = ot.FunctionalChaosAlgorithm(inSample, outSample, distribution, adaptive, projection)
algo.run()
vector = ot.FunctionalChaosRandomVector(algo.getResult())

# Field of Sobol indices
#for i in range(dim):
for i in range(15, 16):
    print("i=", i)
    sobol = [vector.getSobolIndex(i, j) for j in range(mesh.getVerticesNumber())]
    field = ot.Field(mesh, [[x] for x in sobol])
    graph = field.draw()
    graph.setTitle("Sobol index field - component " + str(i))
    #graph.add(field.drawMarginal(0))
    view = View(graph, (800, 600))
    view._ax[0].axis("equal")
    view.save("../plot_sobol_field_" + str(i).zfill(4) + ".png")
    view.close()
